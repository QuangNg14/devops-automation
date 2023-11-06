import match
from flask import Flask, request, jsonify
from threading import Lock
from collections import defaultdict
import asyncio

app = Flask(__name__)

# Map a user_id -> a Map of question_id -> answer
answers = defaultdict(lambda: defaultdict(str))

# Store compatibility between 2 users if already computed
compatibilityMap = defaultdict(float)

# Map a user to their corresponding locks
lockPerUser = defaultdict(Lock)


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    result = data["a"] + data["b"]
    return jsonify({"result": result}), 200


@app.route("/subtract", methods=["POST"])
def subtract():
    data = request.get_json()
    result = data["a"] - data["b"]
    return jsonify({"result": result}), 200


@app.route("/answers", methods=["POST"])
def answer_question():
    # Collecting the data from the request body
    req = request.json
    user_id = req["user_id"]
    question_id = req["question_id"]
    score = req["score"]

    # Save the user_id -> question_id answer to a score
    answers[user_id][question_id] = score

    return jsonify({"ok": True}), 200


async def tryAcquireLock(lock):
    """Try to acquire a lock, returning True if successful and False if not"""
    return lock.acquire(blocking=False)


async def releaseLock(lock):
    """Releasing a lock if the lock is acquired"""
    if lock.locked():
        lock.release()


@app.route("/users/compatibility", methods=["POST"])
async def create_compatibility():
    # Collecting the data from the request body
    req = request.json
    from_id = req["from_id"]
    to_id = req["to_id"]

    # Try to get the lock from both users if fail then return status 403
    tryGetFromUserLock = await tryAcquireLock(lockPerUser[from_id])
    tryGetToUserLock = await tryAcquireLock(lockPerUser[to_id])
    if not (tryGetFromUserLock and tryGetToUserLock):
        # If both locks from users cannot be acquired wait for 3 seconds
        await asyncio.sleep(3)

        # Release the locks only if they were acquired
        await releaseLock(lockPerUser[from_id])
        await releaseLock(lockPerUser[to_id])

        return jsonify({"detail": "locked"}), 403

    try:
        # Quickly get the compatibility score from a map if it has already been calculated
        uniquePairId = "_".join(sorted([from_id, to_id]))
        if uniquePairId in compatibilityMap:
            return jsonify({"compatibility": compatibilityMap[uniquePairId]}), 200

        # Get the dictionary of question to answer for each user
        fromUserQuestionsMap = answers[from_id]
        toUserQuestionMap = answers[to_id]

        # Check if there are any common answers between the users
        # in case compatibility can’t be computed
        commonAns = set(fromUserQuestionsMap.keys()).intersection(
            set(toUserQuestionMap.keys())
        )
        if not commonAns:
            return jsonify({"detail": "no responses in common"}), 400

        # Calculating the compatibility
        compatibility = match.compatibility(fromUserQuestionsMap, toUserQuestionMap)
        compatibilityMap[uniquePairId] = compatibility

        # Lock for 3 seconds before the users can request compatibility to other users
        await asyncio.sleep(3)

    finally:
        # Release the locks at the end
        await releaseLock(lockPerUser[from_id])
        await releaseLock(lockPerUser[to_id])

    return jsonify({"compatibility": compatibility}), 200


if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port=5001)
