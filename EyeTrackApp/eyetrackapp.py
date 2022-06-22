from osc import VRChatOSC
from config import EyeTrackConfig
from camera_widget import CameraWidget, CameraWidgetName
import queue
import threading
import PySimpleGUI as sg

WINDOW_NAME = "EyeTrackApp"
RIGHT_EYE_NAME = "-RIGHTEYEWIDGET-"
LEFT_EYE_NAME = "-LEFTEYEWIDGET-"


def main():
    # Get Configuration
    config: EyeTrackConfig = EyeTrackConfig.load()
    config.save()

    eyes = [
        CameraWidget(CameraWidgetName.RIGHT_EYE, config),
        CameraWidget(CameraWidgetName.LEFT_EYE, config),
    ]

    layout = [
        [
            sg.Column(
                eyes[0].widget_layout, vertical_alignment="top", key=RIGHT_EYE_NAME
            ),
            sg.Column(
                eyes[1].widget_layout, vertical_alignment="top", key=LEFT_EYE_NAME
            ),
        ],
    ]

    # Create the window
    window = sg.Window("Eye Tracking", layout)

    cancellation_event = threading.Event()

    # Check to see if we can connect to our video source first. If not, bring up camera finding
    # dialog.

    # Check to see if we have an ROI. If not, bring up ROI finder GUI.

    # Spawn worker threads
    osc_queue: "queue.Queue[tuple[bool, int, int]]" = queue.Queue()
    osc = VRChatOSC(cancellation_event, osc_queue)
    osc_thread = threading.Thread(target=osc.run)
    osc_thread.start()

    #  t2s_queue: "queue.Queue[str | None]" = queue.Queue()
    #  t2s_engine = SpeechEngine(t2s_queue)
    #  t2s_thread = threading.Thread(target=t2s_engine.run)
    #  t2s_thread.start()
    #  t2s_queue.put("App Starting")

    # GUI Render loop

    while True:
        # First off, check for any events from the GUI
        event, values = window.read(timeout=1)

        # If we're in either mode and someone hits q, quit immediately
        if event == "Exit" or event == sg.WIN_CLOSED:
            for eye in eyes:
                eye.shutdown()
            cancellation_event.set()
            osc_thread.join()
            #      t2s_engine.force_stop()
            #      t2s_queue.put(None)
            #      t2s_thread.join()
            print("Exiting EyeTrackApp")
            return
        for eye in eyes:
            eye.render(window, event, values)


if __name__ == "__main__":
    main()
