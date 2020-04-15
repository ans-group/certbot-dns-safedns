FROM python:latest

RUN apt update && apt install certbot -y
RUN pip install certbot-dns-safedns

ENTRYPOINT certbot certonly --authenticator certbot-dns-safedns:dns_safedns --server https://acme-v02.api.letsencrypt.org/directory --no-eff-email --agree-tos --certbot-dns-safedns:dns_safedns-credentials /safedns.ini