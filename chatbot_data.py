from uuid import uuid4
import os

QUESTION = 0
YES = 1
NO = 2
IDENTIFIER = 3


class Intents:

    def __init__(self, csv_data, webhook_used):
        self.csv_data = csv_data
        self.webhook_used = webhook_used
        self.welcome_intent = {
            "id": str(uuid4()),
            "name": "Default Welcome Intent",
            "auto": True,
            "contexts": [],
            "responses": [
                {
                    "resetContexts": False,
                    "affectedContexts": [
                        {
                            "name": "DefaultWelcomeIntent-followup",
                            "parameters": {},
                            "lifespan": 1
                        }
                    ],
                    "parameters": [],
                    "messages": [
                        {
                            "type": 0,
                            "lang": "en",
                            "condition": "",
                            "speech": f"Hi! {self.csv_data[0][QUESTION]}"
                        }
                    ],
                    "defaultResponsePlatforms": {},
                    "speech": []
                }
            ],
            "priority": 500000,
            "webhookUsed": webhook_used,
            "webhookForSlotFilling": False,
            "fallbackIntent": False,
            "events": [
                {
                    "name": "WELCOME"
                }
            ],
            "conditionalResponses": [],
            "condition": "",
            "conditionalFollowupEvents": []
        }

        self.fallback_intent = {
            "id": "9332f025-2acd-4b98-9fd9-1c0a823a158a",
            "name": "Default Fallback Intent",
            "auto": True,
            "contexts": [],
            "responses": [
                {
                    "resetContexts": False,
                    "action": "input.unknown",
                    "affectedContexts": [],
                    "parameters": [],
                    "messages": [
                        {
                            "type": 0,
                            "lang": "en",
                            "condition": "",
                            "speech": [
                                "I didn\u0027t get that. Can you say it again?",
                                "I missed what you said. What was that?",
                                "Sorry, could you say that again?",
                                "Sorry, can you say that again?",
                                "Can you say that again?",
                                "Sorry, I didn\u0027t get that. Can you rephrase?",
                                "Sorry, what was that?",
                                "One more time?",
                                "What was that?",
                                "Say that one more time?",
                                "I didn\u0027t get that. Can you repeat?",
                                "I missed that, say that again?"
                            ]
                        }
                    ],
                    "defaultResponsePlatforms": {},
                    "speech": []
                }
            ],
            "priority": 500000,
            "webhookUsed": webhook_used,
            "webhookForSlotFilling": False,
            "fallbackIntent": True,
            "events": [],
            "conditionalResponses": [],
            "condition": "",
            "conditionalFollowupEvents": []
        }

    def speech_value(self, queue_head):
        curr_row = self.csv_data[queue_head["index"]]

        if queue_head["curr_yes_or_no"] is None:
            return curr_row[QUESTION]
        answer = curr_row[queue_head["curr_yes_or_no"]]
        if answer.isdigit():
            return self.csv_data[queue_head["index"] + int(answer)][QUESTION]
        else:
            return answer

    def intent_json(self, queue_head, input_context=None):

        curr_row = self.csv_data[queue_head["index"]]
        if queue_head["prev_yes_or_no"] is None and queue_head["curr_yes_or_no"] is None:
            name = f"{curr_row[IDENTIFIER].title()}-initial"
            parameters = []
            speech = curr_row[QUESTION]
        elif queue_head["curr_yes_or_no"] is not None:
            name = curr_row[IDENTIFIER].title() + " - " + ("Yes" if queue_head["curr_yes_or_no"] == YES else "No")
            parameters = [
                {
                    "id": str(uuid4()),
                    "required": True,
                    "dataType": "@confirmation",
                    "name": "confirmation",
                    "value": "$confirmation",
                    "promptMessages": [],
                    "noMatchPromptMessages": [],
                    "noInputPromptMessages": [],
                    "outputDialogContexts": [],
                    "isList": False
                }
            ]
            answer = curr_row[queue_head["curr_yes_or_no"]]
            if answer.isdigit():
                speech = self.csv_data[queue_head["index"] + int(answer)][QUESTION]
            else:
                speech = answer

        elif queue_head["prev_yes_or_no"] is not None:
            prev_yes_or_no = queue_head["prev_yes_or_no"]["value"]
            prev_row = queue_head["prev_yes_or_no"]["prev_row"]

            name = prev_row[IDENTIFIER].title() + " - " + ("Yes" if prev_yes_or_no == YES else "No")
            parameters = [
                {
                    "id": str(uuid4()),
                    "required": True,
                    "dataType": "@confirmation",
                    "name": "confirmation",
                    "value": "$confirmation",
                    "promptMessages": [],
                    "noMatchPromptMessages": [],
                    "noInputPromptMessages": [],
                    "outputDialogContexts": [],
                    "isList": False
                }
            ]
            speech = curr_row[QUESTION]

        output_context_name = queue_head["output_context"]
        data = {
            "id": str(uuid4()),
            "name": name,
            "auto": True,
            "contexts": [] if input_context is None else [input_context],
            "responses": [{
                "resetContexts": False,
                "affectedContexts": [
                    {
                        "name": output_context_name,
                        "parameters": {},
                        "lifespan": 1
                    }
                ],
                "parameters": parameters,
                "messages": [
                    {
                        "type": 0,
                        "lang": "en",
                        "condition": "",
                        "speech": speech
                    }
                ],
                "defaultResponsePlatforms": {},
                "speech": []
            }],
            "priority": 500000,
            "webhookUsed": self.webhook_used,
            "webhookForSlotFilling": False,
            "fallbackIntent": False,
            "events": [],
            "conditionalResponses": [],
            "condition": "",
            "conditionalFollowupEvents": []
        }

        return data


