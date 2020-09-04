# import os
import http.client
from datetime import datetime
from flask_restplus import Namespace, Resource, fields
from flask import abort, request
from message_backend.db import db
from message_backend import config
from message_backend.models import MessageModel
from message_backend.token_validation import validate_token_header


api_namespace = Namespace('api', description='API operations')


def authentication_header_parser(value):
    username = validate_token_header(value, config.PUBLIC_KEY)
    if username is None:
        abort(401)
    return username


# Input and output formats for Messages

authentication_parser = api_namespace.parser()
authentication_parser.add_argument('Authorization', location='headers',
                                   type=str,
                                   help='Bearer Access Token')


message_parser = authentication_parser.copy()
message_parser.add_argument('phoneNumber', type=str, required=True,
                            help='The reciver number')
message_parser.add_argument('message', type=str, required=True,
                            help='The message ')
message_parser.add_argument('typeMessage', type=str, required=True,
                            help='The message')

model = {
    'id': fields.Integer(),
    'username': fields.String(),
    'phoneNumber': fields.String(),
    'message': fields.String(),
    'typeMessage': fields.String(),
    'messageSid': fields.String(),
    'sent': fields.Integer(),
    'status': fields.String(),
    'creation': fields.DateTime(),
    'sentTimestamp': fields.DateTime(),
    'deliveredTimestamp': fields.DateTime()
}
message_model = api_namespace.model('Message', model)


@api_namespace.route('/me/message/')
class MeMessageListCreate(Resource):

    @api_namespace.doc('list_message')
    @api_namespace.expect(authentication_parser)
    @api_namespace.marshal_with(message_model, as_list=True)
    def get(self):
        '''
        Helps a user see his own message details.
        '''
        args = authentication_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        message = (
            MessageModel
            .query
            .filter(MessageModel.username == username)
            .order_by('id')
            .all()
        )
        return message

    @api_namespace.doc('create_message')
    @api_namespace.expect(message_parser)
    @api_namespace.marshal_with(message_model, code=http.client.CREATED)
    def post(self):
        '''
        Create a new message
        '''
        args = message_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        new_message = MessageModel(
            username=username,
            phoneNumber=args['phoneNumber'],
            typeMessage=args['typeMessage'],
            message=args['message'],
            creation=datetime.now()
        )
        db.session.add(new_message)
        db.session.commit()

        return new_message, http.client.CREATED


@api_namespace.route('/status/')
class Test(Resource):

    def post(self):
        message_sid = request.values.get('MessageSid', None)
        message_status = request.values.get('MessageStatus', None)

        message = (MessageModel
                   .query
                   .filter(MessageModel.messageSid == message_sid)
                   .first())

        message.status = message_status

        if message_status == 'sent':
            message.sentTimestamp = datetime.now()

        elif message_status == 'delivered':
            message.deliveredTimestamp = datetime.now()

        else:
            if message.retry == 5:
                message.status == 'error'
            else:
                message.status = '1'

        db.session.add(message)
        db.session.commit()

        return ('', 204)


search_parser = api_namespace.parser()
search_parser.add_argument('search', type=str, required=False,
                           help='Search using message type')


@api_namespace.route('/messages/')
class MessageList(Resource):

    @api_namespace.doc('list_messages')
    @api_namespace.marshal_with(message_model, as_list=True)
    @api_namespace.expect(search_parser)
    def get(self):
        '''
        Retrieves all the messages
        '''
        args = search_parser.parse_args()
        search_param = args['search']
        query = MessageModel.query
        if search_param:
            param = f'%{search_param}%'
            query = (query.filter(MessageModel.messageType.ilike(param)))
            # Old code, that it's not case insensitive in postgreSQL
            # query = (query.filter(MessageModel.text.contains(search_param)))

        query = query.order_by('id')
        messages = query.all()

        return messages
