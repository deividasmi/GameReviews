from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Review, Game
from django.contrib.auth.models import User
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
    paginate_by = 5


class UserReviewListView(ListView):
    model = Review
    template_name = 'reviews/user_reviews.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Review.objects.filter(author=user).order_by('-date_posted')


class ReviewDetailView(DetailView):
    model = Review


class GameListView(ListView):
    model = Game
    template_name = 'reviews/games_list.html'
    context_object_name = 'games'
    ordering = ['-id']
    paginate_by = 5


class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    fields = ['title', 'description', 'developer', 'release_date']
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)


class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Game
    fields = ['title', 'description', 'developer', 'release_date']
    success_url = '/games'


    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        game = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Game
    success_url = '/games'

    def test_func(self):
        game = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


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