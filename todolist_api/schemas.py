# from fastapi.responses import HTMLResponse
from pydantic import BaseModel


class Message(BaseModel):
    message: str


# class HtmlMessage(BaseModel):
#    html_message: HTMLResponse
