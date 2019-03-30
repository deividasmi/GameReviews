from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Review
from django.contrib.auth.mixins import LoginRequiredMixin
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



class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['title', 'content', 'game_score']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.review_score = 0
        form.instance.score_count = 0
        return super().form_valid(form)
        


def about(request):
    return render(request, 'reviews/about.html', {'title': 'About'})