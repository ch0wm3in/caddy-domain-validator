
## Structure

Validator for Caddy's [On-Demand TLS](https://caddyserver.com/docs/automatic-https#on-demand-tls) "ask".
To ensure only valid hostnames are permitted to generate certs, it will ask the service which ones are valid

[ask](https://caddyserver.com/docs/caddyfile/options#on-demand-tls)
> ask will cause Caddy to make an HTTP request to the given URL with a query string of ?domain= containing the value of the domain name. If the endpoint returns a 2xx status code, Caddy will be authorized to obtain a certificate for that name. Any other status code will result in cancelling issuance of the certificate.

This project is meant to approach a method where with the following file structure,
only the correct certificates are generated.

```
/sites
    /alpha.example.com
    /alpha.example.com

```

## Environment

| Variable | Purpose | Example |
| SITE_DIRECTORY | Directory to watch for changes. Not recursive | '/sites' |
| HOST | Listen Address for app | '0.0.0.0' |
| APP_PORT | Port for app | '8080' | 
