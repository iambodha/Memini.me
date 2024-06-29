import os
import shutil
import psycopg2
from psycopg2 import sql
from ImageAnalysis import faceAnalysis, faceVerification, imageCaptioning, cutFace
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import json

dbName = "Memini"
dbUser = "postgres"
dbPassword = "postgres"
dbHost = "localhost"
dbPort = "5432"

conn = psycopg2.connect(
    dbname=dbName, user=dbUser, password=dbPassword, host=dbHost, port=dbPort
)
cursor = conn.cursor()

def getNewImages(directory):
    original_directory = os.getcwd()
    
    try:
        os.chdir(directory)
        Images = os.listdir()
        newImages = [image for image in Images if os.path.isfile(image)]
    finally:
        os.chdir(original_directory)
    
    return newImages

def generateUUID(tableName):
    query = f"SELECT COALESCE(MAX(COALESCE(uuid, 0)), 0) FROM {tableName}"
    cursor.execute(query)
    
    max_uuid = cursor.fetchone()[0]
    
    return max_uuid + 1

def getExifData(imagePath):
    try:
        img = Image.open(imagePath)
        exifData = img._getexif()
        if exifData is not None:
            exif = {}
            for tag, value in exifData.items():
                tagName = TAGS.get(tag, tag)
                exif[tagName] = value

            return exif
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
        
def formatDateTime(dateTimeStr):
    try:
        if dateTimeStr:
            # Example format from EXIF data: '2024:06:26 14:30:00'
            dt = datetime.strptime(dateTimeStr, '%Y:%m:%d %H:%M:%S')
            return dt.strftime('%Y-%m-%d %H:%M:%S%z')
        else:
            return None
    except Exception as e:
        print(f"Error formatting datetime: {e}")
        return None
        

def extractImageMetadata(imagePath):
    exifData = getExifData(imagePath)
    if exifData is not None:
        dateTime = exifData.get('DateTimeOriginal')
        formattedDateTime = formatDateTime(dateTime)
        
        cameraDetails = [
            f"Make: {exifData.get('Make', 'N/A')}",
            f"Model: {exifData.get('Model', 'N/A')}",
            f"ExposureTime: {exifData.get('ExposureTime', 'N/A')}",
            f"FNumber: {exifData.get('FNumber', 'N/A')}",
            f"ISOSpeedRatings: {exifData.get('ISOSpeedRatings', 'N/A')}",
        ]
        
        location = []
        if 'GPSInfo' in exifData:
            gpsInfo = exifData['GPSInfo']
            latitude = gpsInfo.get('GPSLatitude')
            latitudeRef = gpsInfo.get('GPSLatitudeRef')
            longitude = gpsInfo.get('GPSLongitude')
            longitudeRef = gpsInfo.get('GPSLongitudeRef')
            
            if latitude and longitude:
                latitudeDecimal = latitude[0] + latitude[1]/60 + latitude[2]/3600
                longitudeDecimal = longitude[0] + longitude[1]/60 + longitude[2]/3600
                if latitudeRef == 'S':
                    latitudeDecimal = -latitudeDecimal
                if longitudeRef == 'W':
                    longitudeDecimal = -longitudeDecimal
                location = [f"Latitude: {latitudeDecimal}", f"Longitude: {longitudeDecimal}"]
        
        return formattedDateTime, cameraDetails, location
    else:
        return None, [], []

def getPeopleUUIDS():
    query = "SELECT uuid FROM people;"
    cursor.execute(query)
    uuids = cursor.fetchall()
    
    uuidList = [uuid[0] for uuid in uuids]
    
    if not uuidList:
        return None
    else:
        return uuidList

def updatePeopleTable(uuid, faceValue, imageValue):
    sqlQuery = sql.SQL("""
        UPDATE people
        SET faces_list = array_append(faces_list, %s),
            images_list = array_append(images_list, %s)
        WHERE uuid = %s
    """)

    cursor.execute(sqlQuery, (faceValue, imageValue, uuid))
    conn.commit()

