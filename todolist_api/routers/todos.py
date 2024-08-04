from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todolist_api.database import get_session
from todolist_api.models import Todo, User
from todolist_api.schemas import TodoPublic, TodoSchema
from todolist_api.security import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

T_Session = Annotated[Session, Depends(get_session)]
T_Current_User = Annotated[User, Depends(get_current_user)]


@router.post("/", response_model=TodoPublic)
def create_todo(
    todo: TodoSchema, current_user: T_Current_User, session: T_Session
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=current_user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
