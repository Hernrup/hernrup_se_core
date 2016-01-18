#!/usr/bin/env python
import sys
import logging as log
import subprocess
from pelican.server import socketserver, ComplexHTTPRequestHandler
import pelican.server
from livereload import Server as Live_server
from datetime import datetime
from collections import namedtuple
import os
from hernrup_se_core.tools import get_push_subtree
from multiprocessing import Process
from hernrup_se_core import ghp_import as ghp
from os.path import abspath
from functools import partial

logger = log.getLogger(__name__)


def develop(source_path='.', output_path='./output', port=5000, host='127.0.0.1',
            livereload_port=35729, debug=False, dev=False):
    try:
        gen_fn = partial(generate, output_path=output_path, dev=dev,
                         autoreload=True, debug=debug, source_path=source_path)
        lv_fn = partial(livereload, output_path=output_path, port=port,
                        livereload_port=livereload_port, debug=debug)

        generator = Process(target=gen_fn)
        generator.start()

        livereloader = Process(target=lv_fn)
        livereloader.start()

        generator.join()
        livereloader.join()
    finally:
        generator.terminate()
        livereloader.terminate()


def serve(output_path='./output', port=5000, server='0.0.0.0'):
    with cd(output_path):
        socketserver.TCPServer.allow_reuse_address = True
        try:
            httpd = socketserver.TCPServer((server, port),
                                           ComplexHTTPRequestHandler)
        except OSError as e:
            log.error("Could not listen on port %s, server %s.", port, server)
            sys.exit(getattr(e, 'exitcode', 1))

        log.info("Serving at port %s, server %s.", port, server)
        try:
            httpd.serve_forever()
        finally:
            log.info("Shutting down server.")
            httpd.socket.close()


def livereload(output_path='./output', port=5000, host='127.0.0.1',
               livereload_port=35729, debug=False):

    server = Live_server()

    params = namedtuple('params', 'autoreload debug')
    # server.watch('*.md', generate(params(False, True)))
    server.watch(os.path.join(output_path, '*.html'))

    server.serve(root=output_path, liveport=livereload_port,
                 port=port, host=host,
                 open_url=False, open_url_delay=None, debug=debug)


def clean(path='./output'):
    subprocess.call('rm -rf', abspath(path))


def generate(source_path='.', output_path='./output', dev=False,
             autoreload=False, debug=False):

    with cd(source_path):
        logger.info('Generating blog for source [{}] to output [{}]'
                    .format(abspath(source_path), abspath(output_path)))
        output = ['--output', abspath(output_path)]
        settings = ['--settings', 'conf_dev.py'] if dev else ['--settings',
                                                              'conf.py']
        reload = ['--autoreload'] if autoreload else []
        debug = ['--debug'] if debug else []

        run_args = output + settings + reload + debug
        subprocess.check_call(['pelican', 'content'] + run_args)


def publish(output_path='./output', source_path='.'):
    with cd(source_path):
        logger.info('Publishing folder [{}]'.format(abspath(output_path)))
        ghp.cmd(os.path.abspath(output_path), push=True)


def new_entry(title, source_path='.'):
    template = """
Title: {title}
Date: {year}-{month}-{day} {hour}:{minute:02d}
Modified: {year}-{month}-{day} {hour}:{minute:02d}
Category:
Tags:
Slug: {slug}
Authors:
Summary:
    """

    def make_entry(title):
        today = datetime.today()
        slug = title.lower().strip().replace(' ', '-')

        f_create = "{}_{:0>2}_{:0>2}_{}.md".format(
            today.year, today.month, today.day, slug)
        t = template.strip().format(title=title,
                                    hashes='#' * len(title),
                                    year=today.year,
                                    month=today.month,
                                    day=today.day,
                                    hour=today.hour,
                                    minute=today.minute,
                                    slug=slug)
        with open(os.path.join(source_path, 'content', f_create, 'w')) as w:
            w.write(t)
        print("File created -> " + f_create)

    if title:
        make_entry(title)
    else:
        print("No title given")



class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


