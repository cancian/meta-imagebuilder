#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import json
import os
import re
import sys
import subprocess
from subprocess import check_output
import multiprocessing
import socket

def log(s):
  print('[ℕ𝕖𝕥𝔻𝕒𝕖𝕞𝕠𝕟] %s' % str(s))

try:
  from __main__ import FILTER_TOGGLE_ALLOW, \
                       FILTER_TOGGLE_DENY, \
                       FILTER_ALLOW, \
                       FILTER_DENY, \
                       REGISTRATION_TOGGLE, \
                       REGISTRATION_NO_BORDERS, \
                       REGISTERED_WAITLIST, \
                       LEASE_CLIENT_MAX, \
                       LEASE_CLIENT_EXPIRE
except Exception as e:
  log('Endpoints: Error: Config environment at __main__ ' + str(e))
  sys.exit()



## globals

ND_SCRIPT_YGG_UCI  = '/usr/bin/ygguci'
ND_SCRIPT_CJD_UCI  = '/usr/bin/cjdnsconf'
ND_SCRIPT_MESHCTL  = '/usr/bin/meshctl'



class Hemicarp:

  # admin_endpoint=("127.0.0.2", 3959)
  # admin_endpoint="/pirates/microprovision/remote-ygg.sock"

  def __init__(self, name, admin_endpoint):
    self.name = name
    self.admin_endpoint = admin_endpoint
    self.list = self.yggCaller(json.dumps({"request":"list"}))
    self.nodeinfo = self.yggCaller(json.dumps({"request":"getself"}))['response']['self']
    self.ipv6 = list(self.nodeinfo.keys())[0]
    self.build_version = self.nodeinfo[self.ipv6]['build_version']
    self.box_pub_key = self.nodeinfo[self.ipv6]['box_pub_key']
    self.coords = self.nodeinfo[self.ipv6]['coords']
    self.subnet = self.nodeinfo[self.ipv6]['subnet']
  # /init

  def allowSource(self, subnet):
    return self.yggCaller(json.dumps({"request":"addlocalsubnet", "subnet": subnet}))

  def addRoute(self, subnet, pubkey):
    return self.yggCaller(json.dumps({"request":"addremotesubnet", "subnet": subnet, "box_pub_key": pubkey}))

  def addPeer(self, uri):
    return self.yggCaller(json.dumps({"request":"addpeer", "uri": uri}))

  def getPeers(self):
    return self.yggCaller(json.dumps({"request":"getpeers"}))['response']['peers']

  def enableTunnel(self):
    return self.yggCaller(json.dumps({"request":"settunnelrouting", "enabled": True}))['response']['enabled']

  def disableTunnel(self):
    return self.yggCaller(json.dumps({"request":"settunnelrouting", "enabled": False}))['response']['enabled']


  def yggCaller(self, pqrs):
    try:
      if (type(self.admin_endpoint) == str):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
      elif (type(self.admin_endpoint) == tuple):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      else:
        print ('unknown yggdrasil endpoint type', type(self.admin_endpoint))
      s.connect(self.admin_endpoint)
      s.send(pqrs.encode('utf-8'))
      f = s.makefile('r')

    except PermissionError as e:
      print('error:: Permission Error AF_UNIX: ' + self.admin_endpoint)
      print('        Try: chown root:$(whoami) ' + self.admin_endpoint)
      exit()


    while True:
      data = f.read();
      if (data == ""):
        break
      else:
        try:
          gatos += data
        except NameError as e:
          gatos = data

    s.close()

    try:
      return json.loads(gatos)
    except:
      return {"status": "error"}
  #<!-- end caller-->

class NDExec(object):

  def __init__(self, ref_arg=False):

    required_args = [ ]

    try:

      if not ref_arg:
        raise ValueError('Error: NDExec(object) Missing Args')

      for var in required_args:
        if not ref_arg[var]:
          raise ValueError(var)
        else:
          setattr(self, var, ref_arg[var])

    except ValueError as e:
      self.insane = ValueError(e)
  # <!-- __init__ -->


  def file_exists(self, path_filename):
    return (os.path.isfile(path_filename))

  def nd_run_script(self, nd_script=False):
      try:

        if hasattr(self, 'insane'):
          raise self.insane

        try:
          out = check_output(nd_script, stderr=subprocess.STDOUT)
          data = json.loads(out)
          return([ json.dumps(data).encode("utf-8") ])
        except Exception as e:
          return([ json.dumps({'error': str(e)}).encode("utf-8") ])

      except OSError:
        return False
  # <!-- end nd_run_script -->
# <!-- end of NDExec -->



## sanity

def sanitize_path(path):
  newpath = path.split("/")
  newpath = filter(lambda x: x != "", newpath)
  return "/" + "/".join(newpath)

def bad_request(start_response, obj):
  start_response("400 Bad Request", [("content-type", "application/json; charset=utf-8")])
  return json.dumps(obj)


## endpoint functions

def getself(start_response):
  start_response("200 OK", [("content-type", "application/json; charset=utf-8")])
  v = [ "/usr/sbin/yggdrasilctl", "-v", "-json", "getself" ]
  r = NDExec({'courie': 'params'})
  return r.nd_run_script(v)
# <!-- end getself -->


def ping_pong(start_response, data):
  start_response("200 OK", [("content-type", "application/json; charset=utf-8")])
  return [ json.dumps(data).encode("utf-8") ]
# <!-- end ping_pong -->




## main application (routes)

