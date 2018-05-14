from watson_developer_cloud import AssistantV1
import logging

class WatsonConversion(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
            self.message = ''

    def init_app(self,app):
        self.app = app
        self.conversation = AssistantV1(
            username=app.config.get('WATSON_CONV_USER'),
            password=app.config.get('WATSON_CON_PASS'),
            version=app.config.get('WATSON_CON_VER'),
            url=app.config.get('WASTON_CON_URL')
        )

    def get_response(self,input):
        try:
            response = self.conversation.message(
                workspace_id = self.app.config.get('WATSON_CON_WORKSPACE_ID'),
                input ={
                    'text':input
                }
            )
        except Exception as e:
            logging.error('Error in waston Assistant: %s' %e)
            message = 'ops ... There got some problem with Megabot! Please try again! '
        else:
            message = str((response["output"]["text"][0]))

        return message

