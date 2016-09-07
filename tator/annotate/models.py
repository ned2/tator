from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


"""
TODO
 -- help strings for Annotation fields
"""


class Query(models.Model):

    class Meta:
        verbose_name_plural = "queries"

    text = models.CharField(max_length=300)
    count = models.IntegerField() 

    def __str__(self):
        return "Query: '{}'".format(self.text)

    
class SkippedAnnotation(models.Model):
    query = models.ForeignKey(
        Query,
        on_delete=models.CASCADE,
        related_name="skipped_annotations",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skipped_annotations",
    )

    def __str__(self):
        return "{} skipped query '{}'".format(self.user, self.query.text)

            
class Annotation(models.Model):

    class Meta:
        unique_together = ("query", "user")

    query = models.ForeignKey(
        Query,
        on_delete=models.CASCADE,
        related_name="annotations",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="annotations",
    )

    NAVIGATIONAL = 'NAV'
    INFORMATIONAL_DIRECTED_CLOSED = 'IDC'
    INFORMATIONAL_DIRECTED_OPEN = 'IDO'
    INFORMATIONAL_UNDIRECTED = 'IUN'
    INFORMATIONAL_ADVICE = 'IAD'
    INFORMATIONAL_LOCATE = 'ILO'
    INFORMATIONAL_LIST = 'ILI'
    RESOURCE_DOWNLOAD = 'RDO'
    RESOURCE_ENTERTAINMENT = 'RDE'
    RESOURCE_INTERACT = 'RIN'
    RESOURCE_OBTAIN = 'ROB'
    
    query_type_choices = (
        (NAVIGATIONAL, 'Navigational (eg www.facebook.com)'),
        (INFORMATIONAL_DIRECTED_CLOSED,
         'Informational - Directed - Closed (Learn about topic; single answer)'),
        (INFORMATIONAL_DIRECTED_OPEN,
         'Informational - Directed - Open (Learn about topic; unconstrained depth)'),
        (INFORMATIONAL_UNDIRECTED,
         'Informational - Undirected (tell me about; learn everything/anything about topic)'),
        (INFORMATIONAL_ADVICE, 'Informational Advice'),
        (INFORMATIONAL_LOCATE, 'Informational Locate'),
        (INFORMATIONAL_LIST, 'Informational List'),
        (RESOURCE_DOWNLOAD, 'Resource Download'),
        (RESOURCE_ENTERTAINMENT, 'Resource Entertainment'),
        (RESOURCE_INTERACT, 'Resource Interact'),
        (RESOURCE_OBTAIN, 'Resource Obtain'),
    )

    is_geo = models.BooleanField(
        verbose_name='isGEO',
        default=False,
        help_text=''
    )
    is_geo_impl = models.BooleanField(
        verbose_name='isGEOImpl',
        default=False,
        help_text=''
    )
    query_type = models.CharField(
        verbose_name='Query Type',
        max_length=3,
        choices=query_type_choices,
        default=NAVIGATIONAL,
        help_text=''
    )

    def __str__(self):
        return "{} annotated query '{}'".format(self.user, self.query.text)
