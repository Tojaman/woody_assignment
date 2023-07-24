from django.urls import path, include
from . import views
from rest_framework.schemas import get_schema_view
# 스키마 뷰 생성
# schema_view = get_schema_view(
#     title="Your API",
#     renderer_classes=[JSONOpenAPIRenderer, SwaggerUIRenderer]
# )

app_name = "boards"

urlpatterns = [
    path("user/", views.UserAPIView.as_view()),
    path("user/<int:user_id>/", views.UserDeleteAPIView.as_view()),
    path("board/", views.BoardAPIView.as_view()),
    path("board/<int:board_id>/", views.BoardDeleteAPIView.as_view()),
    path("comment/<int:board_id>/", views.CommentAPIView.as_view()),
    path("comment/", views.CommentPostAPIView.as_view()),
    path("comment/put/<int:comment_id>/", views.CommentUpdateAPIView.as_view()),
    path("comment/delete/<int:comment_id>/<int:author_id>/", views.CommentDeleteAPIView.as_view()),
]
