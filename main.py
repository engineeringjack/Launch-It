from renderingEngine import clearLighting, suicideNote, setupLighting
import inputOperator
import outputHandle
import os
import os.path
import json
import traceback
import time


def main(context):
    try:
        print("Starting...")

        reference = os.path.dirname(os.path.abspath(__file__))
        prefData = prefDataLoader(reference)
        noteData = noteDataLoader(reference)
        outputHandle.startUp(prefData, noteData, context)
        inputOperator.startUp(prefData, noteData, context)
        clearLighting(prefData, noteData, context)
        setupLighting(prefData, noteData, context)
        print("Everything looks good!")
        time.sleep(1000)
    except KeyboardInterrupt:
        print("Closing all services, please hold.")
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
    clearLighting(prefData, noteData, context)
    context[0] = True
    inputOperator.startHandle(0, 0, 0, context)
    suicideNote()


if __name__ == "__main__":
    context = [False]
    main(context)
