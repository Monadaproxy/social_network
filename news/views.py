from django.shortcuts import render, redirect, reverse
from .models import Articles
from .forms import ArticlesForm
from .serializers import ArticlesSerializer
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from rest_framework import generics


class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'


class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm

class NewsDeleteView(DeleteView):
    model = Articles
    template_name = 'news/news_delete.html'

    def get_success_url(self):
        return reverse('users:profile', kwargs={'username' : self.request.user.username})

class ArticlesAPIView(generics.ListAPIView):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

@login_required
def news_home(request):
    news = Articles.objects.filter(author=request.user)
    news = news.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('users:profile', kwargs={'username': request.user.username}))
    else:
        form = ArticlesForm()
    return render(request, 'news/create.html', {'form': form})