from authenticate import get_auth_headers

def reset_history(date, to_rewrite='all', movie_id=None, show_id=None, **kwargs):
  headers = get_auth_headers()
  
  
