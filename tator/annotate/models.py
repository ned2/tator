from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete


class Query(models.Model):

    text = models.CharField(max_length=300)
    count = models.IntegerField() 
    collection = models.CharField(max_length=50) 
    
    class Meta:
        verbose_name_plural = "queries"

    def __str__(self):
        return "Query: '{}'".format(self.text)

    
class Annotation(models.Model):
    # Values for loc_type (Q2)
    # values are from the 2x2 binary feature space of:
    #   a) is a location explicit in the query
    #   b) is there a place name in the query
    POS_LOC_POS_PLACE = 'YY'
    POS_LOC_NEG_PLACE = 'YN'
    NEG_LOC_POS_PLACE = 'NY'
    NEG_LOC_NEG_PLACE = 'NN'
    
    LOCATION_TYPE_CHOICES = (
        (POS_LOC_POS_PLACE, 'Yes -- with place name'),
        (POS_LOC_NEG_PLACE, 'Yes -- without place name'),
        (NEG_LOC_POS_PLACE, 'No'),
        (NEG_LOC_NEG_PLACE, 'Not applicable'),
    )
    
    # Values for query_type (Q3)
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
        (NAVIGATIONAL, 'Web Navigation'),
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
        help_text='This questions asks whether this query would be most suitably answered by a spatial interface, such as a map or route directions. It could be presented using one or multiple pins, lines and/or regions, or a set of instructions',
    )

    loc_type = models.CharField(
        verbose_name='2. Is a location explicit in the query?',
        max_length=3,
        choices=LOCATION_TYPE_CHOICES,
        default=None,
        help_text='This questions asks whether this query contains a place name or other location reference (e.g., work) relating to Question 1.',
    )

    query_type = models.CharField(
        verbose_name='3. What type of query is this?',
        max_length=3,
        choices=QUERY_TYPE_CHOICES,
        default=None,
        help_text='This questions asks you to classify the query into one of the subcategories of Navigation, Informational and Resource (Rose and Levinson, 2004). Below are the definitions as provided by Rose and Levinson, and examples for each of the categories. ',
    )

    def get_question(self, question_num):
        if question_num == 1:
            return self.is_geo
        elif question_num == 2:
            return self.loc_type
        elif question_num == 3:
            return self.query_type

        print("Not a valid question.")

    @classmethod    
    def get_num_categories(cls, question_num):
        if question_num == 1:
            return 2
        elif question_num == 2:
            return len(cls.LOCATION_TYPE_CHOICES)
        elif question_num == 3:
            return len(cls.QUERY_TYPE_CHOICES)

        print("Not a valid question.")        
        
    def __str__(self):
        return "Annotation: is_geo={}, is_geo_expl={}, query_type={}".format(
            self.is_geo,
            self.loc_type,
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
        if self.skipped:
            msg = '{} skipped query "{}" at "{}"'
        else:
            msg = '{} annotated query "{}" at {}'

        return msg.format(self.user, self.query.text, self.timestamp)


@receiver(post_delete, sender=UserResponse)
def post_delete_user_response(sender, instance, *args, **kwargs):
    # Make sure we clean up annotations and skippeds associated with any
    # deleted UserResponse objects 

    if instance.skipped:
        instance.skipped.delete()

    if instance.annotation:
        instance.annotation.delete()


class HtmlMessage(models.Model):

    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100) 
    html = models.TextField()

    def __str__(self):
        return "HTML: {}".format(self.name)
