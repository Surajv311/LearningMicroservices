## Project Overview

- Initial intention (rough): 
  - We must have 2 applications say: `businessMicroservice` and `consumerMicroservice`. 
  - Consider having the following db containers running as well locally: `postgresql`, `redis`, `mongodb`, etc.
  - `businessMicroservice` should have endpoints which check the health of db containers, query over tables in the db's, and have the ability to perform basic CRUD operations. 
  - Containzerize the application. 
  - We should be able to spin up multiple instances of the microservice running on different ports. There should be APIs which capture status of another port from a given port.
  - Later, `consumerMicroservice` should be designed to mimic how a user/entity would interact with APIs in `businessMicroservice`. In short, allow 2 microservices to communicate with one another. 
  - Try running `businessMicroservice` in 2 container instances in different ports. And then your `consumerMicroservice` should send request to each of the running containers of `businessMicroservice` in round-robin fashion, kind of acting like a load balancer.

- Future intention (rough)
  - The complexity of project will increase with time. We will have more scenarios to cover like: publishing data to Kafka/Flink; Or having Debezium setup to capture CDC once we update postgres tables via our microservices, etc. 
  - Objective is to mimic how production systems work as closely as possible. As a note, intention is to learn how services or systems interact locally, once, that is clear, understanding how things work in cloud would be much easier, as core concepts remain the same!.  

Note: Some major errors I encountered, learnings, blogs/videos, little help from chatgpt in understanding concepts (and re-verified as well) I have attached at the bottom of the Readme for reference. 

------------------------------------------------------

### Steps followed (Flow) in project: 

Locally, created a directory called: `fastapiproject/` to have all project files saved. 

Necessary installations (mac):
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"\
brew install pyenv
pyenv install 3.10.6
python3
pyenv versions
```
And do ensure you have `pip` package manager installed and docker/podman installed to run containers. 
In this exercise, I have used docker in the beginning later switched to podman (Note all docker commands run same in podman, except instead of using `docker` keyword, use `podman` in commands)
So do install docker, docker desktop, podman, docker compose, podman compose (compose utilities are different and should be installed separately - we learn more about them later)

Create 2 folders or virtual environments where we will have our code: 
`python3 -m venv consumerMicroservice`
`python3 -m venv businessMicroservice`

Ensure env is clean by checking installed packages:
`pip list`

Before starting project my Py version: Python 3.9.6
(Not sure why, but Py 3.10.6 was not installing, so went ahead with 3.9.6 for now)

We will work around developing `businessMicroservice` so activate the env. We can also activate `consumerMicroservice` though not using it now. 
Open 2 terminals and `cd` into the directory for business & consumer service and activate the env. 
In my case: (Eg)
`cd /Users/suraj/Desktop/projectsSimpl/fastapiproject/fapi/consumerMicroservice`
`source bin/activate`
`cd /Users/suraj/Desktop/projectsSimpl/fastapiproject/fapi/businessMicroservice`
`source bin/activate`

Current focus on developing `businessMicroservice` once venv activated:

Installing few packages: 
```
pip install fastapi requests "uvicorn[standard]" SQLAlchemy==1.4.46 psycopg2-binary pydantic pandas redis
```

Exporting the installed packages/dependencies in env in a requirements.txt file: 
`pip freeze > requirements.txt`

My current snapshot of packages based on commands ran earlier: 
```
annotated-types==0.5.0
anyio==3.7.1
async-timeout==4.0.3
certifi==2024.6.2
charset-normalizer==3.3.2
click==8.1.7
exceptiongroup==1.2.1
fastapi==0.103.2
greenlet==3.0.3
h11==0.14.0
httptools==0.6.0
idna==3.7
importlib-metadata==6.7.0
numpy==1.21.6
pandas==1.3.5
psycopg2-binary==2.9.9
pydantic==2.5.3
pydantic_core==2.14.6
python-dateutil==2.9.0.post0
python-dotenv==0.21.1
pytz==2024.1
PyYAML==6.0.1
redis==5.0.6
requests==2.31.0
six==1.16.0
sniffio==1.3.1
SQLAlchemy==1.4.46
starlette==0.27.0
typing_extensions==4.7.1
urllib3==2.0.7
uvicorn==0.22.0
uvloop==0.18.0
watchfiles==0.20.0
websockets==11.0.3
zipp==3.15.0
```

We could have also defined packages in the txt file first and then run `pip install -r requirements.txt`. 

Create core logic files: `touch main.py app.py`

Writing boilerplate fastapi code in `main.py`: 
```
Core logic: 
@app.get("/")
def health_check_root_endpoint():
    return {"Health check: main.py root server"}
