from django.db import models
from django.utils.crypto import get_random_string
import os

def created_id():
    # 22文字のランダムな文字列を生成する
    return get_random_string(22)

def upload_image_to(instance, filename):
    # itemのid
    item_id = instance.id
    # static/items/ itemidというフォルダができてfilenameが入る
    return os.path.join('static', 'items', item_id, filename)

# タグ
class Tag(models.Model):
    # ID
    slug = models.CharField(primary_key=True, max_length=32)
    # タグ名
    name = models.CharField(max_length=32)

# カテゴリ
class Category(models.Model):
    # ID
    slug = models.CharField(primary_key=True, max_length=32)
    # カテゴリ名
    name = models.CharField(max_length=32)

# 商品
class Item(models.Model):
    # ID (文字列にする。primary_key=Trueでidと認識、editable=Falseで一度決まったものを編集できないようにする) 
    id = models.CharField(default=created_id, primary_key=True,max_length=22,editable=False)
    # 商品名
    name = models.CharField(default='', max_length=50)
    # 値段（PositiveIntegerFieldはで整数のみ）
    price = models.PositiveIntegerField(default=0)
    # 在庫
    stock = models.PositiveIntegerField(default=0)
    # 説明
    description = models.TextField(default='',blank=True)
    # 販売数
    sold_count = models.PositiveIntegerField(default=0)
    # 非公開フラグ（trueで公開）
    is_published = models.BooleanField(default=False)
    # 作成日時(auto_now_add=Trueで自動追加,auto_now=Trueで自動更新)
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)
    # 画像(upload_toでどこにアップロードされるか指定)
    image = models.ImageField(default="", blank=True, upload_to=upload_image_to)
    
    # カテゴリ一つに対して複数参照（1対N）
    # （第一引数にどのモデルを参照するか記載（Category）on_delete=models.SET_NULLはカテゴリが削除された場合はNULLを入れる）
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # タグは複数つくので複数形　ManyToManyFieldで中間テーブルを作成して複数つけれる
    tags = models.ManyToManyField(Tag)
    # インスタンス参照時にnameだけを表示
    def __str__(self):
        return self.name
