from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from property.models import Property, Reservation
from property.serializers import PropertiesListSerializer, PropertiesDetailSerializer, ReservationsListSerializer
from useraccount.models import User
from .serializers import UserSerializer,PropertySerializer,ReservationSerializer,GetReservationSerializer
from .forms import UserForm
from property.forms import PropertyForm




@api_view((['GET']))
@authentication_classes([])
@permission_classes([])
def admin_dashboard(request):
 
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

