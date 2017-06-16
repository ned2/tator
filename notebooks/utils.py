import os
import sys
from collections import Counter

import pandas as pd
from statsmodels.stats.inter_rater import aggregate_raters, fleiss_kappa

# configure Django so we can use models from the annotate app 
sys.path.append('/home/nejl/Dropbox/projects/tator/repo/tator')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tagit.settings'
import django
django.setup()


from annotate.models import Query, Annotation, UserResponse


def import_queries(path, sample='first', limit=None):    
    with open(path) as csvfile:
        df = pd.read_csv(csvfile, delimiter=';')

        # filter out queries with length less than 2 characters long
        df = df[df['querystring'].str.len() > 1]
        
    if limit is not None:
        if sample == 'first':
            df = df[:limit]
        elif sample == 'random':
            df = df.sample(limit)
        elif sample == 'proportional':
            df = df.sample(limit, weights='countqstring')
        else:
            print('Unknown sampling method')
            return

    for i, values in enumerate(df.values.tolist()):
         text, count = values
         Query.objects.create(text=text, count=count)

    print("Added {} queries to the database.\n".format(i+1))
    print(df.describe())


def pretty_print_counter(counter):
    lines = []
    for key, value in counter.most_common():
        lines.append("{}: {}".format(key, value))
    return "\n".join(lines)


def get_user_results(username):
    # for each user, display the number of results
    # user
    lines = ["*** Annotator: {} ***".format(username)]
    lines.append("===================================\n")
    responses = UserResponse.objects.filter(user__username=username)
    annotations = [r for r in responses if r.annotation]
    skipped = [r for r in responses if r.skipped]

    lines.append("Skipped queries:\n")
    for response in skipped:
        line ='    "{}" --- "{}"'.format(response.query.text,
                                            response.skipped.description)
        lines.append(line)

    lines.append("\nAnnotations:\n")
    lines.append(Annotation._meta.get_field('is_geo').verbose_name)
    q1 = Counter(r.annotation.is_geo for r in annotations)
    q1_output = pretty_print_counter(q1)
    lines.append(q1_output)

    lines.append("")

    lines.append(Annotation._meta.get_field('loc_type').verbose_name)
    q1 = Counter(r.annotation.is_geo for r in annotations)
    q1_output = pretty_print_counter(q1)
    lines.append(q1_output)

    #lines.append("Q1: \nY: {}\nN:{}")
    
    return "\n".join(lines)
    
    
def get_iaa(question_num, queries=None, users=None, level='fine'):
    data  = get_annotations(question_num, queries, users, level)
    #n_cat = Annotation.get_num_categories(question_num)
    results = aggregate_raters(data, n_cat=None)
    kappa = fleiss_kappa(results[0])
    return kappa


def get_annotations(question_num, queries=None, users=None, level='fine'):
    queries = Query.objects.exclude(responses__skipped__isnull=False).distinct()

    if queries is not None:
        queries = queries.filter(pk__in=queries)
        
    data = []
    for query in queries:
        # get all non-skipped results
        responses = query.responses.exclude(skipped__isnull=False)
        
        if users is not None:
            # restrict annotations to supplied users
            responses = responses.filter(user__username__in=users)

        results = [r.annotation.get_question(question_num) for r in responses]

        if question_num in (2,3) and level == 'course':
            # use course grained agreement
            results = [r[0] for r in results]
            
        if results:
            data.append(results)
    return data