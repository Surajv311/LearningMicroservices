vi ~/.zsh_history

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"\
brew install pyenv\
pyenv install 3.10.6
python3
pyenv versions
ls
python3 -m venv fapi
source ./fapi/bin/activate
ls
touch main.py
pip install fastapi requests\
pip install "uvicorn[standard]"\

sed command: uvicorn app2:app --port 8001 --reload for port 8001, similar app1 file for port 8000
docker run --name redislocal -p 7001:6379 redis 
docker exec -it redislocal redis-cli # inside the container 
127.0.0.1:6379> set name "suraj"
OK
127.0.0.1:6379> get name
"suraj"
127.0.0.1:6379> set nametemp "srjv" EX 10
OK
127.0.0.1:6379> get nametemp
"srjv"
127.0.0.1:6379> get nametemp
(nil)
127.0.0.1:6379> exists name
(integer) 1
127.0.0.1:6379> del name
(integer) 1
127.0.0.1:6379> exists name
(integer) 0
127.0.0.1:6379> append name "verma"
(integer) 5
127.0.0.1:6379> get name
"verma"
127.0.0.1:6379> append name "ABC"
(integer) 8
127.0.0.1:6379> get name
"vermaABC"

127.0.0.1:6379(subscribed mode)> subscribe tempstream
1) "subscribe"
2) "tempstream"
3) (integer) 1
4) "message"
5) "tempstream"

127.0.0.1:6379> publish tempstream "learning redis..."
(integer) 1

You cannot publish if no subscribers

127.0.0.1:6379> info server

docker stop 4c3199c94903
docker stop redislocal 
docker start redislocal


pip install redis
pip freeze > requirements.txt 



docker run --name postgreslocal -p 7002:5432  -e POSTGRES_PASSWORD=1234 postgres # -e is env variable, if you add -d in the command, the terminal will run in detached mode - so in background all postgresql setup commands would run and you can continue using same terminal

docker ps

https://dbeaver.io/ - dbeaver to see postgres gui












https://stackoverflow.com/questions/12857604/python-how-to-check-if-redis-server-is-available
https://www.youtube.com/watch?v=RdPYA-wDhTA
https://hub.docker.com/_/postgres
https://www.youtube.com/watch?v=ZkwKyUZWkp4
https://hub.docker.com/_/redis
https://fastapi.tiangolo.com/
https://medium.com/@AbbasPlusPlus/docker-port-mapping-explained-c453dfb0ae39
https://stackoverflow.com/questions/76046216/fastapi-local-server-every-request-uses-a-different-port-port-in-use-error
https://en.wikipedia.org/wiki/Common_Gateway_Interface
https://docs.python.org/2/howto/webservers.html
https://stackoverflow.com/questions/69641363/how-to-run-fastapi-app-on-multiple-ports
https://www.youtube.com/watch?v=reNPNDustQU
https://www.youtube.com/watch?v=VrZh4f9B-mg
