```
My current dir: `/Users/suraj/Desktop/projectsSimpl/fastapiproject/fapi/businessMicroservice`
To run the app server on a port 8000 command used in env terminal: `uvicorn app:app --port 8000 --reload`
Note in above case, the path where you execute the command and the file path are same. 
Assume you are in a different path and want to run the server, it can also be done (same I have done here for learning purposes in this repo);
To run the main app server on a port 8001 command used in env terminal: `uvicorn sampleService.main:app --port 8001 --reload`. You use `.` operator to give the path. 

As we see, the app is running up on a server we defined. 

**Task1**: Write a logic wherein when you hit an endpoint of app running on port 8000, it returns the health status of app running on port 8001? 
```
Core logic: 
@app.get("/mainappstatus")
def read_root():
    url = 'http://127.0.0.1:8001/currentStatus' # Note that endpoint is camelCase, same is expected when typing in url/testing via postman
    response = requests.get(url)
    print(f"Status of main app server: {response.status_code}")
    data = json.loads(response.text)
    return data
    
Note: I start both the app/main servers in different ports 8000, 8001 and ensure they are running to be able to properly test code, by running previous commands as shown earlier. 
```

Setup Redis locally via docker using commands: 
Note that in below command I am using port mapping 7001:6379, i.e will run the Redis container on a different port 7001 rather than default port 6379 (in a rough way). 
To be more technical (which we will again revisit and understand in later parts):
- We are using concept of port mapping; So this flag maps port 6379 inside the container (the default port Redis listens on) to port 7001 on the host machine. This allows you to connect to Redis on your host machine using localhost:7001.
- When we type http://localhost:7001/ in our browser or postman, we won't get any response though as it (Redis) is a database server, not a web server. Redis container listens for database connections on its port (in this case, 6379 mapped to 7001), but it does not serve web pages or respond to HTTP requests.

```
docker run --name redislocal -p 7001:6379 redis 
docker exec -it redislocal redis-cli # inside the container 

# Similar to docker, we can also use podman; like: 
## podman run --name redislocal -p 7001:6379 redis
## podman exec -it redislocal redis-cli    

Commands to execute inside redis container to setup/play around: 
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

# stopping and starting redis container 
docker stop 4c3199c94903
docker stop redislocal (or) podman stop redislocal
docker start redislocal (or) podman start redislocal

# to get the version or details of the container use: docker inspect redislocal (or) podman inspect redislocal
We get version is, apart from other details (as I am doing the project): "REDIS_VERSION=7.2.4"
```

Setup Postgresql locally via docker using commands: 
```
docker run --name postgreslocal -p 7002:5432  -e POSTGRES_PASSWORD=1234 -e POSTGRES_USER=postgresdockerlocal postgres 
# Note that -e key in command means env variable, if you add -d in the command, the terminal will run in detached mode - so in background all postgresql setup commands would run and you can continue using same terminal

We can also use podman instead of docker; simply: 
podman run --name postgreslocal -p 7002:5432  -e POSTGRES_PASSWORD=1234 -e POSTGRES_USER=postgresdockerlocal postgres

Commands to run inside postgres container to setup/play around: 
docker exec -it postgreslocal bash # to get into container of postgres, we have named container postgreslocal as we know
## Or to use podman: podman exec -it postgreslocal bash

root@e4fb5a81ca46:/# psql -U postgresdockerlocal # we know the user name is postgresdockerlocal

## Creating a database, later we create tables inside it
postgresdockerlocal-# create database fapidb; 
## Note that the semi colon is very important when you execute the commands else it wont work)

# Creating another user and trying to create tables/db using that 
postgresdockerlocal-# CREATE USER postgresdluser WITH PASSWORD '1234'; 
## Note: I have observed in postgresql docker container after executing command, execute it 2-3 times as the shell seems to be not listening very well. Also, sometimes, it doesn't sync well, so better exit the container and enter again for changes to work

postgresdockerlocal=# \du ## Note that \q will exit session
List of roles
      Role name      |                         Attributes                         
---------------------+------------------------------------------------------------
 postgresdluser      | 
 postgresdockerlocal | Superuser, Create role, Create DB, Replication, Bypass RLS
 
## Giving all necessary permissions to our new user which we use to create tables/db. 
postgresdockerlocal-# grant all privileges on database fapidb to postgresdluser;
postgresdockerlocal=# GRANT CONNECT ON DATABASE fapidb TO postgresdluser;
postgresdockerlocal=# GRANT pg_read_all_data TO postgresdluser;
postgresdockerlocal=# GRANT pg_write_all_data TO postgresdluser;
postgresdockerlocal=# GRANT ALL PRIVILEGES ON DATABASE "fapidb" to postgresdluser;
postgresdockerlocal=# GRANT USAGE ON SCHEMA public TO postgresdluser;
postgresdockerlocal=# GRANT ALL ON SCHEMA public TO postgresdluser;
postgresdockerlocal=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgresdluser;

