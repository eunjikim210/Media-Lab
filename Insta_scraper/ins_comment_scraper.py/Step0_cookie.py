import redis

Cookirstr = """
Add cookies

"""

Cookirstrs = ["".join([i for i in i.strip().split("|") if "csrftoken" in i]) for i in Cookirstr.split("\n") if i.strip() != '']
print(Cookirstrs)
redis_map = redis.Redis(db=10)

for cookie in Cookirstrs:
    redis_map.lpush("ins", cookie)


