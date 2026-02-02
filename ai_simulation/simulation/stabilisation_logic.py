import time

threshold = 0.3
start_time = None

def check_stabilisation(vibration):
    global threshold, start_time

    threshold = 0.7 * threshold + 0.3 * vibration

    if vibration > threshold:
        if start_time is None:
            start_time = time.time()
        elif time.time() - start_time >= 5:
            return True, threshold
    else:
        start_time = None

    return False, threshold
