# Reuse a base image made for devcontainers.
#source code of the base image
# https://github.com/devcontainers/images/tree/main/src/base-debian
# https://github.com/docker-library/buildpack-deps/blob/d0ecd4b7313e9bc6b00d9a4fe62ad5787bc197ae/debian/bullseye/curl/Dockerfile
FROM mcr.microsoft.com/vscode/devcontainers/base:bullseye

ARG INSTALLER_VERSION=v3.2.1 # Nix version 2.27.1
ARG DEVBOX_VERSION=0.14.2

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix/tag/${INSTALLER_VERSION} | sh -s -- install linux \
  --extra-conf "sandbox = false" \
  --init none \
  --no-confirm
ENV PATH="${PATH}:/nix/var/nix/profiles/default/bin"

RUN nix profile install github:jetify-com/devbox/${DEVBOX_VERSION}