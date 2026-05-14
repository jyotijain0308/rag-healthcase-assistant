from pydantic import BaseModel

from typing import List, Optional


class MessagePart(BaseModel):

    type: str

    text: Optional[str] = ""

class ChatMessage(BaseModel):

    id: str

    role: str

    parts: List[MessagePart]


class ChatRequest(BaseModel):

    question: str

    messages: Optional[List[ChatMessage]] = []