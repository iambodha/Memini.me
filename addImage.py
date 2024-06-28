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
