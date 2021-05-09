from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Question, Choice

def home(request):
    context = {
        'posts' : Question.objects.all()
    }
    return render(request, 'blog/home.html', context)

class QuestionListView(ListView):
    model = Question
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 7

class UserQuestionListView(ListView):
    model = Question
    template_name = 'blog/user_questions.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Question.objects.filter(author = user).order_by('-date_posted')

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'blog/question_detail.html'

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question_text', 'answer', 'question_image', 'description', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['question_text', 'answer', 'question_image', 'description', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        else:
            return False

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = 'blog/question_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        else:
            return False