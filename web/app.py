from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import threading
import time
import random

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ------------------------
# GLOBAL STATE
# ------------------------
system_running = False
current_vibration = 0.0

STABILISATION_THRESHOLD = 0.35
EMERGENCY_STOP_THRESHOLD = 0.55

blood_flow = 300
arterial_pressure = 120
venous_pressure = 80

treatment_seconds = 0
system_state = "IDLE"

patient = None
alerts = []
last_state = None   # 👈 prevents duplicate alerts

# ------------------------
# SIMULATION LOOP
# ------------------------
def simulation_loop():
    global current_vibration, blood_flow
    global arterial_pressure, venous_pressure
    global treatment_seconds, system_running
    global system_state, last_state

    while True:
        if system_running and treatment_seconds > 0:
            # 🔁 Gradual vibration increase (IMPORTANT)
            if current_vibration < 0.3:
                current_vibration += random.uniform(0.02, 0.05)
            else:
                current_vibration += random.uniform(0.05, 0.1)

            current_vibration = round(min(current_vibration, 0.7), 2)

            # 🔴 EMERGENCY
            if current_vibration >= EMERGENCY_STOP_THRESHOLD:
                if system_state != "EMERGENCY_STOP":
                    system_state = "EMERGENCY_STOP"
                    system_running = False
                    alerts.append({
                        "time": time.strftime("%H:%M:%S"),
                        "message": "EMERGENCY: Severe vibration detected"
                    })

            # 🟠 STABILISATION
            elif current_vibration >= STABILISATION_THRESHOLD:
                system_state = "STABILISATION"
                blood_flow = 200
                arterial_pressure = 180
                venous_pressure = 160

                if last_state != "STABILISATION":
                    alerts.append({
                        "time": time.strftime("%H:%M:%S"),
                        "message": "STABILISATION: Vibration exceeded safe limit"
                    })

            # 🟢 NORMAL
            else:
                system_state = "NORMAL"
                blood_flow = 300
                arterial_pressure = 120
                venous_pressure = 80

            # ⏱ countdown
            treatment_seconds -= 1
            last_state = system_state

        time.sleep(1)

# ------------------------
# ROUTES
# ------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/set_patient", methods=["POST"])
def set_patient():
    global patient, treatment_seconds, system_state, alerts
    global current_vibration, last_state

    data = request.json

    patient = {
        "name": data["name"],
        "age": data["age"],
        "gender": data["gender"]
    }

    treatment_seconds = int(data["hours"]) * 3600
    system_state = "READY"

    # reset state
    alerts.clear()
    current_vibration = 0.0
    last_state = None

    return jsonify({"ok": True})

@app.route("/start", methods=["POST"])
def start():
    global system_running, system_state
    system_running = True
    system_state = "RUNNING"
    return jsonify({"ok": True})

@app.route("/stop", methods=["POST"])
def stop():
    global system_running, system_state
    system_running = False
    system_state = "STOPPED"
    return jsonify({"ok": True})

@app.route("/data")
def data():
    h = treatment_seconds // 3600
    m = (treatment_seconds % 3600) // 60
    s = treatment_seconds % 60

    return jsonify({
        "patient": patient,
        "blood_flow": blood_flow,
        "arterial_pressure": arterial_pressure,
        "venous_pressure": venous_pressure,
        "vibration": current_vibration,
        "remaining_time": f"{h:02}:{m:02}:{s:02}",
        "system_state": system_state,
        "alerts": alerts
    })

# ------------------------
# MAIN
# ------------------------
if __name__ == "__main__":
    threading.Thread(target=simulation_loop, daemon=True).start()
    app.run(debug=True, port=5001)
