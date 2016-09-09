# Copyright 2016 Eyevinn Technology. All rights reserved
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.
# Author: Jonas Birme (Eyevinn Technology)
import pytest
from hlsrelay import HLSRelay

def test_invalid_uri_args():
    # Invalid source argument
    try:
        obj = HLSRelay("notanhttpurl.m3u8", "http://example.com/ingest/")
    except:
        assert True
    else:
        assert False

    # Invalid dest argument
    try:
        obj = HLSRelay("http://example.com/master.m3u8", "notanhttpurl.m3u8")
    except:
        assert True
    else:
        assert False

    # No trailing '/' in dest URI
    try:
        obj = HLSRelay("http://example.com/master.m3u8", "http://example2.com/ingest")
    except:
        assert True
    else:
        assert False

    # Should not allow double trailing '/' in URI
    try:
        obj = HLSRelay("http://example.com/master.m3u8", "http://example2.com/ingest//")
    except:
        assert True
    else:
        assert False

    # Should not allow empty URI in src or dest
    try:
        obj = HLSRelay("", "http://example2.com/ingest/")
    except:
        assert True
    else:
        assert False

    try:
        obj = HLSRelay("http://example.com/master.m3u8", "")
    except:
        assert True
    else:
        assert False

def test_valid_uri_args():
    try:
        obj = HLSRelay("http://example.com/master.m3u8", "http://example2.com/ingest/")
    except:
        assert False
    else:
        assert True

    try:
        obj2 = HLSRelay("https://example.com/master.m3u8", "http://example2.com/ingest/")
    except:
        assert False
    else:
        assert True
