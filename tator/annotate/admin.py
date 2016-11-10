from django.contrib import admin

from .models import Query, Annotation, UserResponse, HtmlMessage


class QueryAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'count'
    ]

    
class AnnotationInline(admin.StackedInline):
    model = Annotation
    can_delete = False


class UserResponseAdmin(admin.ModelAdmin):
    list_display = [
        'query',
        'user',
        'annotation'
    ]
    readonly_fields = [
        'query',
        'user',
        'annotation'
    ]

class HtmlMessageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
    ]


admin.site.register(Query, QueryAdmin)
admin.site.register(UserResponse, UserResponseAdmin)
admin.site.register(HtmlMessage, HtmlMessageAdmin)

