# VoiceControl
Voice control for Geoscan Pioneer is a pet-project for controlling Geoscan Pioneer UAVs using voice commands.
This project uses the [speech_recognition](https://github.com/Uberi/speech_recognition) library for speech recognition and Geoscan [pioneer_sdk](https://github.com/geoscan/pioneer_sdk)

## Requirements

To use this project, you should have:

* **Python** 3.8+
* **pioneer_sdk**  0.5.2+
* **speech_recognition** 3.10.0+
* **PyAudio** 0.2.11+

with their requirements.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required libraries.

```bash
pip install pioneer_sdk
pip install SpeechRecognition
pip install pyaudio
```

## How to use

You must have an internet connection and a connection to the pioneer via Wi-Fi. For example, you can use 2 wi-fi modules or a wi-fi module and a wired connection.

After launch, you will see a window with a picture from the drone's camera.

You can press the **space bar** and say a command within 2 seconds.
After recognizing it, the drone will take the necessary actions. All actions are logged to the console
Press **Esc** to end work.
