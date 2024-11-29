from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.post("/create_post")
def creatre_posts(post: Post):
  print(post)
  return {"message": post}