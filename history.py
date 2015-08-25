from api import TraktTvApi

def reset_movie_history(date, rewrite='all', movie_id=None, **kwargs):
  api = TraktTvApi()
  media_type = 'movies'
  if movie_id:
    histories = [api.get_watched_history(type=media_type, id=movie_id)]
  else:
    all_watched = api.get_watched(type=media_type)
    histories = []
    for watched in all_watched:
      histories.append(api.get_watched_history(type=media_type, id=watched['movie']['ids']['trakt']))
      break

  for history in histories:
    if history:
      sorted_history = sorted(history, lambda h: h['watched_at'])
      if rewrite == 'earliest':
        to_rewrite = sorted_history[0]
      elif rewrite =='latest':
        to_rewrite = sorted_history[-1]
      else:
        to_rewrite = sorted_history

      movies = []
      to_delete = []
      for h in sorted_history:
        movie_info = h['movie']
        movie_info['watched_at'] = date
        movies.append(movie_info)
        to_delete.append(h['id'])

      api.remove_from_history({'ids': to_delete})
      api.add_to_history({'movies': movies})
  
