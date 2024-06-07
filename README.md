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

pip install SQLAlchemy psycopg2-binary
pip install pydantic pandas

used command: uvicorn app2:app --port 8001 --reload 
for port 8001, similar app1 file for port 8000: uvicorn app1:app --port 8000 --reload 
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


docker run --name postgreslocal -p 7002:5432  -e POSTGRES_PASSWORD=1234 -e POSTGRES_USER=postgresdockerlocal postgres # -e is env variable, if you add -d in the command, the terminal will run in detached mode - so in background all postgresql setup commands would run and you can continue using same terminal

docker ps

docker exec -it postgreslocal bash # to get into container of postgres, we have named container postgreslocal as we know
root@e4fb5a81ca46:/# psql -U postgresdockerlocal
postgresdockerlocal-# create database fapidb; (note that the semi colon is very important when you execute the commands else it wont work)
postgresdockerlocal-# CREATE USER postgresdluser WITH PASSWORD '1234'; (also docs: https://www.postgresql.org/docs/8.0/sql-createuser.html)
## Note: I have observed in postgresql docker container after executing command, execute it 2-3 times as the shell seems to be not listening very well. Also, sometimes, it doesn't sync well, so better exit the container and enter again for changes to work
postgresdockerlocal=# \du ## Note that \q will exit session
List of roles
      Role name      |                         Attributes                         
---------------------+------------------------------------------------------------
 postgresdluser      | 
 postgresdockerlocal | Superuser, Create role, Create DB, Replication, Bypass RLS
