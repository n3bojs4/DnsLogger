from flask import Flask, render_template, make_response, request, send_from_directory
import secrets
import redis
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


# Set config from config file
mydomain = config['DEFAULT']['MainDomain']

print("Connecting to Redis server:",config['REDIS']['Host'],"on port",config['REDIS']['Port'])
try:
  r = redis.Redis(host=config['REDIS']['Host'], port=config['REDIS']['Port'], socket_timeout=3, db=0)
  r.ping()
  print('successfully connected to redis !')
except:
  print("cannot connect to redis, stopping the program :(")
  traceback.print_exc(file=sys.stderr)
  sys.exit()

@app.route('/')
def index():
    results = ['']
    bar=''
    subdomain = secrets.token_hex(3) + "." + mydomain
    Token = request.cookies.get('Token')
    SubDomain = request.cookies.get('SubDomain')
    if Token:
      StrToMatch = '*'+SubDomain
      streams=r.scan(int=0,_type="stream",match=StrToMatch, count=5000)
      #print("Streams:",streams[1])
      for stream in streams[1]:
        for line in r.xrange(stream):
          date = line[1][b'date'].decode("utf-8")
          type = line[1][b'type'].decode("utf-8")
          ip = line[1][b'ip'].decode("utf-8")
          dnsreq = line[1][b'subdomain'].decode("utf-8")
          bar = date+" "+type+" "+ip+" "+dnsreq
          results.append(bar)
          
      resp = make_response(render_template('index.html',pagetitle=config['DEFAULT']['PageTitle'], subdomain=SubDomain, token=Token, logs=results))
    else:
      Token = secrets.token_urlsafe(24)
      SubDomain = subdomain
      resp = make_response('<HTML><META HTTP-EQUIV="refresh" CONTENT="1">Token generated successfully, reloading the page !</HTML>')
      resp.set_cookie('Token', Token)
      resp.set_cookie('SubDomain', SubDomain)
    return(resp)
    #return render_template('index.html')

@app.route('/Reset', methods = ['POST'])
def ClearCookies():
  resp = make_response(render_template('index.html'))
  resp.set_cookie('Token', 'SubDomain', max_age=0)
  return resp



# Static content
@app.route('/static/<path:path>')
def send_report(path):
  return send_from_directory('static', path)

@app.route('/favicon.ico')
def favicon():
  return send_from_directory('static','favicon.ico',mimetype='image/x-icon')


#Help
# r.scan(int=0,_type="stream",match="*winner.fr") --> retourne un dico avec les résultats