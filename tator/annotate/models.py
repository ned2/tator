from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from csv import DictReader

"""
TODO
 -- help strings for Annotation fields
"""

def import_queries(path, limit=None):
    
    with open(path) as csvfile:
        reader = DictReader(csvfile, delimiter=';')
        for i, row in enumerate(reader):
            text = row['querystring']
            count = row['countqstring']
            if text == '':
                continue
            Query.objects.create(text=text, count=count)

            if limit is not None and i == limit - 1:
                break
            
        print("Added {} queries to the database.".format(i))


class Query(models.Model):

    text = models.CharField(max_length=300)
    count = models.IntegerField() 

    class Meta:
        verbose_name_plural = "queries"

    def __str__(self):
        return "Query: '{}'".format(self.text)

    
class Annotation(models.Model):
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
    
    QUERY_TYPE_CHOICES = (
        #('', 'Please select a query type'),
        (NAVIGATIONAL, 'Navigational (eg www.facebook.com)'),
        (INFORMATIONAL_DIRECTED_CLOSED,
         'Informational - Directed - Closed'),
        (INFORMATIONAL_DIRECTED_OPEN,
         'Informational - Directed - Open'),
        (INFORMATIONAL_UNDIRECTED,
         'Informational - Undirected'),
        (INFORMATIONAL_ADVICE, 'Informational Advice'),
        (INFORMATIONAL_LOCATE, 'Informational Locate'),
        (INFORMATIONAL_LIST, 'Informational List'),
        (RESOURCE_DOWNLOAD, 'Resource Download'),
        (RESOURCE_ENTERTAINMENT, 'Resource Entertainment'),
        (RESOURCE_INTERACT, 'Resource Interact'),
        (RESOURCE_OBTAIN, 'Resource Obtain'),
    )

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

    is_geo = models.BooleanField(
        verbose_name='1. Can this query be answered with a pin on a map?',
        choices=BOOL_CHOICES,
        default=None,
        help_text='',
    )
    is_geo_impl = models.BooleanField(
        verbose_name='2. Is the location implicit in the query?',
        choices=BOOL_CHOICES,
        default=None,
        help_text=''
    )
    query_type = models.CharField(
        verbose_name='3. What type of query is this?',
        max_length=3,
        choices=QUERY_TYPE_CHOICES,
        default=None,
        help_text='',
    )

    def __str__(self):
        return "Annotation: is_geo={}, is_geo_impl={}, query_type={}".format(
            self.is_geo,
            self.is_geo_impl,
            self.query_type,
        )


class UserResponse(models.Model):
    query = models.ForeignKey(
        Query,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="responses",
    )

    annotation = models.OneToOneField(
        Annotation,
        null=True,
        on_delete=models.CASCADE,
        related_name='response' 
    )

    class Meta:
        unique_together = ("query", "user")

    def __str__(self):
        return "{} responded to query '{}'".format(self.user, self.query.text)

