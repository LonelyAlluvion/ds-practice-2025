import os
import logging
from openai import OpenAI


# 读取 API Key 和 API 地址
DEEPSEEK_API_KEY = "sk-f471a7063e004a8ea4f6260a86d0dde3"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/"  # DeepSeek API 地址

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_API_URL
)

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_deepseek_recommendation(user_history):
    """
    调用 DeepSeek API 生成个性化书籍推荐。

    参数：
    - user_history: List[Dict]，用户购买历史，每个元素包含 book_id, title, author。

    返回：
    - List[Dict]，推荐的书籍列表
    """
    # 生成 Prompt
    user_books = "\n".join([f"- {book['title']} by {book['author']}" for book in user_history])
    prompt = f"""
    我是一个智能书籍推荐系统。用户购买了以下书籍：
    {user_books}

    请根据用户的阅读兴趣推荐 3-5 本书，包括书名和作者。例如：
    - 书名: 机器学习实战, 作者: Peter Harrington
    - 书名: 深度学习, 作者: Ian Goodfellow
    你的推荐：
    """

    try:
        logger.info("调用 DeepSeek 进行智能书籍推荐...")

        response = client.chat.completions.create(
            model="deepseek-chat",  # 选择 DeepSeek 模型
            messages=[
                {"role": "system", "content": "你是一个智能书籍推荐助手"},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0,  # 控制推荐的多样性，值越大越随机
            stream=False
        )

        recommendations = response.choices[0].message.content.strip().split("\n")
        book_recommendations = []

        for rec in recommendations:
            if "书名:" in rec and "作者:" in rec:
                try:
                    title = rec.split("书名:")[1].split(",")[0].strip()
                    author = rec.split("作者:")[1].strip()
                    book_recommendations.append({"book_id": "N/A", "title": title, "author": author})
                except Exception as e:
                    logger.warning(f"解析推荐书籍失败: {rec}，错误: {e}")

        logger.info(f"推荐结果: {book_recommendations}")
        return book_recommendations

    except Exception as e:
        logger.error(f"调用 DeepSeek API 失败: {e}")
        return []


# 示例调用
if __name__ == "__main__":
    user_purchase_history = [
        {"book_id": "123", "title": "Python 数据分析", "author": "Wes McKinney"},
        {"book_id": "456", "title": "人工智能导论", "author": "Stuart Russell"},
    ]

    recommendations = get_deepseek_recommendation(user_purchase_history)
    print("最终推荐书籍列表：", recommendations)


