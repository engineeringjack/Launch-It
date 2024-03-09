# Automated Sound Queue System
**Launchpad MK2 Custom Sound Queue Software**

This software interacts with the Launchpad MK2 to read and write custom sound queues for theater productions or other live performances.

#### Notice
I do not own any songs contained within or in the history of commits of this project and are for placeholder use only, play and use songs you have permission for cafuly. Some song data is incorrect and/or is remixed by other students for production use only.

## Intentions
This software was originally designed for ALIHS' Theater Department, part of the 2024 production of William Shakespeare's play A Midsummer Night's Dream, but designed to be modular for any future productions as well.

## Advantages
* Human-readable JSON file
* Easy to add new songs and sounds on the fly (read below)
* Multithread and won't ruin a production in the event of an error
* Super customizable for fade in/out, start times, and much more
* Open source and free

### Features
* Automatic fading into and out of a song or sound
* Songs can start at a pre-specified position
* Multi-os compatible
* Completely local, no internet use after installing dependencies
* Safe error handling

## Set Up
1. Install all dependencies and project files. (Suggested to use pip and python 3.11)
2. Change the pref.json data to match the midi ports of the MK2. (I found commonly input 0, output 1 for macOS and 1, 1 repectivly for Windows)
3. Run main.py

## Adding / Editing / Removing Queue Data
### Adding a queue
1. Press "Recording Arm" (Buttons will go red to indicate the change)
2. Press the button to add
3. Press the resting color, followed by the flash color
4. Enter in the command line the operation modes for the queue
5. Press the Recording Arm to exit and push changes to the noteData.json file
6. Restart the program to update noteData variables

> [!WARNING]
> After recording, editing, or removing a queue, you need to restart the program to update changes.

### Editing a queue
Some changes are only available through the JSON file, see the instructions below on what each setting means.
Note that if you use the "Adding a queue" instructions the data will be overwritten.

1. Open the noteData.json file
2. Find the queue to edit (The two-digit note number is the row and column, but you can also look for the filename)
3. Edit the data
4. Save, exit, and restart the program to save changes.


> [!WARNING]
> After recording, editing, or removing a queue, you need to restart the program to update changes.

### What each option means
* **note** Leave this number alone, this is how the program internally manages the note information.
* **colorOnPress** This is the value of the color (in velocity) that the note will have when it is active.
* **colorOnRelease** The color (in velocity) the button will have when not in use.
* **actionMode** Snd is for sounds, Aux for audio, Command, and Sound are allowed. Command and Sound are not set up therefor do nothing and are untested. See below the differences between sound and audio.
* **lightMode** Flash and Solid, how the lighting of the button should behave when it is active.
* **fileLocation** The name of the file that should be played (Use an MP3 file with a correct header, otherwise it might not play - untested with other filetypes)
* **command** Placeholder for future use and isn't programmed.
* **flashingDelay** In flashing mode, this is the time between the colors back and forth.
* **layering** If the sound is permitted to play over itself
* **volume** volume that the sound should be played out (0.0-1.0 double value)
* **length** Placeholder for future use and isn't programmed.
* **fadeIn** How long (in microseconds) should it take to reach full volume.
* **fadeOut** How long (in microseconds) should it take to completely fade out of the audio.
* **startAt** Where should the audio start from. (double in seconds)

> [!Note]
> Snd and Aux are diffrent. Aux is used for songs, only one aux can play at a time but allows for the startAt value to be used. However, sounds (Snd) can play at the same time as each other and a the same time as a Aux is being played but must start from the beginning of the file. Sounds are loaded completely before starting the sound while Aux is streamed from the file (allowing for longer files).
