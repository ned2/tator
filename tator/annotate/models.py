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
        (NAVIGATIONAL, 'Navigational'),
        (INFORMATIONAL_DIRECTED_CLOSED,
         'Directed - Closed'),
        (INFORMATIONAL_DIRECTED_OPEN,
         'Directed - Open'),
        (INFORMATIONAL_UNDIRECTED,
         'Undirected'),
        (INFORMATIONAL_ADVICE, 'Advice'),
        (INFORMATIONAL_LOCATE, 'Locate'),
        (INFORMATIONAL_LIST, 'List'),
        (RESOURCE_DOWNLOAD, 'Download'),
        (RESOURCE_ENTERTAINMENT, 'Entertainment'),
        (RESOURCE_INTERACT, 'Interact'),
        (RESOURCE_OBTAIN, 'Obtain'),
    )

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

    is_geo = models.BooleanField(
        verbose_name='1. Is this query best answered with a pin on a map?',
        choices=BOOL_CHOICES,
        default=None,
        help_text='',
    )
    is_geo_expl = models.BooleanField(
        verbose_name='2. Is the location explicit in the query?',
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
        return "Annotation: is_geo={}, is_geo_expl={}, query_type={}".format(
            self.is_geo,
            self.is_geo_expl,
            self.query_type,
        )

class Skipped(models.Model):
    description = models.TextField()
    
    
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
    skipped = models.OneToOneField(
        Skipped,
        null=True,
        on_delete=models.CASCADE,
        related_name='response' 
    )    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("query", "user")

    def __str__(self):
        return "{} responded to query '{}' at {}".format(
            self.user,
            self.query.text,
            self.timestamp
        )

    
class HtmlMessage(models.Model):

    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100) 
    html = models.TextField()

    def __str__(self):
        return "HTML: {}".format(self.name)
