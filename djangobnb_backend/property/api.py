from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from .forms import PropertyForm
from .models import Property, Reservation, Reviews, Complaints ,PropertyVerification, Transaction 
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer, ReservationsListSerializer,ReservationSerializer, ReviewSerializer ,ComplaintSerializer
from useraccount.models import User,StaffMembers
from rest_framework.response import Response
import stripe
import json
from .payment import client
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from djangobnb_backend.settings import EMAIL_HOST_USER

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    #
    # Auth

    try:
        token = request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
        token = AccessToken(token)
        user_id = token.payload['user_id']
        user = User.objects.get(pk=user_id)
    except Exception as e:
        user = None

    #
    #

    favorites = []
    properties = Property.objects.filter(is_verified=True)

    #
    # Filter

    is_favorites = request.GET.get('is_favorites', '')
    landlord_id = request.GET.get('landlord_id', '')

    country = request.GET.get('country', '')
    category = request.GET.get('category', '')
    checkin_date = request.GET.get('checkIn', '')
    checkout_date = request.GET.get('checkOut', '')
    bedrooms = request.GET.get('numBedrooms', '')
    guests = request.GET.get('numGuests', '')
    bathrooms = request.GET.get('numBathrooms', '')

    print('country', country)

    if checkin_date and checkout_date:
        exact_matches = Reservation.objects.filter(start_date=checkin_date) | Reservation.objects.filter(end_date=checkout_date)
        overlap_matches = Reservation.objects.filter(start_date__lte=checkout_date, end_date__gte=checkin_date)
        all_matches = []

        for reservation in exact_matches | overlap_matches:
            all_matches.append(reservation.property_id)
        
        properties = properties.exclude(id__in=all_matches)

    if landlord_id:
        properties = properties.filter(landlord_id=landlord_id,is_verified=True)

    if is_favorites:
        properties = properties.filter(favorited__in=[user],is_verified=True)
    
    if guests:
        properties = properties.filter(guests__gte=guests,is_verified=True)
    
    if bedrooms:
        properties = properties.filter(bedrooms__gte=bedrooms,is_verified=True)
    
    if bathrooms:
        properties = properties.filter(bathrooms__gte=bathrooms,is_verified=True)
    
    if country:
        properties = properties.filter(country=country,is_verified=True)
    
    if category and category != 'undefined':
        properties = properties.filter(category=category,is_verified=True)
    
    #
    # Favorites
        
    if user:
        for property in properties:
            if user in property.favorited.all():
                favorites.append(property.id)

    #
    #

    serializer = PropertiesListSerializer(properties, many=True)

    return JsonResponse({
        'data': serializer.data,
        'favorites': favorites
    })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)

    serializer = PropertiesDetailSerializer(property, many=False)

    return JsonResponse(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
    print(pk)
    property = Property.objects.get(pk=pk)
    # property = Property.objects.get(pk=r)
    reservations = property.reservations.all()

    serializer = ReservationsListSerializer(reservations, many=True)

    return Response(serializer.data)


@api_view(['POST', 'FILES'])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)

    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()
        
        print(property.id)
        propertyObj = Property.objects.get(pk=property.id)
       # staff = StaffMembers.objects.filter(country=property.country).first()
        email = propertyObj.landlord.email
        print(email)
        staffMember = User.objects.get(is_superuser=True)
        PropertyVerification.objects.create(property=propertyObj,verified_staff=staffMember,owner=request.user)
        subject = "Property listing"
        
        message = f"hey {propertyObj.landlord.name if propertyObj.landlord.name else 'Yhome user'} your property is listed for verification the admin will verify the property shortly "
        from_mail = EMAIL_HOST_USER
        send_mail(subject,message,from_mail,[email],fail_silently=False,)
        
        return JsonResponse({'success': True})
    else:
        print('error', form.errors, form.non_field_errors)
        return JsonResponse({'errors': form.errors.as_json()}, status=400)


