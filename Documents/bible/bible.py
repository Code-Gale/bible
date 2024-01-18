import speech_recognition as sr
import re
import requests

# Replace 'YOUR_API_KEY' with your actual API key from scripture.api.bible
API_KEY = '12d76c17ec9c361465226c6bea5153a6'

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        sentence = recognizer.recognize_google(audio)
        return sentence.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def extract_bible_passage(sentence):
    # Regular expression to find Bible passages like "John 3:16" or "Genesis 1:1"
    pattern = re.compile(r'(\b\w+\s?\d+:\d+\b)')
    matches = re.findall(pattern, sentence)

    if matches:
        return matches
    else:
        return None

def get_bible_passage(passage_reference):
    api_url = f'https://api.scripture.api.bible/v1/bibles/nasb/passages/{passage_reference}?include-notes=false'
    headers = {'api-key': API_KEY}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['data']['content']
    else:
        return f"Failed to retrieve Bible passage for {passage_reference}."

def display_bible_passages(passages):
    if passages:
        print("Found Bible passages in the sentence:")
        for passage in passages:
            text = get_bible_passage(passage)
            print(f"{passage}: {text}")
    else:
        print("No Bible passages found in the sentence.")

def main():
    while True:
        sentence = recognize_speech()

        if sentence:
            passages = extract_bible_passage(sentence)
            display_bible_passages(passages)

if __name__ == "__main__":
    main()
