import sys
import os
import grpc
import logging
from concurrent import futures
from openai import OpenAI

# === DeepSeek AI Configuration ===
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-f471a7063e004a8ea4f6260a86d0dde3")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/"

# Initialize OpenAI client
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)

# === Configure Logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# === Import gRPC stubs ===
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
suggestions_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, suggestions_grpc_path)

import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

# === Static Book Recommendations ===
BOOK_RECOMMENDATIONS = {
    "123": [
        {"book_id": "456", "title": "Advanced Python", "author": "Jane Doe"},
        {"book_id": "789", "title": "Data Science Essentials", "author": "Alice Smith"}
    ],
    "456": [
        {"book_id": "101", "title": "Machine Learning Basics", "author": "Bob Johnson"},
        {"book_id": "202", "title": "Deep Learning for Coders", "author": "Charlie Lee"}
    ]
}

class SuggestionsService(suggestions_grpc.SuggestionsServicer):
    def RecommendBooks(self, request, context):
        """
        - First, attempt to use DeepSeek AI for recommendations
        - If AI fails, fall back to static recommendation logic
        """
        user_id = request.user_id
        order_id = request.order_id
        purchased_books = request.purchased_books

        logger.info("\n" + "=" * 50)
        # ✅ 确保收到的数据正确
        logger.info(f"[Suggestions Service] Received books: {purchased_books}")
        logger.info(f"[Suggestions Service] Processing recommendations for Order ID: {order_id}, User ID: {user_id}")

        # Retrieve user's purchase history
        user_history = [{"book_id": book.book_id, "title": book.title, "author": book.author} for book in purchased_books]

        # 1️⃣ Attempt AI-based recommendations
        ai_recommendations = self.get_deepseek_recommendation(user_history)
        if ai_recommendations:
            logger.info(f"[Suggestions Service] ✅ AI recommendation successful, returning {len(ai_recommendations)} books")
            self.log_recommendations(ai_recommendations)  # Log the recommendations
            return self._build_response(ai_recommendations)

        # 2️⃣ AI fails, fall back to static recommendations
        logger.warning("[Suggestions Service] ⚠️ AI recommendation failed, using static recommendation list")
        static_recommendations = self.get_static_recommendations(purchased_books)

        logger.info(f"[Suggestions Service] ✅ Static recommendations returned {len(static_recommendations)} books")
        self.log_recommendations(static_recommendations)  # Log the recommendations
        return self._build_response(static_recommendations)

    def get_static_recommendations(self, purchased_books):
        """Return static recommendations based on purchased books"""
        recommended_books = []
        seen = set()

        for book in purchased_books:
            if book.book_id in BOOK_RECOMMENDATIONS:
                for rec in BOOK_RECOMMENDATIONS[book.book_id]:
                    if rec["book_id"] not in seen:
                        seen.add(rec["book_id"])
                        recommended_books.append(rec)

        return recommended_books

    def get_deepseek_recommendation(self, user_history):
        """
        Call DeepSeek AI for personalized recommendations
        """
        if not DEEPSEEK_API_KEY:
            logger.error("[Suggestions Service] ❌ DeepSeek API Key is not configured")
            return []

        # Generate Prompt
        user_books = "\n".join([f"- {book['title']} by {book['author']}" for book in user_history])
        prompt = f"""
        I am an intelligent book recommendation system. The user has purchased the following books:
        {user_books}

        Please recommend 3-5 books based on the user's reading interests, including the title and author. For example:
        - Title: Machine Learning in Action, Author: Peter Harrington
        - Title: Deep Learning, Author: Ian Goodfellow
        Your recommendations:
        """

        try:
            logger.info("[Suggestions Service] Calling DeepSeek AI for intelligent recommendations...")

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are an intelligent book recommendation assistant"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                stream=False
            )

            recommendations = response.choices[0].message.content.strip().split("\n")
            book_recommendations = []

            for rec in recommendations:
                if "Title:" in rec and "Author:" in rec:
                    try:
                        title = rec.split("Title:")[1].split(",")[0].strip()
                        author = rec.split("Author:")[1].strip()
                        book_recommendations.append({"book_id": "N/A", "title": title, "author": author})
                    except Exception as e:
                        logger.warning(f"[Suggestions Service] Failed to parse recommended book: {rec}, Error: {e}")

            return book_recommendations

        except Exception as e:
            logger.error(f"[Suggestions Service] ❌ DeepSeek API call failed: {e}")
            return []

    def log_recommendations(self, books):
        """Log recommended books"""
        logger.info("[Suggestions Service] Recommended books:")
        for book in books:
            logger.info(f"📖 Title: {book['title']}, Author: {book['author']}")

    def _build_response(self, books):
        """Build gRPC response"""
        return suggestions.RecommendationResponse(
            suggested_books=[
                suggestions.Book(
                    book_id=book["book_id"],
                    title=book["title"],
                    author=book["author"]
                ) for book in books
            ]
        )

def serve():
    """
    Start gRPC server, listening on port 50053
    """
    port = os.getenv("GRPC_PORT", "50053")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    suggestions_grpc.add_SuggestionsServicer_to_server(SuggestionsService(), server)

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"[Suggestions Service] 🚀 Running on port {port}...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
