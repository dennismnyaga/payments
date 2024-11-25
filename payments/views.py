from rest_framework.views import APIView
from rest_framework.response import Response
import paypalrestsdk
from rest_framework.views import APIView
from rest_framework import status
from django.template import loaders
from django.shortcuts import render, get_object_or_404
from .models import *
from django.conf import settings 
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests

# Initialize PayPal SDK environment
paypalrestsdk.configure({
  "mode": "live",  # sandbox or live
  "client_id": "YOUR_PAYPAL_CLIENT_ID",
  "client_secret": "YOUR_PAYPAL_CLIENT_SECRET"
})

class CreateOrderView(APIView):
    def post(self, request):
        # Example request structure can be passed from frontend
        cart = request.data.get('cart', {})
        # Handle creating an order
        try:
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [{
                    "amount": {
                        "total": "100.00",  # Add logic for dynamic amount from cart
                        "currency": "USD"
                    },
                    "description": "Purchase from shop."
                }],
                "redirect_urls": {
                    "return_url": "http://localhost:8000/payment/execute",
                    "cancel_url": "http://localhost:8000/payment/cancel"
                }
            })

            if payment.create():
                # Respond with payment details
                return Response(payment.to_dict(), status=status.HTTP_201_CREATED)
            else:
                return Response(payment.error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentService(APIView):
    def post(self, request):
        print('Requst data ', request.data)
        return Response()
    

class CaptureOrderView(APIView):
    def post(self, request, order_id):
        # Capture payment for the order
        try:
            payment = paypalrestsdk.Payment.find(order_id)
            if payment.execute({"payer_id": request.data['payer_id']}):  # Execute with payer_id from frontend
                return Response(payment.to_dict(), status=status.HTTP_200_OK)
            else:
                return Response(payment.error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def index(request):
    repository = CodeRepository.objects.order_by('-created_at').first()  # Fetch the latest repository
    return render(request, 'payments/index.html', {'repository': repository})


def purchase_repository(request, repository_id):
    repository = get_object_or_404(CodeRepository, id=repository_id)
    context = {
        'repository': repository,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID 
    }
    return render(request, 'payments/index.html', context)


@csrf_exempt  # Use CSRF exemption for API-like endpoints (but secure it in production)
def save_buyer_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        if email:
            # Save the email to the Buyers model
            Buyers.objects.create(email=email)
            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Email is required"}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)


def send_github_invitation(email, github_repo_url):
    # Extract the owner and repo name from the GitHub URL
    repo_owner, repo_name = github_repo_url.split('/')[-2:]

    # GitHub API endpoint to invite a collaborator
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/collaborators/{email}"

    headers = {
        'Authorization': f'token {settings.GITHUB_TOKEN}',  # GitHub token from settings
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.put(api_url, headers=headers)

    if response.status_code == 201:
        print("GitHub invitation sent successfully.")
    else:
        print("Failed to send GitHub invitation:", response.json())


def send_github_invitation(email, github_repo_url):
    # Extract the owner and repo name from the GitHub URL
    repo_owner, repo_name = github_repo_url.split('/')[-2:]

    # GitHub API endpoint to invite a collaborator
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/collaborators/{email}"

    headers = {
        'Authorization': f'token {settings.GITHUB_TOKEN}',  # GitHub token from settings
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.put(api_url, headers=headers)

    if response.status_code == 201:
        print("GitHub invitation sent successfully.")
    else:
        print("Failed to send GitHub invitation:", response.json())