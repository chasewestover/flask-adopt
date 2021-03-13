import requests
from project_secrets import PETFINDER_API_KEY, PETFINDER_SECRET_KEY
from random import choice 

def update_auth_token_string():
    """ Get valid token for petfinder API. """
    resp = requests.post(
    'https://api.petfinder.com/v2/oauth2/token', 
    data={"grant_type": "client_credentials","client_id": PETFINDER_API_KEY,"client_secret": PETFINDER_SECRET_KEY })
    
    return resp.json()["access_token"]

def get_random_pet(auth_token):
    """ Get a random pet from the petfinder API. """

    resp = requests.get(
        "https://api.petfinder.com/v2/animals?limit=100",
        headers={"Authorization": f"Bearer {auth_token}"}
        )
    
    pet_finder_pets = resp.json()
    random_pet = choice(pet_finder_pets["animals"])
    pet_dict = {"name": random_pet["name"], "age":random_pet["age"], "url":random_pet["url"]}
    if random_pet["photos"]:
        pet_dict["photo_url"] = random_pet["photos"][0]["small"]
    else:
        pet_dict["photo_url"] =  'https://tse2.mm.bing.net/th?id=OIP.n1C1oxOvYLLyDIavrBFoNQHaHa&pid=Api'
    return pet_dict