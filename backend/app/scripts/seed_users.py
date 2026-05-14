from sqlalchemy import text

from app.db.db_session import (
    SessionLocal
)

from app.auth.password_handler import (
    hash_password
)

from app.auth.roles import (
    UserRole
)

db = SessionLocal()

users = [
    {
        "username": "admin",
        "email": "admin@test.com",
        "password": "admin123",
        "role": UserRole.ADMIN.value
    },
    {
        "username": "doctor",
        "email": "doctor@test.com",
        "password": "doctor123",
        "role": UserRole.DOCTOR.value
    }
]

try:

    for user in users:

        existing = db.execute(
            text("""
                SELECT id
                FROM users
                WHERE email = :email
            """),
            {
                "email": user["email"]
            }
        ).fetchone()

        if existing:

            print(
                f"User already exists: {user['email']}"
            )

            continue

        db.execute(
            text("""
                INSERT INTO users
                (
                    username,
                    email,
                    hashed_password,
                    role
                )
                VALUES
                (
                    :username,
                    :email,
                    :password,
                    :role
                )
            """),
            {
                "username": user["username"],
                "email": user["email"],
                "password": hash_password(
                    user["password"]
                ),
                "role": user["role"]
            }
        )

        print(
            f"Created user: {user['email']}"
        )

    db.commit()

finally:

    db.close()

print("Seeding completed")