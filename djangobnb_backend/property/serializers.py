from rest_framework import serializers

from .models import Property, Reservation, Complaints, Reviews ,PropertyVerification

from useraccount.serializers import UserDetailSerializer


class PropertiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url',
        )


class PropertiesDetailSerializer(serializers.ModelSerializer):
    landlord = UserDetailSerializer(read_only=True, many=False)

    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'description',
            'price_per_night',
            'image_url',
            'license_url',
            'bedrooms',
            'bathrooms',
            'guests',
            'landlord',
            'country',
            'address'
            
        )


class PropertyVerificationDetailSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'description',
            'price_per_night',
            'image_url',
            'license_url',
            'bedrooms',
            'bathrooms',
            'guests',
            'country',
            'address'
            
        )




class ReservationsListSerializer(serializers.ModelSerializer):
    property = PropertiesListSerializer(read_only=True, many=False)
    
    class Meta:
        model = Reservation
        fields = (
            'id', 'start_date', 'end_date', 'number_of_nights', 'total_price', 'property'
        )
        
        
class ComplaintSerializer(serializers.ModelSerializer):
  complaint_by = UserDetailSerializer(read_only=True,many=False)
  property = PropertiesDetailSerializer(read_only=True,many=False)
  class Meta:
    model = Complaints
    fields = '__all__'
    
    
    
class ReviewSerializer(serializers.ModelSerializer):
  review_by = UserDetailSerializer(read_only=True,many=False)
  property = PropertiesDetailSerializer(read_only=True,many=False)
  class Meta:
    model = Reviews
    fields = '__all__'
    
 
 
class RequestSerializer(serializers.ModelSerializer):
    owner = UserDetailSerializer(read_only=True, many=False)
    property = PropertyVerificationDetailSerializer(read_only=True,many=False)
    verified_staff = UserDetailSerializer(read_only=True,many=False)
    class Meta :
      model = PropertyVerification 
      fields = '__all__'
      
      
  
class ReservationSerializer(serializers.ModelSerializer):
  property = PropertiesDetailSerializer(read_only=True,many=False)

  class Meta:
    model = Reservation
    fields = (
            'id', 'start_date', 'end_date', 'number_of_nights', 'total_price', 'property','guests','created_at',
        )