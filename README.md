# ukfast/certbot-dns-safedns

## About
This container uses the SafeDNS Authenticator plugin for Certbot. It utilizes API calls to create and remove DNS TXT records for SSL validation.

## How to use this image

1, Creat the /etc/letsencrypt to house your configuration and your certificates
```bash
mkdir -p /etc/letsencrypt
```

2, Create the /etc/letsencrypt/safedns.ini configuration file with the below content
```
certbot_dns_safedns:dns_safedns_auth_token = <YOUR API KEY HERE>
certbot_dns_safedns:dns_safedns_propagation_seconds = 60
```

3, Set permissions for the newly created configuration file
```bash
chmod 0600 /etc/letsencrypt/safedns.ini
```

4, Test run the container
```bash
docker run -it -v /etc/letsencrypt:/etc/letsencrypt ukfast/certbot-dns-safedns:latest certonly -d yourdomain.com --test-cert --agree-tos --email email@yourdomain.com --no-eff-email
```

## Usage examples

### Verify current certificates
```bash
docker run -it -v /etc/letsencrypt:/etc/letsencrypt ukfast/certbot-dns-safedns:latest certificates
```

### Delete a certificate
```bash
docker run -it -v /etc/letsencrypt:/etc/letsencrypt ukfast/certbot-dns-safedns:latest delete --cert-name yourdomain.com
```

### Renew all certificates
```bash
docker run -it -v /etc/letsencrypt:/etc/letsencrypt ukfast/certbot-dns-safedns:latest renew
```

## About the certbot-dns-safedns Plugin
### Credentials and Config Options

Use of the plugin can be simplified by using a configuration file containing SafeDNS API credentials, obtained from your MyUKFast [account page](https://my.ukfast.co.uk/applications/index.php). See also the [SafeDNS API](https://developers.ukfast.io/documentation/safedns) documentation.

An example ``safedns.ini`` file:

```ini
dns_safedns_auth_token = 0123456789abcdef0123456789abcdef01234567
dns_safedns_propagation_seconds = 20
```

The path to this file can be provided interactively or using the `--dns_safedns-credentials` command-line argument. Certbot records the path to this file for use during renewal, but does not store the file's contents.

> **CAUTION:** You should protect these API credentials as you would the password to your MyUKFast account. Users who can read this file can use these credentials to issue arbitrary API calls on your behalf. Users who can cause Certbot to run using these credentials can complete a ``dns-01`` challenge to acquire new certificates or revoke existing certificates for associated domains, even if those domains aren't being managed by this server.

Certbot will emit a warning if it detects that the credentials file can be accessed by other users on your system. The warning reads "Unsafe permissions on credentials configuration file", followed by the path to the credentials file. This warning will be emitted each time Certbot uses the credentials file, including for renewal, and cannot be silenced except by addressing the issue (e.g., by using a command like `chmod 600` to restrict access to the file).

### Plugin Examples

To acquire a single certificate for both `example.com` and `*.example.com`, waiting 900 seconds for DNS propagation:

```bash
certbot certonly \
  --authenticator dns_safedns \
  --dns_safedns-credentials ~/.secrets/certbot/safedns.ini \
  --dns_safedns-propagation-seconds 900 \
  -d 'example.com' \
  -d '*.example.com'
```
