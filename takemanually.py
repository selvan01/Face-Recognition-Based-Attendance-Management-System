import tkinter as tk
import os
import pandas as pd
import datetime
import time

# Time and date settings
ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d")
timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Hour, Minute, Second = timeStamp.split(":")
d = {}
index = 0

# Create the directory for attendance CSV if it does not exist
attendance_dir = "Attendance"
if not os.path.exists(attendance_dir):
    os.makedirs(attendance_dir)

# GUI for manually filling attendance
def manually_fill():
    global sb
    sb = tk.Tk()
    sb.iconbitmap("AMS.ico")
    sb.title("Enter subject name...")
    sb.geometry("580x320")
    sb.configure(background="snow")

    def show_error(message):
        ec = tk.Toplevel(sb)
        ec.geometry("300x100")
        ec.iconbitmap("AMS.ico")
        ec.title("Warning!!")
        ec.configure(background="snow")
        tk.Label(ec, text=message, fg="red", bg="white", font=("times", 16, "bold")).pack()
        tk.Button(ec, text="OK", command=ec.destroy, fg="black", bg="lawn green", width=9, height=1,
                  activebackground="Red", font=("times", 15, "bold")).place(x=90, y=50)

    def fill_attendance():
        global subb
        subb = SUB_ENTRY.get()

        if not subb:
            show_error("Please enter subject name!!!")
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.iconbitmap("AMS.ico")
            MFW.title(f"Manual Attendance for {subb}")
            MFW.geometry("880x470")
            MFW.configure(background="snow")

            def enter_data_DB():
                global index, d
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if not ENROLLMENT or not STUDENT:
                    show_error("Please enter Student & Enrollment!!!")
                else:
                    d[index] = {"Enrollment": ENROLLMENT, "Name": STUDENT, Date: 1}
                    index += 1
                    ENR_ENTRY.delete(0, "end")
                    STUDENT_ENTRY.delete(0, "end")
                    print(d)

            def create_csv():
                if not d:
                    show_error("No data to save as CSV!")
                    return
                df = pd.DataFrame.from_dict(d, orient='index')
                csv_name = os.path.join(attendance_dir, f"{subb}_{Date}_{Hour}-{Minute}-{Second}.csv")
                df.to_csv(csv_name, index=False)
                Notifi.configure(text="CSV created Successfully", bg="Green", fg="white")
                Notifi.place(x=180, y=380)

            tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="white", bg="blue2",
                     font=("times", 15, "bold")).place(x=30, y=100)
            tk.Label(MFW, text="Enter Student name", width=15, height=2, fg="white", bg="blue2",
                     font=("times", 15, "bold")).place(x=30, y=200)

            global ENR_ENTRY, STUDENT_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20, bg="yellow", fg="red", font=("times", 23, "bold"))
            ENR_ENTRY.place(x=290, y=105)
            STUDENT_ENTRY = tk.Entry(MFW, width=20, bg="yellow", fg="red", font=("times", 23, "bold"))
            STUDENT_ENTRY.place(x=290, y=205)

            Notifi = tk.Label(MFW, text="", bg="Green", fg="white", width=33, height=2, font=("times", 19, "bold"))

            tk.Button(MFW, text="Clear", command=lambda: ENR_ENTRY.delete(0, 'end'), fg="black",
                      bg="deep pink", width=10, height=1, activebackground="Red", font=("times", 15, "bold")).place(x=690, y=100)
            tk.Button(MFW, text="Clear", command=lambda: STUDENT_ENTRY.delete(0, 'end'), fg="black",
                      bg="deep pink", width=10, height=1, activebackground="Red", font=("times", 15, "bold")).place(x=690, y=200)
            tk.Button(MFW, text="Enter Data", command=enter_data_DB, fg="black", bg="lime green",
                      width=20, height=2, activebackground="Red", font=("times", 15, "bold")).place(x=170, y=300)
            tk.Button(MFW, text="Convert to CSV", command=create_csv, fg="black", bg="red",
                      width=20, height=2, activebackground="Red", font=("times", 15, "bold")).place(x=570, y=300)

            MFW.mainloop()

    tk.Label(sb, text="Enter Subject", width=15, height=2, fg="white", bg="blue2",
             font=("times", 15, "bold")).place(x=30, y=100)
    
    SUB_ENTRY = tk.Entry(sb, width=20, bg="yellow", fg="red", font=("times", 23, "bold"))
    SUB_ENTRY.place(x=250, y=105)

    tk.Button(sb, text="Fill Attendance", command=fill_attendance, fg="white", bg="deep pink",
              width=20, height=2, activebackground="Red", font=("times", 15, "bold")).place(x=250, y=160)
    sb.mainloop()

# Start the GUI
manually_fill()
