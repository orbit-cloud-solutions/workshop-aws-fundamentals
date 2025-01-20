#!/bin/bash

# Variables
NAME_SHORTCUT="fika"
TABLE_NAME="product"
TABLE_FULL_NAME="wksp-${NAME_SHORTCUT}-dynamodb-${TABLE_NAME}-table-cli"
REGION="eu-central-1"

# Delete DynamoDB table using AWS CLI
aws dynamodb delete-table \
    --table-name "$TABLE_FULL_NAME" \
    --region "$REGION"

# Check if the table was deleted successfully
if [ $? -eq 0 ]; then
  echo "DynamoDB table '$TABLE_FULL_NAME' deletion initiated successfully in region '$REGION'."
else
  echo "Failed to initiate deletion of DynamoDB table '$TABLE_FULL_NAME'."
fi
