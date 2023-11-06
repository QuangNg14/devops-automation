# import pytest
# from flask import json
# from app import app


# @pytest.fixture
# def client():
#     app.config["TESTING"] = True
#     with app.test_client() as client:
#         yield client


# def test_answer_question(client):
#     # Test posting an answer
#     response = client.post(
#         "/answers",
#         data=json.dumps({"user_id": "user1", "question_id": "q1", "score": "5"}),
#         content_type="application/json",
#     )
#     assert response.status_code == 200
#     assert response.get_json() == {"ok": True}

#     # Test getting an answer (you would need to create a GET route in your Flask app)
#     response = client.get("/answers?user_id=user1&question_id=q1")
#     assert response.status_code == 200
#     assert response.get_json() == {"score": "5"}


# @pytest.mark.asyncio
# async def test_create_compatibility(client):
#     # Assuming you have some way of mocking the match.compatibility function
#     # and populating the answers dictionary...

#     # Test posting a compatibility request
#     response = client.post(
#         "/users/compatibility",
#         data=json.dumps({"from_id": "user1", "to_id": "user2"}),
#         content_type="application/json",
#     )
#     assert response.status_code == 200
#     assert "compatibility" in response.get_json()

#     # Test error case with no common answers
#     response = client.post(
#         "/users/compatibility",
#         data=json.dumps({"from_id": "user1", "to_id": "user3"}),
#         content_type="application/json",
#     )
#     assert response.status_code == 400
#     assert response.get_json() == {"detail": "no responses in common"}
