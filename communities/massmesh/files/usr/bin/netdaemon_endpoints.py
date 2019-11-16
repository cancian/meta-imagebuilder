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

  # <!-- end GET method -->

  else:

    return bad_request(start_response, {'error': 'bad_request'})

# <!-- end application(env, start_response) -->

