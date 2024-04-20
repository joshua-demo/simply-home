import requests

def multiply(a:float, b:float):
    """returns a * b."""
    return a*b

def set_living_room_light_to_red():
    """changes the living room light to red"""
    url = "http://localhost:3001/api/setLightColor"

    payload = {
        "room": "livingRoom",
        "color": "red"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)
