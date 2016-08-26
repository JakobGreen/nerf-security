# Nerf Security System

Using Amazon Echo for it's most desirable task; shooting roommates with nerf darts.

## Usage

"Alexa, ask security to fire"

(Nerf dart fires)

echo: "Get wrecked"

## Turret Setup

The turret is controlled through python using libusb and a flask webserver.

Install the python 2.7 dependencies:

    $ pip install -r requirements.txt

Start the turret control + webserver

    $ sudo ./main.py

You can test firing the turret through the webserver with a simple cURL request. The webserver defaults to port 5000.

    $ curl http://localhost:5000/fire

**For AWS Lambda function to communicate with the HTTP server you will have to setup port forwarding and make the port for the webserver accessible.**

## Alexa Skill Setup

You can find a tutorial for creating a Alex Skill and a AWS Lambda function [here](https://developer.amazon.com/public/community/post/TxKALMUNLHZPAP/New-Alexa-Skills-Kit-Template-Step-by-Step-Guide-to-Build-a-How-To-Skill#).

### Lambda Function

Make sure you have [npm](https://www.npmjs.com/) installed first, then download the dependencies for the skill:

    $ ./setup.sh

In the [skill/index.js](skill/index.js) file update the `PUBLIC_URL` field to correspond with your webserver.

Create a zip upload for AWS Lambda function:

    $ ./create.sh
    
Use the "skill.zip" to create and AWS Lambda function.

###Intent Schema

The Intent Schema used for the Alexa skill:

    {
      "intents": [
        {
          "intent": "NerfSecurityIntent"
        },
        {
          "intent": "AMAZON.HelpIntent"
        },
        {
          "intent": "AMAZON.StopIntent"
        },
        {
          "intent": "AMAZON.CancelIntent"
        }
      ]
    }

### Sample Utterances

The sample utterances used for the Alexa skill:

    NerfSecurityIntent fire
    NerfSecurityIntent attack
    NerfSecurityIntent destroy

## TODO:

- Leeroy Jenkins mode
- Make udev rule
