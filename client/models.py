from django.db import models


class Gallery(models.Model):  # トップページのメインスライド
    img = models.ImageField(upload_to='gallery/', blank=True, null=True)
    title = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_standby = models.BooleanField(default=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        if self.is_standby:
            return f'[{self.pk}] is on standby.'
        return f'[{self.pk}]{self.title} PATH:{self.img.url}'


class Sample(models.Model):  # デザインデータサンプル画像
    img = models.ImageField(upload_to='sample/', null=True, blank=True)
    name = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_standby = models.BooleanField(default=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        if self.is_standby:
            return f'[{self.pk}] is on standby.'
        return f'[{self.pk}]{self.name} PATH:{self.img.url}'


class Family(models.Model):  # ファミリー
    img = models.ImageField(upload_to='family/', null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(max_length=300, null=True, blank=True)
    is_standby = models.BooleanField(default=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        if self.is_standby:
            return f'[{self.pk}]is on standby.'
        return f'[{self.pk}]{self.title}: {self.img.url}'


class LineUser(models.Model):
    account = models.CharField(max_length=50, default='dev')
    user_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    is_receiver = models.BooleanField(default=False)

    class Meta:
        ordering = ['pk']
        unique_together = [['account', 'user_id'], ['account', 'name']]

    def __str__(self):
        return f'Line User ID: {self.user_id}'
