import time

# Dynamic vibration threshold (moving average)
threshold = 0.35
start_time = None


def check_stabilisation(vibration):
    """
    Returns:
        (bool, float)
        stabilisation_required, updated_threshold
    """
    global threshold, start_time

    # Exponential smoothing for adaptive threshold
    threshold = 0.7 * threshold + 0.3 * vibration

    # Check if vibration stays above limit for 5 seconds
    if vibration >= 0.35:
        if start_time is None:
            start_time = time.time()
        elif time.time() - start_time >= 5:
            return True, threshold
    else:
        start_time = None

    return False, threshold


def get_system_mode(vibration):
    """
    Returns system mode based on vibration intensity.
    """
    if vibration >= 0.55:
        return "EMERGENCY"

    if vibration >= 0.35:
        return "STABILISATION"

    return "NORMAL"
