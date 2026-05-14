from app.auth.permissions import Permission

ROLE_PERMISSIONS = {
    "admin": [
        Permission.CHAT,
        Permission.INGEST
    ],
    "doctor": [
        Permission.CHAT
    ],
    "patient": [
        Permission.CHAT,
    ],
}