## Trying to create a new table from our new user in the database: 
fapidb=# CREATE TABLE tpsqltable(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, TYPE TEXT NOT NULL, PHONE INT NOT NULL);
## But above command gave me error - despite debugging different ways, giving all permissions, still error persisted, so I changed my new user to root user - Not a good way to do, but it is what it is... 

postgresdockerlocal=# ALTER DATABASE fapidb OWNER TO postgresdluser; ## as above changes were not working, despite my new user, it was not getting access/privileges, hence changed the db owner
postgresdockerlocal=# \c fapidb postgresdluser (to connect to our database with the given user) 
### Note: To connect to database with superuser: postgresdockerlocal=# \c fapidb
fapidb-# \dt (to list down all tables)
fapidb=> SELECT current_user;
fapidb=# CREATE TABLE tpsqltable(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, TYPE TEXT NOT NULL, PHONE INT NOT NULL);
fapidb=# INSERT INTO tpsqltable VALUES (1, 'suraj', 'test', 12345);
fapidb=# select * from tpsqltable;
 id | name  | type | phone 
----+-------+------+-------
  1 | suraj | test | 12345
(1 row)

# to get the version or details of the container use: docker inspect postgreslocal (or) podman inspect postgreslocal
We get version is, apart from other details (as I am doing the project): "PG_VERSION=16.2-1.pgdg120+2"
```

**Task2**: Create a logic wherein you can get the health status of your postgres and redis containers from app running on port 8000? 
In database/ dir, I have defined the postgres and redis configs, which I use and later in app.py I check the health of both containers. 
```
I have segregated code in app.py under name Task2 which can be referred. 
Also have created config files in database dir. 
Note that in the postgres config defined: Either I can directly use the postgres url defined in variable, or I can export it in my local env by running command in terminal: 
export POSTGRES_DB_URL="postgresql://postgresdluser:1234@localhost:7002/fapidb"
And then extract value from this variable using os.getenv() ~ same can be seen in the postgresDbConfig.py file
```

**Task3**: Write an async version of health check code for postgres and redis in 8000 port app, and try getting the health status of both sync and async code? 
```
I have segregated code in app.py under name Task3 which can be referred 
```

Note: There could be times when app gets stuck or even after refresh it does not send a response or gives ERROR: Address already in use response, in such case, we can kill the app running on port and restart it. 
Simply put: List the servers using the port using: `lsof -i :8000`. 
Kill the process pid: `kill -9 <pid>`
(Command: `kill <pid>` sends signal (SIGTERM) and tells pid to terminate, but said program can execute some code first or even ignore the signal. `kill -9 <pid>`, on the other hand, forces the program to immediately terminate and cannot be ignored.

**Task4**: Load test the sync and async version of your API using k6, ab (Apache Benchmark), or any other tool? 
First, I have tested using k6. Installing: `brew install k6`
Reading docs, and then put the terminal command: `k6 run loadtest.js`
Configuration used for load testing using k6: 
```
vus: 100,
stages: [
    { duration: '15s', target: 100 }, // ramp up
    { duration: '15s', target: 100 }, // stable
    { duration: '45s', target: 1000 }, // spike - stress test
    { duration: '1m', target: 0 }, // ramp down
  ]
```
k6 testing for async vs sync 
```
Results for async code: 
scenarios: (100.00%) 1 scenario, 1000 max VUs, 2m45s max duration (incl. graceful stop):
      * default: Up to 1000 looping VUs for 2m15s over 4 stages (gracefulRampDown: 30s, gracefulStop: 30s)
✗ api status in load test is 200
↳  96% — ✓ 30984 / ✗ 989
checks.........................: 96.90% ✓ 30984      ✗ 989   
data_received..................: 6.7 MB 50 kB/s
data_sent......................: 2.7 MB 20 kB/s
http_req_blocked...............: avg=65.84ms min=0s     med=1µs      max=19.51s p(90)=2µs   p(95)=4µs  
http_req_connecting............: avg=65.83ms min=0s     med=0s       max=19.51s p(90)=0s    p(95)=0s   
http_req_duration..............: avg=1.26s   min=0s     med=823.22ms max=40.57s p(90)=1.78s p(95)=1.97s
{ expected_response:true }...: avg=1.3s    min=6.13ms med=845.72ms max=40.57s p(90)=1.78s p(95)=1.97s
http_req_failed................: 3.09%  ✓ 989        ✗ 30984 
http_req_receiving.............: avg=24.95µs min=0s     med=12µs     max=9.57ms p(90)=37µs  p(95)=58µs 
http_req_sending...............: avg=7.61µs  min=0s     med=4µs      max=3.41ms p(90)=10µs  p(95)=16µs 
http_req_tls_handshaking.......: avg=0s      min=0s     med=0s       max=0s     p(90)=0s    p(95)=0s   
http_req_waiting...............: avg=1.26s   min=0s     med=823.22ms max=40.57s p(90)=1.78s p(95)=1.97s
http_reqs......................: 31973  236.824871/s
iteration_duration.............: avg=2.05s   min=1.68ms med=867.31ms max=54.89s p(90)=1.88s p(95)=2.23s
iterations.....................: 31973  236.824871/s
vus............................: 1      min=1        max=999 
vus_max........................: 1000   min=1000     max=1000
running (2m15.0s), 0000/1000 VUs, 31973 complete and 46 interrupted iterations

