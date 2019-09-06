from aws_cdk import (
    aws_elasticsearch as es,
    core
)


class DeployConstruct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id)

        domain_name = kwargs['domain_name']
        account_id = core.Aws.ACCOUNT_ID
        region = core.Aws.REGION
        policy_resource = f"arn:aws:es:{region}:{account_id}:domain/{domain_name}/*"

        es.CfnDomain(
            self,
            id="documentELDomain",
            elasticsearch_cluster_config={
                "instanceCount": 2,
                "zoneAwarenessEnabled": True,
                "zoneAwarenessConfig": {
                    "availabilityZoneCount": 2
                },
                "instanceType": "t2.small.elasticsearch"
            },
            ebs_options={
                "ebsEnabled": True,
                "volumeSize": 10,
                "volumeType": "gp2"
            },
            access_policies={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "es:ESHttpGet",
                        "Resource": policy_resource
                    },
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
                        "Action": [
                            "es:ESHttpHead",
                            "es:ESHttpPost",
                            "es:ESHttpGet",
                            "es:ESHttpDelete",
                            "es:ESHttpPut"
                        ],
                        "Resource": policy_resource
                    }
                ]
            },
            domain_name=domain_name,
            snapshot_options={"automatedSnapshotStartHour": 4},
            elasticsearch_version="7.1",
        )
