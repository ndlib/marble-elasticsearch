from aws_cdk import (
    aws_elasticsearch as es,
    core
)
import os


class DeployConstruct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id)

        domain_name = kwargs['domain_name']
        account_id = core.Aws.ACCOUNT_ID
        region = core.Aws.REGION
        full_access_resource = f"arn:aws:es:{region}:{account_id}:domain/{domain_name}/*"
        anon_search_resource = f"arn:aws:es:{region}:{account_id}:domain/{domain_name}/*/_search"
        es_cluster_cfg = self.config_cluster(os.environ.get('STAGE'))

        es.CfnDomain(
            self,
            id="documentELDomain",
            elasticsearch_cluster_config=es_cluster_cfg,
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
                        "Action": [
                            "es:ESHttpPost",
                            "es:ESHttpGet"
                        ],
                        "Resource": anon_search_resource
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
                        "Resource": full_access_resource
                    }
                ]
            },
            domain_name=domain_name,
            snapshot_options={"automatedSnapshotStartHour": 4},
            elasticsearch_version="7.1",
        )

    def config_cluster(self, stage: str) -> dict:
        es_cluster_cfg = {
            "instanceCount": 1,
            "instanceType": "t2.small.elasticsearch"
        }
        if stage and stage.lower().startswith('prod'):
            es_cluster_cfg["instanceCount"] = 2
            es_cluster_cfg["zoneAwarenessEnabled"] = True
            es_cluster_cfg["zoneAwarenessConfig"] = {"availabilityZoneCount": 2}
        return es_cluster_cfg
