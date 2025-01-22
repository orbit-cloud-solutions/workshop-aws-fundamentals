# Exercise 2 - Development Environment Setup

## Install the Required Tools
    * Update system:
    * sudo yum update
    * Install Git:
        * sudo yum install git
        * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git
    * Install Python tools:
        * sudo yum install -y python3-pip python3 python3-setuptools
        * pip3 install boto3
    * Install Node.js:
        * sudo yum install nodejs npm
    * Install CDK:
        * pip install aws-cdk-lib constructs
        * sudo npm install -g aws-cdk
        * sudo ln -s /usr/bin/python3 /usr/bin/python