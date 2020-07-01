from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from homework04 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 指定图片上传的目录
    url(r"^media/(?P<path>.*)", serve, {"document_root": settings.MEDIA_ROOT}),
    # bookapp 的 urls
    path("bookapp/", include("bookapp.urls")),
]
