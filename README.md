
## Structure

Validator for Caddy's [On-Demand TLS](https://caddyserver.com/docs/automatic-https#on-demand-tls) "ask".

[ask](https://caddyserver.com/docs/caddyfile/options#on-demand-tls)
> ask will cause Caddy to make an HTTP request to the given URL with a query string of ?domain= containing the value of the domain name. If the endpoint returns a 2xx status code, Caddy will be authorized to obtain a certificate for that name. Any other status code will result in cancelling issuance of the certificate.

This project approach:  
Use a Regex to define which domains are valid or not.  

eg. `^.*\.subdomain.example.com$`

## Environment

| Variable       | Purpose                                       | Example   | Default     |
|----------------|-----------------------------------------------|-----------|-------------|
| DOMAIN_REGEX   | Regex which defines what domains are valid    | '.*'      |             |
| HOST           | Listen Address for app                        | '0.0.0.0' | '127.0.0.1' |
| APP_PORT       | Port for app                                  | '8080'    | '8080'      |

## Quickstart

```bash
git clone --depth=1 https://github.com/ch0wm3in/caddy-domain-validator
cd caddy-domain-validator/
pip install -r ./requirements.txt
# mkdir -p sites/site_{1..9}
LOG_LEVEL=info DOMAIN_REGEX=.* python3 ./app/
```

## Docker

### docker-compose.yml

```yaml
services:
  caddy:
    image: caddy
    restart: always
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - './data/caddy/data:/data'
      - './data/caddy/conf:/etc/caddy'
      - './data/static_sites:/sites'

  validator:
    image: ghcr.io/ch0wm3in/caddy-domain-validator
    environment:
      LOG_LEVEL: info
      DOMAIN_REGEX: '.*'
      HOST: '0.0.0.0'
      APP_PORT: 8080
```

### Caddyfile

```Caddyfile
{
  on_demand_tls {
    ask http://validator:8080/validate
  }
}
https:// {
    tls {
        on_demand
    }
    root * /sites/{host}
    file_server
}
```
