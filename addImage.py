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

def d7(f, g, h):
    CS.execute(SQ.SQL("UPDATE people SET faces_list = array_append(faces_list, %s), images_list = array_append(images_list, %s) WHERE uuid = %s"), (g, h, f))
    CN.commit()

def d8(i, j, k, l, m, n, o):
    CS.execute("INSERT INTO people (uuid, face_path, faces_list, images_list, average_emotion, average_face_confidence, average_ethnic_group) VALUES (%s, %s, %s, %s, %s, %s, %s);", (i, j, k, l, m, n, o))
    CN.commit()

def d9(p, q, r, s):
    CS.execute("INSERT INTO faces (uuid, person_uuid, image_uuid, emotion_percentages, dominant_emotion, region, face_confidence, age, ethnic_groups_percentages, dominant_ethnic_group) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (p, q, r, J.dumps(s['emotion']), s['dominant_emotion'], J.dumps(s['region']), s['face_confidence'], s['age'], J.dumps(s['race']), s['dominant_race']))
    CN.commit()

def d10(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh):
    CS.execute("INSERT INTO images (uuid, date_time, camera_details, location, image_path, person_tags_list, faces_list, male_count, female_count, average_age, average_confidence, dominant_emotion, angry_average, disgust_average, fear_average, happy_average, sad_average, surprise_average, neutral_average, angry_count, disgust_count, fear_count, happy_count, sad_count, surprise_count, neutral_count, asian_count, indian_count, black_count, white_count, middle_eastern_count, latino_hispanic_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh))
    CN.commit()

def main():
    ni = d1("./Data/New/")
    pl = []
    if not ni:
        return
    
    for img in ni:
        ip = "./Data/New/" + img
        ia = FA(ip)
        ui = d2("images")
        dt, cm, lc = d5(ip)
        np = "./Data/savedImages/" + img
        pt = []
        fl = []
        mc = 0
        fc = 0
        ta = 0
        tc = 0
        ec = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0}
        es = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0}
        rc = {'asian': 0, 'indian': 0, 'black': 0, 'white': 0, 'middle eastern': 0, 'latino hispanic': 0}

        for an in ia:
            pu = d2("people")
            fu = d2("faces")
            op = "./Data/TempFaces/" + str(pu) + ".jpg"
            CF(ip, op, an)
            plst = d6()
            if plst:
                for pr in plst:
                    pp = "./Data/Faces/" + str(pr) + ".jpg"
                    r = FV(op, pp)
                    if r:
                        S.move(op, pp)
                        d7(pr, fu, ui)
                        pl.append(pr)
                        pt.append(pr)
                        pu = pr
                        break
            if O.path.exists(op):
                dp = "./Data/Faces/" + str(pu) + ".jpg"
                S.move(op, dp)
                d8(pu, dp, [fu], [ui], None, None, None)
                pl.append(pu)
                pt.append(pu)

            d9(fu, pu, ui, an)
            fl.append(fu)
            
            if an['dominant_gender'] == 'Man':
                mc += 1
            else:
                fc += 1
            
            ta += an['age']
            tc += an['face_confidence']
            
            for em, v in an['emotion'].items():
                es[em] += v
                if em == an['dominant_emotion']:
                    ec[em] += 1
            
            rc[an['dominant_race']] += 1

        tf = len(ia)
        aa = ta / tf if tf else None
        ac = tc / tf if tf else None

        de = max(ec, key=ec.get) if ec else None

        aa1 = es['angry'] / tf if tf else None
        da = es['disgust'] / tf if tf else None
        fa = es['fear'] / tf if tf else None
        ha = es['happy'] / tf if tf else None
        sa = es['sad'] / tf if tf else None
        su = es['surprise'] / tf if tf else None
        na = es['neutral'] / tf if tf else None

        ac1 = ec['angry']
        dc = ec['disgust']
        fc1 = ec['fear']
        hc = ec['happy']
        sc = ec['sad']
        su1 = ec['surprise']
        nc = ec['neutral']

        as1 = rc['asian']
        ic = rc['indian']
        bc = rc['black']
        wc = rc['white']
        mc1 = rc['middle eastern']
        lc = rc['latino hispanic']

        S.move(ip, np)
        
        d10(ui, dt, cm, lc, np, pt, fl, mc, fc, aa, ac, de, aa1, da, fa, ha, sa, su, na, ac1, dc, fc1, hc, sc, su1, nc, as1, ic, bc, wc, mc1, lc)

if __name__ == "__main__":
    main()
