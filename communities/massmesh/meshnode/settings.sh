#!/bin/sh

export EXTRA_IMAGE_NAME="massmesh-meshnode"

# Packages for all mesh nodes

export PACKAGES="${PACKAGES} yggdrasil" # Yggdrasil mesh routing protocol
export PACKAGES="${PACKAGES} jq" # jq for scripting json config changes
export PACKAGES="${PACKAGES} tor tor-fw-helper tor-resolve torsocks" # Tor
# export PACKAGES="${PACKAGES} nodogsplash" # Captive portal - currently breaks peering and gateway
export PACKAGES="${PACKAGES} kmod-usb-net-rndis" # USB Tethering
export PACKAGES="${PACKAGES} usbreset" # USB HC reset (host side, soft reset)
