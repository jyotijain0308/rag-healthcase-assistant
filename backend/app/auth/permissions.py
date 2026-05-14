from enum import Enum

class Permission(str, Enum):
    CHAT = "chat"
    INGEST = "ingest"
    RETRIEVE = "retrieve"
    ADMIN = "admin"
    AUDIT = "audit"