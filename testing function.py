
import json
import ebooklib
from ebooklib import epub
import re
import io
import split_ebook_paragraphs_testing

def lambda_handler():
    laptop = "C:\\Users\Marcell Szabo\Documents\Egyetem\onlab\pinocchio1.epub"
    desktop = "A:\Egyetem\Önlab\pythonProject\pinocchio1.epub"
    with open(desktop,"rb") as f:
        data_stream = io.BytesIO(f.read())
    book = epub.read_epub(data_stream)
    html_list = []
    for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        html_list.append(doc.get_body_content().decode("utf-8"))
    cleantext = list(map(lambda x: re.sub(r'<.*?>', '', x), html_list))
    cleantext = list(filter(lambda x: not re.fullmatch(r'\s*', x), cleantext))
    for i in cleantext:
        i = re.sub(r'([\r\n]\s?){2,}|(\S\n\s\n)', '///', i)
        i = re.sub(r'\n', '/n/',i)
        json_string = json.dumps({"text": i})
        print(json_string)
        #split_ebook_paragraphs_testing.lambda_handler(json_string)
    return {
        'statuscode': 200,
        'body': json.dumps(cleantext)
    }

if __name__ == '__main__':
    lambda_handler()