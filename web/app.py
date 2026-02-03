import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, jsonify, request, render_template
import threading
import time

from ai_simulation.simulation.vibration_ai import generate_vibration
from ai_simulation.simulation.stabilisation_logic import check_stabilisation
from ai_simulation.simulation.dialysis_machine import DialysisMachine


app = Flask(__name__)

# -----------------------
# GLOBAL STATE
# -----------------------
machine = DialysisMachine()
current_vibration = 0.0
threshold_value = 0.0
alert_log = []
alert_sent = False
t = 0

# -----------------------
# BACKGROUND SIMULATION
# -----------------------
def simulation_loop():
    global current_vibration, threshold_value, alert_sent, t

    while True:
        current_vibration = generate_vibration(t)
        stabilise, threshold_value = check_stabilisation(current_vibration)

        if stabilise and not alert_sent:
            machine.activate_stabilisation()
            alert_log.append({
                "time": time.strftime("%H:%M:%S"),
                "message": "Emergency alert sent to Doctor, Admin, Reception"
            })
            alert_sent = True

        machine.update()
        t += 1
        time.sleep(1)

# -----------------------
# ROUTES
# -----------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify({
        "vibration": current_vibration,
        "threshold": round(threshold_value, 3),
        "stabilisation": machine.stabilisation_mode,
        "blood_flow": machine.blood_flow,
        "arterial_pressure": machine.arterial_pressure,
        "venous_pressure": machine.venous_pressure,
        "treatment_time": machine.treatment_time,
        "alerts": alert_log[-5:]
    })

@app.route("/set_time", methods=["POST"])
def set_time():
    machine.treatment_time = int(request.json["time"])
    return {"status": "updated"}

# -----------------------
# START
# -----------------------
if __name__ == "__main__":
    thread = threading.Thread(target=simulation_loop)
    thread.daemon = True
    thread.start()
    app.run(debug=True)
