import psycopg2
from psycopg2 import sql

dbName = "Memini"
dbUser = "postgres"
dbPassword = "postgres"
dbHost = "localhost"
dbPort = "5432"

def createTables():
    conn = psycopg2.connect(
        dbname=dbName, user=dbUser, password=dbPassword, host=dbHost, port=dbPort
    )
    cur = conn.cursor()

    createImagesTable = """
    CREATE TABLE IF NOT EXISTS images (
        uuid INT PRIMARY KEY,
        date_time TIMESTAMPTZ,
        camera_details TEXT[],
        location FLOAT[],
        image_path TEXT,
        person_tags_list TEXT[],
        faces_list INT[],
        male_count INT,
        female_count INT,
        average_age FLOAT,
        average_confidence FLOAT,
        dominant_emotion TEXT,
        angry_average FLOAT,
        disgust_average FLOAT,
        fear_average FLOAT,
        happy_average FLOAT,
        sad_average FLOAT,
        surprise_average FLOAT,
        neutral_average FLOAT,
        angry_count INT,
        disgust_count INT,
        fear_count INT,
        happy_count INT,
        sad_count INT,
        surprise_count INT,
        neutral_count INT,
        asian_count INT,
        indian_count INT,
        black_count INT,
        white_count INT,
        middle_eastern_count INT,
        latino_hispanic_count INT
        image_caption TEXT,
    );
    """
    createFacesTable = """
    CREATE TABLE IF NOT EXISTS faces (
        uuid INT PRIMARY KEY,
        person_uuid INT,
        image_uuid INT,
        emotion_percentages JSONB,
        dominant_emotion TEXT,
        region JSONB,
        face_confidence FLOAT,
        age INT,
        ethnic_groups_percentages JSONB,
        dominant_ethnic_group TEXT
    );
    """
    createPeopleTable = """
    CREATE TABLE IF NOT EXISTS people (
        uuid INT PRIMARY KEY,
        face_path TEXT,
        faces_list INT[],
        images_list INT[],
        average_emotion TEXT,
        average_face_confidence FLOAT,
        average_ethnic_group TEXT
    );
    """

    cur.execute(createImagesTable)
    cur.execute(createFacesTable)
    cur.execute(createPeopleTable)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    createTables()
    print("Tables created successfully")
