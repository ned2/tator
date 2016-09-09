from django.contrib import admin

# Register your models here.

from .models import Query, Annotation, SkippedAnnotation


class QueryAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'count'
    ]

class AnnotationAdmin(admin.ModelAdmin):
    list_display = [
        'get_query_text',
        'user',
    ]

    def get_query_text(self, obj):
        return obj.query.text
    get_query_text.short_description = 'Query Annotated'

    

admin.site.register(Query, QueryAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(SkippedAnnotation)
