import boto3
import json
import ebooklib
from ebooklib import epub
import re
import io


def lambda_handler(event, context):
    #gets epub from S3 into bytesIO
    s3 = boto3.client('s3')
    aws_lambda = boto3.client('lambda')
    s3_info = event['Records'][0]['s3']
    bucketname = s3_info['bucket']['name']
    objectkey = s3_info['object']['key']

    data_stream = io.BytesIO()
    s3.download_fileobj(bucketname, objectkey, data_stream)
    #gets plaintext chapters from book
    book = epub.read_epub(data_stream)
    html_list = []
    for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        html_list.append(doc.get_body_content().decode("utf-8"))

    #process text
    cleanr = re.compile('<.*?>')
    for i in html_list:
        cleantext = re.sub(cleanr, '', i)
        #convert text into 1 line because of json requirement
        #puts /// on paragraph ending
        cleantext = re.sub(r'([\r\n]\s?){2,}|(\S\n\s\n)', '///', cleantext)
        #puts /n/ on line ending
        cleantext = re.sub(r'\n', '/n/',cleantext)
        json_string = json.dumps({"text": cleantext})
        response = aws_lambda.invoke(FunctionName='split_ebook_paragraphs',
                                     InvocationType='Event',
                                     LogType='Tail',
                                     Payload=bytes(json_string.encode()))
        print("Executed ")
    return {
        'statuscode': 200,
        'body': json.dumps('OK')
    }
