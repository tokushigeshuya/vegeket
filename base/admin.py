from django.contrib import admin
from base.models import Item,Category,Tag
from django.contrib.auth.models import Group

class TagInliine(admin.TabularInline):
    model = Item.tags.through

class ItemAdmin(admin.ModelAdmin):
    inlines = [TagInliine]
    # 除外する項目
    exclude = ['tags']

# 表示
admin.site.register(Item,ItemAdmin)
admin.site.register(Category)
admin.site.register(Tag)
# 非表示
admin.site.unregister(Group)
