import json
import sys
import os

from PyQt5 import QtWidgets

VERSION = "0.0.1"

def convertStrokesToVibration():
    file_name = QtWidgets.QFileDialog.getOpenFileName(
            None,
            caption="Select Stroking Funscript"
    )
    if len(file_name) < 1:
        return "ERROR: No funscript was selected"

    if not os.path.exists(file_name[0]):
        return "ERROR: No funscript was selected"

    if not file_name[0].lower().endswith('.funscript'):
        return "ERROR: Selected file is not a funscript file"

    stroking_funscript_file = file_name[0]

    with open(stroking_funscript_file, "r") as stroking_funscript:
        stroking = json.load(stroking_funscript)

    vibration = {
            k: v for k, v in stroking.items()
            if k != "action"
    }

    if len(stroking['actions']) < 2:
        return "ERROR Funscript do not contain any action"

    projection = [
        abs(stroking['actions'][idx+1]['pos'] - stroking['actions'][idx]['pos']) / \
        (stroking['actions'][idx+1]['at'] - stroking['actions'][idx]['at']) \
        for idx in range(len(stroking['actions'])-1)
    ]
    projection[0] = 0

    scaler = max(projection)
    projection = [round(100 * x / scaler) for x in projection]
    vibration['actions'] = [ {'at': vibration['actions'][idx]['at'], 'pos': x } \
            for idx, x in enumerate(projection)]

    out_file = '.'.join(stroking_funscript_file.split('.')[:-1]) + '-vibration.funscript'
    with open(out_file, "w") as vibration_funscript:
        json.dump(vibration, vibration_funscript)

    return "OK: Save Vibration Funscript to " + str(out_file)


def show_message(message :str) -> None:
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(message+' ')
    msg.setWindowTitle("Funscript Converter " + VERSION)
    msg.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    msg = convertStrokesToVibration()
    show_message(msg)
    sys.exit()
