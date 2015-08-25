import os
import simplejson

BASE_DIR = '~/.autotrakttv'
SECRETS_FILE = os.path.join(BASE_DIR, 'secrets')
AUTH_FILE = os.path.join(BASE_DIR, 'auth')

def _require_file(path):
  try:
    f = open(path, 'r')
  except:
    raise
  else:
    return f

def load_secrets():
  # TODO: check to make sure SECRETS_FILE permissions are strictest
  secrets_file = _require_file(SECRETS_FILE)
  with secrets_file:
    return simplejson.load(secrets_file)

def load_auth():
  auth_file = _require_file(AUTH_FILE)
  with auth_file:
    return simplejson.load(auth_file)


