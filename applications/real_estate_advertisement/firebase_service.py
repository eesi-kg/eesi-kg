import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class FirebaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Initialize Firebase Admin SDK with your service account key
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
            raise

    def send_notification(self, token, title, body, data=None):
        """
        Send notification to a specific device
        
        Args:
            token (str): FCM token of the device
            title (str): Notification title
            body (str): Notification body
            data (dict): Additional data to send with notification
        """
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=token
            )
            response = messaging.send(message)
            logger.info(f"Successfully sent notification: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")
            raise

    def send_multicast_notification(self, tokens, title, body, data=None):
        """
        Send notification to multiple devices
        
        Args:
            tokens (list): List of FCM tokens
            title (str): Notification title
            body (str): Notification body
            data (dict): Additional data to send with notification
        """
        try:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                tokens=tokens
            )
            response = messaging.send_multicast(message)
            logger.info(f"Successfully sent multicast notification: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to send multicast notification: {str(e)}")
            raise

    def send_topic_notification(self, topic, title, body, data=None):
        """
        Send notification to a topic
        
        Args:
            topic (str): Topic name
            title (str): Notification title
            body (str): Notification body
            data (dict): Additional data to send with notification
        """
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                topic=topic
            )
            response = messaging.send(message)
            logger.info(f"Successfully sent topic notification: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to send topic notification: {str(e)}")
            raise 