Results for sync code: 
scenarios: (100.00%) 1 scenario, 1000 max VUs, 2m45s max duration (incl. graceful stop):
      * default: Up to 1000 looping VUs for 2m15s over 4 stages (gracefulRampDown: 30s, gracefulStop: 30s)
✗ api status in load test is 200
↳  99% — ✓ 17680 / ✗ 29
checks.........................: 99.83% ✓ 17680      ✗ 29    
data_received..................: 3.7 MB 26 kB/s
data_sent......................: 1.5 MB 11 kB/s
http_req_blocked...............: avg=184.17µs min=0s       med=1µs   max=96.35ms p(90)=3µs   p(95)=171µs
http_req_connecting............: avg=179.28µs min=0s       med=0s    max=96.26ms p(90)=0s    p(95)=127µs
http_req_duration..............: avg=3.62s    min=212.27ms med=3.6s  max=33.22s  p(90)=6.35s p(95)=6.7s 
{ expected_response:true }...: avg=3.58s    min=212.27ms med=3.59s max=32.51s  p(90)=6.34s p(95)=6.69s
http_req_failed................: 0.16%  ✓ 29         ✗ 17680 
http_req_receiving.............: avg=35.98µs  min=7µs      med=30µs  max=6.08ms  p(90)=52µs  p(95)=64µs 
http_req_sending...............: avg=11.77µs  min=2µs      med=9µs   max=3.23ms  p(90)=17µs  p(95)=26µs 
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s    max=0s      p(90)=0s    p(95)=0s   
http_req_waiting...............: avg=3.62s    min=212.11ms med=3.6s  max=33.22s  p(90)=6.35s p(95)=6.7s 
http_reqs......................: 17709  125.664217/s
iteration_duration.............: avg=3.62s    min=218.01ms med=3.6s  max=33.22s  p(90)=6.35s p(95)=6.7s 
iterations.....................: 17709  125.664217/s
vus............................: 2      min=2        max=1000
vus_max........................: 1000   min=1000     max=1000
running (2m20.9s), 0000/1000 VUs, 17709 complete and 0 interrupted iterations
```
Observation for async vs sync: 
http_req_duration: avg=1.26s vs avg=3.62s. Note that, 1s response time in itself is also quite huge number, but since we bombarded it with requests, the overall avg is effected; Else it would generally be less than 300ms. 

Note: After doing stress test on this, my server went down and not responding ~ http://127.0.0.1:8000/ took too long to respond. Tried restarting app running on port 8000, then postgres/redis containers, still things did not work, so in the end had to kill the processes using `kill -9 <pid>` and then restarted the services using uvicorn. 

Then did the stress testing using ab. Read docs/ videos. 
Simple command eg. that can be used in terminal (no prior setup was needed in my mac, probably it came pre-installed): `ab -k -c 10 -n 50 http://127.0.0.1:8000/asyncrpstatus`. Command means: We will be hitting the endpoint with 10 simultaneous connections until 50 requests are met. It will be done using the keep alive header `-k` used. 
Note: When I increased the connections to a lot say `-c 10000`, got error, since the mac local setup did not allow.
```
Benchmarking 127.0.0.1 (be patient)
socket: Too many open files (24)
```
ab testing for async vs sync
```
async results: 
Command: ab -k -c 350 -n 30000 http://127.0.0.1:8000/asyncrpstatus
Server Software:        uvicorn
Server Hostname:        127.0.0.1
Server Port:            8000
Document Path:          /hasync
Document Length:        91 bytes
Concurrency Level:      100
Time taken for tests:   293.477 seconds
Complete requests:      30000
Failed requests:        0
Keep-Alive requests:    0
Total transferred:      6480000 bytes
HTML transferred:       2730000 bytes
Requests per second:    102.22 [#/sec] (mean)
Time per request:       978.258 [ms] (mean)
Time per request:       9.783 [ms] (mean, across all concurrent requests)
Transfer rate:          21.56 [Kbytes/sec] received
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.4      0      26
Processing:    31  976 192.8    992    1426
Waiting:       28  967 191.7    982    1416
Total:         35  976 192.8    992    1427
Percentage of the requests served within a certain time (ms)
  50%    992
  66%   1082
  75%   1124
  80%   1146
  90%   1211
  95%   1259
  98%   1302
  99%   1327
 100%   1427 (longest request)

sync results:
Command: ab -k -c 750 -n 30000 http://127.0.0.1:8000/syncrpstatus
Server Software:        uvicorn
Server Hostname:        127.0.0.1
Server Port:            8000
Document Path:          /hsync
Document Length:        85 bytes
Concurrency Level:      100
Time taken for tests:   181.606 seconds
Complete requests:      30000
Failed requests:        0
Keep-Alive requests:    0
Total transferred:      6300000 bytes
HTML transferred:       2550000 bytes
Requests per second:    165.19 [#/sec] (mean)
Time per request:       605.353 [ms] (mean)
Time per request:       6.054 [ms] (mean, across all concurrent requests)
Transfer rate:          33.88 [Kbytes/sec] received
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    2  46.9      0    1908
Processing:    51  602 149.3    591    2485
Waiting:       47  602 149.3    591    2485
Total:         52  605 156.6    592    2788
Percentage of the requests served within a certain time (ms)
  50%    592
  66%    650
  75%    688
  80%    711
  90%    767
  95%    824
  98%    922
  99%   1038
 100%   2788 (longest request)
```

