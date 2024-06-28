import os as O
import shutil as S
import psycopg2 as P
from psycopg2 import sql as SQ
from ImageAnalysis import faceAnalysis as FA, faceVerification as FV, imageCaptioning as IC, cutFace as CF
from PIL import Image as I
from PIL.ExifTags import TAGS as T, GPSTAGS as G
from datetime import datetime as DT
import json as J

DBN = "Memini"
DBU = "postgres"
DBP = "postgres"
DBH = "localhost"
DBO = "5432"

CN = P.connect(dbname=DBN, user=DBU, password=DBP, host=DBH, port=DBO)
CS = CN.cursor()

def d1(p):
    try:
        O.chdir(p)
        i = O.listdir()
        return [j for j in i if O.path.isfile(j)]
    finally:
        O.chdir("..")

def d2(t):
    CS.execute(f"SELECT COALESCE(MAX(COALESCE(uuid, 0)), 0) FROM {t}")
    return CS.fetchone()[0] + 1

def d3(i):
    try:
        k = I.open(i)
        l = k._getexif()
        if l:
            m = {}
            for n, o in l.items():
                n = T.get(n, n)
                m[n] = o
            return m
    except:
        return None


def d4(p):
    try:
        if p:
            q = DT.strptime(p, '%Y:%m:%d %H:%M:%S')
            return q.strftime('%Y-%m-%d %H:%M:%S%z')
    except:
        return None

def d5(r):
    s = d3(r)
    if s:
        t = d4(s.get('DateTimeOriginal'))
        u = [f"Make: {s.get('Make', 'N/A')}", f"Model: {s.get('Model', 'N/A')}", f"ExposureTime: {s.get('ExposureTime', 'N/A')}", f"FNumber: {s.get('FNumber', 'N/A')}", f"ISOSpeedRatings: {s.get('ISOSpeedRatings', 'N/A')}"]
        v = []
        if 'GPSInfo' in s:
            w = s['GPSInfo']
            x = w.get('GPSLatitude')
            y = w.get('GPSLatitudeRef')
            z = w.get('GPSLongitude')
            aa = w.get('GPSLongitudeRef')
            if x and z:
                bb = x[0] + x[1]/60 + x[2]/3600
                cc = z[0] + z[1]/60 + z[2]/3600
                if y == 'S':
                    bb = -bb
                if aa == 'W':
                    cc = -cc
                v = [f"Latitude: {bb}", f"Longitude: {cc}"]
        return t, u, v
    return None, [], []

def d6():
    CS.execute("SELECT uuid FROM people;")
    d = CS.fetchall()
    return [e[0] for e in d] if d else None

