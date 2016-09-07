from django.contrib import admin

# Register your models here.

from .models import Query, Annotation, SkippedAnnotation

admin.site.register(Query)
admin.site.register(Annotation)
admin.site.register(SkippedAnnotation)
