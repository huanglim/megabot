from watson_developer_cloud import ConversationV1

class WatsonConversion(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self,app):
        self.app = app
        self.conversation = ConversationV1(
            username = app.config.get('WATSON_CONV_USER'),
            password = app.config.get('WATSON_CON_PASS'),
            version = app.config.get('WATSON_CON_VER')
        )

    def get_response(self,input):
        response = self.conversation.message(
            workspace_id = self.app.config.get('WATSON_CON_WORKSPACE_ID'),
            input ={
                'text':input
            }
        )
        return str((response["output"]["text"][0]))

