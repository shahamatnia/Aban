from django.conf import settings

import redis


class RedisCli:
    primary_redis_client = redis.Redis(host=settings.REDIS_HOST, port=6379, db=0, decode_responses=True)

    pending_cost_prefix = 'PCP'
