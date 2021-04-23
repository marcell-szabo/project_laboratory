import boto3
import json
import ebooklib
from ebooklib import epub
import re
import io
import concurrent.futures

def concurrent_lambdacall(text, aws_lambda):
    text = re.sub(r'([\r\n]\s?){2,}|(\S\n\s\n)', '///', text)
    text = re.sub(r'\n', '/n/', text)
    try:
        aws_lambda.invoke(FunctionName='split_ebook_paragraphs',
                          InvocationType='Event',
                          LogType='Tail',
                          Payload=bytes(json.dumps({"text": text}).encode())
                          )
        print(f'invoked concurrent {text}')
    except Exception:
        print(f'Exception {text}')

def lambda_handler(event, context):
    #gets AWS resources
    s3 = boto3.client('s3')
    aws_lambda = boto3.client('lambda')

    #gets epub object from S3
    s3_info = event['Records'][0]['s3']
    bucketname = s3_info['bucket']['name']
    objectkey = s3_info['object']['key']
    data_stream = io.BytesIO()
    try:
        s3.download_fileobj(bucketname, objectkey, data_stream)
        print('getting ebook from s3 successfull\n')
    except Exception:
        print('S3 error')

    #gets plaintext chapters from book
    book = epub.read_epub(data_stream)
    html_list = []
    for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        html_list.append(doc.get_body_content().decode("utf-8"))

    #process text
    cleantext = list(map(lambda x: re.sub(r'<.*?>', '', x), html_list))
    cleantext = list(filter(lambda x: not re.fullmatch(r'\s*', x), cleantext))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda x: concurrent_lambdacall(x, aws_lambda), cleantext)
    print("Executed ")
    return {
        'statuscode': 200,
        'body': json.dumps('OK')
    }
