from http import HTTPStatus

from fastapi import FastAPI

from todolist_api.schemas import Message

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model = Message)
def readRoot():
    return {"message": "Hello World!"}
