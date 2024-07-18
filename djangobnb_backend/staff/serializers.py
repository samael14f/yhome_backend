from rest_framework import serializers

from property.models import Property, Reservation,Complaints, Reviews 

from useraccount.models import User ,StaffMembers

class UserSerializer(serializers.ModelSerialize):
  class Meta:
    model = User
    fields = ('id','name','avatar_url','email',)

class StaffMemberSerialiizer(serializers.ModelSerializer):
  user_id = UserSerializer(read_only=True,many=False)
  class Meta:
    model = StaffMembers
    fields = '__all__'
    
    
