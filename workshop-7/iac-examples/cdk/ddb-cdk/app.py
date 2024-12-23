#!/usr/bin/env python3
import aws_cdk as cdk
from ddb_cdk.ddb_cdk_stack import DdbCdkStack

# Define parameters directly in app.py as a config
params = {
    "name_shortcut": "fika",
    "table_name": "product",
    "billing_mode": "PAY_PER_REQUEST",
    "table_class": "STANDARD_INFREQUENT_ACCESS",
    "partition_key_name": "ProductID",
    "partition_key_type": "S"
}

# Create an app instance
app = cdk.App()

# Pass the params directly to the DdbCdkStack
DdbCdkStack(
    app, 
    "DdbCdkStack",
    name_shortcut=params["name_shortcut"],
    table_name=params["table_name"],
    billing_mode=params["billing_mode"],
    table_class=params["table_class"],
    partition_key_name=params["partition_key_name"],
    partition_key_type=params["partition_key_type"]
)

# Synthesize the app (prepare for deployment)
app.synth()
