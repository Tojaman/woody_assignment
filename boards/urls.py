from django.urls import path, include
from . import views

app_name = "boards"

# as_view() : 클래스의 모든 속성을 전달
urlpatterns = [
    path("user/", views.UserAPIView.as_view()),
    path("board/", views.BoardAPIView.as_view()),
    path("board/<int:pk>/", views.BoardDetailAPIView.as_view()),
    path("comment/", views.CommentAPIView.as_view()),
    path("comment/<int:pk>/", views.CommentDetailAPIView.as_view())
]