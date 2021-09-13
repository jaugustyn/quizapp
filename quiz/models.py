from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, null=False)
    image = models.ImageField(upload_to='quiz/static/img/', null=False, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Question(models.Model):
    question = models.CharField(max_length=200)
    correct = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    DATA_SCHEMA = {
            "first": "",
            "second": "",
            "third": "",
            "fourth": ""
        }

    details = models.JSONField(default=DATA_SCHEMA)

    def __str__(self):
        return self.question
