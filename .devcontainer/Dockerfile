FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

ADD https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem \
    /usr/local/share/ca-certificates/global-bundle.pem

RUN chmod o+r /usr/local/share/ca-certificates/global-bundle.pem

RUN curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_arm64/session-manager-plugin.deb" \
    -o "session-manager-plugin.deb" && sudo dpkg -i session-manager-plugin.deb
