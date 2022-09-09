export FLASK_APP="webserver:create_app('dev')"
FLASK_ENV=development
flask run -p 5001 -h $(ip -j addr show dev ens2 | awk -F '"local":"' '{print $2}' | awk -F '"' '{print $1}')

