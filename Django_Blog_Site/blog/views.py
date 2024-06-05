from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from .form import NewPostForm
from .models import Post


# functional view
# def post_list_view(request):
#     posts_list = Post.objects.filter(status='pub').order_by('-datetime_modified')
#     return render(request, 'blog/blogpost.html', {'posts_list': posts_list})
# CLASS based view
class PostListView(generic.ListView):
    template_name = 'blog/blogpost.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-datetime_modified')


# def post_detail_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/blogpost_detail.html', {'post': post})
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'


# def post_create_view(request):
#     # django form method
#     if request.method == 'POST':
#         form = NewPostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#     else:
#         form = NewPostForm()
#
#     return render(request, 'blog/blogpost_create.html', context={'form': form})
class PostCreateView(generic.CreateView):
    context_object_name = 'form'
    form_class = NewPostForm
    template_name = 'blog/blogpost_create.html'


# def post_update_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     form = NewPostForm(request.POST or None, instance=post)
#
#     if form.is_valid():
#         form.save()
#         return redirect('post_list')
#
#     return render(request, 'blog/blogpost_create.html', context={'form': form})
class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = NewPostForm
    template_name = 'blog/blogpost_create.html'


# def post_delete_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     if request.method == 'POST':
#         if 'no' in request.POST:
#             return redirect('post_list')
#         else:
#             post.delete()
#             return redirect('post_list')
#
#     return render(request, 'blog/blogpost_delete.html', context={'post': post})
class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/blogpost_delete.html'
    success_url = reverse_lazy('post_list')

    def post(self, request, *args, **kwargs):
        if 'no' in request.POST:
            return redirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)
