import argparse
import sys

from authenticate import auth_flow
from history import reset_movie_history

def cli(argv=sys.argv):
  p = argparse.ArgumentParser(description='autotrakttv CLI')
  subparsers = p.add_subparsers()

  auth_parser = subparsers.add_parser('authenticate')
  auth_parser.set_defaults(func=auth_flow)
  auth_parser.add_argument('--auth-file', default='./auth',
                           help='Path to where authentication should be stored')

  reset_hist = subparsers.add_parser('resetmoviehistory')
  reset_hist.set_defaults(func=reset_movie_history)
  reset_hist.add_argument('date',
                          help='Date to when you want to reset history to')
  reset_hist.add_argument('--movie-id',
                          help='Specific movie to reset')
  history_group = reset_hist.add_mutually_exclusive_group()
  history_group.add_argument('--all', action='store_const', const='all', dest='rewrite')
  history_group.add_argument('--latest', action='store_const', const='latest', dest='rewrite')
  history_group.add_argument('--earliest', action='store_const', const='earliest', dest='rewrite')
  reset_hist.set_defaults(rewrite='all')

  args = p.parse_args(argv[1:])

  args.func(**vars(args))

if __name__ == '__main__':
  cli(argv=sys.argv)
