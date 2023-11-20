# syntax=docker/dockerfile:1.4

FROM node:alpine AS deps
ARG NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
COPY zscaler.cer /usr/local/share/ca-certificates/
COPY mcc-ca.crt /usr/local/share/ca-certificates/
COPY zscaler_root_base64.cer /usr/local/share/ca-certificates/

RUN cat /usr/local/share/ca-certificates/zscaler.cer >>/etc/ssl/certs/ca-certificates.crt
RUN cat /usr/local/share/ca-certificates/mcc-ca.crt >>/etc/ssl/certs/ca-certificates.crt
RUN cat /usr/local/share/ca-certificates/zscaler_root_base64.cer >>/etc/ssl/certs/ca-certificates.crt

#RUN apt update
#RUN apt install -y ca-certificates 
#RUN update-ca-certificates

ENV CI=true
ENV PORT=4200

WORKDIR /nodeapp
COPY ./nodeapp/package.json /nodeapp/package.json
COPY ./nodeapp/package-lock.json /nodeapp/package-lock.json
COPY ./nodeapp/tsconfig.json /nodeapp/tsconfig.json
RUN npm config set strict-ssl false
RUN npm ci
COPY . /nodeapp

CMD [ "npm", "start" ]