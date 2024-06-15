from django.http import JsonResponse
from django.contrib.auth import authenticate
from account.forms import *
from account.models import CustomUser
import json
from .tokens import create_jwt_pair_for_user, expire_tokens
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details_api(request):
    user = request.user
    data = {
        'firstname': user.first_name,
        'lastname': user.last_name,
        'email': user.email
    }
    return JsonResponse(data, status=200)

@csrf_exempt
def user_signup_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request body'}, status=400)
        
        form = SignupForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Your account has been created successfully. Please log in.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors':  json.loads(errors)}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed.'}, status=405)


@csrf_exempt
def user_login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request body'}, status=400)
        
        form = LoginForm(data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            # user = CustomUser.objects.get(id=7)
           
            if user is not None:
                expire_tokens(user)   

                # Using SIMPLE JWT to generate login tokens 
                tokens = create_jwt_pair_for_user(user)

                return JsonResponse({"message": "Login Successfull", "tokens": tokens}, status=405)
            else:
                return JsonResponse({'error': 'Invalid username or password.'}, status=401)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors':  json.loads(errors)}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed.'}, status=405)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout_api(request):
    # logout logic to delete/remove the access tokens 
    # if 'refresh_token' not in request.data:
    #     return JsonResponse({'error': 'Refresh token not provided'}, status=404)

    # refresh_token = request.data["refresh_token"]

    expire_tokens(request.user)    
    # try:
    #     token = RefreshToken(refresh_token)
    #     token.blacklist()

    #     OutstandingToken.objects.filter(user_id=request.user.id).delete() # Empty the record
    # except Exception as e:
    #     return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'message': 'Successfully logged out'}, status=200)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@csrf_exempt
def reset_password_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request body'}, status=400)
        
        form = ResetPasswordForm(data)
        if form.is_valid():
            username = form.cleaned_data['username']
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']

            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User does not exist.'}, status=404)

            user = authenticate(request, username=username, password=current_password)
            if user is not None:
                if current_password == new_password:
                    return JsonResponse({'error': 'New password should be different from the old one.'}, status=400)
                else:
                    user.set_password(new_password)
                    user.save()
                    return JsonResponse({'message': 'Password successfully changed. Please log in with your new password.'})
            else:
                return JsonResponse({'error': 'Incorrect account password.'}, status=401)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors':  json.loads(errors)}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed.'}, status=405)