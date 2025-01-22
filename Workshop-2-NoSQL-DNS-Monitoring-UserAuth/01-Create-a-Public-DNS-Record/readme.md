# Exercise 1 - Cereate a public DNS record

## Create a record
    * Navigate to Route 53 service in AWS Management Console
    * Locate prepared public hosted zone "workshop.virtualcomputing.cz"
    * Create A record:
        * Point to EC2 instance from previous webinar
        * Name: NameShortcut-ec2.workshop.virtualcomputing.cz

## Verify DNS resolution
    * Run nslookup <domain-name> from instance
    * Run nslookup <domain-name> from local computer
