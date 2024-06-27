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
        uuid SERIAL PRIMARY KEY,
        date_time TIMESTAMPTZ,
        camera_details TEXT[],
        location FLOAT[],
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
    );
    """

    cur.execute(createImagesTable)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    createTables()
    print("Tables created successfully")
