from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs
)
from constructs import Construct


class EcsAlbStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, 
                 name_shortcut: str, ecr_repository_arn: str, container_uri: str,
                 container_port: int, app_certificate_arn: str, vpc_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Fetch the existing VPC
        vpc = ec2.Vpc.from_lookup(self, "ExistingVpc", vpc_id=vpc_id)

        # Create an ECS cluster in the VPC
        cluster = ecs.Cluster(
            self,
            f"{name_shortcut}-ecs-cluster",
            vpc=vpc,
            cluster_name=f"wksp-{name_shortcut}-ecs-cluster-cdk",
        )