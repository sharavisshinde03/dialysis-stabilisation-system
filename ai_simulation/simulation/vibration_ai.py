import random

"""
AI-based vibration simulation
Generates synthetic earthquake-like vibration patterns
"""

def generate_vibration(time_step):
    base_noise = random.uniform(0.02, 0.08)

    if 15 <= time_step <= 35:
        quake = random.uniform(0.4, 0.9)
    else:
        quake = 0.0

    return round(base_noise + quake, 3)
