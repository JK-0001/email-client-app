import base64
import math
from allauth.socialaccount.models import SocialToken, SocialApp
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

def get_gmail_service(token: SocialToken):
    # SocialToken.token_secret is a refresh token in case of Google
#     assert token.token_secret, 'Can not use SocialToken without refresh token!'

    google_app = SocialApp.objects.filter(provider='google').first()
    assert google_app, 'Must create SocialApp for google provider first!'

    # this is simple example, but you need to use some credentials storage 
    # instead of SocialToken or manage how to sync creads data to SocialToken
    credentials = Credentials(
         token=token.token,
         refresh_token=token.token_secret,
         token_uri='https://oauth2.googleapis.com/token',
         client_id=google_app.client_id,
         client_secret=google_app.secret)

    service = build('gmail', 'v1', credentials=credentials)
    
    userProfile = service.users().getProfile(userId='me').execute()

    result = service.users().messages().list(userId='me', maxResults=100).execute() 
    pageToken = result['nextPageToken']
    senderArray = []

    for msg in result['messages']:
        txt = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From']).execute()
        payload = txt['payload']
        headers = payload['headers']
        for d in headers:
            if d['name'] == 'From': 
                senderArray.append(d['value'])
            
    sender = set(senderArray)
    
    for i in range(3):
        
        nextPageResult = service.users().messages().list(userId='me', maxResults=100, pageToken=pageToken).execute() 
        
        messages = nextPageResult.get("messages")

        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From']).execute()
            payload = txt['payload']
            headers = payload['headers']
            for d in headers:
                if d['name'] == 'From': 
                    senderArray.append(d['value'])
            
        sender = set(senderArray)
        pageToken = nextPageResult['nextPageToken']

    print(sender)
    print(len(sender))
        
    return messages


