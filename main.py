from pioneer_sdk import Pioneer, Camera
import speech_recognition as sr
from enum import Enum, auto
import pyaudio
import os
import wave
import cv2
import numpy as np
import time


# класс команд для коптера
class State(Enum):
    nothing = auto()
    arm = auto()
    disarm = auto()
    takeoff = auto()
    land = auto()
    forward = auto()
    backward = auto()
    left = auto()
    right = auto()
    up = auto()
    down = auto()
    ledWhite = auto()
    ledRed = auto()
    ledBlue = auto()
    ledGreen = auto()
    ledBlack = auto()


# параметры записи звука
chunk_size = 1024  # определяет форму аудио сигнала
sample_format = pyaudio.paInt16  # шестнадцатибитный формат задает значение амплитуды
channel = 1  # канал записи звука
rate = 44100  # частота дискретизации
rec_time = 2  # длина записи
output_name = "output.wav"  # имя файла для записи

# команды коптера
commands = {"заведи": State.arm,
            "заглуши": State.disarm,
            "взлёт": State.takeoff,
            "посадка": State.land,
            "вперёд": State.forward,
            "назад": State.backward,
            "влево": State.left,
            "вправо": State.right,
            "вверх": State.up,
            "вниз": State.down,
            "белый": State.ledWhite,
            "красный": State.ledRed,
            "синий": State.ledBlue,
            "зелёный": State.ledGreen,
            "чёрный": State.ledBlack}

p = pyaudio.PyAudio()


def listen():
    stream = p.open(format=sample_format, channels=channel, rate=rate, input=True,
                    frames_per_buffer=chunk_size)  # открываем поток для записи
    print("rec start")
    frames = []  # формируем выборку данных фреймов
    for i in range(0, int(rate / chunk_size * rec_time)):
        data = stream.read(chunk_size)
        frames.append(data)
    print("done")
    stream.stop_stream()  # останавливаем и закрываем поток
    stream.close()
    save(frames)


# запись записанного аудио в файл
def save(frames):
    print("saving")
    with wave.open(output_name, 'wb') as wave_file:
        wave_file.setnchannels(channel)
        wave_file.setsampwidth(p.get_sample_size(sample_format))
        wave_file.setframerate(rate)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
    print("done")


def recognize():
    try:
        sample = sr.WavFile(os.getcwd() + '\\' + output_name)
        recognizer = sr.Recognizer()
        with sample as audio:
            content = recognizer.record(audio)
            recognizer.adjust_for_ambient_noise(audio)
            return recognizer.recognize_google(content, language="ru-RU")
    except:
        print("recognition failed")
        return ""


if __name__ == "__main__":

    pioneer_mini = Pioneer()

    camera = Camera()
    command_x = float(0)
    command_y = float(0)
    command_z = float(0)
    command_yaw = float(0)
    try:
        while True:
            frame = camera.get_frame()
            if frame is not None:
                camera_frame = cv2.imdecode(
                    np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR
                )
                cv2.imshow("pioneer_camera_stream", camera_frame)
            key = cv2.waitKey(1)
            command = ""
            if key == 27:  # esc
                print("esc pressed")
                cv2.destroyAllWindows()
                pioneer_mini.land()
                break
            elif key == 32:  # space
                listen()
                command = recognize()
                print(command)

            state = State.nothing

            if command != "":
                if command in commands.keys():
                    state = commands.get(command)

            if state is State.arm:
                pioneer_mini.arm()

            elif state is State.disarm:
                pioneer_mini.disarm()

            elif state is State.takeoff:
                pioneer_mini.takeoff()

            elif state is State.land:
                pioneer_mini.land()

            elif state is State.forward:
                command_y = 0.5

            elif state is State.backward:
                command_y = -0.5

            elif state is State.left:
                command_x = -0.5

            elif state is State.right:
                command_x = 0.5

            elif state is State.up:
                command_z = 0.5

            elif state is State.down:
                command_z = -0.5

            elif state is State.ledWhite:
                pioneer_mini.led_control(r=255, g=255, b=255)

            elif state is State.ledRed:
                pioneer_mini.led_control(r=255, g=0, b=0)

            elif state is State.ledGreen:
                pioneer_mini.led_control(r=0, g=255, b=0)

            elif state is State.ledBlue:
                pioneer_mini.led_control(r=0, g=0, b=255)

            elif state is State.ledBlack:
                pioneer_mini.led_control(r=0, g=0, b=0)

            if command_x != 0 or command_y != 0 or command_z != 0:
                print('sending local point X: {x}, Y: {y}, Z: {z}, YAW: {yaw}'.format(x=command_x, y=command_y,
                                                                                      z=command_z, yaw=command_yaw))
                pioneer_mini.go_to_local_point_body_fixed(x=command_x, y=command_y, z=command_z, yaw=command_yaw)
            command_x = 0
            command_y = 0
            command_z = 0
            time.sleep(0.02)
    finally:
        time.sleep(1)
        pioneer_mini.land()

        pioneer_mini.close_connection()
        del pioneer_mini
