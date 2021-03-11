
import json
import ebooklib
from ebooklib import epub
import re
import io


def lambda_handler():
    with open("A:\Egyetem\Önlab\pythonProject\pinocchio1.epub","rb") as f:
        data_stream = io.BytesIO(f.read())
    book = epub.read_epub(data_stream)
    html_list = []
    for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        html_list.append(doc.get_body_content().decode("utf-8"))
    cleanr = re.compile('<.*?>')
    for i in html_list:
        cleantext = re.sub(cleanr, '', i)
        cleantext = re.sub(r'([\r\n]\s?){2,}|(\S\n\s\n)', '///', cleantext)
        cleantext = re.sub(r'\n', '/n/',cleantext)



    return {
        'statuscode': 200,
        'body': json.dumps(cleantext)
    }

if __name__ == '__main__':
    lambda_handler()