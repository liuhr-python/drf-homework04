from rest_framework.response import Response
from utils.response import APIResponse   # 导入封装文件
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView  # 导入 GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin,CreateModelMixin, UpdateModelMixin,DestroyModelMixin # 导入 `mixins
from rest_framework import generics  # 导入 generics
from rest_framework import viewsets  # 导入 viewsets
from rest_framework import status

from bookapp.models import User
from bookapp.models import Book
from .serializers import BookModelSerializerV2  # 导入整合序列化器
from .serializers import UserDeSerializer

'''viwes 下的 APIResponse'''

# class BookAPIViewV2(APIView):
#
#     def get(self, request, *args, **kwargs):
#         book_list = Book.objects.filter(is_delete=False)
#         data_ser = BookModelSerializerV2(book_list, many=True).data
#
#         return APIResponse(results=data_ser)

'''generics 下的 GenericAPIView'''

class BookGenericAPIView(GenericAPIView,
                         ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin
                         ):

    # # 获取当前视图所操作的模型 与序列化器类
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializerV2

    # 一，GenericAPIView
    # 完成查询操作

    # # 指定获取单条信息的主键的名称
    # lookup_field = "id"
    #
    # def get(self, request, *args, **kwargs):
    #     book_id = kwargs.get("id")
    #     if book_id:
    #         # 查询单个 get_object()
    #         book_obj = self.get_object()
    #         data_ser = self.get_serializer(book_obj)
    #         data = data_ser.data
    #
    #         return APIResponse(results=data)
    #     else:
    #         # 查询全部  get_queryset()
    #         book_list = self.get_queryset()
    #         data_ser = self.get_serializer(book_list, many=True)
    #         data_list = data_ser.data
    #
    #         return APIResponse(results=data_list)


    # 二，通过和 mixins 合作 导入 `ListModelMixin`：提供了查询所有的方法
                                # RetrieveModelMixin`：查询单个
    # 指定获取单条信息的主键的名称
    lookup_field = "id"

    # 查询
    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            # 通过继承RetrieveModelMixin 提供了self.retrieve 完成了查询单个
            return self.retrieve(request, *args, **kwargs)
        else:
            # 通过继承ListModelMixin 提供self.list完成了查询所有
            return self.list(request, *args, **kwargs)

        # 新增图书  通过继承CreateModelMixin 来获得self.create方法  内部完成了新增

    # 添加 导入 CreateModelMixin,
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return APIResponse(results=response.data)

    # 单整体改  导入 UpdateModelMixin,
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(results=response.data)


    # 单局部改 导入 UpdateModelMixin,
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)

        # 通过继承DestroyModelMixin 获取self

    # 删除 导入 DestroyModelMixin,
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return APIResponse(http_status=status.HTTP_204_NO_CONTENT)


'''generics 下的 九种复合方法
1，ListCreateAPIView ： 查询全部 与 添加
2，UpdateAPIView ： 修改
3，DestroyAPIView ：删除
4，GenericAPIView ： GenericAPIView方法（）
5，ListAPIView ： 查询全部
6，RetrieveAPIView ：查询单条
7，RetrieveDestroyAPIView ：查询单条 与 删除
8，RetrieveUpdateAPIView ： 查询单条 与 修改
9，RetrieveUpdateDestroyAPIView  ：查询单条 与 修改 与 删除
'''

class BookListAPIVIew(generics.ListCreateAPIView, generics.UpdateAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializerV2
    lookup_field = "id"


'''Viewsets 下的 ModelViewSet'''

# class BookGenericViewSet(viewsets.ModelViewSet):
#     queryset = Book.objects.filter(is_delete=False)
#     serializer_class = BookModelSerializerV2
#     lookup_field = "id"
#
#     # 如何确定post请求是需要登录
#     def user_login(self, request, *args, **kwargs):
#         # 可以在此方法中完成用户登录的逻辑
#         return self.retrieve(request, *args, **kwargs)
#
#     def get_user_count(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

# 登录 注册
class USERGenericViewSet(viewsets.ModelViewSet):
    serializer_class = UserDeSerializer
    def login(self,requset,*args,**kwargs):
        try:
            uname = requset.data.get("username")
            pwd = requset.data.get("password")
            user = User.objects.get(username=uname,password=pwd)
            user_m = UserDeSerializer(user).data
        except:
            return APIResponse(0,"登录失败")

    def register(self, requset, *args, **kwargs):
        try:
            regist = self.create(requset, *args, **kwargs)
            return APIResponse(1, "注册成功",results=regist.data)
        except:
            return APIResponse(0, "注册失败")


