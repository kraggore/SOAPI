from fastapi import FastAPI
from mangum import Mangum
from cachetools import TTLCache
import requests
import json
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()
handler = Mangum(app)
cache = TTLCache(maxsize=1000, ttl=60)

base_url = "https://api.stackexchange.com/"
version = "2.3/"
base_url += version
answer_filter = "&filter=!)qYyqP4)Fr1HcPrf2Kg1"
question_filter = "&filter=!)rmjGbcIo.qcDATmkC6j"


def get_response(filters):
    response = requests.get(base_url + filters)
    json_str = response.text
    json_dict = json.loads(json_str)
    return json_dict


def format_questions(questions):
    formatted_questions = {"items": []}
    for question in questions['items']:
        formatted_questions['items'].append({
            'ID': question['question_id'],
            'is_answered': question['is_answered'],
            'accepted_answer_id': question['accepted_answer_id'],
            'title': question['title'],
            'body': question['body'],
            'body_markdown': question['body_markdown'],
            'link': question['link'],
            'creation_date': question['creation_date'],
            'last_activity_date': question['last_activity_date'],
            'last_edit_date': question['last_edit_date'],
            'answer_count': question['answer_count'],
            'view_count': question['view_count'],
            'score': question['score'],
            'up_vote_count': question['up_vote_count'],
            'tags': question['tags']
        })
    return formatted_questions


def jsonify_data(data):
    json_compatible_item_data = jsonable_encoder(data)
    data = JSONResponse(content=json_compatible_item_data)
    return data


@app.get("/")
def root():
    return {"mex": "tex"}


@app.get("/tag/{tag}")
def hello(tag: str):
    return get_response(f'questions'
                        f'?pagesize=100'
                        f'&order=desc'
                        f'&sort=votes'
                        f'&tagged={tag}'
                        f'&site=stackoverflow'
                        f'{question_filter}'
                        )


@app.get("/questions/{q_id}/answers")
def get_answers(q_id: str):
    return get_response(f'questions/{q_id}/answers?order=desc&sort=votes&site=stackoverflow'
                        f'{answer_filter}'
                        )
