from flask import Flask, jsonify, request, render_template
import threading
import time
import random

app = Flask(__name__, template_folder="templates", static_folder="static")

# ------------------------
# GLOBAL STATE
# ------------------------
system_running = False
current_vibration = 0.0

# thresholds
STABILISATION_THRESHOLD = 0.35
EMERGENCY_STOP_THRESHOLD = 0.55

blood_flow = 300
arterial_pressure = 120
venous_pressure = 80
treatment_seconds = 2 * 3600

system_state = "NORMAL"

# patient storage
patients = {}
current_patient_id = None
current_session = None

# ------------------------
# SIMULATION LOOP
# ------------------------
def simulation_loop():
    global current_vibration, blood_flow
    global arterial_pressure, venous_pressure
    global treatment_seconds, system_running
    global system_state, current_session

    while True:
        if system_running and current_patient_id:
            current_vibration = round(random.uniform(0.05, 0.7), 2)

            # 🔴 Emergency Stop
            if current_vibration >= EMERGENCY_STOP_THRESHOLD:
                system_state = "EMERGENCY_STOP"
                system_running = False

                alert = {
                    "time": time.strftime("%H:%M:%S"),
                    "message": "EMERGENCY: Severe vibration detected. Dialysis stopped."
                }

                current_session["alerts"].append(alert)
                patients[current_patient_id]["sessions"].append(current_session)
                current_session = None

            # 🟠 Stabilisation
            elif current_vibration >= STABILISATION_THRESHOLD:
                system_state = "STABILISATION"
                blood_flow = 200
                arterial_pressure = 180
                venous_pressure = 160

                alert = {
                    "time": time.strftime("%H:%M:%S"),
                    "message": "ALERT: Stabilisation mode activated."
                }
                current_session["alerts"].append(alert)

            # 🟢 Normal
            else:
                system_state = "NORMAL"
                blood_flow = 300
                arterial_pressure = 120
                venous_pressure = 80

            if treatment_seconds > 0 and system_state != "EMERGENCY_STOP":
                treatment_seconds -= 1

        time.sleep(1)

# ------------------------
# ROUTES
# ------------------------
@app.route("/")
def index():
    return "Dialysis Backend Running"


@app.route("/set_patient", methods=["POST"])
def set_patient():
    global current_patient_id, current_session, treatment_seconds

    data = request.json
    pid = data["id"]

    patients[pid] = {
        "name": data["name"],
        "age": data["age"],
        "gender": data["gender"],
        "sessions": []
    }

    current_patient_id = pid
    current_session = {
        "start_time": time.strftime("%H:%M:%S"),
        "alerts": []
    }

    treatment_seconds = int(data.get("hours", 2) * 3600)

    return jsonify({"ok": True})

@app.route("/data")
def data():
    h = treatment_seconds // 3600
    m = (treatment_seconds % 3600) // 60
    s = treatment_seconds % 60

    patient = patients.get(current_patient_id)

    return jsonify({
        "patient": patient,
        "vibration": current_vibration,
        "blood_flow": blood_flow,
        "arterial_pressure": arterial_pressure,
        "venous_pressure": venous_pressure,
        "remaining_time": f"{h:02}:{m:02}:{s:02}",
        "system_state": system_state,
        "alerts": current_session["alerts"] if current_session else []
    })

@app.route("/start", methods=["POST"])
def start():
    global system_running
    if current_patient_id:
        system_running = True
    return jsonify({"ok": True})

@app.route("/stop", methods=["POST"])
def stop():
    global system_running
    system_running = False
    return jsonify({"ok": True})

# ------------------------
# MAIN
# ------------------------
if __name__ == "__main__":
    threading.Thread(target=simulation_loop, daemon=True).start()
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
