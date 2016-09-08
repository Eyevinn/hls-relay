# Copyright 2016 Eyevinn Technology. All rights reserved
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.
# Author: Jonas Birme (Eyevinn Technology)
import argparse
import m3u8
import threading
import time
import re
import urllib
import os
from subprocess import check_call, STDOUT

STATE_INIT = "state_init"
STATE_PARSED_MASTER = "state_parsed_master"
STATE_MASTER_RELAYED = "state_master_relayed"
STATE_MEDIA_PLAYLIST_INIT = "state_media_playlist_init"
STATE_MEDIA_PLAYLIST_UPDATED = "state_media_playlist_updated"
STATE_MEDIA_PLAYLIST_RELAYED = "state_media_playlist_relayed"

class HLSRelay:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
        self.mediaplaylists = []
        self.state = STATE_INIT

    def start(self):
        self.iteration()

    def iteration(self):
        print(time.ctime() + " --- iteration --- %s" % self.state)

        if self.state == STATE_INIT:
            self.parseMaster()
        elif self.state == STATE_PARSED_MASTER:
            self.downloadAndRelayMaster()
            self.state = STATE_MASTER_RELAYED
        elif self.state == STATE_MASTER_RELAYED:
            for p in self.mediaplaylists:
                if self.mediaPlaylistHasChanged(p):
                    p['state'] = STATE_MEDIA_PLAYLIST_UPDATED
                if p['state'] == STATE_MEDIA_PLAYLIST_UPDATED:
                    # Download and relay
                    self.downloadAndRelay(p)
                    # Delete old segments
                    self.deleteOldSegments(p)

        threading.Timer(5, self.iteration).start()

    def mediaPlaylistHasChanged(self, playlist):
        return True

    def downloadAndRelayMaster(self):
        masterpl_file, headers = urllib.urlretrieve(self.src)
        check_call(['curl', '-X', 'POST', '--data-binary', '@%s' % masterpl_file, '%s%s' % (self.dest, 'master.m3u8')])

    def downloadAndRelay(self, playlist):
        obj = m3u8.load(playlist['uri'])
        print("Download and relay %s" % playlist['uri'])
        mediapl_file, headers = urllib.urlretrieve(playlist['uri'])
        for seg in obj.segments:
            if not seg.uri in playlist['relayedsegments'].keys():
                segment_file, headers = urllib.urlretrieve(playlist['base'] + seg.uri)
                check_call(['curl', '-X', 'POST', '--data-binary', '@%s' % segment_file, '%s%s' % (self.dest, seg.uri)])
                playlist['relayedsegments'][seg.uri] = True
                os.remove(segment_file)
        playlist['state'] = STATE_MEDIA_PLAYLIST_RELAYED
        check_call(['curl', '-X', 'POST', '--data-binary', '@%s' % mediapl_file, '%s%s' % (self.dest, playlist['filename'])])
        os.remove(mediapl_file)

    def deleteOldSegments(self, playlist):
        return        

    def parseMaster(self):
        obj = m3u8.load(self.src)
        if not obj.is_variant:
            raise Exception("Source is not a HLS master playlist")
        for p in obj.playlists:
            mediaplaylist = {}
            mediaplaylist['lastUpdated'] = time.ctime()
            mediaplaylist['uri'] = p.uri
            mediaplaylist['relayedsegments'] = {}
            mediaplaylist['state'] = STATE_MEDIA_PLAYLIST_INIT
            if not re.match('^http', mediaplaylist['uri']):
                mediaplaylist['base'] = obj.base_uri
                mediaplaylist['uri'] = obj.base_uri + p.uri
                mediaplaylist['filename'] = p.uri
            self.mediaplaylists.append(mediaplaylist)
        self.state = STATE_PARSED_MASTER

def main():
    parser = argparse.ArgumentParser(description="Pull a HLS stream from one origin and push to another origin")
    parser.add_argument('source', metavar='SRC', help="URI to HLS stream to pull")
    parser.add_argument('dest', metavar='DEST', help="URI where to push the HLS stream")
    args = parser.parse_args()

    relayer = HLSRelay(args.source, args.dest)
    relayer.start()

if __name__ == '__main__':
    try:
        main()
    except Exception, err:
        raise

