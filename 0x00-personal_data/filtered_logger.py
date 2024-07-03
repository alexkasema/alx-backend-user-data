#!/usr/bin/env python3
""" working with logs """

import re
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
