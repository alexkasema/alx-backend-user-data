#!/usr/bin/env python3
""" working with logs """

import re
import logging
from typing import List


occurrences = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """ Returns a filtered log message """
    extract, replace = (occurrences['extract'], occurrences['replace'])
    return re.sub(extract(fields, separator), replace(redaction), message)


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
