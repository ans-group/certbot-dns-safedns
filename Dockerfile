FROM python:latest

RUN apt update && apt install certbot -y
RUN pip install certbot-dns-safedns

ENTRYPOINT ["certbot", "--authenticator", "certbot-dns-safedns:dns_safedns", "--certbot-dns-safedns:dns_safedns-credentials", "/safedns.ini"]
