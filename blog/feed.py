from django.contrib.syndication.views import Feed
from blog.models import Article,Page,Setting

class BlogFeed(Feed):
    setting=Setting.objects.get(pk=1)
    title=setting.blog_name

    link=''

    description='News from '+setting.blog_name


    def items(self):
        """ 
        This method will return both new articles and new pages of this
        blog.
        """
        articles_and_pages=list(Article.objects.order_by('-pub_time')[:5])
        articles_and_pages.extend(list(Page.objects.order_by('-pub_time')[:5]))

        articles_and_pages.sort(key=lambda item:item.pub_time,reverse=True)
        
        return articles_and_pages[:5]


    def item_title(self,item):
        return item.title


    def item_description(self,item):
        if isinstance(item,Article):
            description=item.summary()
            if description:
                return description
            else:
                return item.content
        else:
            return item.content

        

