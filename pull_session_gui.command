#!/usr/bin/env python
try:
    from tkFileDialog import askopenfilename
    from tkMessageBox import showwarning
    import Tkinter
except ImportError:
    from tkinter.filedialog import askopenfilename
    from tkinter.messagebox import showwarning
    import tkinter as Tkinter
from glob import glob
import os
import shutil
from datetime import datetime, timedelta
import logging
# from pull_session import copy_files




def daterange(start_date, end_date, inclusive=False):
    if inclusive:
        for n in range(int ((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)
    else:
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)

def copy_files(path_to_xeoma, tzone, session_date, input_begin_time,
               input_end_time, force):
    dst_folder = os.path.dirname(os.path.realpath(__file__))
    logging.debug('dst folder: {}'.format(dst_folder))
    logging.debug('path to xeoma files: {}'.format(path_to_xeoma))

    input_begin_time += ':00'
    input_end_time += ':00'

    begin_time_list = session_date.split('-')
    begin_time_list.extend(input_begin_time.split(':'))
    begin_time_list = [int(x) for x in begin_time_list]

    begin_naive_datetime = datetime(*begin_time_list)
    # begin_datetime = tzone.localize(begin_naive_datetime).astimezone(pytz.utc)
    begin_datetime = begin_naive_datetime - timedelta(hours=tzone)

    # begin_date = begin_datetime.date().strftime('%Y-%m-%d')
    begin_time = begin_datetime.time().hour * 60 + begin_datetime.time().minute
    logging.debug('begin time in minutes: {}'.format(begin_time))

    end_time_list = session_date.split('-')
    end_time_list.extend(input_end_time.split(':'))
    end_time_list = [int(x) for x in end_time_list]

    end_naive_datetime = datetime(*end_time_list)
    # end_datetime = tzone.localize(end_naive_datetime).astimezone(pytz.utc)
    end_datetime = end_naive_datetime - timedelta(hours=tzone)

    end_date = end_datetime.date().strftime('%Y-%m-%d')
    end_time = end_datetime.time().hour * 60 + end_datetime.time().minute
    logging.debug('end time in minutes: {}'.format(end_time))

    dst_session_folder = dst_folder + '/' + session_date
    if not os.path.exists(dst_session_folder):
        logging.debug('{} folder does not exist. Making folder'.format(dst_session_folder))
        os.mkdir(dst_session_folder)
    else:
        logging.debug('{} folder does already exist.'.format(session_date))

    camera_dict = {'Preview+Archive.27': 'overhead-mid-right',
                    'Preview+Archive.70': 'dpad-left',
                    'Preview+Archive.4': 'dpad-right',
                    'Preview+Archive.42': 'overhead-right-ptz',
                    'Preview+Archive.62': 'pit-left',
                    'Preview+Archive.55': 'pit-center',
                    'Preview+Archive.48': 'pit-right',
                    'Preview+Archive.23': 'overhead'}
    cameras = glob(path_to_xeoma + '/*')
    logging.debug('{}'.format(cameras))
    for camera_path in cameras:
        camera = os.path.basename(camera_path)
        if camera in camera_dict:
            camera = camera_dict[camera]
        for date in daterange(begin_datetime.date(), end_datetime.date(), inclusive=True):
            session_date = date.strftime('%Y-%m-%d')
            path_to_files = '/'.join([camera_path, session_date, 'h264'])
            logging.debug('path_to_files {}'.format(path_to_files))
            for minute in range(begin_time, end_time):
                srcs = glob(path_to_files + '/' + str(minute).zfill(4) + '*')
                if len(srcs) > 1:
                    logging.debug('src {}'.format(src))
                    # raise ValueError
                if len(srcs) < 1:
                    logging.warning('No file with format: {}'.format(path_to_files + '/' + str(minute).zfill(4) +'*'))
                    continue
                for src in srcs:
                    # src = src[0]
                    logging.debug('src {}'.format(src))
                    base_src = os.path.basename(src)
                    base_src_no_ext = base_src.split('.')[0]
                    ext = base_src.split('.')[1]
                    minute_in_local_time = minute - 300
                    local_hour = str(int(minute_in_local_time / 60.)).zfill(2)
                    local_minute =  str(minute_in_local_time % 60).zfill(2)
                    dst_file_name = '_'.join([session_date, local_hour, local_minute, base_src_no_ext, camera])
                    logging.debug(dst_file_name)
                    dst_file_name += '.' + ext
                    logging.debug(dst_file_name)

                    dst = dst_folder + '/' + session_date + '/'+ dst_file_name
                    if os.path.exists(dst) and not force:
                        logging.debug('path already exists {}'.format(dst))
                        logging.debug('skip')
                    logging.debug(src)
                    logging.debug(dst)
                    shutil.copyfile(src, dst)




class Application(Tkinter.Frame):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def execute_copy_files(self):
        if self.v.get():
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
    root.tk.call('tk', 'scaling', 10.0)
    app = Application(master=root)
    # app.tk.call('tk', 'scaling', 10.0)
    app.mainloop()
    root.destroy()
