#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six
import base64
import argparse
import requests

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import yaml


def get_public_key(repo):
    keyurl = 'https://api.travis-ci.org/repos/{0}/key'.format(repo)
    try:
        r = requests.get(keyurl)
        r.raise_for_status()
    except Exception as e:
        raise SystemExit(e)
    else:
        try:
            key = r.json()
        except Exception as e:
            raise SystemExit(e)

    return key.get('key')


def encrypt(repo, string):
    public_key = get_public_key(repo)
    key = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(key)
    d = cipher.encrypt(bytes(string, 'utf-8'))
    return base64.b64encode(d)


def update_travis_conf(gh_token, repo, travis_path='./.travis.yml'):
    encrypted = encrypt(repo, 'GH_TOKEN={}'.format(gh_token))
    six.print_('secure: "{0}"'.format(encrypted))

    with open(travis_path) as f:
        data = yaml.load(f)

    data["env"]['global']['secure'] = encrypted

    with open(travis_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
