import psycopg2
from fastapi import FastAPI, status, HTTPException, Response, Depends
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts ORDER BY id;""")
    # posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute("""INSERT INTO posts (title, content, published)
    #                VALUES (%s, %s, %s)
    #                RETURNING *;""",
    #                (post.title, post.content, post.published,))
    # new_post = cursor.fetchone()
    # conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id),))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found.")
    return {"post_detail": post}


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate,
                db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s,
    #                                    content = %s,
    #                                    published = %s
    #                   WHERE id = %s
    #                   RETURNING *;""",
    #                (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()
    if update_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found.")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""",
    #                (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
