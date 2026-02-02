import time
from vibration_ai import generate_vibration
from stabilisation_logic import check_stabilisation
from dialysis_machine import DialysisMachine
from alerts import send_emergency_alert

machine = DialysisMachine()
t = 0
alert_sent = False

while True:
    vibration = generate_vibration(t)
    stabilise, threshold = check_stabilisation(vibration)

    if stabilise and not alert_sent:
        machine.activate_stabilisation()
        send_emergency_alert()
        alert_sent = True

    machine.update()

    print(f"""
Time: {t}s
Vibration: {vibration}
Threshold: {round(threshold,3)}
Stabilisation: {machine.stabilisation_mode}
Blood Flow: {machine.blood_flow}
Arterial Pressure: {machine.arterial_pressure}
Venous Pressure: {machine.venous_pressure}
Treatment Time: {machine.treatment_time}
""")

    time.sleep(1)
    t += 1
