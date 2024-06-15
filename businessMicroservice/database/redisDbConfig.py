import redis

"""
Defining the redis database configs. 
"""
REDIS_HOST = "localhost"
REDIS_PORT = 7001
REDIS_USER = None
REDIS_PASSWORD = None
REDIS_DB = None
rd = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
