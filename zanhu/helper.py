#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc : Created by San on 2019/10/9 07:58
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.views.generic import View


def ajax_required(f):
    """验证时候为AJAX请求"""

    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():  # 判断是否是AJAX请求
            return HttpResponseBadRequest("不是AJAX请求! ")
        return f(request, *args, **kwargs)

    return wrap


class AuthorRequiredMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
