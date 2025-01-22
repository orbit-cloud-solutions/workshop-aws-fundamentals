# Exercise 4 - CloudWatch Configuration

## Configure EC2 monitoring
    * Navigate to CloudWatch > Alarms
    * Create alarm wksp-NameShortcut-ec2-alarm:
        * Monitor CPU Utilization > 70%
        * Action: turn off instance when triggered
    * Test alarm:
        * sudo yum install stress-ng
        * stress-ng --cpu 2 --timeout 60s

## Configure DynamoDB monitoring
    * Enable metrics monitoring:
    * Read/write capacity utilization
    * Throttling metrics