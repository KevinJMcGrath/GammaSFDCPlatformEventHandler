from datetime import datetime

class User:
    def __init__(self, user):
        self.user_id = user.get('userId')
        self.firstname = user.get('firstName', '')
        self.lastname = user.get('lastName', '')
        self.displayname = user.get('displayName', '')
        self.email = user.get('email')
        self.username = user.get('username')

class Stream:
    def __init__(self, stream):
        self.stream_id = stream.get('streamId')
        self.type = stream.get('streamType', '')

class MessageEvent:
    def __init__(self):
        self.event_type = ''

class SentMessage(MessageEvent):
    def __init__(self, sent_msg):
        super().__init__()

        self.event_type = 'MESSAGESENT'
        self.message_id = sent_msg.get('messageId')
        self.timestamp = sent_msg.get('timestamp')
        self.msg_datetime = datetime.fromtimestamp(self.timestamp / 1000)
        self.data = sent_msg.get('data', None)
        self.message_ml = sent_msg.get('message', None)

class Message:
    sent_by: User or None
    message: MessageEvent or None
    stream: Stream or None

    def __init__(self, msg):
        self.message_id = msg['messageId']
        self.timestamp = msg['timestamp']
        self.sent_datetime = datetime.fromtimestamp(self.timestamp / 1000)
        self.message_type = msg['type']

        self.initiator: User = User(msg['initiator']['user'])

        self.sent_by = None
        self.message = None
        self.stream = None

        self.parse(msg)

    def parse(self, msg):
        if msg and 'payload' in msg:
            if 'messageSent' in msg['payload']:
                sent_msg = msg['payload']['messageSent']

                self.message = SentMessage(sent_msg['message'])
                self.stream = Stream(sent_msg['message']['stream'])
                self.sent_by = User(sent_msg['message']['user'])
