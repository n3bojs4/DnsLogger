# DnsLogger

This program can be used during pentests to gather informations through dns requests.

## config.ini
Config file for running a mini webserver (Flask), and provide a page which display requests from a redis stream.

## webserver.py
A flask App which show you the logs.

## FakeDnsServer.py
A Fake dns server which log all the requests in a redis stream.
The server replies with i don't know :)

