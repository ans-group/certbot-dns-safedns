FROM python:3.10-alpine AS build

RUN apk add --no-cache py3-pip alpine-sdk libffi-dev
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install certbot certbot-dns-safedns

FROM python:3.10-alpine
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["certbot", "--authenticator", "dns_safedns", "--dns_safedns-credentials", "/etc/letsencrypt/safedns.ini"]
