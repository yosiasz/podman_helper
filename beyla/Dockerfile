# syntax=docker/dockerfile:1.4

FROM node:alpine AS deps

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