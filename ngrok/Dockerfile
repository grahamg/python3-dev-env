FROM alpine:3.18

# Install ngrok
RUN apk add --no-cache curl \
    && curl -s https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.tgz \
    | tar xvz -C /usr/local/bin

ENTRYPOINT ["ngrok"]
