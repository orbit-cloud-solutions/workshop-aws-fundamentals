# Exercise 2 - Create a Private Hosted Zone

## Create Private Hosted Zone
    * Create zone named "NameShortcut.local"
    * Create CNAME record with mock value
    * Test resolution:
        * Run nslookup -q=CNAME record.NameShortcut.local from local computer
        * Run nslookup -q=CNAME record.NameShortcut.local from EC2 instance
