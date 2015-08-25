import datetime
import simplejson

from api import TraktTvApi
from utils import AUTH_PATH

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

