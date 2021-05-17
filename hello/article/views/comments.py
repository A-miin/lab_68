from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views import View
from django.views.generic import CreateView
from django.shortcuts import reverse, get_object_or_404, redirect

from article.forms import CommentForm
from article.models import Comment, Article, CommentLike


class ArticleCommentCreate(PermissionRequiredMixin, CreateView):
    template_name = 'comments/create.html'
    form_class = CommentForm
    model = Comment
    permission_required = 'article.add_comment'

    def get_success_url(self):
        return reverse(
            'article:view',
            kwargs={'pk': self.kwargs.get('pk')}
        )
    
    def form_valid(self, form):
        article = get_object_or_404(Article, id=self.kwargs.get('pk'))

        comment = form.instance
        comment.article = article
        comment.author = self.request.user

        return super().form_valid(form)

class CommentLikeCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        comment = get_object_or_404(Comment, id=kwargs.get('pk'))
        user_likes = user.comment_likes.all()
        if user_likes.filter(comment=comment).count()>0:
            print('already liked')
            return HttpResponseForbidden('Already liked')
        else:
            CommentLike.objects.create(user = user, comment=comment).save()
        return redirect('article:view', kwargs = {'pk':comment.article.pk})

class CommentLikeDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        comment = get_object_or_404(Comment, id=kwargs.get('pk'))
        user_likes = user.comment_likes.all()
        if user_likes.filter(comment=comment).count()>0:
            CommentLike.objects.get(user=user, comment=comment).delete()
        else:
            print('not liked')
            return HttpResponseForbidden('Not liked')
        return redirect('article:view', kwargs = {'pk':comment.article.pk})