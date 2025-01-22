# Exercise 7 - Custom Domain

## Create custom domain
    * Create custom domain:
    * Domain name: api-{NameShortcut}.workshop.virtualcomputing.cz
    * Create API mapping:
        * Select API and stage
    * Configure DNS:
        * Create Route 53 record
        * Record type: A
        * Alias target: API Gateway domain name
    * Test domain resolution:
        * Wait for DNS propagation
        * Verify using nslookup