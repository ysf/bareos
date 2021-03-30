#!/usr/bin/python
#   BAREOS - Backup Archiving REcovery Open Sourced
#
#   Copyright (C) 2020-2021 Bareos GmbH & Co. KG
#
#   This program is Free Software; you can redistribute it and/or
#   modify it under the terms of version three of the GNU Affero General Public
#   License as published by the Free Software Foundation and included
#   in the file LICENSE.
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#   02110-1301, USA.


import os
import re
from setuptools import find_packages, setup


def get_version():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    try:
        with open(os.path.join(base_dir, "bareos", "VERSION.txt")) as version_file:
            # read version
            # and adapt it according to
            # https://www.python.org/dev/peps/pep-0440/.
            fullversion = version_file.read().strip()
            __version__ = re.compile(r"~pre([0-9]+).*").sub(r".dev\1", fullversion)
    except IOError:
        # Fallback version.
        # First protocol implemented
        # has been introduced with this version.
        __version__ = "20.0.0"

    return __version__


setup(
    name="python-bareos-restapi",
    version=get_version(),
    license="AGPLv3",
    author="Bareos Team",
    author_email="packager@bareos.com",
    packages=find_packages(where="src"),
    package_data={"bareos": ["VERSION.txt"]},
    url="https://github.com/bareos/bareos/",
    # What does your project relate to?
    keywords="bareos, REST API",
    description="REST API for Bareos console access.",
    long_description=open("README.md").read(),
    long_description_content_type="text/x-rst",
    # Python 2.6 is used by RHEL/Centos 6.
    # When RHEL/Centos 6 is no longer supported (End of 2020),
    # Python 2.6 will no longer be supported by python-bareos.
    python_requires=">=3.6",
    install_requires=[
        "fastapi",
        "dataclasses",
        "fastapi",
        "pydantic",
        "python-bareos",
        "starlette==0.13.6",
        "python-jose",
        "uvicorn",
        "python-multipart",
        "passlib",
        "packaging",
        "pyyaml",
    ],
    extras_require={"TLS-PSK": ["sslpsk"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python ::3",
        "Topic :: System :: Archiving :: Backup",
    ],
)
