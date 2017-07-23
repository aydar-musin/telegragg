import base64
from bs4 import BeautifulSoup
import re
import quopri

def from_html(html, transfer_encoding):
    inputs = html
    if transfer_encoding == 'base64':
        inputs = base64.urlsafe_b64decode(inputs)
    elif transfer_encoding == 'quoted-printable':
        inputs = quopri.decodestring(base64.urlsafe_b64decode(inputs))

    soup = BeautifulSoup(inputs)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    return clean_str(soup.get_text())


def from_base64(input):
    return clean_str(base64.urlsafe_b64decode(input))


def from_quoted_printable(s):
    return clean_str(quopri.decodestring(s))


def clean_str(str):
    try:
        result= []
        lines = str.split('\n')
        lastLine = 'initial str'

        for line in lines:
            if not (re.match(r'^\s*$', line) and re.match(r'^\s*$', lastLine)):
                result.append(line.strip())
            lastLine = line

        return '\n'.join(result)
    except Exception as e:
        print e.message
        return  str