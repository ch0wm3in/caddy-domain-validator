
## Structure

Validator for Caddy's [On-Demand TLS](https://caddyserver.com/docs/automatic-https#on-demand-tls) "ask".

[ask](https://caddyserver.com/docs/caddyfile/options#on-demand-tls)
> ask will cause Caddy to make an HTTP request to the given URL with a query string of ?domain= containing the value of the domain name. If the endpoint returns a 2xx status code, Caddy will be authorized to obtain a certificate for that name. Any other status code will result in cancelling issuance of the certificate.

This project approach:  
With a specified directory, each immediate child directory will be considered a valid hostname.
With the below example, `alpha.example.com` and `beta.example.com` are valid. `subdir.example.com` is not.

```
/sites
    /alpha.example.com
        /subdir.example.com
    /beta.example.com
```

When loading, it takes O(n) time with n being the number of directories under `SITE_DIRECTORY`  
After loading, queries and changes to directories are O(1).

## Environment

| Variable       | Purpose                                       | Example   | Default     |
|----------------|-----------------------------------------------|-----------|-------------|
| SITE_DIRECTORY | Directory to watch for changes. Not recursive | '/sites'  |             |
| HOST           | Listen Address for app                        | '0.0.0.0' | '127.0.0.1' |
| APP_PORT       | Port for app                                  | '8080'    | '8080'      |

## Quickstart

```bash
git clone --depth=1 https://github.com/tyler71/caddy-domain-validator
cd caddy-domain-validator/
pip install -r ./requirements.txt
# mkdir -p sites/site_{1..9}
LOG_LEVEL=info SITE_DIRECTORY=./sites python3 ./app/
```

## Docker

docker-compose.yml
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
    networks:
      - internal

  validator:
    image: ghcr.io/tyler71/caddy-domain-validator
    environment:
      LOG_LEVEL: info
      SITE_DIRECTORY: '/sites'
      HOST: '0.0.0.0'
      APP_PORT: 8080
    volumes:
      - './data/static_sites:/sites'
    networks:
      - internal

networks:
  internal:
```

```Caddyfile
{
  on_demand_tls {
    ask http://validator:8080/validate
    interval 10h
    burst 5
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