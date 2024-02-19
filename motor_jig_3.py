# ======================================================================
#       MOTOR TORQUE TESTKIT 2024.02.02 Author @yaku
#       GitHub https://github.com/ShigeoYakuno/MOTOR
# ======================================================================

import tkinter as tk
import threading
import tkinter.font as f
import time
from tkinter import messagebox
import sys
import serial
import serial.tools.list_ports
import os

# debug ON/OFF
os.environ["PYTHONBREAKPOINT"] = "0"


driverList = ["7025", "7099"]
dirList = ["CW", "CCW"]
stepList = ["FULL", "HALF"]
currentList = ["2.0A", "2.5A", "3.0A", "3.5A"]
speedList = ["1000", "1500", "2000", "2500", "3000", "3500", "4000"]
exitFlg = 0

CURRENT_AX_Y = 60
SPEED_AX_Y = 120
DIR_AX_Y = 260
DRIVER_AX_Y = 320
STEP_AX_Y = 390
BTN_AX_Y = 440


# ======================================================================

# ======================================================================


# シリアルポートを自動検出する関数
def auto_detect_serial_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)
        if "USB Serial Port" in p.description:
            return p.device
    return None


def open_serial():
    global ser

    try:
        # ser = serial.Serial("COM4", 57600)
        ser = serial.Serial("/dev/serial0", 57600)

        # ser = serial.Serial(auto_detect_serial_port(), 57600, timeout=1)
    except:
        print("uart already open")


def close_serial():
    global ser

    try:
        ser.close()
    except:
        print("uart cannot close")


def motor_start_judge():

    tempval = Motorjig()

    temp_crnt = tempval.get_crnt_val()
    temp_spd = tempval.get_speed_val()
    temp_dir = tempval.get_dir_val()
    temp_driver = tempval.get_driver_val()
    temp_step = tempval.get_step_val()

    print(
        f"current{temp_crnt} speed{temp_spd} dir{temp_dir} driver{temp_driver} step{temp_step}"
    )

    # message add cancel
    startJudge = messagebox.askokcancel(
        "確認",
        "「OK」を押すとモーターが動きます。配線が正しいか確認して下さい\r\n中止する場合は「キャンセル」を押して下さい",
    )

    if startJudge is True:
        open_serial()
        time.sleep(0.1)
        motor_start(temp_crnt, temp_spd, temp_dir, temp_driver, temp_step)
    else:
        pass


def motor_start(temp_crnt, temp_spd, temp_dir, temp_driver, temp_step):

    global ser

    # curent select
    current = {
        0: "A",
        1: "a",
        2: "C",
        3: "c",
    }
    if temp_crnt in current:
        setCrnt = current[temp_crnt]
    ser.write(setCrnt.encode())
    time.sleep(0.3)

    # direction select
    direction = {
        0: "K",
        1: "k",
    }
    if temp_dir in direction:
        setDir = direction[temp_dir]
    ser.write(setDir.encode())
    time.sleep(0.3)

    # driver select
    steppDriver = {
        0: "M",
        1: "m",
    }
    if temp_driver in steppDriver:
        setDriver = steppDriver[temp_driver]
    ser.write(setDriver.encode())
    time.sleep(0.3)

    # step select
    steppMode = {
        0: "P",
        1: "p",
    }
    if temp_step in steppMode:
        setStep = steppMode[temp_step]
    ser.write(setStep.encode())
    time.sleep(0.3)

    # speed select
    setSpd = str(format(temp_spd, "x"))
    sendTxt = "s" + setSpd + "S"
    print(sendTxt)
    ser.write(sendTxt.encode())


def motor_stop():
    global ser

    open_serial()

    print("motor stop")

    strData = "Z"
    ser.write(strData.encode())


def exit_func():
    global exitFlg
    exitFlg = 1

    print("program finish")
    time.sleep(0.5)
    sys.exit()


