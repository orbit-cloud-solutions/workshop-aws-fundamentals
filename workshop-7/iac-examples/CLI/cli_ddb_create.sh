#!/bin/bash

# Variables
NAME_SHORTCUT="fika"
TABLE_NAME="product"
TABLE_FULL_NAME="wksp-${NAME_SHORTCUT}-dynamodb-${TABLE_NAME}-table-cli"
REGION="eu-central-1"
PARTITION_KEY_NAME="ProductID"
PARTITION_KEY_TYPE="S"
BILLING_MODE="PAY_PER_REQUEST"
TABLE_CLASS="STANDARD_INFREQUENT_ACCESS"

# Create DynamoDB table using AWS CLI
aws dynamodb create-table \
    --table-name "$TABLE_FULL_NAME" \
    --attribute-definitions AttributeName="$PARTITION_KEY_NAME",AttributeType="$PARTITION_KEY_TYPE" \
    --key-schema AttributeName="$PARTITION_KEY_NAME",KeyType=HASH \
    --billing-mode "$BILLING_MODE" \
    --table-class "$TABLE_CLASS" \
    --region "$REGION"

# Check if the table was created successfully
if [ $? -eq 0 ]; then
  echo "DynamoDB table '$TABLE_FULL_NAME' created successfully in region '$REGION'."
else
  echo "Failed to create DynamoDB table '$TABLE_FULL_NAME'."
fi
