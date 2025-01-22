# Exercise 5 - SDK Deployment

## Deploy using Python SDK
    * Edit sdk_ddb.py:
        * Set Action to "CREATE"
        * Update NameShortcut parameter
    * Run deployment:
        * python3 sdk_ddb.py
        * Verify in DynamoDB Console
    * Clean up:
        * Set Action to "DELETE"
        * Run python3 sdk_ddb.py