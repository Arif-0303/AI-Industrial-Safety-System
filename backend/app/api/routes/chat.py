from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import generate_chat_response

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    response = generate_chat_response(
        request.message,
        db,
    )

    return ChatResponse(
        response=response,
    )