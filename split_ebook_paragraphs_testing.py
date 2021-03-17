import json
import re

def lambda_handler(event):
    event_dir = json.loads(event)
    chapter = event_dir['text']
    paragraphs = chapter.split('///')
    paragraphs = list(filter(lambda x: not re.fullmatch(r' *',x), paragraphs))
    for i in paragraphs:
        print(json.dumps({"paragraphs": i}))

if __name__ == '__main__':
    event = input()
    lambda_handler(event)