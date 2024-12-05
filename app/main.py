from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


while True:
    # responsible for connecting to database
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="python",
            password="123456",
            cursor_factory=RealDictCursor,
        )  # conection with database postgres, and dbeaver. ( sudo docker run --name fastapi -e POSTGRES_PASSWORD=123456 -e POSTGRES_USER=python -e POSTGRES_DB=fastapi -p 5432:5432 -d postgres)
        cursor = conn.cursor()
        print("Database connection was successfully")
        break
    except Exception as error:
        print("Database not connected")
        print("Error: ", error)
        time.sleep(2)


my_posts = [
    {"title": "Hello", "content": "mundo", "url": "http://api.twitter.com", "id": 1},
    {"title": "oLÁ", "content": "Olu", "id": 2},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


# @app.get("/")
# def root():
#     return {"message": my_posts}


@app.post("/create_post", status_code=status.HTTP_201_CREATED)
def creatre_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"message": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(int(id))
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id: {id} was not found"}
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist"
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist"
        )
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"message": post_dict}


@app.get("/")
def get_posts():
    posts = cursor.execute("""SELECT * FROM posts """) # criar uma tabela na mão no dbaver
    posts = cursor.fetchall()
    print(posts)
    return {"data": my_posts}
