from django.contrib.sitemaps import Sitemap
from blog.models import Article,Page

class DynamicSitemap(Sitemap):
    
    def items(self):
        articles_and_pages=list(Article.objects.filter(published=True))
        articles_and_pages.extend(list(Page.objects.filter(published=True)))
        
        return articles_and_pages


class StaticSitemap(Sitemap):
    # This class is used to return homepage link.

    def items(self):
        return ['']

    def location(self,home_url):
        return home_url


        
