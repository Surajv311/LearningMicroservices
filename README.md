## Project Overview

Note: Do consider skipping below overviews of project and jump to the steps followed in next section to understand the flow of project (from basics). 

- Initial intention (rough): 
  - We must have 2 microservices say: `businessMicroservice` and `consumerMicroservice`. 
  - Consider having the following db containers running as well locally: `postgresql`, `redis`, `mongodb`.
  - `businessMicroservice` should have endpoints which check the health of db containers, query over tables in the db's, and have the ability to perform basic CRUD operations. 
  - We also intend to play around with ports as well hence we will have cases where we are running the service in 2 different ports and trying to get the status of one port from another, etc; Or running containers on 2 different ports etc. 
  - Containzerize the application. 
  - `consumerMicroservice` should be designed to mimic how a user/entity would interact with APIs in `businessMicroservice`. In short, allow 2 microservices to communicate with one another. 
  - Try running `businessMicroservice` in 2 container instances in different ports. And then your `consumerMicroservice` should send request to each of the running containers of `businessMicroservice` in round-robin fashion, so kind of act like load balancer.

- Future intention (rough)
  - The complexity of project will increase with time. 
  - We will have more complex scenarios to cover, and probably add end-to-end flow, like say post interaction, publishing data to Kafka/Flink; Or having Debezium setup to capture CDC once we update postgres tables via our microservice, etc etc. 
  - Objective is to mimic how production systems work as closely as possible. In local if things work well and fine, same is done in cloud - FYI, it's just that some minor tweaks have to be made since ecosystem changes but the core concepts remain the same. We will try to cover as many cases as possible in time and learn!. 

Note: Some major errors I encountered, which was worth learning exp., I have mentioned in the end of Readme. And, as well as the blogs/references/videos I watched to create this project + little help from chatgpt. 

------------------

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
In this exercise, I have used docker in the beginning later switched to podman (Note all docker commands run same in podman, except instead of using docker keyword, use podman)

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
Note that in below command I am using port mapping 7001:6379, i.e will run the Redis container on a different port 7001 rather than default port 6379. 
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
I have created a dockerfile for the repo, and now building the current service using: `docker build --no-cache -t bmservice .` (Note that `.` indicates current dir; Else syntax would be: `docker build -t <image> <path>`). 
In our case we will use podman build: `podman build --no-cache -t bmservice .`
Once image was build, I ran the image, i.e spawn up the container with a name using: `podman run --name bmservicecontainer bmservice`
containers may not aalways be living continuosly, they may die down


**Task7**: Since businessMicroservice also requires Redis/Postgres, integrate all via docker compose?



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


------------------------------------

