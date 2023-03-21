# This will handle the AJAX request from the frontend for crawling the blogs

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import requests
import time
from .models import Blog

def home(request):
    return render(request, 'home.html')


@csrf_exempt
def crawl_blogs(request):
    tag = request.POST.get('tag')
    url = f'https://medium.com/tag/{tag}/latest'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    blogs = soup.find_all('div', {'class': 'js-post'})

    for blog in blogs:
        creator = blog.find('div', {'class': 'postMetaInline-authorLockup'})
        if creator is not None:
            creator = creator.find('a').text.strip()
        else:
            creator = ''

        title = blog.find('h3', {'class': 'graf--title'})
        if title is not None:
            title = title.text.strip()
        else:
            title = ''

        details = blog.find('div', {'class': 'postMetaInline'})
        if details is not None:
            details = details.find_all('a')[-1].text.strip()
        else:
            details = ''

        blog_content = blog.find('div', {'class': 'js-postBody'})
        if blog_content is not None:
            blog_content = str(blog_content)
        else:
            blog_content = ''

        tags = blog.find('ul', {'class': 'tags'})
        if tags is not None:
            tags = ', '.join(tag.text.strip() for tag in tags.find_all('a'))
        else:
            tags = ''

        responses = blog.find('div', {'class': 'js-responsesContainer'})
        if responses is not None:
            responses = str(responses)
        else:
            responses = ''

        blog_obj = Blog(
            creator=creator,
            title=title,
            details=details,
            blog=blog_content,
            tags=tags,
            responses=responses
        )
        blog_obj.save()

    response = {'status': 'success'}
    return JsonResponse(response)
