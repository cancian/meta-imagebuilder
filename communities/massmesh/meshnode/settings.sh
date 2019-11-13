#!/bin/sh

set -x

export EXTRA_IMAGE_NAME="massmesh-meshnode"

# Packages for all mesh nodes

export PACKAGES="${PACKAGES} yggdrasil" # Yggdrasil mesh routing protocol
export PACKAGES="${PACKAGES} luci luci-theme-material" # Luci for web configuration
export PACKAGES="${PACKAGES} jq" # jq for scripting jquery config changes
export PACKAGES="${PACKAGES} iperf3 nano" # Benchmarking / debugging

set +x
