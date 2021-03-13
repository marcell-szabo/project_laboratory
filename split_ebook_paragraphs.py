import boto3
import re
import json

def lambda_handler(event, context):
    chapter = event['text']
    paragraphs = chapter.split('///')
    paragraphs = list(filter(lambda x: not re.fullmatch(r' *', x), paragraphs))
    print(f'Executed: {paragraphs}')
    #aws_lambda = boto3.client('lambda')

    #for i in paragraphs:
    #    aws_lambda.invoke(FunctionName='split_ebook_word',
    #                      InvocationType='Event',
    #                      LogType='Tail',
    #                      !!Payload=bytes(i.encode()))
    return {
        'statuscode': 200,
        'body': 'Everything is OK'
    }