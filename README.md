# DnsLogger

This program can be used during pentests to gather informations through dns requests.


- [DnsLogger](#dnslogger)
  * [Installation](#installation)
  * [Files](#files)
    + [config.ini](#configini)
    + [webserver.py](#webserverpy)
    + [FakeDnsServer.py](#fakednsserverpy)


## Installation

1. Clone the repo
```
git clone https://github.com/n3bojs4/DnsLogger
cd DnsLogger
```


2. Create venv
```
python3 -m venv .
```

3. Install dependencies
```
pip3 install -r requirements.txt
```

4. Run the fake dns server
```
./FakeDnsServer.py --port 5300 --tcp --udp
```

5. Run the web app
```
./run.sh
```

6. Connect to the webpage and enjoy :D


## Files

### config.ini
Config file for running a mini webserver (Flask), and provide a page which display requests from a redis stream.

### webserver.py
A flask App which show you the logs.

### FakeDnsServer.py
A Fake dns server which log all the requests in a redis stream.
The server replies with i don't know :)

