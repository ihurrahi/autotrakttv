import requests
import simplejson

URL_BASE = 'https://api-v2launch.trakt.tv'

from utils import load_auth, load_secrets

def get_auth_headers():
  auth = load_auth()
  secrets = load_secrets()
  # TODO: refresh if expired or about to expire
  return {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + auth['access_token'],
    'trakt-api-version': '2',
    'trakt-api-key': secrets['CLIENT_ID'],
  }

class TraktTvApi():
  def req(self, method, url, headers=None, data=None):
    url = URL_BASE + url
    headers = headers or get_auth_headers()
    response = requests.request(method, url, headers=headers, data=data)
    try:
      r = response.json()
    except Exception as e:
      print e
      r = {}
    
    if response.status_code < 200 or response.status_code >= 300:
      raise Exception('Error authenticating - got %s: %s' % (response.status_code, r.get('error_description', '')))
    return r
  
  def pin_request(self, pin):
    secrets = load_secrets()
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
    return self.req('POST', '/oauth/token', headers=headers, data=simplejson.dumps(data))
    
  def get_watched_history(self, type, id):
    return self.req('GET', '/sync/history/%s/%s' % (type, id))

  def get_watched(self, type):
    return self.req('GET', '/sync/watched/%s' % type)

  def remove_from_history(self, to_remove):
    return self.req('POST', '/sync/history/remove', data=simplejson.dumps(to_remove))

  def add_to_history(self, to_add):
    return self.req('POST', '/sync/history', data=simplejson.dumps(to_add))
