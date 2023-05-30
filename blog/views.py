from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import matplotlib.pyplot as plt
import base64
import io
import pandas as pd
import numpy as np

# posts = [
#     {
#         'author':"Tushar Jain",
#         'title': 'Blog Post 1',
#         'content': "First Post Content",
#         'date_posted':"27th May 2023"
#     },
#     {
#         'author':"Ansh",
#         'title': 'Blog Post 2',
#         'content': "Second Post Content",
#         'date_posted':"28th May 2023"
#     }
# ]

# def home(request):
#     context = {
#         "posts":Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    #to pass on 'posts' to the home.html instead of object
    # put - for newest to oldest post
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
class PostDetailView(DetailView):
    model = Post

#loginRequiredMixin restricts only a loggedin user to update post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#UserPassesTestMixin is used so that user can only edit his own post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title':"About"})
    # return HttpResponse('<h1>About Page</h1>')

def get_graph():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(x,y):
    plt.switch_backend("AGG")
    plt.figure(figsize=(10,5))
    plt.title('No. of Males & Females')
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Gender")
    plt.ylabel("No of people onboarding ship")
    plt.tight_layout()
    graph = get_graph()
    return graph

def displayblog1(request):
    titanic = pd.read_csv('titanic.csv')
    male_ind = len(titanic[titanic['Sex'] == 'male'])
    female_ind = len(titanic[titanic['Sex'] == 'female'])
    gender = ['Male','Female']
    index = [male_ind, female_ind]
    chart = get_plot(gender, index)
    plt.hist([titanic[titanic['Survived']==1]['Fare'], titanic[titanic['Survived']==0]['Fare']], stacked=True, color = ['g','r'],
         bins = 10,label = ['Survived','Not Survived'])
    plt.legend()
    plt.title('Classification of survival rate with fair charges')
    plt.xticks(rotation=0)
    plt.ylabel('No. of Passengers')
    plt.xlabel('Fare')
    plt.tight_layout()
    graph1 = get_graph()
    return render(request, 'blog/blog1.html', {'chart':chart, 'chart1':graph1})