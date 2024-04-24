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
root@e4fb5a81ca46:/# psql -U postgres
postgres-# create database fapidb; (note that the semi colon is very important when you execute the commands else it wont work)
postgres-# CREATE USER postgresdluser WITH PASSWORD '1234'; (also docs: https://www.postgresql.org/docs/8.0/sql-createuser.html)
postgres-# grant all privileges on database fapidb to postgresdluser;
postgres=# \c fapidb (to connect to our database)

######## postgres=# \c fapidb postgresdluser (to connect to our database with the given user) ########

(for all commands above, followed steps in this doc: https://www.commandprompt.com/education/how-to-create-a-postgresql-database-in-docker/, also follwed the youtube video: https://www.youtube.com/watch?v=2X8B_X2c27Q)
fapidb-# \dt (to list down all tables)
fapidb=# CREATE TABLE tpsqltable(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, TYPE TEXT NOT NULL);
fapidb=# INSERT INTO tpsqltable VALUES (1, 'suraj', 'test');
fapidb=# select * from tpsqltable;
 id | name  | type 
----+-------+------
  1 | suraj | test
(1 row)

postgres=# \du
                                  List of roles
      Role name      |                         Attributes                         
---------------------+------------------------------------------------------------
 postgres            | Superuser, Create role, Create DB, Replication, Bypass RLS
 postgresdluser      | 
 postgresdockerlocal | 

to grant privileges to postgresdluser (because same user I am using in code to access the database and tables) used: 
postgres=# GRANT pg_read_all_data TO postgresdluser;
postgres=# GRANT pg_write_all_data TO postgresdluser;
postgres=# GRANT ALL PRIVILEGES ON DATABASE "fapidb" to postgresdluser;

















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










