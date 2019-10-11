from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView

from articles.models import Article
from forms import ArticleForm


class ArticlesListView(LoginRequiredMixin, ListView):
    """已发布的文章列表"""
    model = Article
    paginate_by = 20
    context_object_name = 'articles'
    template_name = 'articles/article_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context

    def get_queryset(self):
        print(Article.objects.get_published())
        return Article.objects.get_published()


class DraftListView(ArticlesListView):

    def get_queryset(self):
        """当前用户的草稿"""
        return Article.objects.filter(user=self.request.user).get_drafts()


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_create.html'
    message = "您的文章已创建成功!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleCreateView, self).form_valid(form)

    def get_success_url(self):
        """创建成功后跳转"""
        messages.success(self.request, self.message)  # 消息传递给下一次请求
        return reverse_lazy('articles:list')


from django.core.signals import request_started, request_finished
