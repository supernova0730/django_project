from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import (
	ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import (
	LoginRequiredMixin, UserPassesTestMixin
)

from .models import Post


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts' # overriding default context name (object_list)
	ordering = ['-date_posted'] # set descending order
	paginate_by = 5


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		posts = Post.objects.filter(author = user).order_by('-date_posted')
		return posts


class PostDetailView(DetailView):
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	
	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author
	

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	
	def get_success_url(self):
		return reverse('blog-home')

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

def about(request):
	context = {
		'title': 'About'
	}
	return render(request, 'blog/about.html', context)