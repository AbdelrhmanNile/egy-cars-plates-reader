import PySimpleGUI as sg
import cv2
import numpy as np
from Prediction import PlatesReader 
from plate_detection import YoloInferenece
from Database import plates_db_api
from time import sleep


pr = PlatesReader("ocr_model.hdf5") 
pd = YoloInferenece("car_plate_detector.pt", 512)
db = plates_db_api()

def popup(name,plate_num):
    layout = [
        [sg.Text(f"Name: {name}")],
        [sg.Text(f"Plate number: {plate_num}")],
        #[sg.Push(), sg.Button('OK')]
    ]
    popup_win = sg.Window('POPUP', layout, modal=True, auto_close=True, auto_close_duration=10)
    popup_win.read()


def main():

    sg.theme('Black')

    # define the window layout
    layout = [
             [sg.Image(filename='', key='image')]
             ]

    # create the window and show it without the plot
    window = sg.Window('Car Plates Reader',
                       layout,icon='cctv.ico' , finalize=True)
    window.Maximize()
    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv2.VideoCapture(0)
    recording = True

    frame_i = 1
    last_plate = ""

    while True:
        event, values = window.read(timeout=20)
        
        if event == sg.WIN_CLOSED:
            return


        if recording:
            ret, frame = cap.read()
            frame_i += 1
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            window['image'].update(data=imgbytes)
            

            if frame_i % 30 == 0 :
                cv2.imwrite("./plt.jpg",frame)
                cord = pd.get_plate_xywh("./plt.jpg")
                if cord != None :
                    x,y,w,h = cord
                    img = cv2.imread("./plt.jpg")
                    plate = img[y:h,x:w]
                    plate_num = pr.read_plate(plate)
                    if plate_num != None:
                        plate_num_ar = pr.label_to_ar(plate_num)
                    if plate_num != last_plate :
                        last_plate = plate_num
                        db_response = db.query(plate_num)

                        if db_response != None :
                            popup(db_response["name"],plate_num_ar)
                        else:
                            popup("Not registered",plate_num_ar)

                frame_i = 1



main()