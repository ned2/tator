from django.forms import ModelForm, HiddenInput, RadioSelect

from .models import Annotation, Skipped


class AnnotationForm(ModelForm):
    class Meta:
        model = Annotation
        fields = '__all__'
        widgets = {
            'user': HiddenInput(),
            'query': HiddenInput(),
            'is_geo': RadioSelect(),
            'is_geo_expl': RadioSelect(),
            'query_type': RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(AnnotationForm, self).__init__(*args, **kwargs)

        # Django assumes that a booleanfield with no supplied value is
        # false. This makes sense for checkboxes, where not checking it is
        # false, but we've changed to Yes/No radio options, where a response is
        # required
        self.fields['is_geo'].required = True
        self.fields['is_geo_expl'].required = True


class SkippedForm(ModelForm):
    class Meta:
        model = Skipped
        fields = '__all__'
