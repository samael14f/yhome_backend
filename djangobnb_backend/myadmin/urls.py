from django.urls import path, include
from . import api

urlpatterns = [
  
  path('',api.admin_dashboard,name="admin-dashboard"),
  path('get-user/<uuid:pk>',api.get_user,name='get-user'),
  path('create-user/',api.create_user,name='create-user'),
  path('update-user/',api.update_user,name='update-user'),
  path('delete-user/',api.delete_user,name='delete-user'),
  path('all-properties/',api.all_properties,name='all-properties'),
  path('get-property/<uuid:pk>',api.get_property,name='get-property'),
  path('get-property-list/<uuid:pk>',api.get_property_list,name='get-property-list'),
  path('create-property/',api.create_property,
  name='create-property'),
  path('update-property/',api.update_property,name='update-property'),
  path('delete-property/',api.delete_property,name='delete-property'),
  path('all-reservations/',api.all_reservations,name='all-reservations'),
  path('get-reservation-list/<uuid:pk>',api.get_reservation_list,name='get-reservation-list'),
  path('get-reservation/<uuid:pk>',api.get_reservation,name='get-reservation'),
  path('create-reservation/',api.create_reservation,name='create-reservation'),
  path('delete-reservation/',api.delete_reservation,name='delete-reservation'),
  
  ]