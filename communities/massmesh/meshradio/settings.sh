#!/bin/sh

set -x

export EXTRA_IMAGE_NAME="massmesh-meshradio"

export PACKAGES="${PACKAGES} -wpad-basic batctl-full kmod-batman-adv kmod-ipt-offload kmod-sched-act-vlan wpad-mesh-openssl"

set +x
