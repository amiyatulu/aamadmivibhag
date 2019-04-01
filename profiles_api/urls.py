from django.urls import re_path, path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name="hello-viewset")
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet, base_name="login")
router.register('post', views.PostViewSet)
router.register(r'post/(?P<pid>[0-9]+)/review',views.ReviewViewSet, base_name="review")
urlpatterns = [
	path('hello-view/', views.HelloApiView.as_view()),
	path('', include(router.urls)),
]