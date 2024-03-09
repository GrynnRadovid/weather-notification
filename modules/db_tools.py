import mysql.connector
import os

# Database configuration


db_config = {
    'user': 'TEST_USER',
    'password': os.getenv('DB_PASSWORD'),
    'host': '127.0.0.1',
    'database': '   weather_data'
}


# DOCS: https://dev.mysql.com/doc/connector-python/en/
def write_to_db(temperature, humidity, row_id):
    """
    Writes the temperature and humidity to the mysql DB at the specified row_id.
    :param temperature: The temperature to write.
    :param humidity: The humidity to write.
    :param row_id: The row ID where the values will be replaced.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        UPDATE temp_humidity
        SET temperature = %s, humidity = %s
        WHERE id = %s;
        """
        cursor.execute(sql, (temperature, humidity, row_id))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"DB ERROR: {err}")
    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()


def read_from_db(row_id):
    """
    Reads the temperature and humidity values from the mysql DB at the specified row_id.
    :param row_id: The row ID where the values will be read from.
    :return temperature: Return the temperature value pulled from DB.
    :return humidity: Return the humidity value pulled from DB.
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        SELECT temperature, humidity FROM temp_humidity WHERE id = %s;
        """
        cursor.execute(sql, (row_id,))
        result = cursor.fetchone()

        if result:
            temperature, humidity = result
            return temperature, humidity
        else:
            print(f"QUERY ERROR: No data found for row with id {row_id}")
            return None, None
    except mysql.connector.Error as err:
        print(f"DB ERROR: {err}")
        return None, None
    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()
