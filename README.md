# HCSR04-VLC

This repository contains a Python project (for Raspberry) that uses an HCSR04 sensor to **detect the presence of a person** in front of a fixed background (e.g. wall or floor) and dynamically **plays or pauses a video accordingly**.

## Project Structure

```
/media					video folder
/src
	/main.py			main code
	/hcsr04.py			hcsr04 sensor class (HCSR04)
	/media_player.py		media player class (MediaPlayer)
requirements.txt			dependencies
```


## Hardware
The project is implemented on a Raspberry Pi 5 8GB, accompanied by an HCSR04 sensor for distance detection. For a detailed schematic diagram illustrating the connection between the Raspberry Pi and the HCSR04 sensor, please refer to the [GPIO Zero documentation](https://gpiozero.readthedocs.io/en/stable/recipes.html#distance-sensor).

### My Setup
No external resistors were used in my setup. The sensor was successfully powered at 3.3V, and it exhibited precise functionality comparable to its performance when powered by 5V.

| Sensor | Pin |
|--------|-----|
| GND |  GND |
| VCC | 3V3 |
| TRIG | GPIO23 (16) |
| ECHO | GPIO24 (18) |


## Video
For optimal performance on Raspberry Pi 5, using the **H.265 (HEVC)** codec for MP4 video files significantly improves playback efficiency and overall video processing (because Raspberry Pi 5 has a 4Kp60 HEVC decoder).


## Implementation Notes

### State Stability (Consistency)
Due to potential sensor errors, the program transitions between states (from `human_detected` to `human_not_detected` or vice versa) only when the new state is stable.

A state is stable iff at least a certain percentage (STABILITY_THRESHOLD) of states are of  the same type among the last n (STABILITY_WINDOW_SIZE) states received.


## Dependencies
- **HCSR04**: gpiozero
- **MediaPlayer**: python-vlc


## TODO
- gpiozero optimization
- handle exceptions
- video KeyboardInterrupt
