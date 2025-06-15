from .models import Articles
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea

class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'anounce']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Заголовок (до 25 символов)'
            }),
            'anounce': TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Описание (до 200 символов)'
            }),
        }
