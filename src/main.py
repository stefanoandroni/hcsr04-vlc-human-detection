
from hcsr04 import HCSR04
from media_player import MediaPlayer

import time
from collections import deque


# - - - - - - - - - - - - - - - - - CONFIG - - - - - - - - - - - - - - - -

# VIDEO
VIDEO_PATH = "..."
VIDEO_FULL_SCREEN = True

# SENSOR (HC-SR04)
TRIGGER_PIN = 23
ECHO_PIN = 24
SENSOR_THRESHOLD = 4 # (cm) sensor error threshold
FLOOR_MEASUREMENTS = 10 # number of measurements to calculate the distance from the floor

# STATE STABILITY (consistency)
# If at least a certain percentage (STABILITY_THRESHOLD) of values are of 
# the same type among the last n (STABILITY_WINDOW_SIZE) values received
STABILITY_THRESHOLD = 80 # (%)
STABILITY_WINDOW_SIZE = 20

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def main():
    # state ∈ {False, True}, True iff human detected
    
    player = MediaPlayer(VIDEO_PATH, VIDEO_FULL_SCREEN)
    sensor = HCSR04(TRIGGER_PIN, ECHO_PIN, FLOOR_MEASUREMENTS)
    
    # PLAYER   
    player.start()
    time.sleep(1)
    player.pause() # initial state is False
    
    # SENSOR
    floor_distance = sensor.measure_floor_distance()
    print(f'> floor distance: {floor_distance}')
    
    current_state = False
    # Initialize last_states to a deque of False values, representing a history of STABILITY_WINDOW_SIZE detections
    last_states = deque([False] * STABILITY_WINDOW_SIZE, maxlen=STABILITY_WINDOW_SIZE)

    while True:
        # Measure a new distance
        new_distance = sensor.measure_distance()
        # Check for human presence
        new_state = check_human_presence(new_distance, floor_distance)
        # Update the deque (window) with the new state
        last_states.append(new_state)

        # Get next state (stable state)
        next_state = get_stable_state(last_states, current_state)

        # 'human not detected' --> 'human detected'
        if current_state == False and next_state == True:
            # Resume video
            player.resume()
            current_state = next_state
        # 'human detected' --> 'human not detected'
        elif current_state == True and next_state == False:
            # Pause video
            player.pause()
            current_state = next_state

        # Video loop
        if player.is_video_ended():
            player.start()
       

def check_human_presence(new_distance, floor_distance):
    return new_distance < floor_distance - SENSOR_THRESHOLD


def get_stable_state(last_states, current_state):
    # Calculate the number of True states in the window 
    true_states_num = sum(1 for state in last_states if state is True)
    # Calculate the percentage of True states in the window
    true_states_percentage = true_states_num / STABILITY_WINDOW_SIZE * 100

    # Change state iif the new state is stable
    if true_states_percentage >= STABILITY_THRESHOLD:
        # 'True' state is stable
        return True
    elif true_states_percentage <= 100 - STABILITY_THRESHOLD:
        # 'False' state is stable
        return False
    else:
        # No new stable state, maintain the current state
        return current_state
    

if __name__ == '__main__':
    main()
        
