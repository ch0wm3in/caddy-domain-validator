
## Structure

Validator for Caddy's [On-Demand TLS](https://caddyserver.com/docs/automatic-https#on-demand-tls) "ask".

[ask](https://caddyserver.com/docs/caddyfile/options#on-demand-tls)
> ask will cause Caddy to make an HTTP request to the given URL with a query string of ?domain= containing the value of the domain name. If the endpoint returns a 2xx status code, Caddy will be authorized to obtain a certificate for that name. Any other status code will result in cancelling issuance of the certificate.

This project approach:
With a root directory, each immediate child directory will be considered a valid hostname.
For example, for `alpha.example.com` and `beta.example.com`

```
/sites
    /alpha.example.com
    /beta.example.com
```

When loading, it takes O(n) time with n being the number of directories under `SITE_DIRECTORY`  
After loading, queries and changes to directories are O(1).

## Environment

| Variable       | Purpose                                       | Example   |
|----------------|-----------------------------------------------|-----------|
| SITE_DIRECTORY | Directory to watch for changes. Not recursive | '/sites'  |
| HOST           | Listen Address for app                        | '0.0.0.0' |
| APP_PORT       | Port for app                                  | '8080'    | 