postgresdockerlocal-# grant all privileges on database fapidb to postgresdluser;
postgresdockerlocal=# GRANT CONNECT ON DATABASE fapidb TO postgresdluser;
(to grant privileges to postgresdluser (because same user I am using in code to access the database and tables) used:)
postgresdockerlocal=# GRANT pg_read_all_data TO postgresdluser;
postgresdockerlocal=# GRANT pg_write_all_data TO postgresdluser;
postgresdockerlocal=# GRANT ALL PRIVILEGES ON DATABASE "fapidb" to postgresdluser;
postgresdockerlocal=# GRANT USAGE ON SCHEMA public TO postgresdluser;
postgresdockerlocal=# GRANT ALL ON SCHEMA public TO postgresdluser;
postgresdockerlocal=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgresdluser;
postgresdockerlocal=# ALTER DATABASE fapidb OWNER TO postgresdluser; ## as above changes were not working, despite my new user, it was not getting access/privileges, hence changed the db owner
postgresdockerlocal=# \c fapidb postgresdluser (to connect to our database with the given user) ### To connect to database with superuser: postgresdockerlocal=# \c fapidb
(for all commands above, followed steps in this doc: https://www.commandprompt.com/education/how-to-create-a-postgresql-database-in-docker/, also followed the youtube video: https://www.youtube.com/watch?v=2X8B_X2c27Q)
fapidb-# \dt (to list down all tables)
fapidb=> SELECT current_user;
fapidb=# CREATE TABLE tpsqltable(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, TYPE TEXT NOT NULL, PHONE INT NOT NULL);
fapidb=# INSERT INTO tpsqltable VALUES (1, 'suraj', 'test', 12345);
fapidb=# select * from tpsqltable;
 id | name  | type | phone 
----+-------+------+-------
  1 | suraj | test | 12345
(1 row)


## setting up podman as in docker removed from laptop - company...
installed podman desktop, later docs: https://podman.io/docs/installation
for all docker commands, just replace with keyword podman, eg: 
podman run --name redislocal -p 7001:6379 redis
podman run --name postgreslocal -p 7002:5432  -e POSTGRES_PASSWORD=1234 -e POSTGRES_USER=postgresdockerlocal postgres

podman exec -it redislocal redis-cli        
podman exec -it postgreslocal bash

brew install k6 - to do load testing of api
after writing k6 test code - in terminal - k6 run loadtest.js
configuration in loadtest.js


first, i let async code run, results:
     checks.........................: 100.00% ✓ 19474      ✗ 0     
     data_received..................: 4.2 MB  116 kB/s
     data_sent......................: 1.7 MB  47 kB/s
     http_req_blocked...............: avg=15.33µs  min=0s      med=1µs      max=3.74ms p(90)=1µs      p(95)=2µs     
     http_req_connecting............: avg=14.08µs  min=0s      med=0s       max=3.19ms p(90)=0s       p(95)=0s      
     http_req_duration..............: avg=185.55ms min=14.04ms med=175.95ms max=2.35s  p(90)=203.18ms p(95)=216.06ms
       { expected_response:true }...: avg=185.55ms min=14.04ms med=175.95ms max=2.35s  p(90)=203.18ms p(95)=216.06ms
     http_req_failed................: 0.00%   ✓ 0          ✗ 19474 
     http_req_receiving.............: avg=14.73µs  min=4µs     med=9µs      max=2.92ms p(90)=29µs     p(95)=37µs    
     http_req_sending...............: avg=3.81µs   min=1µs     med=3µs      max=2.75ms p(90)=6µs      p(95)=7µs     
     http_req_tls_handshaking.......: avg=0s       min=0s      med=0s       max=0s     p(90)=0s       p(95)=0s      
     http_req_waiting...............: avg=185.53ms min=14.01ms med=175.94ms max=2.35s  p(90)=203.16ms p(95)=216.05ms
     http_reqs......................: 19474   537.545307/s
     iteration_duration.............: avg=185.61ms min=14.1ms  med=175.99ms max=2.35s  p(90)=203.23ms p(95)=216.09ms
     iterations.....................: 19474   537.545307/s
     vus............................: 100     min=100      max=100 
     vus_max........................: 1000    min=1000     max=1000

After doing stress test on this, my server went down and not responding ~ http://127.0.0.1:8000/ took too long to respond.
Thinking what to do next, port 8001, is working and thinking to try that - but want to understand how to make port 8000 up again 

So planning to restart containers as API is down post stress testing. 
First seeing running containers: podman ps (since docker removed from our systems by admin, instead of docker ps, using podman ps)
even after restarting redis/postgres container and restarting the fast api app on the port 8000, still application is down post stress testing, and normal health check APIs are not responding for all. If I run app on different port, its fine, but same port, seems some issue.
Update: Now able to restart servers - I killed the process pid. To do so, first listed all services using the port using: 
`lsof -i :8000`. 
Then killed them using: `kill -9 <pid>` - kill pid (which sends signal 15 (SIGTERM)) tells pid to terminate, but said program can execute some code first or even ignore the signal. kill -9 pid, on the other hand, forces the program to immediately terminate (it cannot be ignored).
And then restarted the services using uvicorn

Later ran stress testing of sync code, results: 






pip3 install locust













------------------------------------

References/ Other notes: 

https://dbeaver.io/ - dbeaver to see postgres gui

pydantic: 
One of the primary ways of defining schema in Pydantic is via models. Models are simply classes which inherit from pydantic.BaseModel and define fields as annotated attributes.
Pydantic is the most widely used data validation library for Python.
Data classes are one of the new features of Python 3.7. With data classes, you do not have to write boilerplate code to get proper initialization, representation, and comparisons for your objects.
In Python, a data class is a class that is designed to only hold data values. They aren't different from regular classes, but they usually don't have any other methods. They are typically used to store information that will be passed between different parts of a program or a system.
https://www.dataquest.io/blog/how-to-use-python-data-classes/
Eg of pydantic: 
from pydantic import BaseModel
class User(BaseModel):
    id: int
    name: str = 'Jane Doe'
user = User(id='123')
assert user.id == 123
assert isinstance(user.id, int)


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
https://www.youtube.com/watch?v=d_ugoWsvGLI

https://fastapi.tiangolo.com/async/
https://www.youtube.com/watch?v=2X8B_X2c27Q

https://stackoverflow.com/questions/22483555/postgresql-give-all-permissions-to-a-user-on-a-postgresql-database
https://stackoverflow.com/questions/50180667/how-can-i-connect-to-a-database-as-another-user
https://stackoverflow.com/questions/60138692/sqlalchemy-psycopg2-errors-insufficientprivilege-permission-denied-for-relation
https://stackoverflow.com/questions/63044935/flask-sqlalchemy-postgres-error-could-not-connect-to-server-connection-refuse
https://stackoverflow.com/questions/39257147/convert-pandas-dataframe-to-json-format
https://medium.com/@kevinkoech265/a-guide-to-connecting-postgresql-and-pythons-fast-api-from-installation-to-integration-825f875f9f7d
https://www.squash.io/connecting-fastapi-with-postgresql-a-practical-approach/
reference to use async await in api: https://stackoverflow.com/questions/68733675/can-i-use-await-on-multiple-functions-at-once
https://grafana.com/docs/k6/latest/set-up/fine-tune-os/
https://askubuntu.com/questions/791841/difference-kill-9-pid-and-kill-pid-command
https://stackoverflow.com/questions/19071512/socket-error-errno-48-address-already-in-use




------------------------------------

