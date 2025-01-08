from aws_cdk import (
    Stack,
    aws_cognito as cognito,
    RemovalPolicy,
    Duration
)
from constructs import Construct

class CognitoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, 
                 name_shortcut: str, route53_zone_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_pool = cognito.UserPool(
            self,
            f"{name_shortcut}-userpool",
            user_pool_name=f"wksp-{name_shortcut}-cognito-userpool-cdk",
            self_sign_up_enabled=False,
            sign_in_case_sensitive=False,
            sign_in_aliases=cognito.SignInAliases(email=True),
            account_recovery=None,
            custom_attributes={
                "pid": cognito.StringAttribute(min_len=6, max_len=6, mutable=True)
            },
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Specify Cognito Domain
        cognito_domain=cognito.CognitoDomainOptions(
            domain_prefix=name_shortcut,
        )

        # Define Custom Domain for User Pool with Cognito
        user_pool.add_domain(
            f"{name_shortcut}-userpooldomain",
            cognito_domain=cognito_domain,
        )
        
        user_pool_client = cognito.UserPoolClient(
            self,
            f"{name_shortcut}-appclient",
            user_pool=user_pool,
            user_pool_client_name="ecs-crud-frontend",
            supported_identity_providers=[
                cognito.UserPoolClientIdentityProvider.COGNITO
            ],
            o_auth=cognito.OAuthSettings(
                callback_urls=[
                    f"https://{name_shortcut}.app.{route53_zone_name}"
                ],
                logout_urls=[
                    f"https://{name_shortcut}.app.{route53_zone_name}"
                ],
                scopes=[
                        cognito.OAuthScope.EMAIL,
                        cognito.OAuthScope.OPENID,
                        cognito.OAuthScope.PROFILE,
                        cognito.OAuthScope.COGNITO_ADMIN,
                    ],
                flows=cognito.OAuthFlows(
                    implicit_code_grant=True,
                    authorization_code_grant=True,
                )
            ),
            generate_secret=True,
            prevent_user_existence_errors=True,
            enable_token_revocation=True,
            auth_flows=cognito.AuthFlow(user_srp=True, custom=True),
            refresh_token_validity=Duration.days(30),
            access_token_validity=Duration.minutes(60),
            id_token_validity=Duration.minutes(60),
        )