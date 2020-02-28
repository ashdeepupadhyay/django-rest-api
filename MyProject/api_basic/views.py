from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
#from rest_framework.renderers import JSONRenderer
from .models import Article 
from .serializers import ArticleSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 

from rest_framework import generics,mixins

from rest_framework.authentication import SessionAuthentication , TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets

from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

class ArticleViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class=ArticleSerializers#serializer_class variable name cannot be changed
    queryset=Article.objects.all()#queryset variable name cannot be changed
'''
class ArticleViewSet(viewsets.ViewSet):
    def list(self,request):
        articles=Article.objects.all()
        serilizer=ArticleSerializers(articles,many=True)#if more than one instance then TRUE else FALSE
        return Response(serilizer.data) 
    def create(self,request):
        serilizer = ArticleSerializers(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors ,status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset,pk=pk )
        serilizer=ArticleSerializers(article)#if more than one instance then TRUE else FALSE
        return Response(serilizer.data)
    def update(self,request,pk=None):
        article=Article.objects.get(pk=pk)
        serilizer = ArticleSerializers(article,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        return Response(serilizer.errors ,status=status.HTTP_400_BAD_REQUEST)
'''

class GenericApiView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class=ArticleSerializers#serializer_class variable name cannot be changed
    queryset=Article.objects.all()#queryset variable name cannot be changed
    lookup_field = 'id'
    
    authentication_classes = [TokenAuthentication]
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
    
    def post (self,request):
        return self.create(request)
    
    def put (self,request,id=None):
        return self.update(request,id)

    def delete(self,request,id):
        return self.destroy(request,id)

class ArticleAPIView(APIView):
    def get(self,request):
        articles=Article.objects.all()
        serilizer=ArticleSerializers(articles,many=True)#if more than one instance then TRUE else FALSE
        return Response(serilizer.data) 
    def post(self,request):
        serilizer = ArticleSerializers(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors ,status=status.HTTP_400_BAD_REQUEST)

class ArticleDetails(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        except Article.DoestNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        article=self.get_object(id)
        serilizer=ArticleSerializers(article)
        return Response(serilizer.data)
    
    def put(self,request,id):
        article=self.get_object(id)
        serilizer = ArticleSerializers(article,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        return Response(serilizer.errors ,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        article=self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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