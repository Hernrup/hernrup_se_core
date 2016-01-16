#!/usr/bin/env python
import logging as log
import argparse
from hernrup_se_core.utils import livereload, clean, new_entry, publish, serve, \
    generate, develop

log_instace = log.getLogger()
log_instace.setLevel(log.DEBUG)


def setup_parser():

    def add_develop_parser(root_parser):
        def f(args):
            develop(port=args.port, debug=args.debug, dev=args.dev)
        parser = root_parser.add_parser('develop')
        parser.set_defaults(func=f)
        parser.add_argument('-p', '--port', help='Port to listen to',
                            default=5000)
        parser.add_argument('-debug', '--debug', help='debug',
                            action='store_true', default=False)
        parser.add_argument('-d', '--dev', help='debug', action='store_true',
                            default=False)

    def add_generate_parser(root_parser):
        def f(args):
            generate(debug=args.debug, dev=args.dev,
                     autoreload=args.autoreload)

        parser = root_parser.add_parser('generate')
        parser.set_defaults(func=f)
        parser.add_argument('-d', '--debug', help='debug', action='store_true',
                            default=False)
        parser.add_argument('-dev', '--dev', help='debug', action='store_true',
                            default=False)
        parser.add_argument('-r', '--autoreload', help='autoreload',
                            action='store_true', default=False)

    def add_serve_parser(root_parser):
        def f(args):
            serve(port=args.port)
        parser = root_parser.add_parser('serve')
        parser.set_defaults(func=f)
        parser.add_argument('-p', '--port', help='Port to listen to',
                            default=5000)

    def add_livereload_parser(root_parser):
        def f(args):
            livereload(args.port)
        parser = root_parser.add_parser('livereload')
        parser.set_defaults(func=f)
        parser.add_argument('-p', '--port', help='Port to listen to',
                            default=5000)

    def add_clean_parser(root_parser):
        def f(args):
            clean()
        parser = root_parser.add_parser('clean')
        parser.set_defaults(func=f)

    def add_new_entry_parser(root_parser):
        def f(args):
            new_entry(args.title)
        parser = root_parser.add_parser('add')
        parser.set_defaults(func=f)
        parser.add_argument('-t', '--title', help='Entry title',
                            default='New entry')

    def add_publish_parser(root_parser):
        def f(args):
            publish()
        parser = root_parser.add_parser('publish')
        parser.set_defaults(func=f)

    root_parser = argparse.ArgumentParser(
        description='Hernrup.se blog manager')
    sp = root_parser.add_subparsers()
    add_generate_parser(sp)
    add_serve_parser(sp)
    add_livereload_parser(sp)
    add_clean_parser(sp)
    add_new_entry_parser(sp)
    add_publish_parser(sp)
    add_develop_parser(sp)

    return root_parser, root_parser.parse_args()


def main():
    try:
        parser, args = setup_parser()
        if hasattr(args, 'func'):
            args.func(args)
            return
        parser.print_help()
    except Exception as e:
        log.error(e)
        raise e


if __name__ == '__main__':
    main()

