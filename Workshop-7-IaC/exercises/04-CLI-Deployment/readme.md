# Exercise 4 - CLI Deployment

## Deploy using AWS CLI
    * Verify role:
        * aws sts get-caller-identity
    * Prepare scripts:
        * chmod +x cli_ddb_create.sh
        * chmod +x cli_ddb_delete.sh
        * Update NAME_SHORTCUT in both scripts
    * Execute deployment:
        * ./cli_ddb_create.sh
        * Verify in AWS Console
        * ./cli_ddb_delete.sh