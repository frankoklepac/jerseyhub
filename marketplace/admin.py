from django.contrib import admin

from marketplace.models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'team', 'size', 'brand', 'type', 'price', 'is_retro', 'buyer')
    list_filter = ('team', 'brand', 'type', 'is_retro', 'size')
    search_fields = ('title', 'owner__username', 'team__name', 'brand', 'type')
    prepopulated_fields = {'slug': ('team', 'size', 'type', 'owner')}