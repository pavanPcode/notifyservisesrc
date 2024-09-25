import mysql.connector
import configparser

CONFIG_PATH = 'dbConfig.ini'
dbname = 'HealthCheck_Prod'


def read_db_config(filename=CONFIG_PATH, section=dbname):
    config = configparser.ConfigParser()
    config.read(filename)
    return {
        'user': config.get(section, 'user'),
        'password': config.get(section, 'password'),
        'host': config.get(section, 'host'),
        'database': config.get(section, 'database')
    }


def update_insert(insert_query):
    try:
        # Read database configuration
        db_config = read_db_config()
        # Connect to MySQL database
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        # Execute INSERT statement
        cursor.execute(insert_query)
        # Commit changes to database
        cnx.commit()

        return {"status": True, "message": "Insert successful."}

    except mysql.connector.Error as err:
        return {"status": False, "message": f"MySQL Error: {err}"}

    except Exception as e:
        return {"status": False, "message": f"Unexpected error: {e}"}

    finally:
        # Ensure cursor and connection are closed
        try:
            cursor.close()
        except:
            pass

        try:
            cnx.close()
        except:
            pass



