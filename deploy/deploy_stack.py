from aws_cdk import (
    core
)

from .deploy_constructs import DeployConstruct


class DeployStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        esearch = DeployConstruct(self, "ESSearchConstruct", domain_name=id)
