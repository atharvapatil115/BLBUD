from fastapi import FastAPI, Depends
from db.database import Base, engine
from auth.routes import router as auth_router
from auth.middleware import get_current_user

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include auth routes
app.include_router(auth_router, prefix="/auth")


# ✅ Protected test route
@app.get("/me")
def me(user = Depends(get_current_user)):
    return {"user": user}


# ✅ Example: Connect your RAG pipeline later
@app.post("/query")
def query(q: str, user=Depends(get_current_user)):
    user_id = user["user_id"]

    # 👉 integrate your existing RAG here
    response = f"User {user_id} asked: {q}"

    return {"response": response}