def addPeopleTable(uuid, facePath, facesList, imagesList, averageEmotion, averageFaceConfidence, averageEthnicGroup):
    insertQuery = """
    INSERT INTO people (uuid, face_path, faces_list, images_list, average_emotion, average_face_confidence, average_ethnic_group)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insertQuery, (
        uuid,
        facePath,
        facesList,
        imagesList,
        averageEmotion,
        averageFaceConfidence,
        averageEthnicGroup
    ))
    conn.commit()

def addFacesTable(face_uuid, person_uuid, image_uuid,imageAnalysisData):
    query = """
    INSERT INTO faces (uuid, person_uuid, image_uuid, emotion_percentages, dominant_emotion, region, face_confidence, age, ethnic_groups_percentages, dominant_ethnic_group)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        face_uuid,
        person_uuid,
        image_uuid,
        json.dumps(imageAnalysisData['emotion']),
        imageAnalysisData['dominant_emotion'],
        json.dumps(imageAnalysisData['region']),
        imageAnalysisData['face_confidence'],
        imageAnalysisData['age'],
        json.dumps(imageAnalysisData['race']),
        imageAnalysisData['dominant_race']
    )

    cursor.execute(query, data)
    conn.commit()
    
def insertImageData(uuid, dateTime, cameraDetails, location, imagePath, 
                    personTagsList, facesList, maleCount, femaleCount, 
                    averageAge, averageConfidence, dominantEmotion,
                    angryAverage, disgustAverage, fearAverage, happyAverage, 
                    sadAverage, surpriseAverage, neutralAverage,
                    angryCount, disgustCount, fearCount, happyCount, 
                    sadCount, surpriseCount, neutralCount,
                    asianCount, indianCount, blackCount, whiteCount, 
                    middleEasternCount, latinoHispanicCount):
    
    query = """
    INSERT INTO images (
        uuid, date_time, camera_details, location, image_path, 
        person_tags_list, faces_list, male_count, female_count, 
        average_age, average_confidence, dominant_emotion,
        angry_average, disgust_average, fear_average, happy_average, 
        sad_average, surprise_average, neutral_average,
        angry_count, disgust_count, fear_count, happy_count, 
        sad_count, surprise_count, neutral_count,
        asian_count, indian_count, black_count, white_count, 
        middle_eastern_count, latino_hispanic_count
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """
    
    data = (
        uuid, dateTime, cameraDetails, location, imagePath, 
        personTagsList, facesList, maleCount, femaleCount, 
        averageAge, averageConfidence, dominantEmotion,
        angryAverage, disgustAverage, fearAverage, happyAverage, 
        sadAverage, surpriseAverage, neutralAverage,
        angryCount, disgustCount, fearCount, happyCount, 
        sadCount, surpriseCount, neutralCount,
        asianCount, indianCount, blackCount, whiteCount, 
        middleEasternCount, latinoHispanicCount
    )

    cursor.execute(query, data)
    conn.commit()

def main():
    directoryPath = "./Data/New/"
    facesPath = "./Data/Faces/"
    tempFacesPath = "./Data/TempFaces/"
    savedImagesPath = "./Data/savedImages/"
    newImagesList = getNewImages(directoryPath)
    pendingPersonList = []
    if not newImagesList:
        return
    
    for newImage in newImagesList:
        imagePath = directoryPath + newImage
        imageAnalysisList = faceAnalysis(imagePath)
        uuid = generateUUID("images")
        dateTime, cameraDetails, location = extractImageMetadata(imagePath)
        newImagePath = savedImagesPath + newImage
        personTagsList = []
        facesList = []
        maleCount = 0
        femaleCount = 0
        totalAge = 0
        totalConfidence = 0
        emotionCounts = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0}
        emotionSums = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0}
        raceCounts = {'asian': 0, 'indian': 0, 'black': 0, 'white': 0, 'middle eastern': 0, 'latino hispanic': 0}

        for imageAnalysis in imageAnalysisList:
            people_uuid = generateUUID("people")
            face_uuid = generateUUID("faces")
            outputPath = tempFacesPath + str(people_uuid) + ".jpg"
            cutFace(imagePath, outputPath, imageAnalysis)
            peopleUUIDList = getPeopleUUIDS()
            if peopleUUIDList:
                for person in peopleUUIDList:
                    personImagePath = facesPath + str(person) + ".jpg"
                    result = faceVerification(outputPath, personImagePath)
                    if result:
                        shutil.move(outputPath, personImagePath)
                        updatePeopleTable(person, face_uuid, uuid)
                        pendingPersonList.append(person)
                        personTagsList.append(person)
                        people_uuid = person
                        break
            if os.path.exists(outputPath):
                destinationPath = facesPath + str(people_uuid) + ".jpg"
                shutil.move(outputPath, destinationPath)
                addPeopleTable(people_uuid, destinationPath, [face_uuid], [uuid], None, None, None)
                pendingPersonList.append(people_uuid)
                personTagsList.append(people_uuid)

            addFacesTable(face_uuid, people_uuid, uuid, imageAnalysis)
            facesList.append(face_uuid)
            
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
