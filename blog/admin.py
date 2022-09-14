from django.contrib import admin
from .models import Post, AuthorProfile
# from .models import AuthorProfile

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
admin.site.register(AuthorProfile)
