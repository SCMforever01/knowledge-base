from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    ns_id = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}-{}-{}".format(self.ns_id, self.name, self.role)

    class Meta:
        db_table = 'user'  # 定义数据库表名
        verbose_name = 'User'  # 单数形式
        verbose_name_plural = 'Users'  # 复数形式
        ordering = ['-create_time']  # 默认按创建时间降序排列
        unique_together = ('name', 'ns_id')  # name 和 ns_id 组合唯一


class Collection(models.Model):
    file_name = models.CharField(max_length=255, null=False, blank=False)
    file_path = models.CharField(max_length=500, null=False, blank=False)
    file_size = models.BigIntegerField(null=False, blank=False)
    file_type = models.CharField(max_length=10, null=False, blank=False)
    file_hash = models.CharField(max_length=64, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    index_status = models.BooleanField(default=False)
    is_delete = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    update_time = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        return "{}.{}.{}".format(self.file_name,self.owner,self.file_type)

    class Meta:
        db_table = 'collection'
        verbose_name = 'File Collection'
        verbose_name_plural = 'File Collections'
        ordering = ['-create_time']
        unique_together = ('file_name','file_type','owner')