def application(env, start_response):
  method       = env["REQUEST_METHOD"].upper()
  page         = sanitize_path(env["PATH_INFO"])
  pathinfo     = env["PATH_INFO"]
  query_data   = env["QUERY_STRING"]
  query_string = env['QUERY_STRING']
  remote_addr  = env['REMOTE_ADDR']
  user_agent   = env['HTTP_USER_AGENT']

  if (method == "GET"):

    if (page == "/ping"):

      data = {
        'method': method,
        'page': page,
        'pathinfo': pathinfo,
        'query_string': query_string,
        'remote_addr': remote_addr,
        'user_agent': user_agent
      }

      return ping_pong(start_response, data)
    # /ping

    elif (page == "/getself"):
      return getself(start_response)

    elif (page == "/wip_make_pool_database"):
      return wip_make_pool_database(start_response)

    elif (page == "/wip_read_pool_file"):
      return wip_read_pool_file(start_response)

    elif (page == "/wip_call_into_yggdrasil_socket"):
      return wip_call_into_yggdrasil_socket(start_response)

  # <!-- end GET method -->

  else:

    return bad_request(start_response, {'error': 'bad_request'})

# <!-- end application(env, start_response) -->


## Make Pool
def wip_make_pool_database(start_response):

  start_response("200 OK", [("content-type", "application/json; charset=utf-8")])
  import netaddr

  import csv, random, string
  ## 256 class-c networks (100.100.*.*)
  ip = netaddr.IPNetwork('100.100.0.0/16')

  ## 4 class-c networks (100.100.0-3.*)
  ip = netaddr.IPNetwork('100.100.0.0/22')

  columns = [
    'network_long',
    'network_cidr',
    'public_enckey',
    'status_blob',
    'ident_blob',
  ]

  with open('/tmp/netdaemon.csv', mode='w', encoding='UTF-8') as db:
    writer = csv.DictWriter(db, fieldnames=columns)
    writer.writeheader()

    for network in list(ip.subnet(24)):

      ip_list   = list(network)

      broadcast = ip_list.pop(-1)
      gateway   = ip_list.pop(0)
      poolsize  = len(ip_list)
      reqcloud  = 'cloud-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


      network_cidr  = str(network)
      network_long  = str(netaddr.IPNetwork(gateway).value)
      public_enckey = 'None'
      status_blob   = json.dumps({'status': 'disconnected', 'key': 'value'})
      ident_blob    = json.dumps({'cloud': reqcloud})

      data = [network_long, network_cidr, public_enckey, status_blob, ident_blob]
      data = dict(zip(columns, map(str, data)))

      # print(data)
      writer.writerow(data)
    # <!-- end csv dataWrites -->
  # <!-- closed file descriptor -->
  data = wip_read_pool_file()
  return [ json.dumps(data).encode("utf-8") ]
# <!-- end wip_make_pool_db() -->


## Read Pool file
def wip_read_pool_file():
  import csv
  import netaddr
  data = []
  with open('/tmp/netdaemon.csv', mode='r', encoding='UTF-8') as csv_file:
    for row in csv.DictReader(csv_file):
      data.append(row)
      pass
      # print(row)
  return data
# <!-- end wip_read_pool_db() -->


# ---------------------------------------------------------------

def wip_call_into_yggdrasil_socket(start_response):

  start_response("200 OK", [("content-type", "application/json; charset=utf-8")])


  ygg_thisbox = Hemicarp(name="netdaemon", admin_endpoint="/var/run/yggdrasil.sock")

  ## 1. add source subnets
  # yctl addlocalsubnet subnet=0.0.0.0/0
  # print('allowSource', ygg_thisbox.allowSource('0.0.0.0'))

  ## 2. enable tunnel routing
  # yctl settunnelrouting enabled=true
  # print('enableTunnel', ygg_thisbox.enableTunnel())

  ## 3. Add IP/Network to yggdrasil interface
  # ip addr add ${above_network_100.100.0.1/24} dev ygg0

  ## 4. Tell yggdrasil connectng peers IP/Network and PubKey
  # yctl addremotesubnet subnet=${above_network_fetch_100.100.0.10/32} box_pub_key=${above_pubkey_xxxxxx}
  # print('addRoute', ygg_thisbox.addRoute('100.64.0.10/32', 'ygg_thatbox.box_pub_key'))

  ## 5. Firewall Rules
  # ipt -t filter -A FORWARD     -i ${wan} -j ACCEPT # and not FROM bogons!
  # ipt -t filter -A FORWARD     -o ${wan} -j ACCEPT # and not TO bogons
  # ipt -t nat    -A POSTROUTING -o ${wan} -j MASQUERADE
  # echo 1 | tee /proc/sys/net/ipv4/ip_forward


    # 'ipv6','build_version','coords','box_pub_key',
    # 'subnet',
  data = {
    'ipv6': ygg_thisbox.ipv6,
    'build_version': ygg_thisbox.build_version,
    'coords': ygg_thisbox.coords,
    'box_pub_key': ygg_thisbox.box_pub_key,
    'subnet': ygg_thisbox.subnet,
    'getpeers': json.dumps(list(ygg_thisbox.getPeers())),
    'nodeinfo': ygg_thisbox.nodeinfo,
    'allowSource': ygg_thisbox.allowSource('0.0.0.0'),
    'enableTunnel': ygg_thisbox.enableTunnel(),
    'addRoute': ygg_thisbox.addRoute('100.64.0.10/32', 'ygg_thatbox.box_pub_key')
  }

  ## More WIP
  # print('addRoute', ygg_thisbox.addRoute('100.64.0.10/32', ygg_thatbox.box_pub_key))
  # print('addPeer', ygg_thisbox.addPeer('tcp://ygg.stephen304.com:56088'))
  # print('addPeer', ygg_thisbox.addPeer('tls://74.104.164.126:1443'))

  return [ json.dumps(data).encode("utf-8") ]

# <!-- end wip_call_into_yggdrasil_socket() -->


