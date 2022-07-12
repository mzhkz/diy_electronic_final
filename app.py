# -*- coding: utf-8 -*-
# /usr/bin/python (macOS system python)
import os
import sys
import sqlite3
import datetime
import serial
import time
import tempfile
import inspect
import codecs
import Foundation



def parse_req(req):
    # reqをparseしtitleとbodyのみ取得する
    res = {}
    for x in str(req).split(';'):
        if 'body' in x or 'titl' in x:
            d = x.replace('{','').strip().split(' = ')
            res[d[0]] = d[1].replace('"','')
    return res


def get_notif_json():
    # DBファイルにアクセスしparseして返す
    notificationDB = os.path.realpath(
            tempfile.gettempdir() + '/../0/com.apple.notificationcenter/db2/db')
    conn = sqlite3.connect(notificationDB)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("SELECT data from record");

    res_j = []
    for row in cursor:
        plist, fmt, err = \
                Foundation.NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(
                memoryview(row[0]),
                Foundation.NSPropertyListMutableContainers,
                None, None)
        if err is not None:
            continue

        # print(type(plist))
        # for member in inspect.getmembers(plist, inspect.ismethod):
        #     print(member[0])
        notif_dic = {}
        for key in plist.allKeys():
            # print("key:", key)
            value = plist.get(key)
            if key == 'date':
                notif_dic['date'] = Foundation.NSDate.alloc().initWithTimeIntervalSinceReferenceDate_(value)
            if key == 'req':
                req = parse_req(value)
                if 'titl' in req.keys():
                    notif_dic['title'] = req['titl']
                if 'body' in req.keys():
                    notif_dic['body'] = req['body']
            elif key == 'app':
                notif_dic['app'] = value
        res_j.append(notif_dic)
    return res_j

# データ取得
d = get_notif_json()
# 表示


def get_notif():
    raw_notifis = get_notif_json()
    encoded_notifs = []
    for i, notif in enumerate(raw_notifis):
        try:
            date = notif.get('date', 'no date')
            app = notif.get('app', 'no app')
            title = codecs.decode(notif.get('title','no title').lower(), 'unicode-escape')
            body = codecs.decode(notif.get('body','no body').lower(), 'unicode-escape')
            encoded_notifs.append([date, app, title, body])
            # print(encoded_notifs[i])
        except:
            pass
    return encoded_notifs

def get_app_notifs(apps):
    return list(filter(lambda notif: notif[1] in apps, get_notif()))


def main():
    # SERIAL_CODE = "COM3"
    SERIAL_CODE = "/dev/cu.usbmodem142301"
    DETECT_APPS = ["jp.naver.line.mac"]
    THRESHOLD = 50

    new_notif_count = 0

    notifis_catch = get_app_notifs(DETECT_APPS);
    notifis_index = len(notifis_catch)

    ser = serial.Serial(SERIAL_CODE, 115200, timeout = 0.3)
    ser.write("{value}".format(value = 0).encode("utf-8"))
    time.sleep(2)

    while True:
        notifis_now = get_app_notifs(DETECT_APPS)
        for notif in notifis_now[notifis_index:]:
            print(notif)
        notifis_index = len(notifis_now)
        reserve_notifs_size = len(notifis_now) - len(notifis_catch)
        if reserve_notifs_size < 0:
            notifis_catch = []
            ser.write("{value}".format(value = 0).encode("utf-8"));
            print("delete all")
            continue
        print("{opecode} {operand}".format(opecode = "INC", operand=reserve_notifs_size))
        if (reserve_notifs_size > 0):
            new_notif_count += reserve_notifs_size
            # print(" received -> {0}".format(ser.readline().decode('utf-8')))
            brightness = (float(new_notif_count) / float(THRESHOLD)) * 100.0
            print(brightness)
            brightness = 100 if brightness > 100 else brightness
            ser.write("{value}".format(value = brightness).encode("utf-8"))
        notifis_catch = notifis_now
        time.sleep(1)
if __name__ == "__main__":
    main()