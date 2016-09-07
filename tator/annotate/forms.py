from django.forms import ModelForm, HiddenInput

from .models import Annotation


class AnnotationForm(ModelForm):
    class Meta:
        model = Annotation
        fields = '__all__'
        widgets = {'user': HiddenInput(), 'query': HiddenInput()}
