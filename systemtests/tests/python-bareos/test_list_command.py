#
#   BAREOS - Backup Archiving REcovery Open Sourced
#
#   Copyright (C) 2021-2021 Bareos GmbH & Co. KG
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

# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import logging
import os
import re
import subprocess
from time import sleep
import unittest
import warnings

import bareos.bsock
from bareos.bsock.constants import Constants
from bareos.bsock.protocolmessages import ProtocolMessages
from bareos.bsock.protocolversions import ProtocolVersions
from bareos.bsock.lowlevel import LowLevel
import bareos.exceptions

import bareos_unittest


class PythonBareosListCommandTest(bareos_unittest.Base):
    def test_list_jobs(self):
        """
        verifying `list jobs` and `llist jobs ...` outputs correct data
        """
        logger = logging.getLogger()

        username = self.get_operator_username()
        password = self.get_operator_password(username)

        director = bareos.bsock.DirectorConsoleJson(
            address=self.director_address,
            port=self.director_port,
            name=username,
            password=password,
            **self.director_extra_options
        )

        director.call("run job=backup-bareos-fd yes")
        director.call("wait")

        # Regular list jobs
        result = director.call("list jobs")

        expected_list_keys = [
            "jobid",
            "name",
            "client",
            "starttime",
            "duration",
            "type",
            "level",
            "jobfiles",
            "jobbytes",
            "jobstatus",
        ]
        self.assertEqual(
            list(result["jobs"][0].keys()).sort(),
            expected_list_keys.sort(),
        )
        reg = re.compile("..:..:..")
        self.assertTrue(re.match(reg, result["jobs"][0]["duration"]))

        # Long list jobs
        result = director.call("llist jobs")

        expected_long_list_keys = [
            "jobid",
            "job",
            "name",
            "purgedfiles",
            "type",
            "level",
            "clientid",
            "client",
            "jobstatus",
            "schedtime",
            "starttime",
            "endtime",
            "realendtime",
            "duration",
            "jobtdate",
            "volsessionid",
            "volsessiontime",
            "jobfiles",
            "jobbytes",
            "joberrors",
            "jobmissingfiles",
            "poolid",
            "poolname",
            "priorjobid",
            "filesetid",
            "fileset",
        ]
        self.assertEqual(
            list(result["jobs"][0].keys()).sort(),
            expected_long_list_keys.sort(),
        )

        # Long list with options

        result = director.call("llist jobs current")
        self.assertNotEqual(
            result["jobs"][0],
            "",
        )

        result = director.call("llist jobs enable")
        self.assertNotEqual(
            result["jobs"][0],
            "",
        )

        result = director.call("llist jobs last")
        self.assertNotEqual(
            result["jobs"][0],
            "",
        )

        expected_long_list_last_keys = [
            "jobid",
            "job",
            "name",
            "purgedfiles",
            "type",
            "level",
            "clientid",
            "client",
            "jobstatus",
            "schedtime",
            "starttime",
            "endtime",
            "realendtime",
            "duration",
            "jobtdate",
            "volsessionid",
            "volsessiontime",
            "jobfiles",
            "jobbytes",
            "joberrors",
            "jobmissingfiles",
            "poolid",
            "poolname",
            "priorjobid",
            "filesetid",
            "fileset",
        ]
        self.assertEqual(
            list(result["jobs"][0].keys()).sort(),
            expected_long_list_last_keys.sort(),
        )

        result = director.call("llist jobs last current")
        self.assertNotEqual(
            result["jobs"][0],
            "",
        )

        result = director.call("llist jobs last current enable")
        self.assertNotEqual(
            result["jobs"][0],
            "",
        )

        # Counting jobs
        result = director.call("list jobs count")

        expected_list_count_keys = ["count"]
        self.assertEqual(
            list(result["jobs"][0].keys()),
            expected_list_count_keys,
        )

        self.assertNotEqual(
            result["jobs"][0]["count"],
            "",
        )

        result = director.call("list jobs count last")
        self.assertNotEqual(
            result["jobs"][0]["count"],
            "",
        )

        result = director.call("list jobs count current")
        self.assertNotEqual(
            result["jobs"][0]["count"],
            "",
        )

        # Long list counting

        result = director.call("llist jobs count")
        expected_long_list_count_keys = ["count"]
        self.assertEqual(
            list(result["jobs"][0].keys()),
            expected_long_list_count_keys,
        )
        self.assertNotEqual(
            result["jobs"][0]["count"],
            "",
        )

        result = director.call("llist jobs count last")
        self.assertNotEqual(
            result["jobs"][0]["count"],
            "",
        )

        result = director.call("llist jobs count current")
        self.assertNotEqual(
            result["jobs"][0]["count"],
            "",
        )

    def test_list_media(self):
        """
        verifying `list media` and `llist media ...` outputs correct data
        """
        logger = logging.getLogger()

        username = self.get_operator_username()
        password = self.get_operator_password(username)

        director = bareos.bsock.DirectorConsoleJson(
            address=self.director_address,
            port=self.director_port,
            name=username,
            password=password,
            **self.director_extra_options
        )

        director.call("run job=backup-bareos-fd yes")
        director.call("wait")

        # check for expected keys
        result = director.call("list media")
        expected_list_media_keys = [
            "mediaid",
            "volumename",
            "volstatus",
            "enabled",
            "volbytes",
            "volfiles",
            "volretention",
            "recycle",
            "slot",
            "inchanger",
            "mediatype",
            "lastwritten",
            "storage",
        ]
        self.assertEqual(
            list(result["volumes"]["full"][0].keys()).sort(),
            expected_list_media_keys.sort(),
        )

        # check expected behavior when asking for specific volume by name
        test_volume = "test_volume0001"
        director.call("label volume={} pool=Full".format(test_volume))
        director.call("wait")
        result = director.call("list media=test_volume0001")
        self.assertEqual(
            result["volume"]["volumename"],
            test_volume,
        )
        result = director.call("list volume={}".format(test_volume))
        self.assertEqual(
            result["volume"]["volumename"],
            test_volume,
        )

        # check expected behavior when asking for specific volume by mediaid
        result = director.call("list mediaid=2")
        self.assertEqual(
            result["volume"]["mediaid"],
            "2",
        )
        result = director.call("list volumeid=2")
        self.assertEqual(
            result["volume"]["mediaid"],
            "2",
        )

        result = director.call("llist mediaid=2")
        self.assertEqual(
            result["volume"]["mediaid"],
            "2",
        )
        result = director.call("llist volumeid=2")
        self.assertEqual(
            result["volume"]["mediaid"],
            "2",
        )
        director.call("delete volume=test_volume0001 yes")
        os.remove("storage/{}".format(test_volume))

    def test_list_pool(self):
        """
        verifying `list pool` and `llist pool ...` outputs correct data
        """
        logger = logging.getLogger()

        username = self.get_operator_username()
        password = self.get_operator_password(username)

        director = bareos.bsock.DirectorConsoleJson(
            address=self.director_address,
            port=self.director_port,
            name=username,
            password=password,
            **self.director_extra_options
        )

        director.call("run job=backup-bareos-fd yes")
        director.call("wait")

        result = director.call("list pool")
        expected_list_media_keys = [
            "poolid",
            "name",
            "numvols",
            "maxvols",
            "pooltype",
            "labelformat",
        ]
        self.assertEqual(
            list(result["pools"][0].keys()).sort(),
            expected_list_media_keys.sort(),
        )

        # check expected behavior when asking for specific volume by name
        result = director.call("list pool=Incremental")
        self.assertEqual(
            result["pools"][0]["name"],
            "Incremental",
        )

        result = director.call("llist pool")
        expected_list_media_keys = [
            "poolid",
            "name",
            "numvols",
            "maxvols",
            "useonce",
            "usecatalog",
            "acceptanyvolume",
            "volretention",
            "voluseduration",
            "maxvoljobs",
            "maxvolbytes",
            "autoprune",
            "recycle",
            "pooltype",
            "labelformat",
            "enabled",
            "scratchpoolid",
            "recyclepoolid",
            "labeltype",
        ]
        self.assertEqual(
            list(result["pools"][0].keys()).sort(),
            expected_list_media_keys.sort(),
        )

        # check expected behavior when asking for specific volume by name
        result = director.call("llist pool=Incremental")
        self.assertEqual(
            result["pools"][0]["name"],
            "Incremental",
        )

        result = director.call("list poolid=3")
        self.assertEqual(
            result["pools"][0]["name"],
            "Full",
        )

        self.assertEqual(
            result["pools"][0]["poolid"],
            "3",
        )

        result = director.call("llist poolid=3")
        self.assertEqual(
            result["pools"][0]["name"],
            "Full",
        )

        self.assertEqual(
            result["pools"][0]["poolid"],
            "3",
        )
