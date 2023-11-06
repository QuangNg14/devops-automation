import time
from typing import Dict, Optional

# from match_lib import compatibility as compatibility_func


QuestionId = str
Answer = int


def compatibility(
    from_answers: Dict[QuestionId, Answer], to_answers: Dict[QuestionId, Answer]
) -> Optional[float]:
    """
    Computes the compatibility between 2 people.

    Args:
        from_answers (Dict[QuestionId, Answer]): A dictionary of the requestors question ids to answer scores
        to_answers (Dict[QuestionId, Answer]): A dictionary of the requested persons question ids to answer scores

    Returns:
        float: A score in the range [0, 100.0] representing the compatibility between 2 people
        None: For some reason, we could not compute their compatibility


    Example:
        person_1 = {
            "question_1": 1,
            "question_2": 1,
            "question_3": 1
        }

        person_2 = {
            "question_1": 1,
            "question_2": 2,
            "question_3": 3
        }

        score = compatibility(user_1, user_2)

        print(score)

        >> 83.33
    """
    # return compatibility_func(from_answers, to_answers)
    return 20.0
