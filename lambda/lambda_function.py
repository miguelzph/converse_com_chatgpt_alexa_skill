# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

MAX_QUESTIONS_PER_CONVERSATION = 5
MAX_QUESTIONS_DAY = 15

ASSISTANT_RESPONSE_VOICE = 'Camila'
USER_VOICE = 'Ricardo'

DEFAULT_CONTEXT = 'Responda sucintamente e como se estivesse falando.'

OPENAI_MODEL = 'gpt-3.5-turbo'
OPENAPI_KEY = ''


import logging
import ask_sdk_core.utils as ask_utils

import os
import boto3
import json

from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_dynamodb.adapter import DynamoDbAdapter
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor


from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from ask_sdk_core.utils import is_intent_name

import message_constants as M_C

from skill_exceptions import RequestOpenAPIError, FullUsageLimitError

import time
from datetime import datetime, timezone, timedelta



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        
        response_builder = handler_input.response_builder
        
        session_attributes = handler_input.attributes_manager.session_attributes
        
        # mensagem na primeira visita
        if session_attributes["visits"] < 1:
            speak_output = M_C.LAUNCHER_OUTPUT_FIRST_VISIT
        else:
            speak_output = M_C.LAUNCHER_OUTPUT_NOT_FIRST_VISIT 

        
        session_attributes["visits"] = session_attributes["visits"] + 1
        
        handler_input.attributes_manager.session_attributes = session_attributes
        
        speak_reprompt = M_C.LAUNCHER_REPROMPT

        return (
            response_builder
                .speak(speak_output)
                .ask(speak_reprompt)
                .response
        )


class AskChatGPTIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AskChatGPTIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        start_time = time.time()
        
        session_attributes = handler_input.attributes_manager.session_attributes
        
        if session_attributes["questions_today"] >= MAX_QUESTIONS_DAY:
            
            speak_output = M_C.ASKCHATGPT_MAX_QUESTIONS_DAILY_REACHED.format(max_questions=MAX_QUESTIONS_DAY, interjection='até mais ver')
            return (handler_input.response_builder.speak(speak_output).response)

        
        from chatgpt_functions import add_prompt_message, streaming_response_from_chatgpt
        
        message_for_chatgpt = session_attributes["current_message"]
        
        if not message_for_chatgpt:
            # vazio = adiciona o contexto
            context = session_attributes['chosed_context']

            message_for_chatgpt.append(add_prompt_message(context, role="system"))
            
        if len(message_for_chatgpt) >= (MAX_QUESTIONS_PER_CONVERSATION * 2) + 1: # (user + assistant) * 2 + system

            speak_output = M_C.ASKCHATGPT_MAX_QUESTIONS_PER_CONVERSATION_REACHED.format(max_questions=MAX_QUESTIONS_PER_CONVERSATION)
            return (handler_input.response_builder.speak(speak_output).set_should_end_session(False).response)
        
        
        user_input = handler_input.request_envelope.request.intent.slots["query"].value
        
        message_for_chatgpt.append(add_prompt_message(user_input, role="user"))
        
        response_of_chatgpt = ''
        not_a_full_msg = ''
        first_run = True

        try:

            for sentence in streaming_response_from_chatgpt(message_for_chatgpt,
                                                            start_time=start_time, 
                                                            openapi_key=OPENAPI_KEY,
                                                            openai_model=OPENAI_MODEL):
                
                if isinstance(sentence, str):
                    response_of_chatgpt += sentence
                else: # significa que o tempo acabou
                    not_a_full_msg = M_C.ASKCHATGPT_ADD_NOT_A_FULL_RESPONSE
                    break
                
                if first_run: 
                    
                    speak_output = M_C.ASKCHATGPT_OUTPUT_CHANGE_VOICE.format(voice=ASSISTANT_RESPONSE_VOICE)

                    session_attributes["questions_today"] += 1
                    
                    first_run = False
        
        except Exception as e:
            if type(e).__name__ == 'RateLimitError':
                raise FullUsageLimitError
            else:
                raise RequestOpenAPIError
            
        
        speak_output = speak_output.format(response=response_of_chatgpt, not_a_full_msg=not_a_full_msg)
        
        message_for_chatgpt.append(add_prompt_message(response_of_chatgpt, role="assistant"))
        
        handler_input.attributes_manager.session_attributes = session_attributes
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .response
        )


def listen_conversation(messages: list, assistant_voice: str, user_voice: str):
    
    actual_conversation = ''
    
    for msg in messages:
        if msg['role'] == 'user':
            voice = user_voice
        elif msg['role'] == 'assistant':
            voice = assistant_voice
        else:
            continue
        
        actual_conversation += M_C.LISTEN_A_ROLE.format(talk=msg['content'], voice=voice)
        
        
    return actual_conversation


class ConversationActionsIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ConversationActionsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        response_builder = handler_input.response_builder

        session_attributes = handler_input.attributes_manager.session_attributes

        action = handler_input.request_envelope.request.intent.slots["conversation_action"].value
        
        if action == 'escutar':
            
            messages = session_attributes['current_message']
            
            if messages:
                conversation = listen_conversation(messages=messages, 
                                                    assistant_voice=ASSISTANT_RESPONSE_VOICE, 
                                                    user_voice=USER_VOICE)
                
                speak_output = M_C.LISTEN_OUTPUT.format(conversation=conversation)
            
            else:
                speak_output = M_C.LISTEN_EMPTY_CONVERSATION_OUTPUT
            
        elif action == 'finalizar':
            
            session_attributes['current_message'] = []
            
            handler_input.attributes_manager.session_attributes = session_attributes
            
            speak_output = M_C.END_A_CONVERSATION_OUTPUT

        return (
            response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = M_C.HELP_OUTPUT
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        
        # type: (HandlerInput) -> Response
        speak_output = M_C.CANCEL_OUTPUT.format(interjection='claro')

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = M_C.FALLBACK_OUTPUT
        
        speak_reprompt = M_C.LAUNCHER_REPROMPT

        return handler_input.response_builder.speak(speech).ask(speak_reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Você ativou " + intent_name + ", mas essa funcionalidade ainda não está disponível."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        if type(exception).__name__ == 'FullUsageLimitError':
            speak_output = M_C.ERRORS_OUTPUT_RATELIMITERROR_2_OPTION.format('barbaridade tche')
            return (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            
        elif type(exception).__name__ == 'RequestOpenAPIError':
            speak_output = M_C.ERRORS_OUTPUT_REQUESTAPIERROR
            
            return (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            
        else:
            speak_output = M_C.ERRORS_OUTPUT_DEFAULT
            
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )


class LoadDataInterceptor(AbstractRequestInterceptor):
    """Check if user is invoking skill for first time and initialize preset."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        session_attributes = handler_input.attributes_manager.session_attributes
        
        today = datetime.now().astimezone(timezone(timedelta(hours=-3))).strftime('%Y-%m-%d')

        if ('questions_today' not in persistent_attributes) or (persistent_attributes["last_date"] != today):
            session_attributes["questions_today"] = 0
        else:
            session_attributes["questions_today"] = persistent_attributes["questions_today"]

        session_attributes["last_date"] = today
        
        session_attributes["visits"] = persistent_attributes["visits"] if 'visits' in persistent_attributes else 0
        
        session_attributes["chosed_context"] = persistent_attributes["chosed_context"] if 'chosed_context' in persistent_attributes else DEFAULT_CONTEXT
        
        session_attributes["current_message"] = persistent_attributes["current_message"] if 'current_message' in persistent_attributes else []


class SaveDataInterceptor(AbstractResponseInterceptor):
    """Save persistence attributes before sending response to user."""
    def process(self, handler_input, response):

    #     # type: (HandlerInput, Response) -> None
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        session_attributes = handler_input.attributes_manager.session_attributes

        persistent_attributes["visits"] = session_attributes["visits"] 

        persistent_attributes["chosed_context"] = session_attributes["chosed_context"]

        persistent_attributes["last_date"] = session_attributes["last_date"]
        
        persistent_attributes["questions_today"] = session_attributes["questions_today"]
        
        persistent_attributes["current_message"] = session_attributes["current_message"]

        handler_input.attributes_manager.save_persistent_attributes()


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = StandardSkillBuilder(
    table_name=os.environ.get("DYNAMODB_PERSISTENCE_TABLE_NAME"), auto_create_table=False)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AskChatGPTIntentHandler())

sb.add_request_handler(ConversationActionsIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

# Interceptors
sb.add_global_request_interceptor(LoadDataInterceptor())

sb.add_global_response_interceptor(SaveDataInterceptor())

lambda_handler = sb.lambda_handler()