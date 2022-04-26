# DnsLogger

This program can be used during pentests to gather informations through dns requests.

- [DnsLogger](#dnslogger)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Running](#running)
  * [Files](#files)
    + [config.ini](#configini)
    + [webserver.py](#webserverpy)
    + [FakeDnsServer.py](#fakednsserverpy)
    + [static dir](#static-dir)
  * [License](#License)
  
## Prerequisites

Python3+

A redis server 5.0+ (which support streams)


## Installation

Clone the repo
```
git clone https://github.com/n3bojs4/DnsLogger
cd DnsLogger
```


Create venv
```
python3 -m venv .
```

Install dependencies
```
pip3 install -r requirements.txt
```

## Running

Run the fake dns server
```
./FakeDnsServer.py --port 5300 --tcp --udp
```

Run the web app
```
./run.sh
```

Connect to the webpage and enjoy :D


## Files

### config.ini
Config file for running a mini webserver (Flask), and provide a page which display requests from a redis stream.

### webserver.py
A flask App which show you the logs.

### FakeDnsServer.py
A Fake dns server which log all the requests in a redis stream.
The server replies with i don't know :)

## static dir
All css and js needed by the app.


# LICENSE
MIT LICENSE, see LICENSE file for more informations.