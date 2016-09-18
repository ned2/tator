from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Annotation, SkippedAnnotation, Query
from .forms import AnnotationForm


def index(request):
    return redirect('annotate')

@method_decorator(login_required(login_url='/login/'), name='dispatch')
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
            initial = {'user': request.user, 'query': query}
            form = AnnotationForm(initial=initial)
            context = {'form': form, 'query': query.text}
            return render(request, 'annotate/annotate.html', context)

    def post(self, request):
        if 'skip' in request.POST:
            # User skipped this annotation
            query = Query.objects.get(pk=request.POST['query'])
            skipped = SkippedAnnotation.objects.create(user=request.user, query=query)
            return redirect('annotate')

        form = AnnotationForm(request.POST)

        if form.is_valid():
            # create user's annotation and go to next annotation
            annotation = form.save()

            # delete any matching SkippedAnnotation for this query.
            # note that this should not happen, but we do it just in case.
            skipped = SkippedAnnotation.objects.filter(user=annotation.user, query=annotation.query)
            skipped.delete()
            return redirect('annotate')

        return render(request, 'annotate/annotate.html', {'form': form})
