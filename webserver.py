from flask import Flask, render_template, make_response, request, send_from_directory
import secrets
import redis
import configparser
import hmac
import traceback
import sys

# Read config file
settings = configparser.ConfigParser()
settings.read('config.ini')

# Set domain from config file
mydomain = settings['DEFAULT']['MainDomain']

# Connect to Redis
print("Connecting to Redis server:",settings['REDIS']['Host'],"on port",settings['REDIS']['Port'])
try:
  r = redis.Redis(host=settings['REDIS']['Host'], port=settings['REDIS']['Port'], socket_timeout=3, db=0)
  r.ping()
  print('successfully connected to redis !')
except:
  print("cannot connect to redis, stopping the program :(")
  traceback.print_exc(file=sys.stderr)
  sys.exit()


def create_app(config):
    app = Flask(__name__)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    

    @app.route('/')
    def index():
        results = ['']
        bar=''
        Token = request.cookies.get('Token')
        SubDomain = request.cookies.get('SubDomain')
        if Token and SubDomain:
                # checking the token
                Secret = settings['DEFAULT']['Secret']
                Secret = str.encode(Secret)
                Encrypted = hmac.new(Secret,SubDomain.encode(),digestmod='sha256')
                Challenge = Encrypted.hexdigest()
                if Challenge not in Token:
                    SubDomain = 'YouCantOwnThisToken'
                StrToMatch = '*'+SubDomain
                try:
                    streams=r.scan(int=0,_type="stream",match=StrToMatch, count=5000)
                except:
                    print("Error: cannot scan redis streams. Exiting.")
                    traceback.print_exc(file=sys.stderr)
                    sys.exit()
    
                for stream in streams[1]:
                    for line in r.xrange(stream):
                        date = line[1][b'date'].decode("utf-8")
                        type = line[1][b'type'].decode("utf-8")
                        ip = line[1][b'ip'].decode("utf-8")
                        dnsreq = line[1][b'SubDomain'].decode("utf-8")
                        bar = date+" "+type+" "+ip+" "+dnsreq
                        results.append(bar)
          
                resp = make_response(render_template('index.html',pagetitle=settings['DEFAULT']['PageTitle'], subdomain=SubDomain, token=Token, logs=results))
        else:
            # Here we generate a random subdomain for first time
            SubDomain = secrets.token_hex(3) + "." + mydomain
            print("SubDomain =",SubDomain)
            # Generate the token with secret and subdomain
            Secret = settings['DEFAULT']['Secret']
            Secret = str.encode(Secret)
            Encrypted = hmac.new(Secret,SubDomain.encode(),digestmod='sha256')
            Token = Encrypted.hexdigest()
            resp = make_response('<HTML><META HTTP-EQUIV="refresh" CONTENT="1">Token generated successfully, reloading the page !</HTML>')
            resp.set_cookie('Token', Token)
            resp.set_cookie('SubDomain', SubDomain)
        return(resp)

    @app.route('/Reset', methods = ['POST'])
    def ClearCookies():
        resp = make_response(render_template('index.html'))
        resp.set_cookie('Token', 'SubDomain', max_age=0)
        return resp



    # Serve Static content
    @app.route('/static/<path:path>')
    def send_report(path):
        return send_from_directory('static', path)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory('static','favicon.ico',mimetype='image/x-icon')
    return app



