from django import forms
from .models import Friendship

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = ['to_user']
        widgets = {
            'to_user': forms.HiddenInput()
        }

class FriendRequestActionForm(forms.Form):
    action = forms.ChoiceField(choices=(
        ('accept', 'Принять'),
        ('reject', 'Отклонить'),
    ))