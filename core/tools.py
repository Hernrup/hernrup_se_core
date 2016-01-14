import subprocess
import os
import shutil
import errno
import os.path as op
from subprocess import call

def _get_git_path():
    return os.path.join(os.path.expandvars('%PROGRAMFILES(x86)%'),
                        'Git', 'cmd', 'git.exe')

def _git(args):
    subprocess.check_call([_get_git_path()] + args)


def git_add_and_commit(files, commit_message, author=None):
    _git(['add'] + files)

    args = ['commit', '-m', commit_message]
    if author:
        args = args + ['--author', author]

    _git(args)


def get_push_subtree(folder, upstream, branch, force=False):
    if force:
        raise NotImplementedError()
        # git push origin `git subtree split --prefix build_folder master`:gh-pages --force
    _git(['subtree', 'push', '--prefix', folder, upstream, branch])


def git_tag(version):
    _git(['tag', '-a', version, '-m', "\"{} release\"".format(version)])
    _git(['pull'])
    _git(['push'])
    _git(['push', 'origin', version])


def move_file(source, dest):
    if os.path.exists(dest):
        os.remove(dest)

    shutil.move(source, dest)


def copy(src, dest, exclude=tuple()):
    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns(*exclude))
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            if os.path.exists(dest):
                os.remove(dest)
            shutil.copy(src, dest)
        else:
            print('Copy failed. Error: %s' % e)


def zipdir(outfile, path):
    if os.path.exists(outfile):
        os.remove(outfile)

    shutil.make_archive(outfile, 'zip', path)


def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def base_path():
    return op.abspath(op.dirname(__file__))

