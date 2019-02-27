try:
    from tkFileDialog import askopenfilename
    from tkMessageBox import showwarning
    import Tkinter
except ImportError:
    from tkinter.filedialog import askopenfilename
    from tkinter.messagebox import showwarning
    import tkinter as Tkinter
from datetime import datetime
import logging
from pull_session import copy_files


class Application(Tkinter.Frame):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def execute_copy_files(self):
        if self.v:
            logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                                datefmt='%Y-%m-%d:%H:%M:%S',level=logging.DEBUG)
        copy_files(self.xeoma_path.get(), self.tzone.get(), self.session.get(), self.begin_time.get(), self.end_time.get(), self.force.get())
        self.quit()

    def create_widgets(self):
        # Xeoma path Frame
        self.path_frame = Tkinter.Frame(self)
        self.path_frame.pack(fill=Tkinter.BOTH, expand=1)
        w = Tkinter.Label(self.path_frame, text="Xeoma path:")
        w.pack(fill=Tkinter.BOTH, expand=1)
        self.xeoma_path = Tkinter.StringVar(root, value='/Volumes/DataRAID/xeoma')
        self.xeoma_path_entry = Tkinter.Entry(self.path_frame, textvariable=self.xeoma_path)
        self.xeoma_path_entry.pack(fill=Tkinter.BOTH, expand=1)

        # tzone frame
        self.tzone_frame = Tkinter.Frame(self.path_frame)
        self.tzone_frame.pack(fill=Tkinter.BOTH, expand=1)
        w2 = Tkinter.Label(self.tzone_frame, text="Time zone (NYC is -5):")
        w2.pack(fill=Tkinter.BOTH, expand=1)
        self.tzone = Tkinter.IntVar(root, value=-5)
        tzones = range(-12, 15)
        self.tzone_menu = Tkinter.OptionMenu(self.tzone_frame, self.tzone,
                                             *tzones)
        self.tzone_menu.pack(fill=Tkinter.BOTH, expand=1)

        # session frame
        self.session_frame = Tkinter.Frame(self.tzone_frame)
        self.session_frame.pack(fill=Tkinter.BOTH, expand=1)
        w3 = Tkinter.Label(self.session_frame, text="Session (yyyy-mm-dd):")
        w3.pack()
        today = datetime.today().strftime('%Y-%m-%d')
        self.session = Tkinter.StringVar(root, value=today)
        self.session_entry = Tkinter.Entry(self.session_frame, textvariable=self.session)
        self.session_entry.pack(fill=Tkinter.BOTH, expand=1)

        # begin frame
        self.begin_frame = Tkinter.Frame(self.session_frame)
        self.begin_frame.pack(fill=Tkinter.BOTH, expand=1)
        w4 = Tkinter.Label(self.begin_frame, text="begin time (hh-mm):")
        w4.pack()
        self.begin_time = Tkinter.StringVar(root, value='08:00')
        self.begin_entry = Tkinter.Entry(self.begin_frame, textvariable=self.begin_time)
        self.begin_entry.pack(fill=Tkinter.BOTH, expand=1)

        # end frame
        self.end_frame = Tkinter.Frame(self.session_frame)
        self.end_frame.pack(fill=Tkinter.BOTH, expand=1)
        w4 = Tkinter.Label(self.end_frame, text="end time (hh-mm):")
        w4.pack()
        self.end_time = Tkinter.StringVar(root, value='08:00')
        self.end_entry = Tkinter.Entry(self.end_frame, textvariable=self.end_time)
        self.end_entry.pack(fill=Tkinter.BOTH, expand=1)

        # verbose frame
        self.verbose_frame = Tkinter.Frame(self.end_frame)
        self.verbose_frame.pack(fill=Tkinter.BOTH, expand=1)
        w4 = Tkinter.Label(self.verbose_frame, text="Verbose option (check if you want to debug or see progress)")
        w4.pack()
        self.v = Tkinter.BooleanVar(value=False)
        self.check_v = Tkinter.Checkbutton(self.verbose_frame,
                                            text="verbose",
                                            variable=self.v)
        self.check_v.pack()

        # force frame
        self.force_frame = Tkinter.Frame(self.verbose_frame)
        self.force_frame.pack(fill=Tkinter.BOTH, expand=1)
        w4 = Tkinter.Label(self.force_frame, text="Force option (check if you want to overwrite files)")
        w4.pack()
        self.force = Tkinter.BooleanVar(value=False)
        self.check_f = Tkinter.Checkbutton(self.force_frame,
                                            text="verbose",
                                            variable=self.force)
        self.check_f.pack()

        # copy button frame
        self.copy_frame = Tkinter.Frame(self.force_frame)
        self.copy_frame.pack(fill=Tkinter.BOTH, expand=1)
        self.copy_button = Tkinter.Button(self.copy_frame)
        self.copy_button["text"] = "Copy",
        self.copy_button["command"] = self.execute_copy_files
        self.copy_button.pack({"side": "right"})


if __name__ == '__main__':
    root = Tkinter.Tk()
    # root.tk.call('tk', 'scaling', 10.0)
    app = Application(master=root)
    app.mainloop()
    root.destroy()
