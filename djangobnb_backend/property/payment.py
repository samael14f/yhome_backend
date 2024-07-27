from django.conf import settings 

import razorpay


client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET_KEY))