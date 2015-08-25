import requests

URL_BASE = 'https://api-v2launch.trakt.tv/'

from utils import load_auth, load_secrets

def get_auth_headers():
  auth = load_auth()
  secrets = load_secrets()
  # TODO: refresh if expired or about to expire
  return {
    'Content-Type': 'application/json',
    'Authorization': auth['access_token'],
    'trakt-api-version': '2',
    'trakt-api-key': secrets['CLIENT_ID'],
  }

class TraktTvApi():
  def req(url, headers=None, body=None, data=None):
    url = URL_BASE + url
    headers = headers or get_auth_headers()
    response = requests.post(url, headers=headers, data=data, body=body)
    try:
      r = response.json()
    except Exception as e:
      print e
      r = {}
    
    if response.status_code != 200:
      print 'Error authenticating: %s' % r.get('error_description', '')
      raise
    return r
  
  def pin_request(pin, client_id, client_secret):
    headers = {
      'Content-Type': 'application/json'
    }
    data = {
      'code': pin,
      'client_id': client_id,
      'client_secret': client_secret,
      'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
      'grant_type': 'authorization_code',
    }
    return self.req('oauth/token', headers=headers, data=data)
    
