import os
import pyttsx3
import speech_recognition as sr
from src.main.inputOutputCommands.InOutCmd import *


if __name__ == '__main__':

    speak_text_cmd('Hello Sir, i am Friday Your personal assistant')

    while True:
        voice_note = read_text_cmd()
        print('cmd: {}'.format(voice_note))

        if 'hello' in voice_note:
            speak_text_cmd('Hello Sir, How may i help you')
            continue
        elif 'open' in voice_note:
            #webbrowser.open('file:///C:/'.format(voice_note.replace('open ', '')))
            os.system('explorer C:\\{}'.format(voice_note.replace('open ', '')))
            speak_text_cmd('Please Wait i am Opening '+voice_note.replace('open', '')+'')
            continue
        elif 'bye' in voice_note:
            speak_text_cmd('Bye Sir, Glad to Help you, Come again, good day')
            exit()


