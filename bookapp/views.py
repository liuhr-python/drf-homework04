from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from bookapp.models import Book
from .serializers import BookModelSerializerV2  # 导入整合序列化器

# 在序列化器与反序列化器 整合情况下的类试图
class BookAPIViewV2(APIView):

    # 查询信息
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            print(book_id)
            book_obj = Book.objects.get(pk=book_id, is_delete=False)
            print(book_obj, type(book_obj), "1111")
            book_ser = BookModelSerializerV2(book_obj).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询单个图书成功",
                "results": book_ser
            })

        else:
            book_list = Book.objects.filter(is_delete=False)
            book_list_ser = BookModelSerializerV2(book_list, many=True).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询所有图书成功",
                "results": book_list_ser
            })

    # 添加信息
    def post(self, request, *args, **kwargs):

        request_data = request.data
        if isinstance(request_data, dict):  # 代表增加的是单个图书
            # 将前端发送过来的数据交给反序列化器进行校验
            many = False
        elif isinstance(request_data, list):  # 代表添加多个图书
            many = True
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "请求参数格式有误",
            })

        book_ser = BookModelSerializerV2(data=request_data, many=many)
        # 校验数据是否合法 raise_exception：一旦校验失败 立即抛出异常
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "添加图书成功",
            # 当群增多个时，无法序列化多个对象到前台  所以报错
            "result": BookModelSerializerV2(book_obj, many=many).data
        })

    # 删除信息
    def delete(self, request, *args, **kwargs):

        book_id = kwargs.get("id")
        if book_id:
            # 删除单个  也作为删除多个
            ids = [book_id]
        else:
            # 删除多个
            ids = request.data.get("ids")

        # 判断传递过来的图书的id是否在数据库  且还未删除
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "删除成功"
            })

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "删除失败或图书不存在"
        })

    # 修改信息（单个的整体与局部，多个的整体与局部）
    def patch(self, request, *args, **kwargs):

        request_data = request.data
        book_id = kwargs.get("id")

        # url中有id存在且传递的参数是字典   单个修改  修改单个  群改一个
        if book_id and isinstance(request_data, dict):
            book_ids = [book_id, ]
            request_data = [request_data]

        # url中无id不存在且参数是列表 修改多个
        elif not book_id and isinstance(request_data, list):
            book_ids = []
            # 将要修改的图书的id取出放进 book_ids中
            for dic in request_data:
                pk = dic.pop("pk", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "PK不存在",
                    })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "数据格式有误",
            })

        book_list = []  # 所有要修改的图书对象
        new_data = []  # 所有要修改的参数

        # 禁止在循环中对列表的长度做改变
        for index, pk in enumerate(book_ids):
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                new_data.append(request_data[index])

            except:
                # 如果图书对象不存在  跳过

                continue

        book_ser = BookModelSerializerV2(data=new_data, instance=book_list, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "修改成功",
        })