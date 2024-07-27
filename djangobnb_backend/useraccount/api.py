from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import User, OTPtoken
from .serializers import UserDetailSerializer
from django.views.decorators.csrf import csrf_exempt

from property.models import Property,Reservation 
from property.serializers import PropertiesListSerializer, PropertiesDetailSerializer, ReservationsListSerializer,ReservationSerializer
import json
from rest_framework.response import Response
from django.core.mail import send_mail

from djangobnb_backend.settings import EMAIL_HOST_USER

import math, random
from django.contrib.auth.hashers import check_password


def generateOTP() :

    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP




@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def landlord_detail(request, pk):
    user = User.objects.get(pk=pk)
    print(user)
    serializer = UserDetailSerializer(user, many=False)
    print(serializer)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def reservations_list(request):
    reservations = request.user.reservations.all()

    print('user', request.user)
    print(reservations)
    
    serializer = ReservationsListSerializer(reservations, many=True)
    return JsonResponse(serializer.data, safe=False)
    
    
@api_view(['POST','FILES'])
@authentication_classes([])
@permission_classes([])
def edit_profile(request,pk):
  user = User.objects.get(pk=pk)
  
  userData = UserDetailSerializer(instance=user,data=request.data)
  if userData.is_valid():
    userData.save()
  return Response({"success": True})
  
  
@csrf_exempt
def forgot_password(request):
  if request.method == 'POST':
    
    try :
      data = json.loads(request.body)
      email = data['email']
      if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        token = generateOTP()
        otp =  OTPtoken.objects.create(user=user,token=token)
        otp_id = otp.id
        print(data)
        print(type(data))
        print(otp.id)
        
        subject = "Forgot password"
        
        message = f"hey {user.name} here is the otp {token} for reseting the password of your Yhome account."
        from_mail = EMAIL_HOST_USER
        send_mail(subject,message,from_mail,[email],fail_silently=False,)
        
        
        return JsonResponse({"success":True,"otp_user":email})
      else:
        return JsonResponse({"success":False,"errors":['email not registered']})
    except Exception as e:
      print(e)
      return JsonResponse({"success":False,
       "errors":["unexpected error"]
      })
      
    
  
  
  

  
  
@csrf_exempt
def check_otp(request):
  if request.method == "POST":
    try :
      data = json.loads(request.body)
      print(data)
      email = data['email']
      user = User.objects.get(email=email)
      print(user)
      otp = OTPtoken.objects.filter(user=user).latest('created_at');
      token = ''
      
      token = otp.token
      print("ttt",token)
    
        
      print(token)
      if token == data['otp']:
        return JsonResponse({"success":True})
      else:
        return JsonResponse({'success':False,"errors":["otp not correct renter it"]})
  
    except Exception as e:
      print("expt",e)
      
      return JsonResponse({"success":False,
       "errors":["unexpected error"]
      })
      
    
    
@csrf_exempt
def reset_password(request):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      email = data['email']
      password = data['password1']
      print(data)
      user = User.objects.get(email=email)
      user.set_password(str(password))
      user.save()
      return JsonResponse({"success":True,"message":["Password changed successfully"]})
    except Exception as e:
      print(e)
      return JsonResponse({"success":False,"errors":"unexpected error occurred please refresh the page"})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_reservations(request):
  properties = Property.objects.filter(is_verified=True, landlord = request.user)
  
  reservation = []
  for property in properties:
    if Reservation.objects.filter(property=property).exists():
      reservation.append(Reservation.objects.filter(property=property))
      reservation_list
      
  ReservationsListSerializer(reservation)
  return Response({"success":True,"data":reservation_list.data})
  