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
tmp=$(mktemp)
jq '.Peers = ["tcp://50.236.201.218:56088"]' /etc/yggdrasil.conf > "$tmp" && mv "$tmp" /etc/yggdrasil.conf
jq '.Peers += ["tcp://45.76.166.128:12345"]' /etc/yggdrasil.conf > "$tmp" && mv "$tmp" /etc/yggdrasil.conf
jq '.Peers += ["tcp://45.77.107.150:34660"]' /etc/yggdrasil.conf > "$tmp" && mv "$tmp" /etc/yggdrasil.conf
jq '.Peers += ["tcp://108.175.10.127:61216"]' /etc/yggdrasil.conf > "$tmp" && mv "$tmp" /etc/yggdrasil.conf
jq '.Peers += ["tcp://198.58.100.240:44478"]' /etc/yggdrasil.conf > "$tmp" && mv "$tmp" /etc/yggdrasil.conf

# Add yggdrasil tunnel routing config
jq '.TunnelRouting.Enable = true' /etc/yggdrasil.conf > "$tmp" && mv "$tmp" /etc/yggdrasil.conf
jq '.TunnelRouting.IPv4LocalSubnets = ["0.0.0.0/0"]' /etc/yggdrasil.conf > "$tmp" && mv "$tmp" /etc/yggdrasil.conf
