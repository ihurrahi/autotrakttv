import os
import simplejson

BASE_DIR = os.path.expanduser('~/.autotrakttv')
SECRETS_PATH = os.path.join(BASE_DIR, 'secrets')
AUTH_PATH = os.path.join(BASE_DIR, 'auth')

def _require_file(path):
  try:
    f = open(path, 'r')
  except:
    raise
  else:
    return f

def load_secrets():
  # TODO: check to make sure SECRETS_FILE permissions are strictest
  secrets_file = _require_file(SECRETS_PATH)
  with secrets_file:
    return simplejson.load(secrets_file)

def load_auth():
  auth_file = _require_file(AUTH_PATH)
  with auth_file:
    return simplejson.load(auth_file)


