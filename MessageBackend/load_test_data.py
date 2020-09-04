from message_backend.app import create_app
from datetime import datetime
from message_backend.models import MessageModel


if __name__ == '__main__':
    application = create_app()
    application.app_context().push()

    # Create some test data
    test_data = [
        ('bruce', "bruce", '+2344', '2445ss', datetime.now(), 'test',
         '0', 1, 4, datetime.now(), datetime.now()),
        ('stephen', "stephen", '+2344', '2445ss', datetime.now(), 'test',
         'sent', 0, 5, datetime.now(), datetime.now()),
    ]
    for username, message, phoneNumber, messageSid, creation, typeMessage,\
            status, sent, retry, sentTimestamp, deliveredTimestamp\
            in test_data:
        message = MessageModel(
            username=username, message=message, phoneNumber=phoneNumber,
            creation=creation, messageSid=messageSid, status=status,
            typeMessage=typeMessage, sent=sent, retry=retry,
            sentTimestamp=sentTimestamp,
            deliveredTimestamp=deliveredTimestamp)
        application.db.session.add(message)

    application.db.session.commit()
