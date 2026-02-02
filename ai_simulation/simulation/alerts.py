from datetime import datetime

def send_emergency_alert():
    print("\n📧 EMERGENCY ALERT SENT")
    print("Recipients: Doctor | Admin | Reception")
    print("Subject: Dialysis Stabilisation Activated")
    print(f"Time: {datetime.now()}\n")
