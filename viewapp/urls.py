from django.urls import path

from viewapp import views

urlpatterns = [
    #  APIResponse  的 url
    # path("books/", views.BookAPIViewV2.as_view()),
    # path("books/<str:id>/", views.BookAPIViewV2.as_view()),
    #  GenericAPIView  的 url
    path("gen/", views.BookGenericAPIView.as_view()),
    path("gen/<str:id>/", views.BookGenericAPIView.as_view()),
    # #  generics 的 url
    path("list/", views.BookListAPIVIew.as_view()),
    path("list/<str:id>/", views.BookListAPIVIew.as_view()),

    path("set/", views.BookGenericViewSet.as_view({"post": "user_login", "get": "get_user_count"})),
    path("set/<str:id>/", views.BookGenericViewSet.as_view({"post": "user_login"})),


]
