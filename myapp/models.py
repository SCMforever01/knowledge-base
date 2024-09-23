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

