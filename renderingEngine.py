import outputHandle
import threading
import time
import pygame
import os
import json
from verbose import printv

global recording, lightQueue, backgroundQueue, suicide, recordingState, recordingInfo
recording = False
lightQueue = []
backgroundQueue = []
suicide = False
recordingState = 0
recordingInfo = {}


def mainLighting(prefData, noteData, context, rawInput, directConnect=False):
    global recording, lightQueue, backgroundQueue, recordingState, recordingInfo
    if directConnect == True:
        outputHandle.mainHandler(prefData, rawInput, context)
        return
    try:
        noteIn = rawInput.note
    except:
        print(
            "[W] We just saved a performance. Don't press that again. (Message has no note data)")
        return
    veloIn = rawInput.velocity
    noteOut = -1
    veloOut = 0
    # Check if the pressed button has a dedicated function
    if veloIn == 0:
        if noteIn == prefData["RecordingID"]:
            if recording:
                clearLighting(prefData, noteData, context)
                print("Done programming.")
                veloOut = 0
                noteOut = noteIn
                recording = False
            else:
                veloOut = prefData["RecordingColor"]
                recordingState = 0
                noteOut = noteIn
                recording = True
    if not int(noteIn) % 10 == 9 and not recording:
        if veloIn == 0:
            try:
                if noteIn in lightQueue:
                    lightQueue.remove(noteIn)
                    noteOut = noteIn
                    veloOut = 0
                else:
                    if noteData["note"][str(noteIn)]["lightMode"] == "Flash":
                        noteOut = noteIn
                        if not noteIn in backgroundQueue:
                            veloOut = prefData["InQueueColor"]
                        newBackgroundTask(prefData, noteData, context, noteIn)
                    elif noteData["note"][str(noteIn)]["lightMode"] == "Solid":
                        lightQueue.append(noteIn)
                        noteOut = noteIn
                        veloOut = noteData["note"][str(noteIn)]["colorOnPress"]
                    elif noteData["note"][str(noteIn)]["lightMode"] == "None":
                        noteOut = noteIn
                        veloOut = 0
                    else:
                        print("Invalid lighting type!")
                audioBuffer(prefData, noteData, context, noteIn)
            except Exception as e:
                print(
                    "[W] Failed to get note data! Please record an option for this button.", noteIn)
    recTask = False
    if recording == True:
        noteOut = noteIn
    if veloIn == 0:
        if recordingState == 0 and recording and not recTask:
            recordingInfo = {}
            print("Select button for programming.")
            setAllColors(prefData, noteData, context, recordingState)
            recordingState += 1
            recTask = True
        if recordingState == 1 and recording and not recTask:
            print("Note Selected:", noteIn)
            recordingInfo["note"] = (str(noteIn))
            clearLighting(prefData, noteData, context)
            veloOut = 69
            recTask = True
            time.sleep(1)
            clearLighting(prefData, noteData, context)
            print("Select a on press color.")
            showColorOptions(prefData, noteData, context)
            recordingState += 1
        if recordingState == 2 and recording and not recTask:
            print("Selected color:", noteIn)
            recordingInfo["colorOnPress"] = (int(noteIn))
            clearLighting(prefData, noteData, context)
            print("Select release color.")
            showColorOptions(prefData, noteData, context)
            recTask = True
            recordingState += 1
        if recordingState == 3 and recording and not recTask:
            print("Selected color:", noteIn)
            recordingInfo["colorOnRelease"] = (int(noteIn))
            action = ""
            while not action in ["a", "l", "c"]:
                action = input("(a)ux mode, (l)ight mode or (c)ommand mode?")
                action.lower()
            if action == "a":
                recordingInfo["actionMode"] = ("Aux")
            if action == "l":
                recordingInfo["actionMode"] = ("Light")
            if action == "c":
                recordingInfo["actionMode"] = ("Command")
            action = ""
            while not action in ["f", "s"]:
                action = input("(f)lash mode or (s)olid mode?")
                action.lower()
            if action == "f":
                recordingInfo["lightMode"] = ("Flash")
            if action == "s":
                recordingInfo["lightMode"] = ("Solid")
            print("Make sure to place your mp3 file in the AuxData folder, then type in the name of the file here WITH the file extension!")
            action = input("File is named: ")
            recordingInfo["fileLocation"] = (action)
            print("All others will be set to the default value.")
            recordingInfo["command"] = ("")
            recordingInfo["flashingDelay"] = (0.5)
            recordingInfo["layering"] = (False)
            recordingInfo["volume"] = (1.0)
            recordingInfo["length"] = (0)
            recordingInfo["fadeIn"] = (100)
            recordingInfo["fadeOut"] = (100)
            recordingInfo["startAt"] = (0)
            noteData["note"][str(recordingInfo["note"])] = recordingInfo
            noteDataUploader(noteData)
            clearLighting(prefData, noteData, context)
            recordingState = 0
            setAllColors(prefData, noteData, context, recordingState)
            print("Next!")
    # Send Changes

    if not noteOut == -1:
        outputHandle.mainHandler(prefData, [noteOut, veloOut], context)
    else:
        if veloIn != 0 and not int(noteIn) % 10 == 9:
            outputHandle.mainHandler(
                prefData, [noteIn, prefData["NoActionColor"]], context)
        elif not int(noteIn) % 10 == 9:
            outputHandle.mainHandler(
                prefData, [noteIn, 0], context)


