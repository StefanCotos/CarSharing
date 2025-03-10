from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

commands = {}
car_states = {}


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = sqlite3.connect("carsharing.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=? AND password=?", (data["name"], data["password"]))
    user = c.fetchone()
    conn.close()
    return jsonify({"success": bool(user)})


@app.route("/cars", methods=["GET"])
def get_cars():
    conn = sqlite3.connect("carsharing.db")
    c = conn.cursor()
    location = request.args.get('location')
    if location:
        c.execute("SELECT id, vin, location FROM cars WHERE available=1 AND location=?", (location,))
    else:
        c.execute("SELECT id, vin, location FROM cars WHERE available=1")
    cars = [{"id": row[0], "vin": row[1], "location": row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify({"cars": cars})


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = sqlite3.connect("carsharing.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (name, password, phoneNumber, driverLicense) VALUES (?, ?, ?, ?)",
                  (data["name"], data["password"], data["phoneNumber"], data["driverLicense"]))
        conn.commit()
        return jsonify({"success": True, "message": "Account created!"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Username already exists!"})
    finally:
        conn.close()


@app.route("/check_license", methods=["GET"])
def check_license():
    username = request.args.get("username")
    conn = sqlite3.connect("carsharing.db")
    c = conn.cursor()
    c.execute("SELECT driverLicense FROM users WHERE name=?", (username,))
    user = c.fetchone()
    conn.close()
    return jsonify({"driverLicense": bool(user and user[0])})


@app.route("/rent_car", methods=["POST"])
def rent_car():
    data = request.json
    conn = sqlite3.connect("carsharing.db")
    c = conn.cursor()
    try:
        c.execute("UPDATE cars SET available=0 WHERE id=?", (data["car_id"],))
        conn.commit()
        return jsonify({"success": True, "message": "Car rented successfully!"})
    except sqlite3.Error as e:
        return jsonify({"success": False, "message": str(e)})
    finally:
        conn.close()


@app.route("/stop_rent", methods=["POST"])
def stop_rent():
    data = request.json
    conn = sqlite3.connect("carsharing.db")
    c = conn.cursor()
    try:
        c.execute("UPDATE cars SET available=1 WHERE id=?", (data["car_id"],))
        conn.commit()
        return jsonify({"success": True, "message": "Car rental stopped successfully!"})
    except sqlite3.Error as e:
        return jsonify({"success": False, "message": str(e)})
    finally:
        conn.close()


@app.route("/send_command", methods=["POST"])
def send_command():
    data = request.json
    car_id = data["car_id"]
    command = data["command"]

    if command in ["unlock", "lock", "close_doors", "open_doors", "lights_on", "lights_off", "start_engine",
                   "stop_engine"]:
        commands[car_id] = command

        return jsonify({"success": True, "message": f"Command '{command}' sent to car {car_id}."})
    else:
        return jsonify({"success": False, "message": "Invalid command."}), 400


@app.route("/get_command/<int:car_id>", methods=["GET"])
def get_command(car_id):
    return jsonify({"command": commands.pop(car_id, "none")})


@app.route("/update_state", methods=["POST"])
def update_state():
    data = request.json
    car_states[data["car_id"]] = data["state"]
    return jsonify({"message": "State updated."})


@app.route("/get_state/<int:car_id>", methods=["GET"])
def get_state(car_id):
    return jsonify({"state": car_states.get(car_id, {"unknown": "No data"})})


if __name__ == "__main__":
    app.run(debug=True)
