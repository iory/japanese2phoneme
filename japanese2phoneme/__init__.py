# flake8: noqa

import pkg_resources


__version__ = pkg_resources.get_distribution("japanese2phoneme").version


import japanese2phoneme.exceptions

from japanese2phoneme.core import get_chunked_kana
