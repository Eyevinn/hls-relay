# Copyright 2016 Eyevinn Technology. All rights reserved
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.
# Author: Jonas Birme (Eyevinn Technology)
import pytest
from hlsrelay import HLSRelay

def test_valid_live_master():
    try:
        obj = HLSRelay("http://localhost:8111/validlive/master.m3u8", "http://localhost:8111/ingest/")
        obj.parseMaster()
    except:
        assert False
    else:
        assert True

def test_not_a_master():
    try:
        obj = HLSRelay("http://localhost:8111/validlive/master2500.m3u8", "http://localhost:8111/ingest/")
        obj.parseMaster()
    except:
        assert True
    else:
        assert False

def test_not_a_vod():
    try:
        obj = HLSRelay("http://localhost:8111/vod/master.m3u8", "http://localhost:8111/ingest/")
        obj.parseMaster()
    except:
        assert True
    else:
        assert False
