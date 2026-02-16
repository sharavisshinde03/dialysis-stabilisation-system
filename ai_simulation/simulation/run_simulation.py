import time

from .dialysis_machine import DialysisMachine
from ..core.vibration_ai import generate_vibration
from ..core.stabilisation_logic import check_stabilisation



def run():
    machine = DialysisMachine()
    t = 0

    while True:
        vibration = generate_vibration(t)
        stabilise, threshold = check_stabilisation(vibration)

        if stabilise:
            machine.activate_stabilisation()

        machine.update()

        print(f"""
-----------------------------
Time: {t}s
Vibration: {vibration}
Threshold: {round(threshold, 3)}
Stabilisation Mode: {machine.stabilisation_mode}
Blood Flow: {machine.blood_flow}
Arterial Pressure: {machine.arterial_pressure}
Venous Pressure: {machine.venous_pressure}
Treatment Time: {machine.treatment_time}
-----------------------------
""")

        time.sleep(1)
        t += 1


if __name__ == "__main__":
    run()
