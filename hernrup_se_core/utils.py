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

log_instace = log.getLogger()
log_instace.setLevel(log.DEBUG)


def develop(root='output', port=5000, host='127.0.0.1', livereload_port=35729,
            debug=False, dev=False):
    try:
        generator = Process(target=generate,
                            args=('./output', dev, True, debug))
        generator.start()

        livereloader = Process(
            target=livereload,
            args=('output', port, host, livereload_port, debug))
        livereloader.start()

        # open_browser(host, port)

        generator.join()
        livereloader.join()
    finally:
        generator.terminate()
        livereloader.terminate()


def serve(root='./output', port=5000, server='0.0.0.0'):
    with cd(root):
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
        except KeyboardInterrupt as e:
            log.info("Shutting down server.")
            httpd.socket.close()


def livereload(root='output', port=5000, host='127.0.0.1', livereload_port=35729, debug=False):

    server = Live_server()

    params = namedtuple('params', 'autoreload debug')
    # server.watch('*.md', generate(params(False, True)))
    server.watch('output/*.html')

    server.serve(root='output', liveport=livereload_port,
                 port=port, host=host,
                 open_url=False, open_url_delay=None, debug=debug)


def open_browser(url, port):
    path = os.path.join(get_chrome_path(), 'chrome.exe')
    subprocess.Popen([path, '{}:{}'.format(url, port)])


def get_chrome_path():
    return os.path.abspath(os.path.join(
        os.getenv('APPDATA'), '..', 'Local', 'Google', 'Chrome', 'Application'
    ))


def add_chrome_to_path():
    sys.path.append(get_chrome_path())


def clean(path='./output'):
    subprocess.call('rm -rf', path)


def generate(path='./output', dev=False, autoreload=False, debug=False):
    output = ['--output', path]
    settings = ['--settings', 'conf_dev.py'] if dev else ['--settings',
                                                            'conf.py']
    reload = ['--autoreload'] if autoreload else []
    debug = ['--debug'] if debug else []

    run_args = output + settings + reload + debug
    subprocess.check_call(['pelican', 'content'] + run_args)


def publish(path='./output'):
    ghp.cmd(os.path.abspath(path), push=True)


def new_entry(title):
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
        f_create = "content/{}_{:0>2}_{:0>2}_{}.md".format(
            today.year, today.month, today.day, slug)
        t = template.strip().format(title=title,
                                    hashes='#' * len(title),
                                    year=today.year,
                                    month=today.month,
                                    day=today.day,
                                    hour=today.hour,
                                    minute=today.minute,
                                    slug=slug)
        with open(f_create, 'w') as w:
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


