from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Review, Game
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


def home(request):
    context = {
        'posts': Review.objects.all()
    }
    return render(request, 'reviews/home.html', context)


class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class ReviewDetailView(DetailView):
    model = Review


class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    fields = ['title', 'description', 'developer', 'release_date']
    def form_valid(self, form):
        return super().form_valid(form)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['title', 'content', 'game_score', 'game']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.review_score = 0
        form.instance.score_count = 0
        return super().form_valid(form)
        

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['title', 'content', 'game_score', 'game']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = '/'

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False


def about(request):
    return render(request, 'reviews/about.html', {'title': 'About'})