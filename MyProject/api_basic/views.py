from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
#from rest_framework.renderers import JSONRenderer
from .models import Article 
from .serializers import ArticleSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET','POST'])
def article_list(request):
    if request.method == "GET":
        articles=Article.objects.all()
        serilizer=ArticleSerializers(articles,many=True)#if more than one instance then TRUE else FALSE
        return Response(serilizer.data) 
    elif request.method == "POST":
        serilizer = ArticleSerializers(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors ,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoestNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serilizer=ArticleSerializers(article)
        return Response(serilizer.data)
    elif request.method == "PUT":
        serilizer = ArticleSerializers(article,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        return Response(serilizer.errors ,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)