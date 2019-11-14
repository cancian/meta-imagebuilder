#!/bin/sh

export VERSION="snapshots"

export TARGET="x86/64"
export PROFILE=""

export PACKAGES=" ${PACKAGES} -wpad-basic"
export PACKAGES=" ${PACKAGES} batctl-full"
export PACKAGES=" ${PACKAGES} kmod-ipt-offload kmod-sched-act-vlan"
export PACKAGES=" ${PACKAGES} mini_snmpd alfred"
export PACKAGES=" ${PACKAGES} wpad-mesh luci-proto-relay relayd"
export PACKAGES=" ${PACKAGES} dnscrypt-proxy dnscrypt-proxy-resolvers luci-app-dnscrypt-proxy"
