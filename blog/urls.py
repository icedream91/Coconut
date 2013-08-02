from django.conf.urls import patterns,include,url

from blog.sitemap import DynamicSitemap,StaticSitemap
from blog.feed import BlogFeed

sitemaps={
    'static':StaticSitemap,
    'dynamic':DynamicSitemap,
}

urlpatterns=patterns('',
    url(r'^$', 'blog.views.index', name='index'),
    url(r'^article/(\d+)/$','blog.views.article',name='article'),
    url(r'^page/(\d+)/$','blog.views.page',name='page'),
    url(r'^category/(\d+)/$','blog.views.category',name='category'),
    url(r'^tag/(\d+)/$','blog.views.tag',name='tag'),
    url(r'^search/$','blog.views.search',name='search'),
    url(r'^sitemap\.xml$','django.contrib.sitemaps.views.sitemap',{'sitemaps':sitemaps}),
    url(r'^feed/$',BlogFeed()),
) 
