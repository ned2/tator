from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import View

from .models import UserResponse, Annotation, Query
from .forms import AnnotationForm


def index(request):
    return redirect('annotate')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AnnotateView(View):
    
    def get(self, request):
        # retrieve all queries which the user hasn't either annotated or skipped
        query = Query.objects.exclude(
            responses__user=request.user
        ).first()
        
        if query is None:
            # User is finished annotating
            return render(request, 'annotate/finished.html', {})
        else:
            form = AnnotationForm()
            context = {'form': form, 'query': query}
            return render(request, 'annotate/annotate.html', context)

    def post(self, request):
        query = Query.objects.get(pk=request.POST['query'])
        
        if 'skip' in request.POST:
            # User skipped this annotation
            response = UserResponse.objects.create(user=request.user, query=query)
            return redirect('annotate')

        form = AnnotationForm(request.POST)

        if form.is_valid():
            # create user's annotation and go to next annotation
            annotation = form.save()
            response = UserResponse.objects.create(
                user=request.user,
                query=query,
                annotation=annotation
            )
            return redirect('annotate')

        #import ipdb; ipdb.set_trace()
        context = {'form': form, 'query': query.text}
        return render(request, 'annotate/annotate.html', context)
