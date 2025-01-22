# Exercise 6 - CDK Deployment

## Deploy using AWS CDK
    * Install prerequisites:
        * python -m pip install -r requirements.txt
        * sudo npm install -g aws-cdk
    * Configure CDK:
        * Navigate to cdk/ddb-cdk
        * Update name_shortcut in app.py
    * Deploy infrastructure:
        * cdk list
        * cdk synth
        * cdk diff
        * cdk deploy
    * Clean up:
        * cdk destroy