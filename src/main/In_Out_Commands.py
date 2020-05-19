import pyttsx3
from src.FridayToPlaySounds import read_voice_cmd_error
import speech_recognition as sr

speech = sr.Recognizer()

try:
    engine = pyttsx3.init()
except ImportError:
    print("Requested Driver not Available")
except RuntimeError:
    print("Requested Driver not Installed")


voices = engine.getProperty('voices')

engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
rate = engine.getProperty('rate')

engine.setProperty('rate', rate)


class InOutCommands:
    def speak_text_cmd(self, cmd):
        engine.say(cmd)
        engine.runAndWait()

    def read_text_cmd(self):
        voice_text = ''
        print('Listening...')
        with sr.Microphone() as source:
            #audio = speech.record(source, duration=3)
            audio = speech.listen(source=source, timeout=10, phrase_time_limit=5)
        try:
            voice_text = speech.recognize_google(audio)
        except sr.UnknownValueError as e:
            read_voice_cmd_error()
            pass
        except sr.RequestError as e:
            read_voice_cmd_error()
            print('Network error')
        return voice_text