# ======================================================================
#      class
# ======================================================================
class Motorjig(tk.Frame):
    """Motor operation setting class"""

    """ constructor """

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        return

    """ get value func """

    def get_crnt_val(self):
        return crntVal.get()

    def get_speed_val(self):
        return spdScale.get()

    def get_dir_val(self):
        return dirVal.get()

    def get_driver_val(self):
        return driverVal.get()

    def get_step_val(self):
        return stepVal.get()

    """ create button func """

    def create_current_btn(self):

        global crntVal

        crntVal = tk.IntVar()
        crntVal.set(2)

        current_label = tk.Label(root, text="電流設定(A)").place(
            x=10, y=CURRENT_AX_Y - 30
        )

        tk.Radiobutton(
            master=root, text=currentList[0], value=0, variable=crntVal
        ).place(x=100, y=CURRENT_AX_Y)

        tk.Radiobutton(
            master=root, text=currentList[1], value=1, variable=crntVal
        ).place(x=300, y=CURRENT_AX_Y)

        tk.Radiobutton(
            master=root, text=currentList[2], value=2, variable=crntVal
        ).place(x=500, y=CURRENT_AX_Y)

        tk.Radiobutton(
            master=root, text=currentList[3], value=3, variable=crntVal
        ).place(x=700, y=CURRENT_AX_Y)

    def create_speed_btn(self):

        global spdScale

        speed_label = tk.Label(root, text="速度設定(pps)").place(
            x=10, y=SPEED_AX_Y - 20
        )

        spdScale = tk.Scale(
            master=root,
            orient=tk.HORIZONTAL,
            length=750,
            width=40,
            sliderlength=10,
            from_=200,
            to=4000,
            resolution=10,
            tickinterval=200,
        )
        spdScale.place(x=20, y=SPEED_AX_Y)

        spdScale.set(1000)

    def create_dir_btn(self):

        global dirVal

        dir_label = tk.Label(root, text="回転方向設定").place(x=10, y=DIR_AX_Y - 30)

        dirVal = tk.IntVar()
        dirVal.set(0)

        tk.Radiobutton(master=root, text=dirList[0], value=0, variable=dirVal).place(
            x=100, y=DIR_AX_Y
        )

        tk.Radiobutton(master=root, text=dirList[1], value=1, variable=dirVal).place(
            x=300, y=DIR_AX_Y
        )

    def create_driver_btn(self):

        global driverVal

        driver_label = tk.Label(root, text="ドライバ設定").place(
            x=10, y=DRIVER_AX_Y - 30
        )

        driverVal = tk.IntVar()
        driverVal.set(0)

        tk.Radiobutton(
            master=root, text=driverList[0], value=0, variable=driverVal
        ).place(x=100, y=DRIVER_AX_Y)

        tk.Radiobutton(
            master=root, text=driverList[1], value=1, variable=driverVal
        ).place(x=300, y=DRIVER_AX_Y)

    def create_step_btn(self):

        global stepVal

        step_label = tk.Label(root, text="動作モード設定").place(x=10, y=STEP_AX_Y - 30)

        stepVal = tk.IntVar()
        stepVal.set(0)

        tk.Radiobutton(master=root, text=stepList[0], value=0, variable=stepVal).place(
            x=100, y=STEP_AX_Y
        )

        tk.Radiobutton(master=root, text=stepList[1], value=1, variable=stepVal).place(
            x=300, y=STEP_AX_Y
        )

    def create_btn(self):
        tk.Button(master=root, text="START", command=motor_start_judge).place(
            x=100, y=BTN_AX_Y
        )
        tk.Button(master=root, text="STOP ", command=motor_stop).place(
            x=400, y=BTN_AX_Y
        )
        tk.Button(master=root, text="EXIT  ", command=exit_func).place(
            x=700, y=BTN_AX_Y
        )


# ======================================================================
#      rx thread(not used)
# ======================================================================
def uartRx():

    global exitFlg
    global ser

    while True:

        if exitFlg == 1:
            return

        open_serial()

        if ser is not None:
            data = ser.readline()
            data = data.strip()
            data = data.decode("CP932")
            # data = data.decode("Shift_JIS")
            print(data)

            close_serial()

        time.sleep(0.1)

    print(f"terminate thread 1")


# ======================================================================
#      main thread
# ======================================================================


def main():
    global app
    global root

    root = tk.Tk()
    root.geometry("800x480")
    root.title("MOTOR JIG for P-1186 Ver1.0 @yaku ")

    # make thread
    threadUartRx = threading.Thread(target=uartRx, daemon=True)

    # start thread
    # threadUartRx.start()

    app = Motorjig(master=root)

    app.create_current_btn()
    app.create_speed_btn()
    app.create_driver_btn()
    app.create_step_btn()
    app.create_dir_btn()
    app.create_btn()

    breakpoint()

    app.mainloop()

    print("PROGRAM FINISH")
    pass


if __name__ == "__main__":
    main()
