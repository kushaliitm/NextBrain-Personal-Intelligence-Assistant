import os
from twilio.rest import Client


class WhatsAppChannel:
    def __init__(self):
        """
        Initializes the WhatsAppChannel with Twilio client.
        """
        self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

    def send_message(self, to_number, body):
        """
        Sends a WhatsApp message.
        """
        try:
            from_number = os.getenv('FROM_WHATSAPP_NUMBER')
            if not from_number:
                raise ValueError("FROM_WHATSAPP_NUMBER environment variable is not set")
            
            # Ensure both numbers have whatsapp: prefix
            if not from_number.startswith("whatsapp:"):
                from_number = f"whatsapp:{from_number}"
            
            if not to_number.startswith("whatsapp:"):
                to_number = f"whatsapp:{to_number}"
            
            print(f"Sending WhatsApp message from {from_number} to {to_number}")
            print(f"Message body: {body[:200]}...")  # Log first 200 chars
            
            message = self.client.messages.create(
                body=str(body),
                from_=from_number,
                to=to_number
            )
            print(f"Message sent successfully with SID: {message.sid}")
            return f"Message sent successfully with SID: {message.sid}"
        except Exception as e:
            error_msg = f"Failed to send message: {e}"
            print(f"ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return error_msg

    def receive_messages(self):
        """
        Receiving messages is handled via webhooks.

        This method is not implemented because incoming WhatsApp messages are typically received through a webhook configured in the Twilio account. 
        The webhook sends an HTTP request to our server when a message is received.
        """
        pass 