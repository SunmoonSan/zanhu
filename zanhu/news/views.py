from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView

from helper import AuthorRequiredMixin, ajax_required
from news.models import News


class NewsListView(LoginRequiredMixin, ListView):
    """首页动态"""
    model = News
    # queryset = News.objects.all()
    paginate_by = 20  # URL分页参数page
    template_name = 'news/news_list.html'

    # page_kwarg = 'p'
    # context_object_name = 'news_list'
    # ordering = 'created_at'

    # def get_ordering(self):
    #     """自定义排序"""
    #     pass

    # def get_paginate_by(self, queryset):
    #     pass
    #
    def get_queryset(self):
        return News.objects.filter(reply=False)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     """添加额外的上下文"""
    #     context = super().get_context_data()
    #     context['view'] = 100
    #     return context


class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    slug_url_kwarg = 'slug'  # 通过URL传入要删除的对象主键ID, 默认值是slug
    pk_url_kwarg = 'pk'  # 通过URL传入要删除的对象主键ID, 默认值是PK
    success_url = reverse_lazy('news:list')


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_news(request):
    """
    发布动态, AJAX请求
    :param request:
    :return:
    """
    post = request.POST['post'].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        html = render_to_string('news/news_single.html', {
            'news': posted,
            'request': request
        })
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空! ")


@login_required
@ajax_required
@require_http_methods(['POST'])
def like(request):
    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)
    news.switch_like(request.user)
    return JsonResponse({
        'likes': news.count_likers()
    })
