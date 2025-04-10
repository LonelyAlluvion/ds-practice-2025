<<<<<<< HEAD
=======

>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
import time
import sys
import os
import grpc
from concurrent import futures

# === Import gRPC stubs ===
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
suggestions_grpc_path = os.path.abspath(os.path.join(FILE, '../../utils/pb/suggestions'))
sys.path.insert(0, suggestions_grpc_path)

import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc


def test_book_recommendation(order_id, user_id, purchased_books):
    with grpc.insecure_channel("localhost:50053") as channel:
        stub = suggestions_grpc.SuggestionsStub(channel)

        # 构建请求对象
        request = suggestions.RecommendationRequest(
            order_id=order_id,
            user_id=user_id,
            purchased_books=[suggestions.Book(
                book_id=book['book_id'],
                title=book['title'],
                author=book['author']
            ) for book in purchased_books]
        )

        # 发送请求并获取响应
        response = stub.RecommendBooks(request)

        # 打印返回的推荐书籍
        print(f"Recommendations for Order {order_id}, User {user_id}:")
        for book in response.suggested_books:
            print(f"Book ID: {book.book_id}, Title: {book.title}, Author: {book.author}")


<<<<<<< HEAD

test_book_recommendation(
    order_id="ORD-AdvancedPython-1",
    user_id="user890",
    purchased_books=[{"book_id": "456", "title": "Human History", "author": "Jane Doe"}]
)

=======
# ✅ 测试 1：用户购买 "The Best Book"
test_book_recommendation(
    order_id="ORD-JohnDoe-3",
    user_id="user567",
    purchased_books=[{"book_id": "123", "title": "The Best Book", "author": "John Smith"}]
)

# ✅ 测试 2：用户购买 "Advanced Python"
test_book_recommendation(
    order_id="ORD-AdvancedPython-1",
    user_id="user890",
    purchased_books=[{"book_id": "456", "title": "Advanced Python", "author": "Jane Doe"}]
)

# ❌ 测试 3：用户购买未在推荐规则中的书籍
test_book_recommendation(
    order_id="ORD-UnknownBook-1",
    user_id="user123",
    purchased_books=[{"book_id": "999", "title": "Unknown Book", "author": "Unknown Author"}]
)
>>>>>>> 34889cd (✅ Complete checkpoint-2: system integration with leader election, vector clock and backend orchestration)
