from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from property.models import Property, Reservation, Reviews, Complaints,PropertyVerification
from property.serializers import PropertiesListSerializer, PropertiesDetailSerializer,PropertyVerificationDetailSerializer,ReservationsListSerializer,RequestSerializer
from useraccount.models import User
from .serializers import UserSerializer,PropertySerializer,ReservationSerializer,GetReservationSerializer
from .forms import UserForm
from property.forms import PropertyForm

from django.core.mail import send_mail

from djangobnb_backend.settings import EMAIL_HOST_USER


@api_view((['GET']))
@authentication_classes([])
@permission_classes([])
def admin_dashboard(request):
 
  is_staff = request.GET.get('is_staff','')
  if is_staff:
    users = User.objects.filter(is_staff=True)
  else:
    users = User.objects.all()
 
  userData = UserSerializer(users,many=True)
  
  
  return Response(userData.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_user(request,pk):
  user = User.objects.get(pk=pk)
  
  userData = UserSerializer(user,many=False)
  return Response(userData.data)
  
  
@api_view(['POST'])
def create_user(request):
  if request.method == "POST":
    if User.objects.filter(email=request.POST['email']).exists():
      return Response({"success":False,"errors":['email already exists']})
    User.objects.create_user(email=request.POST['email'], password=request.POST['password'])
    
  return Response({"success":True})

@api_view(['POST','FILE'])
@authentication_classes([])
@permission_classes([])
def update_user(request,pk):
  if request.method=="POST":
    user = User.objects.get(pk=pk)
    userForm = UserForm(request.POST,request.FILES,instance=user)
    if userForm.is_valid():
      userForm.save()
   
      return Response({'Success':True})
    else:
      print('error', userForm.errors, userForm.non_field_errors)
      return Response({'errors': userForm.errors.as_json()}, status=400)
  
  
  
@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([])
def delete_user(request,pk):
  if request.method=="DELETE":
   user = User.objects.get(pk=pk)
   user.delete()
   print('deleted')
  
  return Response({"success":True})
  
  

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def all_properties(request):
  properties = Property.objects.all()
  propertiesData = PropertiesListSerializer(properties,many=True)
  return Response(propertiesData.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_property_list(request,pk):
  user = User.objects.get(pk=pk)
  if Property.objects.filter(landlord=user).exists():
    properties = Property.objects.filter(landlord=user)
    propertiesData = PropertiesListSerializer(properties,many=True)
    return Response(propertiesData.data)
    
  else:
    return Response(False)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_property(request,pk):
  propertyObj = Property.objects.get(pk=pk)
  propertyData = PropertySerializer(propertyObj,many=False)
  return Response(propertyData.data)

@api_view(['POST'])
def create_property(request):
  pass


@api_view(['POST','FILES'])
@authentication_classes([])
@permission_classes([])
def update_property(request,pk):
  propertyObj = Property.objects.get(pk=pk)
  propertyForm = PropertyForm(request.POST,request.FILES, instance=propertyObj)
  if propertyForm.is_valid():
    propertyForm.save()
    return JsonResponse({'success': True})
  else:
    print('error', form.errors, form.non_field_errors)
    return JsonResponse({'errors':form.errors.as_json()}, status=400)

    

@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([])
def delete_property(request,pk):
  if request.method == "DELETE":
    propertyObj = Property.objects.get(pk=pk)
    propertyObj.delete()
  return Response({"success":True})
    
    
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def all_reservations(request):
  reservation = Reservation.objects.all()
  reservationData = ReservationSerializer(reservation,many=True)
  
  return Response(reservationData.data)

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_reservation(request,pk):
  reservation = Reservation.objects.get(pk=pk)
  reservationData = GetReservationSerializer(reservation,many=False)
  return Response(reservationData.data)
  
  
  
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_reservation_list(request,pk):
  user = User.objects.get(pk=pk)
  if Reservation.objects.filter(created_by=user):
    
    reservationList = Reservation.objects.filter(created_by=user)
    reservationsData = ReservationSerializer(reservationList,many=True)
    return Response(reservationsData.data)
  else:
    return Response(False)
    
    
    
@api_view(['POST'])
def create_reservation(request):
  pass

@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([])
def delete_reservation(request,pk):
  if request.method == "DELETE":
    reservation = Reservation.objects.get(pk=pk)
    reservation.delete()
  return Response({"success":True})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_non_staffs(request):
  non_staffs = User.objects.filter(is_staff=False)
  
  non_staffs_list = []
  
  for user in non_staffs:
    user_obj = dict()
    user_obj['value'] = user.id
    user_obj['label'] = user.email
    non_staffs_list.append(user_obj)
  print(non_staffs_list)
  return Response(non_staffs_list)
    
    
    

    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_request_list(request):
  property_request_list = PropertyVerification.objects.filter(is_canceled=False,is_verified_by_admin=False)
  request_list = RequestSerializer(property_request_list,many=True)
  
  return Response(request_list.data)
  

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_property_request(request,pk):
  property_request = PropertyVerification.objects.get(pk=pk)
  request_property = RequestSerializer(property_request,many=False)
  return Response(request_property.data)
  
  
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def cancel_request(request,pk):
  if request.method == "POST":
    property_request = PropertyVerification.objects.get(pk=pk)
    propertyObj = Property.objects.get(pk=property_request.property.id)
    property_request.is_canceled = True
    property_request.save()
    subject = "Property Verification"
    
    email = propertyObj.landlord.email
    name = propertyObj.landlord.name
    message = f"hey { name if name else 'Yhome user' } your property has been verified by admin and is  not fit to be yhome please correct the details re host the property"
    from_mail = EMAIL_HOST_USER
    send_mail(subject,message,from_mail,[email],fail_silently=False,)
    
    
    return Response({"success":True})
    
    
  
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def accept_request(request,pk):
  if request.method == "POST":
    property_request = PropertyVerification.objects.get(pk=pk)
    property = Property.objects.get(pk=property_request.property.id)
    property.is_verified = True
    property_request.is_verified_by_staff = True
   
    property_request.is_verified_by_admin = True
    property.save()
    property_request.save()
    
    subject = "Property Verification"
    name = property.landlord.name
    email = property.landlord.email
    message = f" hey { name  if name else 'Yhome user' } your property has been verified by admin and is fit to be yhome thankyou for using Yhome"
    from_mail = EMAIL_HOST_USER
    send_mail(subject,message,from_mail,[email],fail_silently=False,)
    
   
    return Response({"success":True})
    
    
