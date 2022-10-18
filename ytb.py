import logging
import json
# import azure.functions as func
from youtube_transcript_api import YouTubeTranscriptApi
from gensim.summarization.summarizer import summarize
import os
import io
import re
import requests


def main(video_id):
    logging.info('Python HTTP trigger function processed a request.')

    # video_id = req.params.get('video_id')
    # if not video_id:
    #     try:
    #         req_body = video_id.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         video_id = req_body.get('video_id')
    #req_body =  video_id.get_json() # json.loads(video_id)
    #video_id = req_body.get('video_id')

    if video_id:
        try:
            transcripts = YouTubeTranscriptApi.get_transcript(video_id)
            textTranscripts = ""
            for t in transcripts:
                text = re.sub("[\(\[].*?[\)\]]", " ",
                              t['text']).replace("-", "")
                text = " ".join(text.splitlines())
                text = re.sub('\s{2,}', ' ', text).strip()

                if len(text.strip()) > 3 and len(text.strip().split(" ")) > 1:
                    # print(text)
                    textTranscripts += text + " "

            punctuatedTranscripts = punctuate_online(textTranscripts)
            summary = summarize(punctuatedTranscripts,
                                ratio=0.5, split=True, word_count=300)
            summary = " ".join(summary)
            results = {
                "transcripts": transcripts,
                "summary": summary
            }
            # json.dumps(results) #, status_code=200, mimetype="application/json")
            #
            return results # json.dumps(results)
        except Exception as e:
            print(str(e))
            return "No subtitles"

    else:
        return "This HTTP function executed successfully. Pass a video_id in the query string or in the request body for a personalized response."
        #     status_code=201
        # )


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
