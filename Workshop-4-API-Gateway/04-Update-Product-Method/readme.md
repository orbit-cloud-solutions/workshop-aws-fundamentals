# Exercise 4 - Update Product Method

## Configure PUT method
    * Select /products/{productId} resource
    * Create PUT method:
        * Integration type: Lambda Function
        * Lambda Function: wksp-{NameShortcut}-update-product
        * Use Lambda Proxy integration: Yes
    * Configure method request:
        * API Key Required: true
        * URL path parameters: productId
    * Configure integration request:
        * Verify proxy settings
    * Test method:
        * Use path parameter: productId = "123"
        * Use test payload: { "ProductName": "Updated Product", "Price": 199.99 }