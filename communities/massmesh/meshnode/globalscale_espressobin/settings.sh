#!/bin/sh

export VERSION="snapshots"

export TARGET="mvebu/cortexa53"
export PROFILE="globalscale_espressobin"

export PACKAGES="${PACKAGES} -wpad-basic"
export PACKAGES="${PACKAGES} batctl-full"
export PACKAGES="${PACKAGES} kmod-batman-adv kmod-ipt-offload kmod-sched-act-vlan"
export PACKAGES="${PACKAGES} alfred"
export PACKAGES="${PACKAGES} wpad-mesh luci-proto-relay relayd"
export PACKAGES="${PACKAGES} dnscrypt-proxy dnscrypt-proxy-resolvers luci-app-dnscrypt-proxy"
