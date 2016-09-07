from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View

from .models import Annotation, SkippedAnnotation, Query
from .forms import AnnotationForm


@login_required(login_url='/login/')
def index(request):
    return redirect('annotate')


@method_decorator(login_required, name='dispatch')
class AnnotateView(View):
    
    def get(self, request):
        # retrieve all queries which the user hasn't either annotated or skipped
        query = Query.objects.exclude(
            annotations__user=request.user
        ).exclude(
            skipped_annotations__user=request.user
        ).first()
        
        if query is None:
            # User is finished annotating
            return render(request, 'annotate/finished.html', {})
        else:
            form = AnnotationForm(initial={'user': request.user, 'query': query})
            return render(request, 'annotate/annotation_form.html', {'form': form})

    def post(self, request):
        form = AnnotationForm(request.POST)
        if form.is_valid():
            # create user's annotation and go to next annotation
            annotation = form.save()

            # delete any matching SkippedAnnotation for this query.
            # note that this should not happen, but we do it just in case.
            skipped = SkippedAnnotation.objects.filter(user=annotation.user, query=annotation.query)
            skipped.delete()
            return redirect('annotate')
        return render(request, 'annotate/annotation_form.html', {'form': form})


# A user looking at an annotation form
# when form is submitted, the view that saves it needs
# to have query PK. so either
# -- form has it has hidden field that is sent back
# -- send back as post data
