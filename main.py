from renderingEngine import clearLighting, suicideNote, setupLighting
from verbose import printv
import inputOperator
import outputHandle
import os
import os.path
import json
import traceback
import time
import platform

verbose = False


def main(context):
    try:
        print("Welcome to LaunchIt!")
        printv("Verbose Enabled!", context[1])
        print("Starting...")
        print("Using OS data for... " + platform.system() + "!")
        print("Running script version: Early Release!")
        print("Script files look okay. Errors will be logged when required.")
        reference = os.path.dirname(os.path.abspath(__file__))
        prefData = prefDataLoader(reference)
        noteData = noteDataLoader(reference)
        inputOperator.startUp(prefData, noteData, context)
        outputHandle.startUp(prefData, noteData, context)
        clearLighting(prefData, noteData, context)
        setupLighting(prefData, noteData, context)
        print("Everything looks good!")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing all services by user request, please hold.")
    except Exception as e:
        print("Critical error occurred. Graceful shutdown initiated. See below:")
        print(traceback.format_exc())
    finally:
        close(prefData, noteData, context)
        print("Showdown finished.")
        quit()


def prefDataLoader(reference):
    preferences_file = os.path.join(reference, 'pref.json')

    with open(preferences_file, 'r') as file:
        preferences = json.load(file)

    return preferences


def noteDataLoader(reference):
    preferences_file = os.path.join(reference, 'data', 'noteData.json')

    with open(preferences_file, 'r') as file:
        preferences = json.load(file)

    return preferences


def close(prefData, noteData, context):
    try:
        clearLighting(prefData, noteData, context)
    except:
        print("Failed to reset board! Artifacts may appear on reconnect.")
    context[0] = True
    inputOperator.startHandle(0, 0, 0, context)
    suicideNote()


if __name__ == "__main__":
    context = [False, verbose]
    main(context)
