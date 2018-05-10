# -*- coding:utf8 -*-

# Author - Naresh Ganatra
# https://www.youtube.com/c/NareshGanatra


import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/ride', methods=['POST'])
def ride():
    try :
        invoke_next_question = True
        req = request.get_json(silent=True, force=True)

        print("----------------START-------------------")
        print("Request:")
        #print(json.dumps(req, indent=4))

        parameters = req.get("result").get("parameters")
        current_answer = req.get("result").get("action")
        current_question = req.get("result").get("contexts")[0].get("parameters").get("current-question")
        print("current_question - ", current_question)
        print ("current_answer - ", current_answer)
        next_question = "question" + str(int(current_question[-1:]) + 1 )
        print ("next question - ", next_question)

        #I am not using these parameters anywhere but just an showing here how one can extract all the answers
        parameter1 = req.get("result").get("contexts")[0].get("parameters").get("parameter1")
        parameter2 = req.get("result").get("contexts")[0].get("parameters").get("parameter2")
        parameter3 = "question3." + current_answer
        print ("paramters - ", parameter1, parameter2, parameter3)


        if current_answer == "no" :

            bot_reply = {
                "speech": "I am afraid you cannot ride",
                "displayText": "I am afraid you cannot ride"
            }
        else:
            if current_question == "question3" :
                bot_reply = {
                "speech": "Enjoy the ride",
                "displayText": "Enjoy the ride",
            }
            else:
                bot_reply = {
            #user-answer is not used anywhere in the code but just showing you how to pass some values to the intent you are calling
            #https://dialogflow.com/docs/events
            "followupEvent": {
                "name": next_question,
                "data": {
                    "user-answer": current_question + "." + current_answer
                }
                }
            }
        print ("rreached here...")
        res = json.dumps(bot_reply, indent=4)
        # print(res)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        print("about to return")
        return r


    except:
        speech = "oops...I am not able to help you at the moment, please try again.."
        bot_reply = {
            "speech": speech,
            
            "displayText": speech,
            "source": "VA webhook"
        }

    res = json.dumps(bot_reply, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print (bot_reply)
    print("###############################")
    return r


@app.route('/test', methods=['GET'])
def test():
    return  "Hello there my friend !!"

@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    my_result =  {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-weather-webhook-sample"
    }
    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
