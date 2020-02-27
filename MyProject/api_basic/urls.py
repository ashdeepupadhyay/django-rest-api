from django.urls import path,include
from .views import article_list,article_detail,ArticleAPIView,ArticleDetails,GenericApiView,ArticleViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('article',ArticleViewSet,basename='article')
urlpatterns = [
    path('viewset/',include(router.urls)),
    path('viewset/<int:pk>/',include(router.urls)),
    path('article/', article_list),
    path('articleapi/', ArticleAPIView.as_view()),
    path('generic/article/<int:id>', GenericApiView.as_view()),
    path('detail/<int:pk>/', article_detail),
    path('detailapi/<int:id>/', ArticleDetails.as_view()),
]