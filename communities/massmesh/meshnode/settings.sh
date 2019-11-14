#!/bin/sh

set -x

export EXTRA_IMAGE_NAME="massmesh-meshnode"

# Packages for all mesh nodes

export PACKAGES="${PACKAGES} yggdrasil" # Yggdrasil mesh routing protocol
export PACKAGES="${PACKAGES} luci luci-theme-material" # Luci for web configuration
export PACKAGES="${PACKAGES} jq" # jq for scripting jquery config changes
export PACKAGES="${PACKAGES} nano iperf3 tcpdump iputils-ping iputils-ping6 vnstat dig whois mtr noping ss" # Benchmarking / debugging
export PACKAGES="${PACKAGES} tor tor-fw-helper tor-resolve torsocks" # Tor
export PACKAGES="${PACKAGES} haveged" # Ensure entropy
export PACKAGES="${PACKAGES} nodogsplash" # Captive portal
export PACKAGES="${PACKAGES} kmod-ath10k-ct ath10k-firmware-qca988x-ct" # QCA wireless firmware for mesh mode
export PACKAGES="${PACKAGES} kmod-usb-net-rndis" # USB Tethering

set +x
