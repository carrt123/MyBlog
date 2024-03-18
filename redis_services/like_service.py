import redis


class LikeService:
    def __init__(self):
        # 初始化 Redis 客户端
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def like(self, user_id, post_id):
        # 将 user_id 添加到 post_id 的点赞集合中
        self.redis_client.sadd(f"post:{post_id}:likes", user_id)

    def unlike(self, user_id, post_id):
        # 从 post_id 的点赞集合中移除 user_id
        self.redis_client.srem(f"post:{post_id}:likes", user_id)

    def get_likes(self, post_id):
        # 获取 post_id 的总点赞数
        return self.redis_client.scard(f"post:{post_id}:likes")

# 示例用法
# like_system = LikeSystem()
# like_system.like(user_id=1, post_id=123)
# like_system.like(user_id=2, post_id=123)
# like_system.like(user_id=3, post_id=123)
# like_system.unlike(user_id=2, post_id=123)
# total_likes = like_system.get_likes(post_id=123)
# print(f"帖子 123 的总点赞数：{total_likes}")
