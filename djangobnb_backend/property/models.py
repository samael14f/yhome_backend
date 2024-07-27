import uuid

from django.conf import settings
from django.db import models

from useraccount.models import User


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    guests = models.IntegerField()
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    favorited = models.ManyToManyField(User, related_name='favorites', blank=True)
    image = models.ImageField(upload_to='uploads/properties')
    is_verified = models.BooleanField(default=False)
    address = models.TextField(default='')
    license = models.FileField(upload_to='uploads/properties/licence',default='')
    landlord = models.ForeignKey(User, related_name='properties', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return f'{settings.WEBSITE_URL}{self.image.url}'
    def license_url(self):
        if self.license == '':
          return f'No license provided for this property'
        return f'{settings.WEBSITE_URL}{self.license.url}'
    def __str__(self):
        return self.title
   

class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, related_name='reservations', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_nights = models.IntegerField()
    guests = models.IntegerField()
    total_price = models.FloatField()
    created_by = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_status = models.BooleanField(default=False)
    
    
    
class PropertyVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property,related_name="property_verification",on_delete=models.CASCADE)
    owner = models.ForeignKey(User,related_name="owned_by",on_delete=models.CASCADE)
    verified_staff = models.ForeignKey(User,related_name="verified_staff",on_delete=models.CASCADE)
    is_canceled = models.BooleanField(default=False)
    is_verified_by_staff = models.BooleanField(default=False)
    is_verified_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
class Reviews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    review_by = models.ForeignKey(User,related_name="review_by",on_delete=models.CASCADE)
    property = models.ForeignKey(Property,related_name='property_review',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
      ordering = ['-created_at']
    
    
class Complaints(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    complaint_by = models.ForeignKey(User,related_name='complaint_by',on_delete=models.CASCADE)
    property = models.ForeignKey(Property,related_name='property_complaint',on_delete=models.CASCADE)
    is_taken_action = models.BooleanField(default=False)
    
    
class Transaction(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    payment_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length = 255)
    signature = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,related_name='order_by',on_delete=models.SET_NULL,null=True)
    reservation_id = models.ForeignKey(Reservation,related_name='reservations_id',on_delete=models.SET_NULL,null=True)