from rest_framework import serializers

from property.models import Property, Reservation

from useraccount.models import User

List =( 'id', 'name', 'avatar_url','email','is_superuser'
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = List
        
        
class PropertySerializer(serializers.ModelSerializer):
  landlord = UserSerializer(read_only=True, many=False)
  class Meta:
    model = Property
    fields = (
            'id',
            'title',
            'description',
            'price_per_night',
            'image_url',
            'bedrooms',
            'bathrooms',
            'guests',
            'landlord',
            'description',
        )



  
class ReservationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reservation
    fields = (
            'id', 'start_date', 'end_date', 'number_of_nights', 'total_price', 'property','guests','created_at',
        )
    
    
      