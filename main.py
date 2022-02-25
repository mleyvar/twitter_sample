# python
from email import message
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List


import logging
import logging.config

# pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

logger = logging.getLogger(__name__)
app = FastAPI(debug=True)

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
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)    
    

class Recipe(BaseModel):
    recipe_id: UUID = Field(...)
    title: str = Field(
        ..., 
        max_length=500,
        min_length=1
        )
    detail: str = Field(
        ..., 
        max_length=1250,
        min_length=1
        )
    image_url: str = Field(
        ..., 
        min_length=1
        )
    author: str = Field(
        ..., 
        min_length=1
        )
        
    created_at: datetime = Field(default=datetime.now())    
    
class UserRecipe(BaseModel):
    user_id: UUID = Field(...)
    user: str = Field(
        ..., 
        max_length=25,
        min_length=1
        )
    password: str = Field(
        ..., 
        max_length=25,
        min_length=1
        )
    created_at: datetime = Field(default=datetime.now())    


    
class Result(BaseModel):
    code: str = Field(
        ..., 
        max_length=5,
        min_length=1
        )
    message: str = Field(
        ..., 
        max_length=50,
        min_length=1
        )
    
class AccessResponse(BaseModel):
    access_response: Result = Field(...)


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
def signup(user: UserRegister = Body(...)):
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
        - birth_date: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user


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
    """
    SignUp

    This path operation show all users in the app

    Parameters:
                
    Return a json list with all users in the app, with the following:
        - user_id: UUID
        - email: Emailstr
        - first_name: stri
        - last_name: str
        - birth_date: datetime
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results
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
    """
    Home

    This path operation show all tewwts in the app

    Parameters:
        - tweet_id: UUID 
        - content: str 
        - created_at: datetime 
        - updated_at: Optional[datetime] 
        - by: User   

    Return a json list with all tweet in the app, with the following:
       
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
    return results


### post a tweet
@app.post(
    path='/post',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a Tweet",
    tags=["Tweets"]
    )
def post(tweet: Tweet = Body(...)):
    """
    Post a Tweet

    This path operation post a tweet in the app

    Parameters:
        - Request body parameter
            - tweet: Tweet
    Return a json with de basic tweet information:
        - tweet_id: UUID 
        - content: str 
        - created_at: datetime 
        - updated_at: Optional[datetime] 
        - by: User   
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        if tweet_dict["updated_at"]:
            tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"]) 
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"]) 

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet



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
    return {"delete": "true"}


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

## get recetas
@app.get(
    path='/recipe',
    status_code=status.HTTP_200_OK,
    summary="Recipes",
    tags=["Recipes"]
    )
def get_recipe():
    """
    Recipes

    This path operation show all recipes in the app

    Parameters:
                
    Return a json list with all users in the app, with the following:
        - recipe_id: UUID
        - title: str
        - image_url: stri
        - created_at: datetime
    """
    cad = ""
    with open("recipe.json", "r", encoding="utf-8") as f:

        results =  json.loads(f.read())

        return {"recipes": results}

#        return {"recipes":list}  



## get recetas
@app.post(
    path='/recipe',
    response_model=Recipe,
    status_code=status.HTTP_200_OK,
    summary="Recipes",
    tags=["Recipes"]
    )
def post_recipe(recipe: Recipe = Body(...)):
    """
     Recipes

    This path operation add recipes in the app

    Parameters:
                
    Return a json list with all users in the app, with the following:
        - recipe_id: UUID
        - title: str
        - image_url: stri
        - created_at: datetime
    """
    with open("recipe.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        recipe_dict = recipe.dict()
        recipe_dict["recipe_id"] = str(recipe_dict["recipe_id"])
        recipe_dict["title"] = str(recipe_dict["title"])
        recipe_dict["detail"] = str(recipe_dict["detail"])
        recipe_dict["image_url"] = str(recipe_dict["image_url"])
        recipe_dict["created_at"] = str(recipe_dict["created_at"])

        results.append(recipe_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return recipe     


## get recetas
@app.post(
    path='/access',
    status_code=status.HTTP_200_OK,
    summary="Recipes",
    tags=["Recipes"]
    )
def access(userLogin: UserLogin = Body(...)):
    """
    Access

    This path operation return access in the app

    Parameters:
                
    Return a json with message from access in the app, with the following:
        - code: str   (code=0 = OK;  code=-1 = ERROR)
        - message: str (message="OK" = OK;  message="text" = ERROR)
    """
    base = Result(code="0", message="base")
    res = AccessResponse(access_response = base)
    if userLogin.email == "admin@admin.com" and userLogin.password == "Password123":
        res.access_response.code = "0"
        res.access_response.message = "OK"
        return res   
    else:
        res.access_response.code = "-1"
        res.access_response.message = "Invalid access"
        return res
         
