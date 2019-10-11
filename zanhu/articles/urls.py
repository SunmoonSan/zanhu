#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc : Created by San on 2019/10/10 01:19
from django.urls import path

from zanhu.articles import views

app_name = "articles"
urlpatterns = [
    path("", views.ArticlesListView.as_view(), name="list"),
    path("write-new-article/", views.ArticleCreateView.as_view(), name='write_new'),
    path("drafts/", views.DraftListView.as_view(), name='drafts')
]