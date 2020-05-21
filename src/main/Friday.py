import os
from src.main.GreetingCmd import welcomeGreetingDict, afterGreetingDict
from src.main.InOutCmd import *


if __name__ == '__main__':

    speak_text_cmd('Hello Sir, i am Friday Your personal assistant')

    while True:
        voice_note = read_text_cmd().lower().replace(' ', '_')

        if get_key(voice_note, welcomeGreetingDict) in welcomeGreetingDict.keys():
            speak_text_cmd(welcomeGreetingDict.get(get_key(voice_note, welcomeGreetingDict)).format('How may i help you'))
            continue

        elif 'open' in voice_note:
            #webbrowser.open('file:///C:/'.format(voice_note.replace('open ', '')))
            os.system('explorer C:\\{}'.format(voice_note.replace('open', '')))
            speak_text_cmd('Please Wait i am Opening '+voice_note.replace('open', '')+'')
            continue

        elif get_key(voice_note, afterGreetingDict) in afterGreetingDict.keys():
            speak_text_cmd(afterGreetingDict.get(get_key(voice_note, afterGreetingDict))+' Glad to Help you, good day')
            exit()


