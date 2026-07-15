FROM python:3.13-alpine AS build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ARG CERTBOT_DNS_SAFEDNS_VERSION=""

RUN apk add --no-cache alpine-sdk libffi-dev
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install --python /opt/venv/bin/python certbot "certbot-dns-safedns${CERTBOT_DNS_SAFEDNS_VERSION:+==${CERTBOT_DNS_SAFEDNS_VERSION}}"

FROM python:3.13-alpine
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["certbot", "--authenticator", "dns_safedns", "--dns_safedns-credentials", "/etc/letsencrypt/safedns.ini"]
