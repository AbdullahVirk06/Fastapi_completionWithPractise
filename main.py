from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

app = FastAPI()

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

my_posts = [{"title" : "title of post 1", "content" : " content of post 1","id": 1},{"title":"favourite food","content":"I like pizza","id":2}]
@app.get("/")
def root():
    return {"message":"Hello World"}
@app.get("/post")
def post():
    return {"data" : my_posts}

@app.post("/posts",status_code = status.HTTP_201_CREATED)
def create_post(post : Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return{"data" : post_dict}

#@app.get("/post/{id}")
#def get_post(id : int):
#    post = find_post(id)
#    return{"post_detail": post}

@app.get("/post/{id}")
def get_post(id : int, response : Response):
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id: {id} was not found"}
    return{"post_detail": post}