import mido

global outputController
outputController = None


def startUp(prefData, noteData, context):
    global outputController
    print("Looking for device...")
    outputController = connectOutput(prefData)
    context = False
    print("Now handling output requests.")
    return


def connectOutput(prefData):
    global outputController
    alreadySaid = False
    output_ports = mido.get_output_names()
    while not output_ports:
        output_ports = mido.get_output_names()
        if output_ports and prefData["midi_output_port"] < 0 or prefData["midi_output_port"] >= len(output_ports) and alreadySaid == False:
            print("Invalid port index, we'll keep looking.")
            alreadySaid = True
    print("Found output: " + output_ports[prefData["midi_output_port"]])
    return mido.open_output(output_ports[prefData["midi_output_port"]])


def mainHandler(prefData, outputData, context):
    global outputController
    outputController.send(mido.Message(
        'note_on', note=outputData[0], velocity=outputData[1]))
