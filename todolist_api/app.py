from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from todolist_api.schemas import Message

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Hello World!"}


@app.get(
    "/html_response",
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,
)
def html_response():
    return """
    <div>
        <h1>Título</>
    </div>
    """
