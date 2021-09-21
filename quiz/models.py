from django.db import models
from django.utils.text import slugify

# Create your models here.

class Answer(models.Model):
    a = models.CharField(max_length=200, default="a")
    b = models.CharField(max_length=200, default="b")
    c = models.CharField(max_length=200, default="c")
    d = models.CharField(max_length=200, default="d")
    correct_answer = models.CharField(max_length=200, default="x")

    def __str__(self):
        return self.correct_answer


class Question(models.Model):
    question = models.CharField(max_length=200)
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True)
    points = models.PositiveIntegerField()

    def __str__(self):
        return self.question


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    image = models.ImageField(upload_to='static/img/')
    slug = models.SlugField(unique=True, null=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Quiz(models.Model):
    description = models.TextField(max_length=500)
    category = models.ForeignKey(Category, to_field='name', on_delete=models.CASCADE)
    question = models.ManyToManyField(Question, blank=True)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.description
