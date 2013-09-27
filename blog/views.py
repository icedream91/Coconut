from html.parser import HTMLParser
import re

from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from blog.models import *


def _get_common_content(request):
    """ 
    This function return some common content, like blog name,
    tag list, category list, and so on.
    """
    setting=Setting.objects.get(pk=1)
    page_list=Page.objects.filter(published=True).order_by('page_order')

    category_list=Category.objects.extra(select=
        {'lower_name':'lower(name)'}
    ).order_by('lower_name')

    tag_list=Tag.objects.extra(select=
        {'lower_name':'lower(name)'}
    ).order_by('lower_name')

    return {
        'blog_name':setting.blog_name,
        'page_list':page_list,
        'category_list':category_list,
        'tag_list':tag_list,
        'authenticated':request.user.is_authenticated(),
    }
        
def _get_pagination(article_list,request):
    
    setting=Setting.objects.get(pk=1)
    paginator=Paginator(article_list,setting.showed_article_num)

    requested_page_num=request.GET.get('page')

    if requested_page_num==None:
        requested_page_num=1
        article_list=paginator.page(requested_page_num)
    else:
        try:
            article_list=paginator.page(requested_page_num)
        except (PageNotAnInteger,EmptyPage):
            """
            If request for a page number bigger than the biggest existing
            page number, Django will raise EmptyPage exception, and we 
            catch this exception and raise Http404 exception.
            """
            raise Http404
   

    requested_page_num=int(requested_page_num)
    
    remainder_page_num=10
    first_page_num=requested_page_num
    last_page_num=requested_page_num
    while remainder_page_num:
        if 1<first_page_num:
            first_page_num-=1
            remainder_page_num-=1
        if last_page_num<paginator.page_range[-1]:
            last_page_num+=1
            remainder_page_num-=1
        if first_page_num==1 and last_page_num==paginator.page_range[-1]:
            break


    pagination_list=list(range(first_page_num,last_page_num+1))

    return article_list,requested_page_num,pagination_list
      
    
def index(request):
    
    content=_get_common_content(request)

    article_list=Article.objects.filter(published=True).order_by('-pub_time')


    article_list,current_page,pagination_list=\
        _get_pagination(article_list,request)

    content.update(
        article_list=article_list,
        current_page=current_page,
        pagination_list=pagination_list
    )
        
    return render(request,'blog/index.html',content)


def article(request,article_id):
    
    content=_get_common_content(request)

    article=get_object_or_404(Article,pk=article_id)
    if request.user.is_anonymous() and article.published==False:
        raise Http404

        
    content.update(article=article)

    return render(request,'blog/article.html',content)


def page(request,page_id):

    content=_get_common_content(request)

    page=get_object_or_404(Page,pk=page_id)
    if request.user.is_anonymous() and page.published==False:
        raise Http404
    
    
    content.update(page=page)
    
    return render(request,'blog/page.html',content)


def category(request,category_id):

    content=_get_common_content(request)

    category=get_object_or_404(Category,pk=category_id)
    article_list=Article.objects.filter(category=category,published=True).order_by('-pub_time')
    

    article_list,current_page,pagination_list=\
        _get_pagination(article_list,request)

    content.update(
        category=category,
        article_list=article_list,
        current_page=current_page,
        pagination_list=pagination_list,
    )

    return render(request,'blog/category.html',content)


def tag(request,tag_id):

    content=_get_common_content(request)

    tag=get_object_or_404(Tag,pk=tag_id)
    article_list=Article.objects.filter(tags=tag,published=True).order_by('-pub_time')
   

    article_list,current_page,pagination_list=\
        _get_pagination(article_list,request)

    content.update(
        tag=tag,
        article_list=article_list,
        current_page=current_page,
        pagination_list=pagination_list,
    )
    
    return render(request,'blog/tag.html',content)
 
def search(request):
    
    def _get_plain_text(html):

        class PlainTextHTMLParser(HTMLParser):
            def __init__(self):
                super().__init__(self)
                self.data=[]

            def handle_data(self,data):
                self.data.append(data)

            def get_plain_data(self):
                return ''.join(self.data)

        pattern_of_script=re.compile(r'<\s*script\s*>.*<\s*/\s*script\s*>',re.DOTALL)
        pattern_of_style=re.compile(r'<\s*style\s*>.*<\s*/\s*style\s*>',re.DOTALL)
        
        html=html.lower()
        # Strip any string within script tag and style tag.
        html=pattern_of_script.sub('',html)
        html=pattern_of_style.sub('',html)
        
        parser=PlainTextHTMLParser()
        parser.feed(html)
        plain_content=parser.get_plain_data()

        return plain_content


    try:    
        input_keywords=request.GET.get('keywords').lower()
    except AttributeError:
        """ 
        If no keywords is in request.GET, request.GET.get('keywords') will be
        None and has no lower() method. Catch AttributeError exception and set
        keywords to "".
        """
        input_keywords=''
        
    keyword_list=input_keywords.split()
    
    eligible_article_and_page_list=[]

    article_list=list(Article.objects.order_by('-pub_time'))
    for article in article_list:
        if article.published:
            for keyword in keyword_list:
                if keyword not in _get_plain_text(article.content) and \
                    keyword not in article.title.lower():
                    break
            else:
                article.type='article'
                eligible_article_and_page_list.append(article)
    

    page_list=list(Page.objects.order_by('-pub_time'))
    for page in page_list:
        if page.published:
            for keyword in keyword_list:
                if keyword not in _get_plain_text(page.content) and \
                    keyword not in page.title.lower():
                    break
            else:
                page.type='page'
                eligible_article_and_page_list.append(page)

    content=_get_common_content(request)
    article_and_page_list,current_page,pagination_list=\
        _get_pagination(eligible_article_and_page_list,request)

    content.update(
        article_and_page_list=article_and_page_list,
        current_page=current_page,
        pagination_list=pagination_list,
        keywords=input_keywords,
        keyword_list=keyword_list,
    )

    return render(request,'blog/search.html',content) 

    
