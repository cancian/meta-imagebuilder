#!/bin/sh

export PACKAGES="${PACKAGES} luci luci-theme-material" # Luci for web configuration
export PACKAGES="${PACKAGES} haveged" # Ensure entropy
export PACKAGES="${PACKAGES} kmod-ath10k-ct ath10k-firmware-qca988x-ct" # QCA wireless firmware for mesh mode
export PACKAGES="${PACKAGES} nano iperf3 tcpdump iputils-ping iputils-ping6 vnstat mtr noping ss" # Benchmarking / debugging
