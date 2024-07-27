from django.urls import path

from . import api


urlpatterns = [
    path('', api.properties_list, name='api_properties_list'),
    path('create/', api.create_property, name='api_create_property'),
    path('<uuid:pk>/', api.properties_detail, name='api_properties_detail'),
    path('<uuid:pk>/book/', api.book_property, name='api_book_property'),
    path('<uuid:pk>/reservations/', api.property_reservations, name='api_property_reservations'),
    path('<uuid:pk>/toggle_favorite/', api.toggle_favorite, name='api_toggle_favorite'),
    path('reservation/<uuid:pk>',api.get_reservation,name='reservation'),
    path('get-reviews/<uuid:pk>',api.get_reviews,
    name='get-reviews'),
    path('post-review/',api.post_review,name="post-review"),
    path('create-checkout/',api.create_checkout_session,name='create_checkout_session'),
    path('complete-payment/',api.complete_payment,name='complete-payment'),
    
]