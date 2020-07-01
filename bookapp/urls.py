from django.urls import path

from bookapp import views

urlpatterns = [
    # 整合序列化器
    path("v2/books/", views.BookAPIViewV2.as_view()),
    path("v2/books/<str:id>/", views.BookAPIViewV2.as_view()),

]
