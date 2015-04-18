#coding=utf8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'onedy.views.indexhtml'),
    url(r'^dy/(?P<dyid>.+)\.html$', 'onedy.views.detailhtml'),
    url(r'^list/(?P<search_type>.+)$', 'onedy.views.listhtml'),
    url(r'^type/(?P<search_type>.+)$', 'onedy.views.typehtml'),
    url(r'^search$','onedy.views.search'),
    url(r'^ph/(?P<paihang_type>.+).html$', 'onedy.views.paihanghtml'),
)
urlpatterns += staticfiles_urlpatterns()
