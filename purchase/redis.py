import redis

primary_redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

pending_cost_prefix = 'PCP'
