from email.mime import image
from django.db import models
from django.contrib.auth.models import User
# from froala_editor.fields import FroalaField
from tinymce import models as tinymce_models
from django.utils.safestring import mark_safe
from django.utils.text import slugify

# Create your models here.
class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    bio = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return self.user.username


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
    

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(AuthorProfile, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    # content = models.TextField()
    # content = FroalaField()
    content = tinymce_models.HTMLField()
    image = models.ImageField(upload_to='pics')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)   

    def __str__(self):
        return self.title
    
    def image_tag(self): # new
        return mark_safe('<img src="/../../media/%s" width="50" height="50" />' % (self.image))

class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.name)
