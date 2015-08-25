URL_BASE = 'https://api-v2launch.trakt.tv/'

class TraktTvApi():
  def __init__(self):
    pass

  def req(url, headers=None, body=None, data=None):
    url = URL_BASE + url
    default_headers = {
      'Content-Type': 'application/json'
    }
    headers = headers or default_headers
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
    data = {
      'code': pin,
      'client_id': client_id,
      'client_secret': client_secret,
      'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
      'grant_type': 'authorization_code',
    }
    return self.req('oauth/token', data=data)
    
