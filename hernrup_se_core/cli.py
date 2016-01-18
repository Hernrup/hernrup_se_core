#!/usr/bin/env python
import logging
from hernrup_se_core.utils import (livereload as livereload_fn,
                                   clean,
                                   new_entry,
                                   serve as serve_fn,
                                   publish as publish_fn,
                                   generate as generate_fn,
                                   develop as develop_fn)
import argh
import sys

logger = logging.getLogger(__name__)


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


def publish(source_path='.'):
    generate_fn(source_path=source_path, debug=False, dev=False,
                autoreload=False)
    publish_fn(source_path=source_path)


def serve(output_path='./output', port=5000, livereload=True):
    if livereload:
        livereload_fn(port=port, output_path=output_path)
    else:
        serve_fn(port=port, output_path=output_path)


def generate(source_path='.'):
    generate_fn(source_path=source_path)


def develop(source_path='.', output_path='./output', port=5000, dev=True):
    develop_fn(source_path=source_path, output_path=output_path,
               port=port, dev=dev)


def main():
    try:
        setup_logging()
        parser = argh.ArghParser()
        parser.add_commands([generate, develop, serve, clean,
                             new_entry, publish])
        parser.dispatch()
    except Exception as e:
        logger.error(e)
        return -1


if __name__ == '__main__':
    main()

