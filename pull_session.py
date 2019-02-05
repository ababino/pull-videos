from glob import glob
from datetime import datetime
import pytz
import os
import shutil
import argparse

# tzone = 'US/Eastern'
# input_date = '2019-01-23'
# input_begin_time = '08:00'
# input_end_time = '17:00'

def copy_files(path_to_xeoma, tzone, session_date, input_begin_time, input_end_time):
    dst_folder = os.path.dirname(os.path.realpath(__file__))
    print('dst_folder', dst_folder)

    tzone = pytz.timezone(tzone)

    # path_to_xeoma = '/media/andres/Blue/Xeoma new setup '
    input_begin_time += ':00'
    input_end_time += ':00'

    begin_time_list = session_date.split('-')
    begin_time_list.extend(input_begin_time.split(':'))
    begin_time_list = [int(x) for x in begin_time_list]

    begin_naive_datetime = datetime(*begin_time_list)
    begin_datetime = tzone.localize(begin_naive_datetime).astimezone(pytz.utc)

    # begin_date = begin_datetime.date().strftime('%Y-%m-%d')
    begin_time = begin_datetime.time().hour * 60 + begin_datetime.time().minute


    end_time_list = session_date.split('-')
    end_time_list.extend(input_end_time.split(':'))
    end_time_list = [int(x) for x in end_time_list]

    end_naive_datetime = datetime(*end_time_list)
    end_datetime = tzone.localize(end_naive_datetime).astimezone(pytz.utc)

    end_date = end_datetime.date().strftime('%Y-%m-%d')
    end_time = end_datetime.time().hour * 60 + begin_datetime.time().minute



    if not os.path.exists(session_date):
        os.mkdir(session_date)

    cameras = glob(path_to_xeoma + '/*')

    for camera_path in cameras:
        camera = os.path.basename(camera_path)
        path_to_files = '/'.join([camera_path, session_date, 'h264'])
        for minute in range(begin_time, end_time):
            src = glob(path_to_files + '/' + str(minute).zfill(4) +'*')
            if len(src) > 1:
                raise ValueError
            if len(src) < 1:
                print('No file with format:')
                print(path_to_files + '/' + str(minute).zfill(4) +'*')
                raise ValueError
            src = src[0]
            base_src = os.path.basename(src)
            base_src_no_ext = base_src.split('.')[0]
            ext = base_src.split('.')[1]

            dst_file_name = '_'.join([session_date, base_src_no_ext, camera])
            print(dst_file_name)
            dst_file_name += '.' + ext
            print(dst_file_name)

            dst = dst_folder + '/' + session_date + '/'+ dst_file_name

            print(src, dst)
            shutil.copyfile(src, dst)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pull Xeoma files for one session.', epilog='Examples...')
    parser.add_argument('--xeoma_path', type=str, help='Path to the Xeoma files. For example, /mnt/xeoma/')
    parser.add_argument('--tzone', type=str, default='US/Eastern', help='Time zone where you are. For example, use US/Eastern if you are in Baltimore.')
    parser.add_argument('--session', type=str, help='Session date in YYYY-mm-dd format. For example, use 2019-01-23 to pull out videos captured on January 23 2019.')
    parser.add_argument('--begin_time', type=str,  help='Inital time in hh:mm format. For example, use 07:30 to pull out videos from 7:30 AM.')
    parser.add_argument('--end_time', type=str,  help='Final time in hh:mm format. For example, use 15:30 to pull out videos until 4:30 PM.')

    args = parser.parse_args()
    print(args)
    print(args.xeoma_path, args.tzone, args.session, args.begin_time, args.end_time)
    copy_files(args.xeoma_path, args.tzone, args.session, args.begin_time, args.end_time)
