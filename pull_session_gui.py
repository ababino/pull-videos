try:
    from tkFileDialog import askopenfilename
    from tkMessageBox import showwarning
    import Tkinter
except ImportError:
    from tkinter.filedialog import askopenfilename
    from tkinter.messagebox import showwarning
    import tkinter as Tkinter
from datetime import datetime
from pull_session import copy_files


class Application(Tkinter.Frame):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Xeoma path Frame
        self.path_frame = Tkinter.Frame(self)
        self.path_frame.pack(fill=Tkinter.BOTH, expand=1)
        w = Tkinter.Label(self.path_frame, text="Xeoma path:")
        w.pack(fill=Tkinter.BOTH, expand=1)
        self.xeoma_path = Tkinter.StringVar(root, value='/Volumes/DataRAID/xeoma')
        self.e = Tkinter.Entry(self.path_frame, textvariable=self.xeoma_path)
        self.e.pack(fill=Tkinter.BOTH, expand=1)

        # tzone frame
        self.tzone_frame = Tkinter.Frame(self.path_frame)
        self.tzone_frame.pack(fill=Tkinter.BOTH, expand=1)
        w2 = Tkinter.Label(self.tzone_frame, text="Time zone (NYC is -5):")
        w2.pack(fill=Tkinter.BOTH, expand=1)

        self.tzone = Tkinter.IntVar(root, value=-5)
        tzones = range(-12, 15)
        self.rtype_menu = Tkinter.OptionMenu(self.tzone_frame, self.tzone,
                                             *tzones)
        self.rtype_menu.pack(fill=Tkinter.BOTH, expand=1)

        # session frame
        self.session_frame = Tkinter.Frame(self.tzone_frame)
        self.session_frame.pack(fill=Tkinter.BOTH, expand=1)
        w3 = Tkinter.Label(self.session_frame, text="Session (yyyy-mm-dd):")
        w3.pack()
        today = datetime.today().strftime('%Y-%m-%d')
        self.session = Tkinter.StringVar(root, value=today)
        self.e = Tkinter.Entry(self.session_frame, textvariable=self.session)
        self.e.pack({"side": "left"})



if __name__ == '__main__':
    root = Tkinter.Tk()
    # root.tk.call('tk', 'scaling', 10.0)
    app = Application(master=root)
    app.mainloop()
    root.destroy()
