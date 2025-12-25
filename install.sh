#!/bin/bash
INSTALLER_VERSION=v3.2.1
DEVBOX_VERSION=0.14.2

curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix/tag/${INSTALLER_VERSION} | \
 sh -s -- install


. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
nix profile install github:jetify-com/devbox/${DEVBOX_VERSION}