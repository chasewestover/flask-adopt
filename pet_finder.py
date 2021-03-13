import requests
from project_secrets import PETFINDER_API_KEY, PETFINDER_SECRET_KEY
from random import choice 

def update_auth_token_string():
    """ Get valid token for petfinder API. """
    auth_token =  requests.post(
    'https://api.petfinder.com/v2/oauth2/token', "grant_type=client_credentials&client_id=CUzV5T4JYVrrnBIRsyuyLLu8u0qSnFZzt288bnvsTwByP3CJuM&client_secret=xauVmTmYXmeZFZhV4yPpAB8xmoewBfix2TlfWEqQ")


def get_random_pet(auth_token):
    """ Get a random pet from the petfinder API. """

    resp = requests.get(
        "https://api.petfinder.com/v2/animals?limit=100",
        headers={"Authorization": f"Bearer {auth_token}"}
        )
    
    pet_finder_pets = resp.json()
    random_pet = choice(pet_finder_pets["animals"])
    print(random_pet)
    pet_dict = {"name": random_pet["name"], "age":random_pet["age"], "url":random_pet["url"]}
    if random_pet["photos"]:
        pet_dict["photo_url"] = random_pet["photos"][0]["small"]
    else:
        pet_dict["photo_url"] =  'https://tse2.mm.bing.net/th?id=OIP.n1C1oxOvYLLyDIavrBFoNQHaHa&pid=Api'
    print(pet_dict)

    return pet_dict