from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
#from rest_framework.renderers import JSONRenderer
from .models import Article 
from .serializers import ArticleSerializers
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def article_list(request):
    if request.method == "GET":
        articles=Article.objects.all()
        serilizer=ArticleSerializers(articles,many=True)#if more than one instance then TRUE else FALSE
        return JsonResponse(serilizer.data,safe=False) 
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serilizer = ArticleSerializers(data=data)
        if serilizer.is_valid():
            serilizer.save()
            return JsonResponse(serilizer.data,status=201)
        return JsonResponse(serilizer.errors ,status=400)

@csrf_exempt
def article_detail(request,pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoestNotExist:
        return HttpResponse(404)
    
    if request.method == "GET":
        serilizer=ArticleSerializers(article)
        return JsonResponse(serilizer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serilizer = ArticleSerializers(article,data=data)
        if serilizer.is_valid():
            serilizer.save()
            return JsonResponse(serilizer.data)
        return JsonResponse(serilizer.errors ,status=400)
    elif request.method == "DELETE":
        article.delete()
        return HttpResponse(status=204)