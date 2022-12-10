
'''Importing the necessary libraries for speech recognition and text to speech'''

'''Speech recognition is used for converting user speech into text data and processing it'''
import speech_recognition as sr

'''Pyttsx3 converts text data into speech'''
import pyttsx3

'''Sys is used for accessing system properties such as changing the voice of text to speech'''
import sys

'''Initialize the recognizer'''
r = sr.Recognizer()

''' Function to convert text to speech '''
def SpeakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    
    engine.setProperty(
        "voice",
        "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0",
    )
    engine.say(command)
    engine.runAndWait()


'''This function initializes user audio input device and prompts the user to speak, 
it then uses google speech recognition API to determine which words were spoken'''
def getMove():

    # Exception handling to handle
    # exceptions at the runtime
    try:

        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
            SpeakText("Speak now")

            # listens for the user's input
            audio2 = r.record(source2, duration=5)
            print("Speech recorded")

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            print("Speech recognized...")

            MyText = MyText.lower()

            
            return MyText

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")
        sys.exit(0)
