# -*- coding: utf-8 -*-

import os
import sys

from deconstrst.deconstrst import build, submit, get_conf_builder
from deconstrst.config import Configuration

__author__ = 'Ash Wilson'
__email__ = 'ash.wilson@rackspace.com'
__version__ = '0.1.0'


def main(directory=False):

    config = Configuration(os.environ)

    if config.content_root:
        if directory and directory != config.content_root:
            print("Warning: Overriding CONTENT_ROOT [{}] with argument [{}].".format(config.content_root, directory))
        else:
            os.chdir(config.content_root)
    elif directory:
        os.chdir(directory)

    if os.path.exists("_deconst.json"):
        with open("_deconst.json", "r", encoding="utf-8") as cf:
            config.apply_file(cf)

    # Lock source and destination to the same paths as the Makefile.
    srcdir = '.'
    destdir = os.path.join('_build', get_conf_builder(srcdir))

    status = build(srcdir, destdir)
    if status != 0:
        sys.exit(status)

    reasons = config.skip_submit_reasons()
    if reasons:
        print("Not submitting content to the content service because:",
              file=sys.stderr)
        print(file=sys.stderr)
        for reason in reasons:
            print(" * " + reason, file=sys.stderr)
        print(file=sys.stderr)
        return

    submit(destdir,
           config.content_store_url,
           config.content_store_apikey,
           config.content_id_base,
           config.tls_verify)


if __name__ == '__main__':
    main()
