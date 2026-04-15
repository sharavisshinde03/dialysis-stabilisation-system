import sys
import os
import threading
import time
import random
import smtplib
from email.mime.text import MIMEText
from flask import send_from_directory

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from core.vibration_ai import generate_vibration
from core.stabilisation_logic import get_system_mode
from supabase import create_client, Client

@app.route('/')
def serve_flutter():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_files(path):
    return send_from_directory('static', path)


# -------------------------------------------------
# EMAIL FUNCTION (🔥 ADDED ONLY)
# -------------------------------------------------
def send_email(message):
    sender = "sharavisshinde03@gmail.com"
    password = "yzamxznobiraxuos"   # 🔥 use Gmail app password
    receiver = "ronakludbe@gmail.com"

    msg = MIMEText(message)
    msg['Subject'] = "Dialysis Alert 🚨"
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("✅ Email sent")
    except Exception as e:
        print("❌ Email error:", e)


# -------------------------------------------------
# SUPABASE CONFIG
# -------------------------------------------------
SUPABASE_URL = "https://gzaerodxgvnibuznqdqb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd6YWVyb2R4Z3ZuaWJ1em5xZHFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEyNzU5NjYsImV4cCI6MjA4Njg1MTk2Nn0.tfPPhMVoJjJ1ZtKb_tVJboAEF_RNRHCEkWINm_jPK1o"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# -------------------------------------------------
# APP CONFIG
# -------------------------------------------------
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)


# -------------------------------------------------
# GLOBAL STATE
# -------------------------------------------------
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
last_state = None

email_sent = False   # 🔥 ADDED


# -------------------------------------------------
# SIMULATION LOOP
# -------------------------------------------------
def simulation_loop():
    global current_vibration, blood_flow
    global arterial_pressure, venous_pressure
    global treatment_seconds, system_running
    global system_state, last_state, email_sent

    while True:
        if system_running and treatment_seconds > 0:

            if current_vibration < 0.3:
                current_vibration += random.uniform(0.02, 0.05)
            else:
                current_vibration += random.uniform(0.05, 0.1)

            current_vibration = round(min(current_vibration, 0.7), 2)

            # 🔴 EMERGENCY (ONLY CHANGE HERE)
            if current_vibration >= EMERGENCY_STOP_THRESHOLD:
                if system_state != "EMERGENCY_STOP":
                    system_state = "EMERGENCY_STOP"
                    system_running = False

                    alerts.append({
                        "time": time.strftime("%H:%M:%S"),
                        "message": "EMERGENCY: Severe vibration detected"
                    })

                    if not email_sent:
                        send_email("⚠️ STABILISATION: Vibration exceeded safe limit in Dialysis System.")
                        send_email("🚨 EMERGENCY: Severe vibration detected in Dialysis System!")
                        email_sent = True

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
                system_state = "RUNNING"
                blood_flow = 300
                arterial_pressure = 120
                venous_pressure = 80

                email_sent = False   # 🔥 RESET

            treatment_seconds -= 1
            last_state = system_state

        time.sleep(1)


# -------------------------------------------------
# ROUTES (UNCHANGED)
# -------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/patients", methods=["POST"])
def create_patient():
    global patient, treatment_seconds, system_state
    global alerts, current_vibration, last_state

    data = request.json

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    try:
        supabase.table("patients").insert({
            "name": data["name"],
            "age": data["age"],
            "gender": data["gender"]
        }).execute()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    patient = {
        "name": data["name"],
        "age": data["age"],
        "gender": data["gender"]
    }

    treatment_seconds = int(data["hours"]) * 3600
    system_state = "READY"

    alerts.clear()
    current_vibration = 0.0
    last_state = None

    return jsonify({"message": "Patient saved & activated"})


@app.route("/start", methods=["POST"])
def start():
    global system_running, system_state

    if not patient:
        return jsonify({"error": "No patient set"}), 400

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


@app.route("/status")
def status():
    vibration = generate_vibration(int(time.time()))
    mode = get_system_mode(vibration)

    popup_msg = ""
    if mode == "STABILISATION":
        popup_msg = "⚠️ Earthquake detected! Stabilisation mode active."
    elif mode == "EMERGENCY":
        popup_msg = "🚨 Earthquake detected! Emergency stop activated."

    return jsonify({
        "mode": mode,
        "popup": popup_msg
    })


# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":
    threading.Thread(target=simulation_loop, daemon=True).start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)