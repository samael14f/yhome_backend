from django.forms import ModelForm
from useraccount.models import User



class UserForm(ModelForm):
  class Meta :
    model = User
    fields = ('name','avatar',)
    
    
