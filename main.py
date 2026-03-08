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

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

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

@app.delete("/post/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            my_posts.pop(index)
            return{"message": f"post with id: {id} was successfully deleted"}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")

@app.put("/post/{id}")
def update_post(id : int, post : Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"data": post_dict}
