import psycopg2

from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg2.connect(host='localhost', database='fastapi',
                            user='postgres', password='password123',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('DB connection successful.')
except Exception as error:
    print('Connecting to DB failed.')
    print(f'Error was {error}')


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts ORDER BY id;""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published)
                   VALUES (%s, %s, %s) 
                   RETURNING *;""",
                   (post.title, post.content, post.published,))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found.")
    return {"post_detail": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, 
                                       content = %s, 
                                       published = %s
                      WHERE id = %s
                      RETURNING *;""",
                   (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found.")
    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""",
                   (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
