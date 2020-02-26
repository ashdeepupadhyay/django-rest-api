from django.urls import path
from .views import article_list,article_detail,ArticleAPIView,ArticleDetails,GenericApiView

urlpatterns = [
    path('article/', article_list),
    path('articleapi/', ArticleAPIView.as_view()),
    path('generic/article/<int:id>', GenericApiView.as_view()),
    path('detail/<int:pk>/', article_detail),
    path('detailapi/<int:id>/', ArticleDetails.as_view()),
]