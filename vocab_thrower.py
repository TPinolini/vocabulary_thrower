import googletrans
from googletrans import Translator
from pprint import PrettyPrinter
from random import randint
from bs4 import BeautifulSoup
import requests
from plyer import notification
import time

printer = PrettyPrinter()
translator = Translator()

languages = googletrans.LANGUAGES

def get_random_word(file):
    if file == 0:
        with open("nouns.csv", "r") as file:
            words = file.readlines()
            random_word = words[randint(0, 200)].split(";")[1]
            return f"the {random_word}"
    elif file == 1:
        with open("verbs.csv", "r") as file:
            words = file.readlines()
            random_word = words[randint(0, 200)].split(";")[1]
            return f"to {random_word}"
    elif file == 2:
        with open("adjectives.csv", "r") as file:
            words = file.readlines()
            random_word = words[randint(0, 200)].split(";")[1]
            return random_word

def notifyMe(title, message):
    notification.notify(
        title = title,
        message = message,
        app_icon = "FlagsGermany.ico",
        timeout = 15, 
    )

if __name__ == '__main__':
    while True:
        word = get_random_word(randint(0,2))

        html_text = requests.get(f"https://sentencestack.com/q/{word}")
        soup = BeautifulSoup(html_text.text, "lxml")
        phrases = soup.find_all("div", class_="sent-txt")
        list_of_phrases = [i.text for i in phrases if len(i.text) < 70]
        shorten_list_of_phrases = list_of_phrases[:5]

        english_raw_translation = translator.translate(word)
        spanish_raw_translation = translator.translate(word, 'es')
        german_translation = translator.translate(word, 'de')
        phrase_german_translation = [translator.translate(phrase, dest='de').text for phrase in shorten_list_of_phrases]

        english_translation = english_raw_translation.text
        spanish_translation = spanish_raw_translation.text

        translations = f'''- English: {english_translation.capitalize()} \n- Spanish: {spanish_translation.capitalize()} '''

        notifyMe(german_translation.text.capitalize(), translations)
        time.sleep(15)

        print(f">>> {german_translation.text.capitalize()}")
        print(f"- English: {english_translation.capitalize()}")
        print(f"- Spanish: {spanish_translation.capitalize()}")

        for i in phrase_german_translation:
            print("- "+i)