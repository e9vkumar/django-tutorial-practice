import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Question

# Create your tests here.


class QuestionModelTests(TestCase):
    def test_was_done_recently_with_future_question(self):
        future_time = timezone.now() + datetime.timedelta(days=30)
        future_ques = Question(pub_date=future_time)
        self.assertIs(future_ques.was_published_recently(),False)


    def test_was_done_recently_with_past_question(self):
        past_time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        past_ques = Question(pub_date=past_time)
        self.assertIs(past_ques.was_published_recently(),False)

    def test_was_done_recently_with_recent_question(self):
        recent_time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_ques = Question(pub_date=recent_time)
        self.assertIs(recent_ques.was_published_recently(),True)

def create_questions(question_text,days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question(question=question_text,pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertIs(response.status_code,200)
        self.assertContains(response,"No available polls")
        self.assertQuerySetEqual(response.context['latest_question_list'],[])


    def test_past_questions(self):
        ques = create_questions(question_text="past",days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[ques])


    def test_past_questions(self):
        ques = create_questions(question_text="past",days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[])


    def test_past_and_future_ques(self):
        past_ques = create_questions(question_text="",days=-30)
        future_ques = create_questions(question_text="",days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[past_ques])


    def test_two_past_ques(self):
        ques1 = create_questions(question_text="",days=-30)
        ques2 = create_questions(question_text="",days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[ques2,ques1])