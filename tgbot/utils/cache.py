from cachetools import TTLCache

from tgbot.config import RATE_LIMIT

throttling_cache = TTLCache(maxsize=10_000, ttl=RATE_LIMIT)
