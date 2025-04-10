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
<<<<<<< HEAD
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
=======
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
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

<<<<<<< HEAD
class SuggestionsService(suggestions_grpc.SuggestionsServicer):
    def RecommendBooks(self, request, context):
        """
        - First, attempt to use DeepSeek AI for recommendations
        - If AI fails, fall back to static recommendation logic
=======
# Store order data and vector clocks
order_cache = {}


class SuggestionsService(suggestions_grpc.SuggestionsServicer):
    def RecommendBooks(self, request, context):
        """
        - First, attempt to use DeepSeek AI for recommendations.
        - If AI fails, fall back to static recommendation logic.
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        """
        user_id = request.user_id
        order_id = request.order_id
        purchased_books = request.purchased_books
<<<<<<< HEAD

        logger.info("\n" + "=" * 50)
        # ✅ 确保收到的数据正确
        logger.info(f"[Suggestions Service] Received books: {purchased_books}")
        logger.info(f"[Suggestions Service] Processing recommendations for Order ID: {order_id}, User ID: {user_id}")
=======
        vector_clock = list(request.vector_clock)

        logger.info(f"[Suggestions Service] --- Start: Processing Order {order_id} ---")
        logger.debug(f"[Suggestions Service] gRPC Request: {request}")

        # Store order data in cache
        order_cache[order_id] = {
            "user_id": user_id,
            "vector_clock": vector_clock,
        }
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)

        # Retrieve user's purchase history
        user_history = [{"book_id": book.book_id, "title": book.title, "author": book.author} for book in purchased_books]

        # 1️⃣ Attempt AI-based recommendations
        ai_recommendations = self.get_deepseek_recommendation(user_history)
        if ai_recommendations:
            logger.info(f"[Suggestions Service] ✅ AI recommendation successful, returning {len(ai_recommendations)} books")
<<<<<<< HEAD
            self.log_recommendations(ai_recommendations)  # Log the recommendations
            return self._build_response(ai_recommendations)
=======
            self.log_recommendations(ai_recommendations)
            vector_clock[2] += 1
            logger.info(f"[Suggestions Service] Updated Vector Clock: {vector_clock}")
            logger.info(f"[Suggestions Service] --- End: Processing Order {order_id} ---")
            return self._build_response(ai_recommendations, vector_clock)
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)

        # 2️⃣ AI fails, fall back to static recommendations
        logger.warning("[Suggestions Service] ⚠️ AI recommendation failed, using static recommendation list")
        static_recommendations = self.get_static_recommendations(purchased_books)

        logger.info(f"[Suggestions Service] ✅ Static recommendations returned {len(static_recommendations)} books")
<<<<<<< HEAD
        self.log_recommendations(static_recommendations)  # Log the recommendations
        return self._build_response(static_recommendations)

    def get_static_recommendations(self, purchased_books):
        """Return static recommendations based on purchased books"""
=======
        self.log_recommendations(static_recommendations)
        vector_clock[2] += 1
        logger.info(f"[Suggestions Service] Updated Vector Clock: {vector_clock}")
        logger.info(f"[Suggestions Service] --- End: Processing Order {order_id} ---")
        return self._build_response(static_recommendations, vector_clock)

    def get_static_recommendations(self, purchased_books):
        """Return static recommendations based on purchased books."""
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
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
<<<<<<< HEAD
        Call DeepSeek AI for personalized recommendations
=======
        Call DeepSeek AI for personalized recommendations.
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        """
        if not DEEPSEEK_API_KEY:
            logger.error("[Suggestions Service] ❌ DeepSeek API Key is not configured")
            return []

<<<<<<< HEAD
        # Generate Prompt
=======
        # Generate prompt
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
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
<<<<<<< HEAD
                        logger.warning(f"[Suggestions Service] Failed to parse recommended book: {rec}, Error: {e}")
=======
                        logger.warning(f"[Suggestions Service] ⚠️ Failed to parse recommended book: {rec}, Error: {e}")
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)

            return book_recommendations

        except Exception as e:
            logger.error(f"[Suggestions Service] ❌ DeepSeek API call failed: {e}")
            return []

    def log_recommendations(self, books):
<<<<<<< HEAD
        """Log recommended books"""
        logger.info("[Suggestions Service] Recommended books:")
        for book in books:
            logger.info(f"📖 Title: {book['title']}, Author: {book['author']}")

    def _build_response(self, books):
        """Build gRPC response"""
=======
        """Log recommended books."""
        logger.info("[Suggestions Service] 📖 Recommended books:")
        for book in books:
            logger.info(f"📘 Title: {book['title']}, Author: {book['author']}")

    def _build_response(self, books, vector_clock):
        """Build gRPC response."""
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
        return suggestions.RecommendationResponse(
            suggested_books=[
                suggestions.Book(
                    book_id=book["book_id"],
                    title=book["title"],
                    author=book["author"]
                ) for book in books
<<<<<<< HEAD
            ]
        )

def serve():
    """
    Start gRPC server, listening on port 50053
=======
            ],
            vector_clock=vector_clock
        )

    def ClearOrderData(self, request, context):
        """
        Clears stored order data only if local vector clock <= final vector clock.
        """
        order_id = request.order_id
        vc_final = list(request.vector_clock)

        def is_vc_less_equal(vc1, vc2):
            return all(x <= y for x, y in zip(vc1, vc2))

        if order_id in order_cache:
            vc_local = order_cache[order_id]["vector_clock"]
            if is_vc_less_equal(vc_local, vc_final):
                del order_cache[order_id]
                logger.info(f"[Suggestions Service] 🗑️ Cleared order data for Order ID: {order_id}")
                return suggestions.ClearOrderResponse(success=True)
            else:
                logger.warning(f"[Suggestions Service] ⚠️ Rejecting cleanup for Order ID: {order_id} - Local VC {vc_local} is newer than Final VC {vc_final}")
                return suggestions.ClearOrderResponse(success=False)

        return suggestions.ClearOrderResponse(success=False)



def serve():
    """
    Starts gRPC server, listening on port 50053.
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
    """
    port = os.getenv("GRPC_PORT", "50053")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    suggestions_grpc.add_SuggestionsServicer_to_server(SuggestionsService(), server)

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"[Suggestions Service] 🚀 Running on port {port}...")
    server.wait_for_termination()

<<<<<<< HEAD
=======

>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
if __name__ == "__main__":
    serve()
