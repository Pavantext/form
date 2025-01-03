import requests
import json
from django.core.mail import send_mail
from django.conf import settings
import logging
from django.urls import reverse
from .views import encrypt_data  # Import the encryption function

logger = logging.getLogger(__name__)

def fetch_users():
    """Fetch users data from the API"""
    api_url = "https://mocki.io/v1/d7b3e61b-bef1-4297-b4c6-a1ef39166808"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        users = response.json()
        logger.info(f"Successfully fetched {len(users)} users from API")
        return users
    except requests.RequestException as e:
        logger.error(f"Error fetching users: {e}")
        return []

def send_whatsapp_message(phone_number, message):
    """Send WhatsApp message using Aisensy API"""
    url = "https://api.aisensy.com/whatsapp/campaign/send"
    
    headers = {
        "Content-Type": "application/json",
        "apikey": settings.AISENSY_API_KEY
    }
    
    payload = {
        "campaignName": "feedback_notification",
        "destination": phone_number,
        "userName": "State of Equality",
        "template": {
            "name": "statueofequality",
            "language": {
                "code": "en"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": message.split()[1]  # This will get the name
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        logger.info(f"Attempting to send WhatsApp message to {phone_number}")
        logger.info(f"WhatsApp Payload: {json.dumps(payload, indent=2)}")  # Add this for debugging
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        logger.info(f"WhatsApp API Response: {response_data}")
        return True
    except requests.RequestException as e:
        logger.error(f"Error sending WhatsApp message to {phone_number}: {e}")
        logger.error(f"Response content: {getattr(e.response, 'text', 'No response content')}")
        return False

def send_email(email, subject, message):
    """Send email using Django's email system"""
    try:
        logger.info(f"Attempting to send email to {email}")
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        logger.info(f"Successfully sent email to {email}")
        return True
    except Exception as e:
        logger.error(f"Error sending email to {email}: {e}")
        return False

def send_notifications(message, subject="Notification", context=None):
    """Send notifications to all users"""
    users = fetch_users()
    results = {
        "success": [],
        "failed": []
    }
    
    if not users:
        logger.error("No users found to send notifications")
        return results
    
    for user in users:
        user_name = user.get("name", "User")
        user_results = {
            "name": user_name,
            "whatsapp": False,
            "email": False
        }
        
        # Create personalized message for this user
        personalized_message = f"Thank you {user_name} for visiting State of Equality, please let us know how we can improve your experience by giving us feedback"
        if context:
            # Create data dictionary for encryption
            data = {
                'username': user_name,
                'phone': user.get('phone', ''),
                'email': user.get('email', ''),
                'location': user.get('location', '')
            }
            
            # Encrypt the data
            encrypted_data = encrypt_data(data)
            
            # Create the feedback URL with encrypted data
            feedback_url = f"https://pavanpython123.pythonanywhere.com/?data={encrypted_data}"
            personalized_message = f"{personalized_message} {feedback_url}"
        
        # Send WhatsApp message
        if "phone" in user and user["phone"]:
            phone = user["phone"].strip()
            if not phone.startswith('+'):
                phone = '+91' + phone
            user_results["whatsapp"] = send_whatsapp_message(phone, personalized_message)
            
        # Send email
        if "email" in user and user["email"]:
            user_results["email"] = send_email(user["email"], subject, personalized_message)
            
        if user_results["whatsapp"] or user_results["email"]:
            results["success"].append(user_results)
        else:
            results["failed"].append(user_results)
    
    logger.info(f"Notification results: {json.dumps(results, indent=2)}")
    return results