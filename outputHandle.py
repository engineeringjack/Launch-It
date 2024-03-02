import mido
from verbose import printv

global outputController
outputController = None


def startUp(prefData, noteData, context):
    global outputController
    print("Looking for device...")
    outputController = connectOutput(prefData, context)
    context = False
    print("Now handling output requests.")
    return


def connectOutput(prefData, context):
    global outputController
    alreadySaid = False
    output_ports = mido.get_output_names()
    printv(output_ports, context[1])
    alreadySaid2 = False
    while True:
        while not output_ports:
            output_ports = mido.get_output_names()
            if output_ports and prefData["midi_output_port"] < 0 or prefData["midi_output_port"] >= len(output_ports) and alreadySaid == False:
                print("Device not found, we'll keep looking...")
                alreadySaid = True
        try:
            print("Found output: " +
                  output_ports[prefData["midi_output_port"]])
            return mido.open_output(output_ports[prefData["midi_output_port"]])
        except:
            if not alreadySaid2:
                print(
                    "Invalid index detected. Change output midi index in the configuration file.")
                alreadySaid2 = True


def mainHandler(prefData, outputData, context):
    global outputController
    printv("Sent output note: " +
           str(outputData[0]) + ", velocity: " + str(outputData[1]), context[1])
    outputController.send(mido.Message(
        'note_on', note=outputData[0], velocity=outputData[1]))
