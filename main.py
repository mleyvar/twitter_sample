# python
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List


# pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status


app = FastAPI()

# Models
class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field (..., min_length=8)

class User(UserBase):
    password: str = Field (..., min_length=8)
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    birth_date: Optional[date] = Field(default=None)    

class UserRegister(User):
       password: str = Field (..., min_length=8)

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ..., 
        max_length=253,
        min_length=1
        )
    created_at: datetime = Field(default=datetime.now())    
    update_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)    
    


# path operations


## Users
### Register a user
@app.post(
    path='/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
    )
def signup():
    """
    SignUp
    
    This path operation register a user in the app

    Parameters:
        - Request body parameter
            - User: UserRegister
    Return a json with de basic user information:
        - user_id: UUID
        - email: Emailstr
        - first_name: stri
        - last_name: str
        - birth_date: str
    """
    pass

### Login a user
@app.post(
    path='/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
    )
def login():
    pass

### Show all users
@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all Users",
    tags=["Users"]
    )
def show_all_users():
    pass

### show a user
@app.get(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
    )
def show_a_user():
    pass


@app.delete(
    path='/users/{user_id}/delete',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
    )
def delete_a_user():
    pass

@app.put(
     path='/users/{user_id}/update',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
    )
def update_a_user():
    pass

## Tweet

### show all tweets
@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
    )
def home():
    return {"Hello": "World"}


### post a tweet
@app.post(
    path='/post',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a Tweet",
    tags=["Tweets"]
    )
def post():
    pass


### show a tweet
@app.get(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="show a Tweet",
    tags=["Tweets"]
    )
def show_a_tweet():
    pass


### delete a tweet
@app.delete(
    path='/tweets/{tweet_id}/delete',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Deleete a Tweet",
    tags=["Tweets"]
    )
def delete_a_tweet():
    pass


### delete a tweet
@app.put(
    path='/tweets/{tweet_id}/update',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="update a Tweet",
    tags=["Tweets"]
    )
def update_a_tweet():
    pass

