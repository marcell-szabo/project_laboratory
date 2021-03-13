import boto3
import json
import ebooklib
from ebooklib import epub
import re
import io


def lambda_handler(event, context):
    #gets AWS resources
    s3 = boto3.client('s3')
    aws_lambda = boto3.client('lambda')

    #gets epub object from S3
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
    cleantext = list(map(lambda x: re.sub(r'<.*?>', '', x), html_list))
    cleantext = list(filter(lambda x: not re.fullmatch(r'\s*', x), cleantext))
    for i in cleantext:
        i = re.sub(r'([\r\n]\s?){2,}|(\S\n\s\n)', '///', i)
        i = re.sub(r'\n', '/n/', i)
        json_string = json.dumps({"text": i})

        #invoke lambda asyncronously
        response = aws_lambda.invoke(FunctionName='split_ebook_paragraphs',
                                     InvocationType='Event',
                                     LogType='Tail',
                                     Payload=bytes(json_string.encode()))
        print(f"invoked: {i}")
    print("Executed ")
    return {
        'statuscode': 200,
        'body': json.dumps('OK')
    }