class Entities:
    confirmation_entity = {
        "id": "c2916dea-dec1-4a65-9163-96017d0dc31b",
        "name": "confirmation",
        "isOverridable": True,
        "isEnum": False,
        "isRegexp": False,
        "automatedExpansion": False,
        "allowFuzzyExtraction": False
    }

    confirmation_entries = [
        {
            "value": "yes",
            "synonyms": [
                "yes",
                "yeah",
                "that is correct",
                "correct",
                "yup"
            ]
        },
        {
            "value": "no",
            "synonyms": [
                "no",
                "nope",
                "incorrect",
                "that\u0027s not correct",
                "that\u0027s not right",
                "thats not right"
            ]
        }
    ]


class Usersays:
    yes_usersays_data = [
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "yes that is correct",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "that is correct",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "they do",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "does",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "it does",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "yup",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "y",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": True
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "right",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "yes it does",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "yes",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": True
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        }
    ]

    no_usersays_data = [
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "it does not",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "nop",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "not right",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "not",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": str(uuid4()),
            "data": [
                {
                    "text": "no",
                    "alias": "confirmation",
                    "meta": "@confirmation",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        }
    ]

    welcome_usersays_data = [
        {
            "id": "9fe716ea-f9ad-4d5f-82f2-56641f99c093",
            "data": [
                {
                    "text": "hiya",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": "aa3a4008-1fbe-4f6a-b223-e8ca0b30e1b7",
            "data": [
                {
                    "text": "hello",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        },
        {
            "id": "fdfdf4dd-2119-44c5-aad2-501cb812ea68",
            "data": [
                {
                    "text": "hi",
                    "userDefined": False
                }
            ],
            "isTemplate": False,
            "count": 0,
            "updated": 0
        }
    ]


class Agent:
    def __init__(self, webhook_used):
        self.webhook_used = webhook_used

        if self.webhook_used:
            self.webhook_data = {
                "url": "https://your-webhook-api.com",
                "username": "",
                "headers": {
                    "": ""
                },
                "available": True,
                "useForDomains": False,
                "cloudFunctionsEnabled": False,
                "cloudFunctionsInitialized": False
            }
        else:
            self.webhook_data = {
                "url": "",
                "username": "",
                "headers": {},
                "available": False,
                "useForDomains": False,
                "cloudFunctionsEnabled": False,
                "cloudFunctionsInitialized": False
            }

        self.agent_data = {
            "description": "Automatically Generated Agent",
            "language": "en",
            "shortDescription": "Automatically Generated Agent",
            "examples": "",
            "linkToDocs": "",
            "disableInteractionLogs": False,
            "disableStackdriverLogs": True,
            "googleAssistant": {
                "googleAssistantCompatible": False,
                "project": "testing-auto-create-neojhe",
                "welcomeIntentSignInRequired": False,
                "startIntents": [],
                "systemIntents": [],
                "endIntentIds": [],
                "oAuthLinking": {
                    "required": False,
                    "providerId": "",
                    "authorizationUrl": "",
                    "tokenUrl": "",
                    "scopes": "",
                    "privacyPolicyUrl": "",
                    "grantType": "AUTH_CODE_GRANT"
                },
                "voiceType": "MALE_1",
                "capabilities": [],
                "env": "",
                "protocolVersion": "V2",
                "autoPreviewEnabled": False,
                "isDeviceAgent": False
            },
            "defaultTimezone": "Africa/Casablanca",
            "webhook": self.webhook_data,
            "isPrivate": True,
            "customClassifierMode": "use.after",
            "mlMinConfidence": 0.3,
            "supportedLanguages": [],
            "onePlatformApiVersion": "v2",
            "analyzeQueryTextSentiment": False,
            "enabledKnowledgeBaseNames": [],
            "knowledgeServiceConfidenceAdjustment": -0.4,
            "dialogBuilderMode": False,
            "baseActionPackagesUrl": ""
        }


class PackageJson:
    package_json_data = {"version": "1.0.0"}


class AgentAPI:
    # agent.js code
    code = \
        """
        "use strict";
        const express = require("express");
        const router = express.Router();

        var mongoUtil = require("../../mongoUtil");
        var db = mongoUtil.getDbData();
        const { WebhookClient } = require("dialogflow-fulfillment");
        const info = {};
        var currentUsername;
        process.env.DEBUG = "dialogflow:debug"; // enables lib debugging statements
        """

    def handler_function(self, curr_intent, next_intent):
        agent_add_definition = ""
        speech = next_intent['responses'][0]['messages'][0]['speech']
        if isinstance(speech, list):
            for s in speech:
                agent_add_definition += f'\tagent.add("{s}"){os.linesep}'
        else:
            agent_add_definition = f'\tagent.add("{speech}"){os.linesep}'
        return (
            f"function handle{curr_intent['name'].replace(' ', '').replace('-', '')}(agent) {{{os.linesep}"
            f"{agent_add_definition}"
            f"}}{os.linesep}"
        )

    def intent_map(self, intent):
        return f'intentMap.set("{intent["name"]}", handle{intent["name"].replace(" ", "").replace("-", "")});{os.linesep}'

    def agent_code(self, intents_list):
        code = \
            """
                "use strict";
                const express = require("express");
                const router = express.Router();
                
                var mongoUtil = require("../../mongoUtil");
                var db = mongoUtil.getDbData();
                const { WebhookClient } = require("dialogflow-fulfillment");
                const info = {};
                var currentUsername;
                process.env.DEBUG = "dialogflow:debug"; // enables lib debugging statements
                router.post("/", async (request, response) => {
                  const agent = new WebhookClient({ request, response });
                  console.log("Dialogflow Request headers: " + JSON.stringify(request.headers));
                  console.log("Dialogflow Request body: " + JSON.stringify(request.body));
            """
        for i in range(len(intents_list)-1):
            code += self.handler_function(intents_list[i], intents_list[i+1])

        code += \
            """
              // Run the proper function handler based on the matched Dialogflow intent name
              let intentMap = new Map();
            """

        for intent in intents_list:
            code += self.intent_map(intent)

        code += \
            """
              agent.handleRequest(intentMap);
            });
            
            module.exports = router;
            """
        return code