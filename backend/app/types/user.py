class User(BaseModel):

    username: str

    role: "user" | "admin"