@api_view(['POST'])
def book_property(request, pk):
    try:
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        number_of_nights = request.POST.get('number_of_nights', '')
        total_price = request.POST.get('total_price', '')
        guests = request.POST.get('guests', '')

        property = Property.objects.get(pk=pk)

        Reservation.objects.create(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user
        )

        return JsonResponse({'success': True})
    except Exception as e:
        print('Error at e ', e)

        return JsonResponse({'success': False})


@api_view(['POST'])
def toggle_favorite(request, pk):
    property = Property.objects.get(pk=pk)

    if request.user in property.favorited.all():
        property.favorited.remove(request.user)

        return JsonResponse({'is_favorite': False})
    else:
        property.favorited.add(request.user)

        return JsonResponse({'is_favorite': True})
        
        
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_reservation(request,pk):
  print(pk)
  reservation = Reservation.objects.get(pk=pk)
  reservationData = ReservationSerializer(reservation,many=False)
  return Response(reservationData.data)
  
@api_view(['GET']) 
@authentication_classes([])
@permission_classes([])
def get_reviews(request,pk):
  propertyObj = Property.objects.get(pk=pk)
  print(propertyObj)
  reviews = Reviews.objects.filter(property=propertyObj)
  reviewsData = ReviewSerializer(reviews,many=True)
  return Response(reviewsData.data)
  

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def post_review(request):
  
  propertyId = request.POST.get('propertyId')
  print(propertyId)
  property = Property.objects.get(pk=propertyId)
  body = request.POST.get('body')
  print(body)
  try:
    token = request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
    token = AccessToken(token)
    user_id = token.payload['user_id']
    user = User.objects.get(pk=user_id)
    print(user_id)
  except Exception as e:
    print(e)
  print(user)
  
  Reviews.objects.create(body=body, review_by=user,property=property)
  
  return Response({"success":True})
  
  
  
  
  
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
@csrf_exempt
def create_checkout_session(request):
  try:
    details = json.loads(request.body)
    print(details)
    data = dict()
    data['amount'] = int(details['id']['amount']) * 100 * 83
    data['currency'] = 'INR'
    
    payment = client.order.create(data=data)
    print('dkdkd',payment)
    return Response({"success":True,"data":payment})
  except Exception as e:
    print('kdkdk',e)
    return Response({'success':False,'error':'validation error'})

  
   
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
@csrf_exempt
def complete_payment(request):
  try :
    details = json.loads(request.body)
    #print("details ",details)
    
    razorpay_order_id = details['razorpay_order_id']
    razorpay_payment_id = details['razorpay_payment_id']
    razorpay_signature = details['razorpay_signature']
    reservation_id = details['reservation_id']['id']
    
    reservation = Reservation.objects.get(pk=reservation_id)
    user = User.objects.get(pk=reservation.created_by.id)
    
    Transaction.objects.create(order_id=razorpay_order_id,payment_id=razorpay_payment_id,signature=razorpay_signature,user=user,reservation_id=reservation)
    reservation.paid_status = True
    reservation.save()
    
   # print(reservation,user)
    
    return Response({"success":True})
  except Exception as e:
    print("error",e)
    return Response({"success":False,"error":"payment error occurred"})
    
    
  
  
'''
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
@csrf_exempt
def create_checkout_session(request):try
    
    try:
        data = json.loads(request.body)
        print(data)
        id_ = data['id']
        id = id_['id']
        print(id)
        reservation = Reservation.objects.get(pk=id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            
            customer_email=f'{reservation.created_by}',
            
          
            line_items=[
                {

                  'price_data': {
                    'currency':'inr',
                    'product_data' : {
                      'name': f'Yhome - {reservation.property}',
                      'description': f'The booking for {reservation.property} from {reservation.start_date} to {reservation.end_date} from Yhome ',
                      },
                    'unit_amount':int(reservation.total_price)*100,
                  },
                  'quantity': 1,
                },
            ],
            mode='payment',
            success_url=settings.DOMAIN_URL+ '?success=true',
            cancel_url=settings.DOMAIN_URL + '?canceled=true',
            
        )
        print(checkout_session)
        return redirect(checkout_session.url)
    except Exception as e:
        print(e)
        
    return Response({"success": True})
    
'''
   