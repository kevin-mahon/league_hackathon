import json
import requests
from errors import get_error_string



if __name__ == "__main__":
    with open(".secrets") as f:
        secrets = f.read().strip()
    api_key = secrets.split("=")[1]
    print(api_key)
    url = f"https://americas.api.riotgames.com/lol/summoner/v4/summoners/by-name/Huntley?api_key={api_key}"
    response = requests.get(url)#, headers=headers)

    if get_error_string(response.status_code):
        print(get_error_string(response.status_code))
    print(response.status_code)
    print(response)


