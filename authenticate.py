import datetime
import os
import requests
import simplejson

from api import TraktTvApi

BASE_DIR = '~/.autotrakttv'
SECRETS_FILE = os.path.join(BASE_DIR, 'secrets')
AUTH_FILE = os.path.join(BASE_DIR, 'auth')
PIN_URL = 'https://trakt.tv/pin/5954'

def auth_flow(**kwargs):
  api = TraktTvApi()

  print 'Head to %s to authenticate and enter your PIN below:' % PIN_URL
  pin = raw_input('PIN: ')
  while not pin_valid(pin):
    pin = raw_input('PIN: ')

  secrets = _load_secrets()

  response = api.pin_request(pin, secrets['CLIENT_ID'], secrets['CLIENT_SECRET'])

  with open(AUTH_PATH, 'w') as auth_file:
    expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=response['expires_in'])
    response['expires_on'] = expires.isoformat()
    simplejson.dump(response, auth_file, indent=2)
  print 'Successfully authenticated.'

def pin_valid(pin):
  if len(pin) == 0:
    print "No PIN entered"
    return False
  return True

def _require_file(path):
  try:
    f = open(SECRETS_FILE, 'r')
  except:
    raise
  else:
    return f

def _load_secrets():
  # TODO: check to make sure SECRETS_FILE permissions are strictest
  secrets_file = _require_file(SECRETS_FILE)
  with secrets_file:
    return simplejson.load(secrets_file)

def _load_auth():
  auth_file = _require_file(AUTH_FILE)
  with auth_file:
    return simplejson.load(auth_file)

def get_auth_headers():
  auth = _load_auth()
  secrets = _load_secrets()
  # TODO: refresh if expired or about to expire
  return {
    'Content-Type': 'application/json',
    'Authorization': auth['access_token'],
    'trakt-api-version': '2',
    'trakt-api-key': secrets['CLIENT_ID'],
  }

