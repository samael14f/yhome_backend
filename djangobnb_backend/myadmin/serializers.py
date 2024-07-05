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
  class Meta:
    model = Property
    fields = (
            'id',
            'title',
            'price_per_night',
            'image_url',
        )
        
  
class ReservationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reservation
    fields = (
            'id', 'start_date', 'end_date', 'number_of_nights', 'total_price', 'property'
        )
    
    
      