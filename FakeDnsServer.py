#!/usr/bin/env python
"""
LICENSE http://www.apache.org/licenses/LICENSE-2.0
"""

import argparse
import datetime
from operator import sub
import sys
import time
import threading
import traceback
import socketserver
import struct
import redis
import json

try:
    from dnslib import *
except ImportError:
    print("Missing dependency dnslib: <https://pypi.python.org/pypi/dnslib>. Please install it with `pip`.")
    sys.exit(2)


class DomainName(str):
    def __getattr__(self, item):
        return DomainName(item + '.' + self)




def dns_response(data):
    request = DNSRecord.parse(data)


    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    qn = str(qname)
    qtype = request.q.qtype
    qt = QTYPE[qtype]



    return reply.pack()


class BaseRequestHandler(socketserver.BaseRequestHandler):

    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        try:
            data = self.get_data()
            d = DNSRecord.parse(data)
            subdomain=str(d.questions[0]).split()[0].split(';')[1][:-1]
            #Display logs
            print(now,"req type:",self.__class__.__name__[:3],"ip=",self.client_address[0],"subdomain:",subdomain)
            #Store in redis
            record = {
                b'date': str.encode(now),
                b'type': str.encode(self.__class__.__name__[:3]),
                b'ip': str.encode(self.client_address[0]),
                b'subdomain': str.encode(subdomain)
            }
            stream_key = subdomain

            #record = json.dumps(record)
            if(r):
                r.xadd(stream_key,record)
                r.expire(stream_key,86400) # stream expire after 24h
            self.send_data(dns_response(data))
        except Exception:
            traceback.print_exc(file=sys.stderr)


class TCPRequestHandler(BaseRequestHandler):

    def get_data(self):
        data = self.request.recv(8192)
        sz = struct.unpack('>H', data[:2])[0]
        if sz < len(data) - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > len(data) - 2:
            raise Exception("Too big TCP packet")
        return data[2:]

    def send_data(self, data):
        sz = struct.pack('>H', len(data))
        return self.request.sendall(sz + data)


class UDPRequestHandler(BaseRequestHandler):

    def get_data(self):
        return self.request[0]

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)


def main():
    parser = argparse.ArgumentParser(description='Start a DNS implemented in Python.')
    parser = argparse.ArgumentParser(description='Start a DNS implemented in Python. Usually DNSs use UDP on port 53.')
    parser.add_argument('--port', default=5053, type=int, help='The port to listen on.')
    parser.add_argument('--tcp', action='store_true', help='Listen to TCP connections.')
    parser.add_argument('--udp', action='store_true', help='Listen to UDP datagrams.')
    parser.add_argument('--rhost', default='127.0.0.1', type=str, help='The redis host to connect to.')
    parser.add_argument('--rport', default=6379, type=int, help='The redis port to connect to.')

        
    args = parser.parse_args()
    if not (args.udp or args.tcp): parser.error("Please select at least one of --udp or --tcp.")

    print("Connecting to Redis server:",args.rhost,"on port",args.rport)
    try:
        global r
        r = redis.Redis(host=args.rhost, port=args.rport, socket_timeout=3, db=0)
        r.ping()
        print('successfully connected to redis !')
    except:
        print("cannot connect to redis, stopping the program :(")
        traceback.print_exc(file=sys.stderr)
        sys.exit()
    
    


    print("Starting nameserver...")

    servers = []
    if args.udp: servers.append(socketserver.ThreadingUDPServer(('', args.port), UDPRequestHandler))
    if args.tcp: servers.append(socketserver.ThreadingTCPServer(('', args.port), TCPRequestHandler))

    for s in servers:
        thread = threading.Thread(target=s.serve_forever)  # that thread will start one more thread for each request
        thread.daemon = True  # exit the server thread when the main thread terminates
        thread.start()
        print("%s server loop running in thread: %s" % (s.RequestHandlerClass.__name__[:3], thread.name))

    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        for s in servers:
            s.shutdown()

if __name__ == '__main__':
    main()

