import logging
from gensim.summarization.summarizer import summarize
# import azure.functions as func
import requests
import json
import re


def main(req_body):
    logging.info('Python HTTP trigger function processed a request.')

    # try:
    #     req_body = req.get_json()
    # except ValueError:
    #     pass
    # else:
    req_body = json.loads(req_body)
    text = req_body.get('text')
    word_count = req_body.get('word_count')

    if text and word_count:
        punctuatedText = punctuate_online(text)
        summary = summarize(punctuatedText, ratio=0.5,
                            split=True, word_count=int(word_count))
        summary = [re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", " ", s).strip()
                   for s in summary]
        summary = ". ".join(summary)
        results = {
            "summary": summary
        }
        return json.dumps(results)
    else:
        return "This HTTP triggered function executed successfully. Pass a text in the request body for a personalized response."


def punctuate_online(text):
    # defining the api-endpoint
    API_ENDPOINT = "http://bark.phon.ioc.ee/punctuator"
    # data to be sent to api
    data = dict(text=text)
    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data)

    # extracting response text
    punctuatedText = r.text
    return punctuatedText