Observation for async vs sync: 
Mean Time per request: 978.258ms vs 605.353. Surprisingly, it showed sync was faster. Again, its probably because the way time per response is spread and not very accurate. 
p50 to p100 gap: (992 to 1427) vs (592 to 2788) - we observe this is kind of aligned - sync requests did take more time as gap is noticeable. 

Other tools that can be used for testing: jmeter, locust, etc. 

**Task5**: Insert 1M+ records in postgres table and create an endpoint querying some record from the table?
First, I cleaned up the table and refreshed it then inserted records; Steps: 
```
Logged into my fapidb db: postgresdockerlocal=# \c fapidb postgresdluser
fapidb=> truncate tpsqltable;
fapidb=> alter table tpsqltable add address varchar(300);
fapidb=> CREATE TABLE tpsqltable(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, TYPE TEXT NOT NULL, PHONE INT NOT NULL);
fapidb=> ALTER TABLE tpsqltable ADD COLUMN created_at TIMESTAMP;
fapidb=> \d+ tpsqltable
                                                    Table "public.tpsqltable"
   Column   |            Type             | Collation | Nullable | Default | Storage  | Compression | Stats target | Description 
------------+-----------------------------+-----------+----------+---------+----------+-------------+--------------+-------------
 id         | integer                     |           | not null |         | plain    |             |              | 
 name       | text                        |           | not null |         | extended |             |              | 
 type       | text                        |           | not null |         | extended |             |              | 
 phone      | integer                     |           | not null |         | plain    |             |              | 
 address    | character varying(300)      |           |          |         | extended |             |              | 
 created_at | timestamp without time zone |           |          |         | plain    |             |              | 
Indexes:
    "tpsqltable_pkey" PRIMARY KEY, btree (id)
Access method: heap
fapidb=> alter table tpsqltable alter column phone type bigint;
Now, time to insert 1M records; Script to run in db container terminal: 
Query: 
INSERT INTO tpsqltable (id, name, type, phone, address, created_at)
SELECT s AS id, 'name_' || s AS name,
CASE WHEN s % 3 = 0 THEN 'type1'
     WHEN s % 3 = 1 THEN 'type2'
     ELSE 'type3'
END AS type,
(CASE WHEN random() < 0.5 THEN 8000000000 ELSE 9000000000 END + s % 1000000) AS phone,
'address data ' || s AS address,
'2000-01-01'::timestamp + (s % 3650 || ' days')::interval AS created_at
FROM generate_series(1, 5000000) AS s;

Now, shuffling all the records:
-- Step 1: Create a new table with shuffled rows: CREATE TABLE shuffled_table AS SELECT * FROM tpsqltable ORDER BY random();
-- Step 2: Drop the original table: DROP TABLE tpsqltable;
-- Step 3: Rename the shuffled table to the original table name: ALTER TABLE shuffled_table RENAME TO tpsqltable;

To understand query details we can use 'explain' keyword in pgsql. 
Eg: 
------------------------------------------------------------------------------
fapidb=> explain select * from tpsqltable where phone=9000516507;
 Gather  (cost=1000.00..83875.96 rows=3 width=66)
   Workers Planned: 2
   ->  Parallel Seq Scan on tpsqltable  (cost=0.00..82875.66 rows=1 width=66)
         Filter: (phone = '9000516507'::bigint)
(4 rows)
------------------------------------------------------------------------------
fapidb=> explain select * from tpsqltable;
 Seq Scan on tpsqltable  (cost=0.00..106835.82 rows=5000382 width=66)
(1 row)
------------------------------------------------------------------------------
fapidb=> explain select * from tpsqltable order by created_at;
 Gather Merge  (cost=468247.39..954429.47 rows=4166984 width=66)
   Workers Planned: 2
   ->  Sort  (cost=467247.37..472456.10 rows=2083492 width=66)
         Sort Key: created_at
         ->  Parallel Seq Scan on tpsqltable  (cost=0.00..77666.93 rows=2083492 width=66)
(5 rows)
------------------------------------------------------------------------------
```
Then added API endpoint to do the same defined as `Task5` in the app.py file.

