from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, null=False)
    image = models.ImageField(upload_to='quiz/static/images/category_images/', null=False, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
