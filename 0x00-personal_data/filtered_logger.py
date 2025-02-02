#!/usr/bin/env python3
""" working with logs """

import os
import re
import logging
import mysql.connector
from typing import List


occurrences = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """ Returns a filtered log message """
    extract, replace = (occurrences['extract'], occurrences['replace'])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """ create a log for user data """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Creates a connector to the database and returns it """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    connecton = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_password,
        database=db_name,
    )

    return connecton


def main():
    """ get information from users table and display it in a filtered format
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    cols = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)

    logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]), zip(cols, row),
            )
            data = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, data, None, None)
            log_record = logging.LogRecord(*args)
            logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Formatting log records """
        data = super(RedactingFormatter, self).format(record)
        text = filter_datum(self.fields, self.REDACTION, data, self.SEPARATOR)

        return text