**Task6**: Dockerize/Containerize the businessMicroservice?
I have created a dockerfile for the repo, and now building the current service using: `podman build --no-cache -t bmserviceimage .` (Note that `.` indicates current dir; Else syntax would be (docker/podman): `docker build -t <image> <path>`). 
Once image was build, I ran the image, i.e spawn up the container with a name using: `podman run -p 4500:8900 --name bmservicecontainer bmserviceimage`. In short, it is port mapping to our fastapi server running inside the container. Then we can hit APIs via Postman/Browser and see response. Our postgres and redis cotainers are anyways running from previous commands.
I have added explicit details inside the Dockerfile. Also, note, if there is a code change made, then image must be rebuilt. 
To run the container in some other port parallely using same image, simply: `podman run -p 4600:8900 --name bmservicecontainer bmserviceimage` 

**Task7**: Since businessMicroservice is dockerized try connecting to the other Redis/Postgres containers - for now we can say it is loosely coupled? 
The only thing changed is the host machine in the redis/postgres configs. 
Now what changed?: 
When I did not dockerize my fastapi app and ran it on localhost (means it basically ran on my macbook/host machine) and hit postgres or redis container for health check - I got a response. Understand that postgres and redis containers were also running on host machine only. Hence all shared the same network namespace. This means that localhost referred to the same machine for both the FastAPI application and PostgreSQL/Redis.
So credentials like: POSTGRES_HOST/REDIS_HOST = "localhost". 
When I dockerized my fastapi app and ran it in a docker container the networking context changed. Key points:
Isolation: Each Docker container has its own network stack. localhost within a Docker container refers to the container itself, not the host machine.
Networking: By default, Docker containers are attached to a default network (bridge network) which isolates them from the host network and from each other unless configured otherwise.
By default, Docker containers are connected to a bridge network. To allow your FastAPI container to communicate with PostgreSQL/Redis running on the host machine, you should use the host machine's IP address. So its like host machine is a common ground/platform for multiple containers running inside it, so any request should be routed via the machine so that it can exactly know which container is interacting with which one - in a rough explanation. 
You can find host machine (in my case macbook) ip using `ping -c 1 $(hostname)` or `ifconfig` command; If it were an AWS EC2 machine, we would anyways know the IP of the machine...; Then update your FastAPI configuration to use this IP address (host machine) instead of localhost i.e update POSTGRES_HOST url, which I did in code in postgresDbConfig.py. 
We can ask how is docker able to route the connection from container to host machine via bridge network concept?: 
Bridge Network Creation: By default, Docker containers are connected to a bridge network. This is an internal virtual network that allows containers to communicate with each other and the host machine.
Container-to-Host Communication: When you specify the host machine's IP address in the container, the container's networking stack knows to route the traffic out of the container to the host machine's network interface.
Network Address Translation (NAT): Docker uses Network Address Translation to map container ports to host ports. When a container tries to access an IP address and port, Docker's networking translates these into appropriate network requests.
To access a service running on the host machine from a Docker container, you specify the host machine's IP address. For example, if your host machine's IP address is 192.168.1.100, you can configure your application to connect to this IP.

**Task8**: Use docker compose and integrate all 3 services (fastapi app, postgres, redis) and tighten up the coupling? 
A Docker Compose file, typically named docker-compose.yml, is used to define and manage multi-container Docker applications. It allows you to define services, networks, and volumes in a single YAML file, providing a streamlined way to manage your Docker environment. (More details added in docker-compose.yaml file in the project)
Can check the docker-compose.yaml file for reference. Do ensure docker/podman compose utilities are installed as they need to be installed seaprately and do not come packed with usual docker/podman. 
To build the compose file: `docker-compose build` (or `podman-compose build`). Note you can remove `-` and run command as well like: `podman compose build`. 
To run it: `docker-compose up` (or `podman-compose up`); To run in detached mode add `-d` flag. 
Then you can access the service on from browser/postman. You may also use: `docker-compose up --build` (or podman)
To stop and remove containers created by docker-compose up, use Ctrl+C in the terminal where it's running or use: `docker-compose down`. If you add `-v` flag in docker-compose down it will remove the volumes as well apart from stopping containers. 
Note that in docker file I have made the CMD command to run both app.py fastapi server as well as main.py fastapi server. Though we won't be able to get the status in the usual way from app.py to main.py; Same is objective in next task.  

