from django.contrib import admin

from jerseys.models import Jersey, Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Jersey)
class JerseyAdmin(admin.ModelAdmin):
    list_display = ('team', 'type', 'size', 'brand', 'price', 'is_retro', 'stock')
    list_filter = ('team', 'brand', 'type', 'is_retro', 'size')
    search_fields = ('team', 'brand', 'type')
    prepopulated_fields = {'slug': ('team', 'size', 'type')}
