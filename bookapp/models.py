from django.db import models

# Create your models here.

# 抽象表 基表
class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        # 在元数据中一旦声明此属性后  不会在数据库中创建对应的表结构
        # 其他模型继承这个模型后  可以继承表中的字段
        abstract = True

# 图书表
class Book(BaseModel):
    book_name = models.CharField(max_length=128)  # 书名
    price = models.DecimalField(max_digits=5, decimal_places=2)  # 价钱
    pic = models.ImageField(upload_to="img", default="img/1.jpeg")  # 样图
    publish = models.ForeignKey(to="Press",  # 关联表     # 外键 关联出版社表
                                on_delete=models.CASCADE,  # 级联删除
                                db_constraint=False,  # 删除后对应字段的值可以为空
                                related_name="books")  # 反向查询的名称
    authors = models.ManyToManyField(to="Author", db_constraint=False, related_name="books")
    # 作者

    class Meta:
        db_table = "book_list"
        verbose_name = "图书表"   #表示单数形式的显示    指定在admin管理界面中显示中文
        verbose_name_plural = verbose_name   #表示复数形式的显示

    def __str__(self):
        return self.book_name

    # 自定义序列化字段  作为类属性
    @property
    def publish_name(self):
        return self.publish.press_name

    @property
    def press_address(self):
        return self.publish.address

    @property
    def author_list(self):
        return self.authors.values("author_name", "age", "detail__phone")

# 出版社表
class Press(BaseModel):
    press_name = models.CharField(max_length=128)    # 出板社名
    pic = models.ImageField(upload_to="img", default="img/1.jpeg")   # 出版社示图
    address = models.CharField(max_length=256)    # 出版社地址

    class Meta:
        db_table = "press"
        verbose_name = "出版社"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.press_name


# 作者表
class Author(BaseModel):
    author_name = models.CharField(max_length=128)   # 作者名称
    age = models.IntegerField()                      # 作者年龄

    class Meta:
        db_table = "author_list"
        verbose_name = "作者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name

# 作者详情表
class AuthorDetail(BaseModel):
    phone = models.CharField(max_length=11)    # 联系方式
    author = models.OneToOneField(to="Author", on_delete=models.CASCADE, related_name="detail")
    # 外键   关联 作者表

    class Meta:
        db_table = "author_detail"
        verbose_name = "作者详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s的详情" % self.author.author_name
