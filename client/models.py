from django.db import models


class Gallery(models.Model):  # トップページのメインスライド
  img = models.ImageField(upload_to='gallery/')
  title = models.TextField(max_length=100)
  
  def __repr__(self):
    return f'<[{self.pk}]{self.title}: {self.img.url}>'


class Sample(models.Model):  # デザインデータサンプル画像
  img = models.ImageField(upload_to='sample/')
  name = models.CharField(max_length=15, unique=True)

  def __repr__(self):
    return f'<[{self.pk}]{self.img.url}>'
  

class Family(models.Model):  # ファミリー
  img = models.ImageField(upload_to='family/')
  title = models.TextField(max_length=100)
  text = models.TextField(max_length=300)

  def __repr__(self):
    return f'<[{self.pk}]{self.title}: {self.img.url}>'
  