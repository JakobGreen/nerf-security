/**
    Copyright 2014-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
        http://aws.amazon.com/apache2.0/
    or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

/**
 * App ID for the skill
 */
var APP_ID = undefined; //replace with "amzn1.echo-sdk-ams.app.[your-unique-value-here]";

var PUBLIC_URL = "";

/**
 * The AlexaSkill prototype and helper functions
 */
var AlexaSkill = require('./AlexaSkill'),
    request = require('request');

function securityAPICall(path, cb) {
	console.log("URL  = "+PUBLIC_URL+path);
	request.get(PUBLIC_URL+path, function (error, response, body) {
		if (!error && response.statusCode == 200) {
			var data = JSON.parse(body);

			cb(data.result);
		} else {
			console.log("Error = "+error+" Statuscode = "+response.statusCode);
			cb(false);
		}
	});
}


var NerfSecurity = function () {
    AlexaSkill.call(this, APP_ID);
};

// Extend AlexaSkill
NerfSecurity.prototype = Object.create(AlexaSkill.prototype);
NerfSecurity.prototype.constructor = NerfSecurity;

NerfSecurity.prototype.eventHandlers.onLaunch = function (launchRequest, session, response) {
    var speechOutput = "Welcome to the Nerf security skill, you can say fire";
    var repromptText = "You can say fire";
    response.ask(speechOutput, repromptText);
};

NerfSecurity.prototype.intentHandlers = {
    // register custom intent handlers
    "NerfSecurityIntent": function (intent, session, response) {
	securityAPICall("/fire", function(success) {
		if (success) {
			response.tellWithCard("Get Wrecked!", "Security", "Get Wrecked!");
		} else {
			response.tellWithCard("Fail", "Security", "Fail");
		}
	});
    },
    "LeeroyIntent": function (intent, session, response) {
	securityAPICall("/leeroy", function(success) {
		if (success) {
			response.tellWithCard("LEEROY JENKINS", "Security", "LEEROY JENKINS");
		} else {
			response.tellWithCard("Fail", "Security", "Fail");
		}
	});
    },
    "AMAZON.HelpIntent": function (intent, session, response) {
        response.ask("You can say fire to me!", "You can say fire to me!");
    }
};

// Create the handler that responds to the Alexa Request.
exports.handler = function (event, context) {
    // Create an instance of the NerfSecurity skill.
    var security = new NerfSecurity();
    security.execute(event, context);
};

