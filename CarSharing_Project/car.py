import requests
import sys
import time

CAR_ID = int(sys.argv[1])
BACKEND_URL = "http://127.0.0.1:5000"

car_state = {
    "locked": True,
    "doors_closed": True,
    "lights_off": True,
    "engine_off": True
}


def get_command():
    response = requests.get(f"{BACKEND_URL}/get_command/{CAR_ID}")
    return response.json().get("command")


def execute_command(command):
    global car_state
    if command == "unlock":
        car_state["locked"] = False
        print(f"Car {CAR_ID} unlocked!")
    elif command == "lock":
        car_state["locked"] = True
        print(f"Car {CAR_ID} locked!")
    elif command == "open_doors":
        car_state["doors_closed"] = False
        print(f"Doors of car {CAR_ID} opened!")
    elif command == "close_doors":
        car_state["doors_closed"] = True
        print(f"Doors of car {CAR_ID} closed!")
    elif command == "lights_on":
        car_state["lights_off"] = False
        print(f"Lights of car {CAR_ID} turned on!")
    elif command == "lights_off":
        car_state["lights_off"] = True
        print(f"Lights of car {CAR_ID} turned off!")
    elif command == "start_engine":
        car_state["engine_off"] = False
        print(f"Engine of car {CAR_ID} started!")
    elif command == "stop_engine":
        car_state["engine_off"] = True
        print(f"Engine of car {CAR_ID} stopped!")


def send_state():
    requests.post(f"{BACKEND_URL}/update_state", json={"car_id": CAR_ID, "state": car_state})


while True:
    command = get_command()
    if command and command != "none":
        execute_command(command)
        send_state()

    time.sleep(2)
