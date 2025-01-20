from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    RemovalPolicy,
    aws_iam as iam,
    aws_logs as logs,
    Fn,
    Duration,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_actions as actions,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_cognito as cognito
)
from constructs import Construct


class EcsAlbStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, 
                 name_shortcut: str, container_uri: str, app_certificate_arn: str, vpc_id: str, route53_zone_id: str, route53_zone_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import the API Gateway URL from the ApiGatewayStack 
        apigateway_url = Fn.import_value(f"wksp-{name_shortcut}-apigateway-cdk-stack-url")
        # Import cognito values from CognitoStack
        cognito_user_pool_id = Fn.import_value(f"wksp-{name_shortcut}-cognito-cdk-stack-userpool-id")
        cognito_user_pool_client_id = Fn.import_value(f"wksp-{name_shortcut}-cognito-cdk-stack-userpool-client-id")
        cognito_user_pool_domain = Fn.import_value(f"wksp-{name_shortcut}-cognito-cdk-stack-domain")

        # Fetch the existing VPC
        vpc = ec2.Vpc.from_lookup(self, "ExistingVpc", vpc_id=vpc_id)

        # Create an ECS cluster in the VPC
        cluster = ecs.Cluster(
            self,
            f"{name_shortcut}-ecs-cluster",
            vpc=vpc,
            cluster_name=f"wksp-{name_shortcut}-ecs-cluster-cdk",
        )

        ecs_execution_role = iam.Role(
            scope=self,
            id="CoreECSExecutionRole",
            role_name=f"wksp-{name_shortcut}-ecs-execution-role-cdk",
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(
                    scope=self,
                    id="AdministratorAccess",
                    managed_policy_arn="arn:aws:iam::aws:policy/AdministratorAccess",
                ),
                iam.ManagedPolicy.from_managed_policy_arn(
                    scope=self,
                    id="AmazonECSTaskExecutionRolePolicy",
                    managed_policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
                )
            ],
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("ecs.amazonaws.com"),
                iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            ),
        )

        log_group = logs.LogGroup(
            self,
            "LogGroup",
            log_group_name=f"wksp-{name_shortcut}-ecs-log-group-cdk",
            retention=logs.RetentionDays.ONE_DAY,
            removal_policy=RemovalPolicy.DESTROY,
        )
        
        task_definition = ecs.FargateTaskDefinition(
            self,
            "ECSTaskDefinition",
            family=f"wksp-{name_shortcut}-ecs-task-def-cdk",
            memory_limit_mib=int(512),
            cpu=int(256),
            runtime_platform=ecs.RuntimePlatform(
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                cpu_architecture=ecs.CpuArchitecture.X86_64
            ),
            execution_role=ecs_execution_role
        )

        # Add a container to the task definition
        container = task_definition.add_container(
            f"{name_shortcut}-frontend-container",
            image=ecs.ContainerImage.from_registry(container_uri),
            logging=ecs.LogDriver.aws_logs(
                stream_prefix=f"{name_shortcut}-logs", log_group=log_group
            ),
            port_mappings=[
                ecs.PortMapping(
                    container_port=80,
                    name="frontend-80-tcp",
                    protocol=ecs.Protocol.TCP,
                    app_protocol=ecs.AppProtocol.http
                )
            ],
            environment={"BACKEND_URL": apigateway_url},
        )

        ecs_security_group = ec2.SecurityGroup(
            self,
            "SecurityGroupEcs",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security Group for the workshop ECS cluster.",
            security_group_name=f"wksp-{name_shortcut}-ecs-sg-cdk",
        )
        
        service = ecs.FargateService(
            self,
            "EcsFargateService",
            cluster=cluster,
            security_groups=[ecs_security_group],
            task_definition=task_definition,
            desired_count=1,
            service_name=f"wksp-{name_shortcut}-ecs-service-cdk",
            assign_public_ip=True
        )
        
        alb_security_group = ec2.SecurityGroup(
            self,
            "SecurityGroupAlb",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security Group for the workshop ALB.",
            security_group_name=f"wksp-{name_shortcut}-alb-sg-cdk",
        )
        
        # Create the Application Load Balancer (ALB)
        alb = elbv2.ApplicationLoadBalancer(
            self,
            f"{name_shortcut}-alb",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name=f"wksp-{name_shortcut}-alb-cdk",
            security_group = alb_security_group
        )

        # Add a listener for HTTP (80) with redirection to HTTPS
        alb.add_redirect(
            source_protocol=elbv2.ApplicationProtocol.HTTP,
            source_port=80,
            target_protocol=elbv2.ApplicationProtocol.HTTPS,
            target_port=443,
        )
        
        applicationTargetGroup = elbv2.ApplicationTargetGroup(
            self,
            f"{name_shortcut}-ecs-service-tg",
            target_type=elbv2.TargetType.IP,
            target_group_name=f"wksp-{name_shortcut}-ecs-service-tg-cdk",
            protocol=elbv2.ApplicationProtocol.HTTP,
            port=80,
            vpc=vpc
        )

        listener_https = alb.add_listener(
            f"{name_shortcut}-https-listener",
            port=443,
            open=True,
            ssl_policy=elbv2.SslPolicy.TLS13_RES,
            default_action=actions.AuthenticateCognitoAction(
                user_pool=cognito.UserPool.from_user_pool_id(
                    self, "ImportedUserPool", user_pool_id=cognito_user_pool_id
                ),
                user_pool_client=cognito.UserPoolClient.from_user_pool_client_id(
                    self, "ImportedUserPoolClient", user_pool_client_id=cognito_user_pool_client_id
                ),
                user_pool_domain=cognito.UserPoolDomain.from_domain_name(
                    self, "ImportedUserPoolDomain", user_pool_domain_name=cognito_user_pool_domain
                ),
                session_timeout=Duration.hours(8),
                next=elbv2.ListenerAction.forward([applicationTargetGroup]),
            ),
            certificates=[elbv2.ListenerCertificate.from_arn(app_certificate_arn)],
            protocol=elbv2.ApplicationProtocol.HTTPS,
        )

        # Add ECS service to the target group
        service.attach_to_application_target_group(applicationTargetGroup)

        # Allow ALB to communicate with the ECS service security group
        ecs_security_group.add_ingress_rule(
            alb_security_group,
            ec2.Port.tcp(80),
            "Allow traffic from ALB to ECS service"
        )
        
        # Allow public access to ALB
        alb_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            "Allow HTTPS traffic from anywhere"
        )
        
        alb_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow HTTP traffic from anywhere (redirects to HTTPS)"
        )

        # add route 53 record:
        zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "existing-zone",
            hosted_zone_id=route53_zone_id,
            zone_name=route53_zone_name,
        )

        # Create a Route 53 A record pointing to the ALB
        route53.ARecord(
            self,
            f"{name_shortcut}-alb-record",
            record_name=f"{name_shortcut}.app",  # Replace with your desired subdomain
            target=route53.RecordTarget.from_alias(targets.LoadBalancerTarget(alb)),
            zone=zone,
        )
