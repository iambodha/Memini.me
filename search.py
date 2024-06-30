import psycopg2
from psycopg2 import sql

dbName = "Memini"
dbUser = "postgres"
dbPassword = "postgres"
dbHost = "localhost"
dbPort = "5432"

conn = psycopg2.connect(
    dbname=dbName, user=dbUser, password=dbPassword, host=dbHost, port=dbPort
)
cursor = conn.cursor()

def getImagesListByUuid(uuid):
    try:
        query = sql.SQL("SELECT images_list FROM people WHERE uuid = %s")
        cursor.execute(query, (uuid,))
        
        result = cursor.fetchone()
        
        if result is None:
            print(f"No entry found for uuid: {uuid}")
            return None
        
        imagesList = result[0]
        return imagesList
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    finally:
        if conn:
            cursor.close()
            conn.close()

uuidToSearch = 123
imagesList = getImagesListByUuid(uuidToSearch)
print(f"Images list for uuid {uuidToSearch}: {imagesList}")
