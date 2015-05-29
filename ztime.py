#!/usr/bin/python3

from zocp import ZOCP
import socket
import logging
import time
import json
import statistics

class TimeNode(ZOCP):
    # Constructor
    def __init__(self, nodename):
        super(TimeNode, self).__init__(nodename)

        self.interval = 0.02
        self.loop_time = 0

        self.time_offset = None
        self.time = 0
        self.time_offsets = []
        self.sync_timeout = 0

        self.register_float("Time", self.time, 'rwe')
        self.start()

        self.group = self.own_groups()[0]
        self.sync_timeout = time.time() + 1

        while True:
            try:
                self.run_once(0)
                if time.time() >= self.loop_time:
                    self.loop_time = time.time() + self.interval
                    self.on_timer()
            except (KeyboardInterrupt, SystemExit):
                break
        self.stop()


    def on_peer_enter(self, peer, name, *args, **kwargs):
        if self.time_offset is None:
            self.request_sync()


    def on_timer(self):
        if self.time_offset is None:
            if time.time() > self.sync_timeout:
                # did not receive sync responses
                self.time_offset = time.time()
        else:
            self.emit_signal('Time', time.time() - self.time_offset)
            print(time.time() - self.time_offset)
    

    def request_sync(self):
        self.time_offsets = []
        msg = json.dumps({'DTIME_GET': time.time()})
        self.shout(self.group, msg.encode('utf-8'))
        self.sync_timeout = time.time() + 1


    def handle_DTIME_GET(self, msg, peer, name, grp):
        if self.time_offset is None:
            return
        msg = json.dumps({'DTIME_REP': [msg, time.time(), self.time_offset]})
        self.whisper(peer, msg.encode('utf-8'))


    def handle_DTIME_REP(self, msg, peer, name, grp):
        peer_time = (time.time() + msg[0])/2
        self.time_offsets.append(peer_time - msg[1] + msg[2])
        self.time_offset = statistics.median(self.time_offsets)


        
if __name__ == '__main__':
    zl = logging.getLogger("zocp")
    zl.setLevel(logging.DEBUG)

    z = TimeNode("time@%s" % socket.gethostname())
    del z
    print("FINISH")
