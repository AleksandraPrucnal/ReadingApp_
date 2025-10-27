from src.infrastructure.dto.exerciseDTO import ExerciseMatchDTO, ExerciseQuestionDTO

def test_match_from_record_ok():
    row = {
        "id_exercise": 1, "type": "MATCH_IMAGE", "level": 2,
        "topics": [{"id_topic": 1, "name": "dogs"}],
        "text": "abc", "image_urls": ["a.png"], "correct_index": 0
    }
    dto = ExerciseMatchDTO.from_record(row)
    assert dto.type == "MATCH_IMAGE"
    assert dto.topics[0].id_topic == 1

def test_question_from_record_alias_text_q():
    row = {
        "id_exercise": 2, "type": "TEXT_QUESTION", "level": 1,
        "topics": [], "text_q": "xyz", "image_url": "img.png", "questions": []
    }
    dto = ExerciseQuestionDTO.from_record(row)
    assert dto.text == "xyz"
