#!/usr/bin/env python
from glob import glob
from datetime import datetime, timedelta
import os
import shutil
import argparse
import logging
try:
    input = raw_input
except NameError:
    pass

def daterange(start_date, end_date, inclusive=False):
    if inclusive:
        for n in range(int ((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)
    else:
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)

def copy_files(path_to_xeoma, tzone, session_date, input_begin_time, input_end_time):
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


    if not os.path.exists(session_date):
        logging.debug('{} folder does not exist. Making folder'.format(session_date))
        os.mkdir(dst_folder + '/' + session_date)
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
                src = glob(path_to_files + '/' + str(minute).zfill(4) + '*')
                if len(src) > 1:
                    logging.debug('src {}'.format(src))
                    raise ValueError
                if len(src) < 1:
                    logging.warning('No file with format: {}'.format(path_to_files + '/' + str(minute).zfill(4) +'*'))
                    continue
                src = src[0]
                logging.debug('src {}'.format(src))
                base_src = os.path.basename(src)
                base_src_no_ext = base_src.split('.')[0]
                ext = base_src.split('.')[1]

                dst_file_name = '_'.join([session_date, base_src_no_ext, camera])
                logging.debug(dst_file_name)
                dst_file_name += '.' + ext
                logging.debug(dst_file_name)

                dst = dst_folder + '/' + session_date + '/'+ dst_file_name

                logging.debug(src)
                logging.debug(dst)
                shutil.copyfile(src, dst)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pull Xeoma files for one session.',
                                     epilog='Examples \n python pull_session.py --session 2019-02-14 --begin_time 08:00 --end_time 14:03',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--xeoma_path', type=str, default='/Volumes/DataRAID/xeoma', help='Path to the Xeoma files. For example, /mnt/xeoma/')
    parser.add_argument('--tzone', type=int, default=-5, help='Time zone where you are. For example, use -5 if you are in Baltimore, during the winter.')
    parser.add_argument('--session', type=str, default=None, help='Session date in YYYY-mm-dd format. For example, use 2019-01-23 to pull out videos captured on January 23 2019.')
    parser.add_argument('--begin_time', type=str, default=None, help='Inital time in hh:mm format. For example, use 07:30 to pull out videos from 7:30 AM.')
    parser.add_argument('--end_time', type=str, default=None,  help='Final time in hh:mm format. For example, use 15:30 to pull out videos until 4:30 PM.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase verbosity.')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%Y-%m-%d:%H:%M:%S',level=logging.DEBUG)
    if not args.session:
        args.session = input('Session date in YYYY-mm-dd format: ')
        tzone = input('Time zone (default -5):')
        if tzone != '':
            args.tzone = tzone
    if not args.begin_time:
        args.begin_time = input('Begin time in hh:mm format: ')
    if not args.end_time:
        args.end_time = input('End time in hh:mm format: ')
        verbose = input('Do you want verbose output (y/n): ')
        if verbose == 'y':
            logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                                datefmt='%Y-%m-%d:%H:%M:%S',level=logging.DEBUG)
    logging.debug(args)
    copy_files(args.xeoma_path, args.tzone, args.session, args.begin_time, args.end_time)
