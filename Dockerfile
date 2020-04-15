FROM python:latest

ADD safedns.ini /

RUN apt update
RUN apt install certbot -y
RUN pip install certbot-dns-safedns

CMD /bin/bash