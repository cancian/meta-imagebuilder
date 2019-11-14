#!/bin/sh

export VERSION="snapshots"

export TARGET="x86/64"
export PROFILE=""

# kmod-batman-adv kmod-ath10k-ct ath10k-firmware-qca988x-ct
export PACKAGES=" ${PACKAGES} -wpad-basic"
export PACKAGES=" ${PACKAGES} batctl-full haveged"
export PACKAGES=" ${PACKAGES} kmod-ipt-offload kmod-sched-act-vlan"
export PACKAGES=" ${PACKAGES} mini_snmpd alfred nodogsplash"
export PACKAGES=" ${PACKAGES} tcpdump wpad-mesh luci-proto-relay relayd"
export PACKAGES=" ${PACKAGES} dnscrypt-proxy dnscrypt-proxy-resolvers luci-app-dnscrypt-proxy"
export PACKAGES=" ${PACKAGES} ipset kmod-ipt-ipset kmod-usb-net-rndis"
export PACKAGES=" ${PACKAGES} tor-fw-helper tor-resolve torsocks tor socat kmod-ipt-nat6"
