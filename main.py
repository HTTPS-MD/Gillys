from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from authentication import user_signin, user_signup, delete_user  # Kukunin nito yung ginawa mo sa kabila

app = FastAPI()

# Format ng data na tatanggapin galing sa frontend
class UserCredentials(BaseModel):
    username: str
    password: str

class DeleteRequest(BaseModel):
    username : str

@app.post("/api/signup")
def create_account(user: UserCredentials):
    success = user_signup(user.username, user.password)

    if success:
        return {"message": "Account successfully created!"}
    else:
        raise HTTPException(status_code=400, detail="Username already exists")


@app.post("/api/login")
def login_account(user: UserCredentials):
    is_valid = user_signin(user.username, user.password)

    if is_valid:
        return {"message": "Login successful!"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


@app.delete("/api/delete")
def remove_account(user : DeleteRequest):
    is_valid = delete_user(user.username)

    if is_valid:
        return {"message": "Account deleted successfully!"}
    else:
        raise HTTPException(status_code = 404, detail="User does not exist!")