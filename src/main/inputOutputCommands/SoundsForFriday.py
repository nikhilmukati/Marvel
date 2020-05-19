import ctypes
import os
import random
import webbrowser

import boto3
import export as export
from google import google
from playsound import playsound
import pyttsx3

from src.main.inputOutputCommands.InOutCmd import *
from src.main.SearchDirectory.lookupDriveChange import lookup_dict
from src.main.fb import facebook
from src.main.SearchDirectory.run_lookup import RunLookup
AWS_DEFAULT_REGION = 'us-west-2'
os.environ['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION

greeting_dict = {'hello': 'hello', 'hi': 'hi'}
open_launch_dict = {'open': 'open', 'launch': 'launch'}
google_searches_dict = {'what': 'what', 'why': 'why', 'who': 'who', 'which': 'which'}
social_media_dict = {'facebook': 'https://www.facebook.com', 'twitter': 'https://www.twitter.com'}
social_post = {'post': 'post'}

mp3_thanktou_list = ['C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/thankyou_1.mp3', 'C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/thankyou_2.mp3']
mp3_listening_problem_list = ['C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/listening_problem_1.mp3', 'C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/listening_problem_2.mp3']
mp3_struggling_list = ['C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/struggling_1.mp3']
mp3_google_search = ['C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/google_search_1.mp3', 'C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/google_search_2.mp3']
mp3_greeting_list = ['C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/greeting_accept.mp3', 'C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/greeting_accept_2.mp3']
mp3_open_launch_list = ['C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/open_1.mp3', 'C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/open_3.mp3', 'C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/open_2.mp3']

# RunLookup()

python_scripts = {'greeting': 'scripts/test.py'}

error_occurrence = 0
counter = 0

polly = boto3.client('polly')


def to_be_posted(voice_note):
    for key in social_media_dict.keys():
        if key in voice_note:
            return key


def get_index(text):
    if 'first' in text:
        return 0
    elif 'second' in text:
        return 1
    elif 'third' in text:
        return 2
    else:
        return None


def google_search_result(query):
    search_result = google.search(query)

    for result in search_result:
        print(result.description.replace('...', '').rsplit('.', 3)[0])
        if result.description != '':
            play_sound_from_polly(result.description.replace('...', '').rsplit('.', 3)[0], is_google=True)
            break


def play_sound_from_polly(result, is_google=False):
    global counter
    mp3_name = "output{}.mp3".format(counter)

    obj = polly.synthesize_speech(Text=result, OutputFormat='mp3', VoiceId='Joanna')
    if is_google:
        play_sound(mp3_google_search)

    with open(mp3_name, 'wb') as file:
        file.write(obj['AudioStream'].read())
        file.close()

    playsound(mp3_name)
    os.remove(mp3_name)
    counter += 1


def run_python_script(voice_note):
    script_name = voice_note.split(' ')[2]
    for key, value in python_scripts.items():
        if key == script_name:
            os.system('python {}'.format(value))


def is_valid_google_search(phrase):
    if google_searches_dict.get(phrase.split(' ')[0]) == phrase.split(' ')[0]:
        return True


def is_valid_note(greet_dict, voice_notes):
    for key, value in greet_dict.items():
        # 'Hello Friday'
        try:
            if value == voice_notes.split(' ')[0]:
                return True

            elif key == voice_notes.split(' ')[1]:
                return True

        except IndexError:
            pass

    return False


def play_sound(mp3_list):
    mp3 = random.choice(mp3_list)
    playsound(mp3)
    

if __name__ == '__main__':

    playsound('C:\\Users\\nikhi\PycharmProjects\Marvel\mp3\\friday\greeting.mp3')

    while True:

        voice_note = read_text_cmd().lower()
        print('cmd : {}'.format(voice_note))

        if is_valid_note(greeting_dict, voice_note):
            print('In greeting...')
            play_sound(mp3_greeting_list)
            continue
        elif is_valid_note(open_launch_dict, voice_note):
            print('In open...')
            play_sound(mp3_open_launch_list)
            if is_valid_note(social_media_dict, voice_note):
                # Launch Facebook
                key = voice_note.split(' ')[1]
                webbrowser.open(social_media_dict.get(key))
            else:
                key = voice_note.replace('open ', '').replace('launch ', '')
                print('Key is : ' + key)
                # print(list(lookup_drive_change.lookup_dict.keys()))

                opt_dict = {}
                for k in list(lookup_dict.keys()):
                    if key in k.lower():
                        opt_dict.update({k: lookup_dict.get(k)})

                print(opt_dict)
                if len(opt_dict) == 1:
                    for key in opt_dict.keys():
                        print('explorer {}'.format(opt_dict.get(key)))
                        os.system('explorer {}'.format(opt_dict.get(key)))
                elif len(opt_dict) > 1:
                    play_sound_from_polly('I have found multiple instances. Which one you want?', is_google=False)
                    default = 0
                    index = None
                    for i, k in enumerate(opt_dict.keys()):
                        print(k.split('.')[0].split('_')[0] + ' from {} folder'.format(opt_dict.get(k).split('\\')[-2]))
                        play_sound_from_polly(
                            k.split('.')[0].split('_')[0] + ' from {} folder '.format(opt_dict.get(k).split('\\')[-2]),
                            is_google=False)

                        default = i

                    text = read_text_cmd().lower()
                    print(text)
                    index = get_index(text)

                    if index != None:
                        print('explorer {}"'.format(
                            lookup_dict.get(list(opt_dict.keys())[index])) + ' ' + str(index))
                        play_sound_from_polly('Ok Sir', False)
                        os.system(
                            'explorer {}"'.format(lookup_dict.get(list(opt_dict.keys())[index])))

            continue
        elif is_valid_google_search(voice_note):
            print('in google search...')
            playsound('C:\\Users\\nikhi\PycharmProjects\Marvel\mp3/friday/search_1.mp3')
            # webbrowser.open('https://www.google.co.in/search?q={}'.format(voice_note))
            google_search_result(voice_note)
            continue
        elif 'post' in voice_note:
            media = to_be_posted(voice_note)
            play_sound_from_polly('Sure sir')
            if media == 'facebook':
                facebook().post_on_wall(voice_note.split(media + ' ')[1].capitalize())
                play_sound_from_polly('Posted sir')
            continue
        elif 'lock' in voice_note:
            play_sound_from_polly('Sure sir')
            for value in ['pc', 'system', 'windows']:
                ctypes.windll.user32.LockWorkStation()
            play_sound_from_polly('Your system is locked.')
        elif 'thank you' in voice_note:

            play_sound(mp3_thanktou_list)
            continue
        elif 'run python script' in voice_note:

            run_python_script(voice_note)
            continue
        elif 'goodbye' in voice_note:
            playsound('C:\\Users\\nikhi\PycharmProjects\Marvel\mp3\\friday\\bye.mp3')
            continue
        else:
            if voice_note != '':
                play_sound_from_polly('command not found.')
                play_sound_from_polly('sorry sir, i did not get you please repeat')
                continue


