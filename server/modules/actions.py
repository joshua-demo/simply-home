import requests

def turn_on(room:str, device:str):
    """
    Turn on a device
    Parameters: String "room" and String "device"
    Valid rooms are "livingRoom", "kitchen", "bedroom"
    Valid devices are "light", "speaker"

    If no room is specified, default to using the living room.
    If you want to turn on all devices in a room, turn each device in each room on individually. Don't separate function calls with a "\n"
    """
    url = "http://sim:3001/api/turnOn"
    payload = {
        "room": room,
        "device": device
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)

def turn_device_on(room:str, device:str):
    """
    Turn on a device
    Parameters: String "room" and String "device"
    Valid rooms are "livingRoom", "kitchen", "bedroom"
    Valid devices are "light", "speaker"

    If no room is specified, default to using the living room.
    If you want to turn on all devices in a room, turn each device in each room on individually. Don't separate function calls with a "\n"
    """
    url = "http://sim:3001/api/turnOn"
    payload = {
        "room": room,
        "device": device
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)
    
def turn_off(room:str, device:str):
    """
    Turn off a device
    Parameters: String "room" and String "device"
    Valid rooms are "livingRoom", "kitchen", "bedroom"
    Valid devices are "light", "speaker"

    If no room is specified, default to using the living room.
    """
    url = "http://sim:3001/api/turnOff"
    payload = {
        "room": room,
        "device": device
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)

def turn_device_off(room:str, device:str):
    """
    Turn off a device
    Parameters: String "room" and String "device"
    Valid rooms are "livingRoom", "kitchen", "bedroom"
    Valid devices are "light", "speaker"

    If no room is specified, default to using the living room.
    """
    url = "http://sim:3001/api/turnOff"
    payload = {
        "room": room,
        "device": device
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)

def set_light_color(room:str, color:str):
    """
    Changes the light in a room to a new color.
    Parameters: String "room" and String "color"
    Valid rooms are "livingRoom", "kitchen", "bedroom"
    Valid colors are "aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "white", "yellow"

    If no room is specified, default to using the living room.
    """
    url = "http://sim:3001/api/setLightColor"

    payload = {
        "room": room,
        "color": color
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)

def play_sound(room:str, sound:str):
    """
    Plays a selected sound on a speaker.
    Parameters: String "room" and String "sound"
    Valid rooms are "livingRoom", "kitchen", "bedroom". "frontHouse" is NOT valid because it has no speaker.
    Valid sounds are "alarm", "doorbell", "dog", "fire", "siren", "thunder", "water", a specific song name, or onomatopoeia. If there is a sense of urgency, make the sound in ALL CAPS.

    If a user asks to play a song, just set the sound to the song name. For example, "livingRoom Hello" will play a song titled "Hello" in the living room.

    If no room is specified, default to using the living room. DO NOT play the sound in the frontHouse.
    """
    url = "http://sim:3001/api/playSound"
    payload = {
        "room": room,
        "sound": sound
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)

def lock_door():
    """
    Lock the door to the house. There's only one door.
    """
    url = "http://sim:3001/api/lockDoor"
    try:
        response = requests.post(url)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)

def unlock_door():
    """
    Unlock the door to the house. There's only one door.
    """
    url = "http://sim:3001/api/unlockDoor"
    try:
        response = requests.post(url)
        response.raise_for_status()
        print("POST request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making POST request:", e)

def check_camera():
    """
    Check the camera at the front of the house.
    """
    url = "http://sim:3001/api/checkCamera"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("GET request successful:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making GET request:", e)
