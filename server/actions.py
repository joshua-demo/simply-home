import requests

def turn_device_on(room_and_device:str):
    """
    Turn on a device
    Parameters: String "room" and String "device"
    Valid rooms are "livingRoom", "kitchen", "bedroom", "frontHouse"
    Valid devices are "light", "speaker"
    """
    url = "http://localhost:3001/api/turnOn"
    payload = {
        "room": room_and_device.split(" ")[0],
        "device": room_and_device.split(" ")[1]
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)

def turn_device_off(room_and_device:str):
    """
    Turn off a device
    Parameters: String "room" and String "device"
    Valid rooms are "livingRoom", "kitchen", "bedroom", "frontHouse"
    Valid devices are "light", "speaker"
    """
    url = "http://localhost:3001/api/turnOff"
    payload = {
        "room": room_and_device.split(" ")[0],
        "device": room_and_device.split(" ")[1]
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)

def play_sound(room_and_sound:str):
    """
    Plays a selected sound on a speaker.
    Parameters: String "room" and String "sound"
    Valid rooms are "livingRoom", "kitchen", "bedroom". "frontHouse" is NOT valid because it has no speaker.
    Valid sounds are "alarm", "doorbell", "dog", "fire", "siren", "thunder", "water", a specific song name, or onomatopoeia.
    """
    url = "http://localhost:3001/api/playSound"
    payload = {
        "room": room_and_sound.split(" ")[0],
        "sound": room_and_sound.split(" ")[1]
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)


def set_living_room_light(color_name:str):
    """changes the living room light to color_name"""
    url = "http://localhost:3001/api/setLightColor"

    payload = {
        "room": "livingRoom",
        "color": color_name
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)
