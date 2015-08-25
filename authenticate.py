import datetime
import simplejson

from api import TraktTvApi
from utils import AUTH_PATH, load_secrets

PIN_URL = 'https://trakt.tv/pin/%s'

def auth_flow(**kwargs):
  api = TraktTvApi()

  secrets = load_secrets()
  pin_url = PIN_URL % secrets[PIN_ID]

  print 'Head to %s to authenticate and enter your PIN below:' % pin_url
  pin = raw_input('PIN: ')
  while not pin_valid(pin):
    pin = raw_input('PIN: ')

  response = api.pin_request(pin)

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

