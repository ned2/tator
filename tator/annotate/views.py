from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import View

from .models import UserResponse, Annotation, Query, HtmlMessage
from .forms import AnnotationForm, SkippedForm


def index(request):
    return redirect('annotate')


def welcome(request):
    welcome = HtmlMessage.objects.get(name='welcome')
    instructions = HtmlMessage.objects.get(name='instructions')
    context = {"welcome_html": welcome.html, "instructions_html": instructions.html}
    return render(request, 'annotate/welcome.html', context)


def instructions(request):
    instructions = HtmlMessage.objects.get(name='instructions')
    context = {"instructions_html": instructions.html}
    return render(request, 'annotate/instructions.html', context)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AnnotateView(View):
    
    def get(self, request):
        # get the first from all queries which the user hasn't either annotated
        # or skipped
        query = Query.objects.exclude(
            responses__user=request.user
        ).first()
        
        if query is None:
            # User is finished annotating
            finished = HtmlMessage.objects.get(name='instructions')
            context = {"finished_html": finished.html}
            return render(request, 'annotate/finished.html', {})
        else:
            context = {
                'annotation_form': AnnotationForm(),
                'skipped_form': SkippedForm(),
                'query': query,
            }
            return render(request, 'annotate/annotate.html', context)

    def post(self, request):
        query = Query.objects.get(pk=request.POST['query'])
        skipped_form = SkippedForm(request.POST)
        annotation_form = AnnotationForm(request.POST)

        if skipped_form.is_valid():        
            # User skipped this annotation
            skipped = skipped_form.save()
            response = UserResponse.objects.create(
                user=request.user,
                query=query,
                skipped=skipped
            )
            return redirect('annotate')

        if annotation_form.is_valid():
            # create user's annotation and go to next annotation
            annotation = annotation_form.save()
            response = UserResponse.objects.create(
                user=request.user,
                query=query,
                annotation=annotation
            )
            return redirect('annotate')

        context = {
            'annotation_form': annotation_form,
            'skipped_form': skipped_form,
            'query': query
        }
        return render(request, 'annotate/annotate.html', context)