def clearLighting(prefData, noteData, context):
    printv("Clearing lighting.", context[1])
    for x in range(127):
        mainLighting(prefData, noteData, context, [x, 0], True)


def setupLighting(prefData, noteData, context):
    printv("Setting up lighting.", context[1])
    for x in range(127):
        try:
            mainLighting(prefData, noteData, context, [
                x, noteData["note"][str(x)]["colorOnRelease"]], True)
        except:
            mainLighting(prefData, noteData, context, [
                x, 0], True)


def newBackgroundTask(prefData, noteData, context, note):
    global backgroundQueue
    if note in backgroundQueue:
        printv("Removing rendering background task for: " +
               str(note), context[1])
        backgroundQueue.remove(note)
    else:
        backgroundQueue.append(note)
        printv("New rendering background task on: " + str(note), context[1])
        thread = threading.Thread(target=backgroundTask, args=(
            prefData, noteData, context, note,))
        thread.start()


def suicideNote():
    global suicide
    suicide = True


def backgroundTask(prefData, noteData, context, note):
    global backgroundQueue, suicide
    clippy = True
    if noteData["note"][str(note)]["lightMode"] == "Flash":
        masterDelay = noteData["note"][str(note)]["flashingDelay"]
        steppingDelay = masterDelay * 10
        while note in backgroundQueue:
            for x in range(int(steppingDelay)):
                time.sleep(0.1)
                if not note in backgroundQueue or suicide:
                    try:
                        mainLighting(prefData, noteData, context, [
                            note, noteData["note"][str(note)]["colorOnRelease"]], True)
                    except:
                        mainLighting(prefData, noteData, context, [
                            note, 0], True)
                    return
            clippy = not clippy

            if clippy:
                mainLighting(prefData, noteData, context, [
                             note, noteData["note"][str(note)]["colorOnPress"]], True)
            else:
                mainLighting(prefData, noteData, context, [
                             note, noteData["note"][str(note)]["colorOnRelease"]], True)
        try:
            mainLighting(prefData, noteData, context, [
                note, noteData["note"][str(note)]["colorOnRelease"]], True)
        except:
            mainLighting(prefData, noteData, context, [
                note, 0], True)
        return


def audioBuffer(prefData, noteData, context, note):
    global backgroundQueue
    thread = threading.Thread(target=audioTask, args=(
        prefData, noteData, context, note,))
    printv("New audio background task for: " + str(note), context[1])
    thread.start()


def audioTask(prefData, noteData, context, note):
    global backgroundQueue, suicide
    pygame.mixer.init()
    pathToFile = (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'AuxData',
                               noteData["note"][str(note)]["fileLocation"]))
    while note in backgroundQueue and not suicide:
        if noteData["note"][str(note)]["actionMode"] == "Aux" and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(pathToFile)
            pygame.mixer.music.set_volume(
                noteData["note"][str(note)]["volume"])
            pygame.mixer.music.play(
                fade_ms=noteData["note"][str(note)]["fadeOut"])
            pygame.mixer.music.set_pos(
                noteData["note"][str(note)]["startAt"])

            while (pygame.mixer.music.get_busy()):
                time.sleep(0.1)
                if not note in backgroundQueue or suicide:
                    pygame.mixer.music.fadeout(
                        noteData["note"][str(note)]["fadeOut"])
                    return
            backgroundQueue.remove(note)
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            return


def setAllColors(prefData, noteData, context, recordingState):
    printv("Setting all color data.", context[1])
    for x in range(127):
        if not x % 10 == 9:
            mainLighting(prefData, noteData, context, [
                x, prefData["RecordingColor"]], True)


def showColorOptions(prefData, noteData, context):
    for x in range(127):
        if not x % 10 == 9:
            mainLighting(prefData, noteData, context, [
                x, x], True)


def reloadNoteData():
    reference = os.path.dirname(os.path.abspath(__file__))
    preferences_file = os.path.join(reference, 'data', 'noteData.json')

    with open(preferences_file, 'r') as file:
        preferences = json.load(file)

    return preferences


def noteDataUploader(newData):
    reference = os.path.dirname(os.path.abspath(__file__))
    preferences_file = os.path.join(reference, 'data', 'noteData.json')

    with open(preferences_file, 'w') as file:
        json.dump(newData, file, indent=4)
    return