**Task9**: Ensure you are able to get status of main.py server in sampleService from app.py service from the docker-compose file?
If we see the current way in which we get status of main app server is: 
```
@app.get("/mainappstatus")
def get_other_server_status():
    url = 'http://127.0.0.1:8001/currentStatus' # Note that endpoint is camelCase, same is expected when typing in url/testing via postman
    response = requests.get(url)
    print(f"Status of main app server: {response.status_code}")
    data = json.loads(response.text)
    return data
```
But now, since we are considering spinning up the multiple fastapi servers inside the container - to be able to access them from our host machine (i.e macbook) - we need to be able to map a host machine port to that service port, and then anyways we are aware of the concept of docker bridge network, etc., it will be able to get the status. 
Changes to do the same have been made in the docker compose file. 
To explain in other way: 
In Docker Compose, the ports directive is used to map ports from the host machine to the container. This allows services running inside the container to be accessible from the host machine.
Mapping ports is essential because containers are isolated environments, and by default, the services running inside them are not accessible from the outside world. By mapping a container's port to a port on the host machine, you make the service inside the container accessible from outside the container, using the host's IP address and the mapped port.
If we observe current docker-compose file:
"4500:8900": This maps port 8900 inside the container to port 4500 on the host machine. It means that if you access http://localhost:4500 from browser/postman on your host machine, it will be directed to the service running on port 8900 inside the container.
Then - Change that we made: "4501:8901": This maps port 8901 inside the container to port 4501 on the host machine. It means that if you access http://localhost:4501 from browser/postman on your host machine, it will be directed to the service running on port 8901 inside the container.
If you have two FastAPI applications running on different ports (8900 and 8901) inside the same container, you need to map both ports to the host machine to access them:
Primary FastAPI Application: Internal port: 8900, Mapped host port: 4500, Access via: http://localhost:4500
For this: Secondary FastAPI Application: Internal port: 8901, Mapped host port: 4501, Access via: http://localhost:4501
This is the case when we are acessing them from our browser/postman. 
But now, if I want to check the health of main.py server from app.py server - remember both of them are running in the same container environment - so the request in code will be from one port to another inside the container itself not on host machine. 
This is an inter-service communication - for this we leverage docker (or podman) compose’s internal DNS resolution, allowing one service to communicate with another by using its service name.
Hence the url we hit to changed to: `url = 'http://businessmicroservice:8901/currentmainstatusdockercompose'`
To reiterate simply, to access main.py app server - there are 2 ways: 
One, we type-in the url from our browser/postman (which is host machine) and access the main.py server running inside container - which we did by port mapping 4501:8901. 
Two, we type-in url to access app.py server running inside container since it is already exposed. And then we define an endpoint inside app.py server which internally communicates with main.py server - which is what we did in this particular url case: `url = 'http://businessmicroservice:8901/currentmainstatusdockercompose'`. With `businessmicroservice:8901`, we ensured our app.py server is able to access main.py server inside container. Else, we get `ERROR: requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=8901): Max retries exceeded with url`

