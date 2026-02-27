from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, BlogPost, LoginAttempt
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.models import User


# ================= LIKE FUNCTION (FIXED) =================
def Likes(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return HttpResponseRedirect(reverse('blogdetail', args=[str(pk)]))


# ================= LOGIN SECURITY =================
MAX_ATTEMPTS = 5
TIMEFRAME = 5

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        recent_attempts = LoginAttempt.get_recent_attempts(username, minutes=TIMEFRAME)

        if recent_attempts >= MAX_ATTEMPTS:
            messages.error(request, "Too many failed login attempts. Please try again later.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            LoginAttempt.objects.create(username=username)
            messages.error(request, "Invalid credentials, please try again.")
            return redirect('login')

    return render(request, 'login.html')


# ================= HOME VIEW =================
class Home(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_posts'] = Post.objects.count()
        context['total_comments'] = Comment.objects.count()
        context['total_users'] = User.objects.count()

        context['top_posts'] = (
            Post.objects
            .annotate(total_likes=Count('likes'))
            .order_by('-total_likes')[:3]
        )

        return context


# ================= DETAIL VIEW =================
class Detail(DetailView):
    model = Post
    template_name = 'detail-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        post = self.get_object()

        context['total_likes'] = post.total_likes()

        if self.request.user.is_authenticated:
            context['liked'] = post.likes.filter(id=self.request.user.id).exists()
        else:
            context['liked'] = False

        context['likers'] = post.likes.all()

        return context


# ================= CREATE POST =================
class Create(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create-post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogdetail', kwargs={'pk': self.object.pk})


# ================= ADD COMMENT =================
class AddComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add-comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogdetail', kwargs={'pk': self.kwargs['pk']})


# ================= UPDATE =================
class Update(UpdateView):
    model = Post
    template_name = 'update-post.html'
    fields = ('title', 'body', 'image')

    def get_success_url(self):
        return reverse('blogdetail', kwargs={'pk': self.object.pk})


# ================= DELETE =================
class Delete(DeleteView):
    model = Post
    template_name = 'delete-post.html'
    success_url = reverse_lazy('all')


# ================= FEATURED =================
class Featured(ListView):
    model = Post
    template_name = 'featured-blogs.html'
    ordering = ['-post_date']