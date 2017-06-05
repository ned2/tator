from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from .models import Query, Annotation, UserResponse, HtmlMessage, Skipped


def get_instance_admin_url(instance):
    lookup = 'admin:{0}_{1}_change'.format(instance._meta.app_label,
                                           instance._meta.model_name)
    admin_url = reverse(lookup, args=(instance.pk,))
    return admin_url

def linkify(url, text):
    return format_html('<a href="{url}">{text}</a>', url=url, text=text)


class QueryAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'count'
    ]

class AnnotationAdmin(admin.ModelAdmin):
    list_display = [
        'response',
    ]

    readonly_fields = [
        'is_geo',
        'loc_type',
        'query_type',
    ]
    
class UserResponseAdmin(admin.ModelAdmin):
    list_display = [
        'query',
        'user',
        '__str__',
    ]
    readonly_fields = [
        'query',
        'user',
        'annotation'
    ]

class SkippedAdmin(admin.ModelAdmin):
    list_display = [
        'query',
        'description',
        'response'
    ]
    readonly_fields = ['description']
    
    def query(self, obj):
        url = get_instance_admin_url(obj.response.query)
        return linkify(url, '"{}"'.format(obj.response.query.text)) 
    

class HtmlMessageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
    ]


admin.site.register(Query, QueryAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(UserResponse, UserResponseAdmin)
admin.site.register(Skipped, SkippedAdmin)
admin.site.register(HtmlMessage, HtmlMessageAdmin)