**Task10**: Build a simple consumerMicroservice app pinging root server of businessMicroservice? 
Wrote Dockerfile of the consumerMicroservice and fastapi code to ping to businessMicroservice app. 
Since consumerMicroservice is a separate service altogether I am spinning it up manually from Docker. 
Docker compose is not needed as its just 1 service. From docker compose anyways I have spinned up businessMicroservice app/ postgres/ redis.
Command used (docker/podman): 
`podman build --no-cache -t cmserviceimage .`
Once image was build, to run container (BUT DO CHECK BELOW NOTES): `podman run -p 3500:6800 --name cmservicecontainer cmserviceimage` - Connecting host's 3500 port with 6800 port of container (Note check Dockerfile - I am exposing port 6800 of container where the consumer service fastapi server is running using uvicorn)
In app.py code of both consumer & business microservice, see the url is connecting to the fast api server running in another container; Though understand that both containers are running in same host machine (my macbook). 
Recall that: A network is a group of two or more devices that can communicate with each other either physically or virtually. The Docker network is a virtual network created by Docker to enable communication between Docker containers. If two containers are running on the same host they can communicate with each other without the need for ports to be exposed to the host machine.
In our case, we put our docker compose containers from businessMicroservice in a network named: `bmservice_compose_network`
We use this and connect our consumerMicroservice which is an external container. 
In businessMicroservice: Defined `/bmserviceserverstatus` to return response when we hit a service running in another container; url we are hitting: `http://businessmicroservice:8901/bmserviceserverstatus` - Recall we are running the app server using docker compose at port 8901 in businessMicroservice, for run via normal docker (without compose) or from host we use different  ports as seen in earlier tasks, but for testing current task we have activated this port by keeping the service up using docker compose and it is running in network: `bmservice_compose_network`. 
In consumerMicroservce: From host machine I hit `/bmservicestatus` endpoint to get `/bmserviceserverstatus` defined in businessMicroservice
ALERT NOTE: Upon running earlier command: `podman run -p 3500:6800 --name cmservicecontainer cmserviceimage` and hitting `http://0.0.0.0:3500/bmservicestatus` on browser/postman did not yield me any response from other container. Why?: It was because the containers running via compose are on a different network. Hence I need to connect the container to that network; It can be done by running (docker/podman): 
`podman run --network bmservice_compose_network -p 3500:6800 --name cmservicecontainer cmserviceimage` - network added. (Note rebuild image and then run, also ensure the directory you are building your dockerfile and all - don't mess up here)
Note that - we can also imagine coupling the consumerMicroservice inside the same docker-compose file as well specifying the path (build context as something like `./consumerMicroservice` than giving `.`) and have all services - businessMicroservice, postgres, redis, etc running up altogether. But we are restricting now as a fundamental understanding has been developed by this far and we can try avoiding cluttering things more... 

**Task11**: Publish the docker-compose file having businessMicroservice, postgres, redis to dockerhub and check if another developer can pull the image and run it on their machine?


**Task12**: Run the businessMicroservice container in 2 different ports (basically 2 instances of the service). And your consumerMicroservice app should be pinging root server of businessMicroservice app in round-robin fashion of each service; In case it dies in 1 port, then redirect all request to other port - This pretty much explains how a simple load balancer would work? 
Should I define multiple services in docker compose file and then individually ping them for this or is there another way? 

**Task13**: Setup a NoSQL db like mongodb via docker and health check mongodb service?  

**Task14**: Build CRUD operations in databases (postgres, redis, mongodb) logic in businessMicroserviceApp and expose the endpoints to consumerMicroserviceApp. Hence use consumerMicroserviceApp to alter the data using businessMicroserviceApp as intermediary. 

**Task15**: Setup Kafka locally or via docker. Create JSON events from the service and publish it to Kafka service?  


--------------------------------------


Now focus on developing `consumerMicroservice` once venv activated:







------------------------------------

References/ Other notes: (refactor this part later...)

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
https://stackoverflow.com/questions/12732182/ab-load-testing
https://gist.github.com/vinayaksuresh/c1b6eeb09f71cb6df980d4fc9e425989
https://www.youtube.com/watch?v=gvounvDSDGg
https://www.youtube.com/watch?v=ghuo8m7AXEM&t=217s
https://stackoverflow.com/questions/59169855/inserting-1-million-random-data-into-postgresql
order by random() works but ~ https://dba.stackexchange.com/questions/261549/order-by-random-meaning-postgresql
https://www.youtube.com/watch?v=P7EUFtjeAmI

postgres
(also docs: https://www.postgresql.org/docs/8.0/sql-createuser.html)
(for all commands above, followed steps in this doc: https://www.commandprompt.com/education/how-to-create-a-postgresql-database-in-docker/, also followed the youtube video: https://www.youtube.com/watch?v=2X8B_X2c27Q)

tasks todo: 
mongodb integrate

error faced with sqlalchemy
https://www.youtube.com/watch?v=epaopuvvOGs
https://stackoverflow.com/questions/75282511/df-to-table-throw-error-typeerror-init-got-multiple-values-for-argument

https://www.youtube.com/watch?v=fSmLiOMp2qI
https://www.youtube.com/watch?v=KuCwrySinqI

docker builds on top of another layer by layer as it helps in caching
docker build time - check the steps which need not be reexeucted even for a small change.. and docker image size - check the os base layr you are installing
we want local databSes to retain infromation across restarts - hence docker volumes
say you create a mongo db container and now you want to persist data s well,
ensure you have volume created for it: 
docker volume create dbvol
docker run -v dbvol:/data/db -p 27017:27017 mongo
inside the container it will create volume at the /data/db path
as we know we can go inside mongo/postgres/redis container using docker exec -it <>
if container restarts or kills. etc... vol has saved data... once conteinaer spins up it can reconnect to volume

volume a logical space inside container where you can dump data into volume, if container goes down, sicne volumne persists data still tehre
docker volume create --name hello
docker run -d -v hello:/container/path/for/volume container_image my_command

explore later - but interesting thing - running something in background using fastapi: https://fastapi.tiangolo.com/tutorial/background-tasks/



------------------------------------

