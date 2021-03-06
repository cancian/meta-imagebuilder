#!/bin/sh

# Remove all forwardings (LAN -> WAN should be the only one by default)
uci show firewall | grep -o "firewall\.\@forwarding\[[0-9]\+\]" | uniq | xargs uci delete
uci commit

# Re-add forwardings between ygg and lan
uci add firewall forwarding
uci set firewall.@forwarding[-1].dest='yggdrasil'
uci set firewall.@forwarding[-1].src='lan'
uci commit
uci add firewall forwarding
uci set firewall.@forwarding[-1].dest='lan'
uci set firewall.@forwarding[-1].src='yggdrasil'
uci commit

# Enable masquerading on ygg interface
uci set firewall.yggdrasil.masq='1'
uci commit

# Add yggdrasil peers
uci add yggdrasil peer
uci set yggdrasil.@peer[-1].uri='tcp://50.236.201.218:56088'
uci add yggdrasil peer
uci set yggdrasil.@peer[-1].uri='tcp://45.76.166.128:12345'
uci add yggdrasil peer
uci set yggdrasil.@peer[-1].uri='tcp://45.77.107.150:34660'
uci add yggdrasil peer
uci set yggdrasil.@peer[-1].uri='tcp://108.175.10.127:61216'
uci add yggdrasil peer
uci set yggdrasil.@peer[-1].uri='tcp://198.58.100.240:44478'
uci commit

# Add yggdrasil tunnel routing config
uci set yggdrasil.yggdrasil.TunnelRouting_Enable=1
uci add yggdrasil ipv4_local_subnet
uci set yggdrasil.@ipv4_local_subnet[-1].subnet='0.0.0.0/0'
uci commit

# Set ula
uci set network.globals.ula_prefix=$(ygguci get | yggdrasil -useconf -normaliseconf -json | yggdrasil -useconf -subnet)
uci commit
