from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice
from django.shortcuts import render,get_object_or_404
from django.db.models import F
from django.urls import reverse
from .forms import QuestionForm
from django.views import generic
from django.utils import timezone

# Create your views here.
# def main_page(request):
#     return HttpResponse("Main Page works!!")

# def display(generic.DetailView):
#     ques_list = Question.objects.all()
#     data = {"latest_question_list":ques_list}
#     return render(request,"index.html",data) 

# def get_one(request,question_id):
#     ques = get_object_or_404(Question,pk=question_id)
#     data = {"question":ques}
#     return render(request,"one.html",data)

def vote(request,question_id):
    ques = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = ques.choice_set.get(pk=request.POST["choice"])

    except (KeyError,Choice.DoesNotExist):
        return render(request,"vote.html", {"question":ques,"error_message":"You didnt select anything"}
        )

    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # return HttpResponse("You voted")
        return HttpResponseRedirect(reverse("polls:results",args=(question_id,)))

def results(request,question_id):
    ques = get_object_or_404(Question,pk=question_id)
    return render(request,"results.html",{"question":ques})


class IndexView(generic.ListView):
    template_name="index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    

class DisplayView(generic.DetailView):
    model = Question
    template_name = "one.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "results.html"
    


