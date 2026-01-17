from django.contrib import admin

from jerseys.models import Jersey, Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Jersey)
class JerseyAdmin(admin.ModelAdmin):
    list_display = ['team', 'size', 'brand', 'type', 'price', 'is_retro', 'stock', 'slug', 'created_at']
    list_filter = ['size', 'brand', 'type', 'is_retro', 'team', 'created_at']
    search_fields = ['team__name', 'description', 'slug']
    prepopulated_fields = {'slug': ('team', 'type', 'size')}  
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {'fields': ('team', 'size', 'brand', 'type', 'slug')}),
        ('Pricing & Stock', {'fields': ('price', 'stock', 'is_retro')}),
        ('Media & Description', {'fields': ('image', 'description')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )