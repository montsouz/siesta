from calendar_api import create_calendar_event


def siesta_time(event, context):

    create_calendar_event()

    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'Okay! I set up some lunch time for you on your calendar. Enjoy, and take some rest',
            }
        }
    }

    return response
