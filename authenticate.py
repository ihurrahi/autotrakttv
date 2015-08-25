import datetime
import requests
import simplejson

SECRETS_FILE = 'secrets'
PIN_URL = 'https://trakt.tv/pin/5954'
PIN_REQUEST_URL = 'https://api-v2launch.trakt.tv/oauth/token'

def auth_flow(auth_path, **kwargs):
  print 'Head to %s to authenticate and enter your PIN below:' % PIN_URL
  pin = raw_input('PIN: ')
  while not pin_valid(pin):
    pin = raw_input('PIN: ')

  secrets = _load_secrets()

  headers = {
    'Content-Type': 'application/json'
  }
  data = {
    'code': pin,
    'client_id': secrets['CLIENT_ID'],
    'client_secret': secrets['CLIENT_SECRET'],
    'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
    'grant_type': 'authorization_code',
  }

  response = requests.post(PIN_REQUEST_URL, data=data)
  try:
    r = response.json()
  except Exception as e:
    print e
    r = {}
  
  if response.status_code != 200:
    print 'Error authenticating: %s' % r.get('error_description', '')
  else:
    with open(auth_path, 'w') as auth_file:
      expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=r['expires_in'])
      r['expires_on'] = expires.isoformat()
      simplejson.dump(r, auth_file, indent=2)
    print 'Successfully authenticated.'

def pin_valid(pin):
  if len(pin) == 0:
    print "No PIN entered"
    return False
  return True

def _load_secrets():
  # TODO: check to make sure SECRETS_FILE permissions are strictest
  try:
    secrets_file = open(SECRETS_FILE, 'r')
  except:
    raise
  else:
    with secrets_file:
      return simplejson.load(secrets_file)

def get_auth_headers(auth_path):
  try:
    auth_file = open(auth_path, 'r')
    secrets_file = open(SECRETS_FILE, 'r')
  except:
    raise
  else:
    with auth_file, secrets_file:
      auth = simplejson.load(auth_file)
      secrets = simplejson.load(secrets_file)
      # TODO: refresh if expired or about to expire
      return {
        'Content-Type': 'application/json',
        'Authorization': auth['access_token'],
        'trakt-api-version': '2',
        'trakt-api-key': secrets['CLIENT_ID'],
      }

