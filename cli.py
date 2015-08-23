import argparse
import sys

from authenticate import auth_flow

def cli(argv=sys.argv):
  p = argparse.ArgumentParser(description='autotrakttv CLI')
  subparsers = p.add_subparsers()

  auth_parser = subparsers.add_parser('authenticate')
  auth_parser.add_argument('--auth-file', default='./auth',
                           help='Path to where authentication should be stored')
  auth_parser.set_defaults(func=auth_flow)

  args = p.parse_args(argv[1:])

  args.func(args)

if __name__ == '__main__':
  cli(argv=sys.argv)
