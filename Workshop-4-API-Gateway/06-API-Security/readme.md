# Exercise 6 - API Security

## Configure API protection
    * Create API key:
    * Name: wksp-{NameShortcut}-api-key
    * Create usage plan:
        * Name: wksp-{NameShortcut}-usage-plan
        * Rate limit: 10 requests/second
        * Burst limit: 20 requests
        * Quota: 1000 requests/day
    * Associate API with usage plan:
        * Add API and stage
        * Add API key to usage plan