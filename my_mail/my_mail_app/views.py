from django.shortcuts import render
from django.http import HttpResponse
from requests import HTTPError
from get_mails import get_gmail_service
from allauth.socialaccount.models import SocialToken

# Create your views here.
def index(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def get_emails(request):
    # service = get_gmail_service(SocialToken.objects.first())
    service = get_gmail_service(SocialToken.objects.first())
    try:
        return HttpResponse("Hello")
    except HTTPError as err:
        print('GMAIL ACCESS CHECK ERROR:', err)