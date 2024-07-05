from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from property.models import Property, Reservation
from property.serializers import PropertiesListSerializer, PropertiesDetailSerializer, ReservationsListSerializer
from useraccount.models import User
from .serializers import UserSerializer,PropertySerializer,ReservationSerializer


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
  pass 

@api_view(['POST'])
def update_user(request):
  pass

@api_view(['DELETE'])
def delete_user(request):
  pass

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


@api_view(['POST'])
def update_property(request):
  pass


@api_view(['DELETE'])
def delete_property(request):
  pass


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def all_reservations(request):
  reservation = Reservation.objects.all()
  reservationData = ReservationSerializer(reservation,many=True)
  
  return Response(reservationData.data)

@api_view(['GET'])
def get_reservation(request):
  pass

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
def delete_reservation(request):
  pass


