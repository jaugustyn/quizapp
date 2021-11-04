from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.db import models


# Create your models here.


class Answer(models.Model):
    answer1 = models.CharField(max_length=200)
    answer2 = models.CharField(max_length=200)
    answer3 = models.CharField(max_length=200)
    answer4 = models.CharField(max_length=200)
    choices = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")]
    correct_answer = models.CharField(max_length=200, choices=choices, help_text="Which answer is correct: 1, 2, 3 or 4?")

    def __str__(self):
        return self.correct_answer


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    image = models.ImageField(upload_to='static/img/', blank=True, null=True)
    slug = models.SlugField(unique=True, null=False, help_text="Category_url", db_column="Category_url")
    color = models.CharField(max_length=10, default="#")  # For frontend guy
    description = models.TextField(max_length=500, default="Category description")

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Question(models.Model):
    category = models.ForeignKey(Category, to_field='name', db_column="category_name", blank=True, null=True, on_delete=models.SET_NULL)
    question = models.CharField(max_length=200)
    answers = models.OneToOneField(Answer, on_delete=models.CASCADE, related_name="answers")
    points = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], default=1, help_text="1 - 3 points")
    approved = models.BooleanField(default=True, help_text="Does the question meet the rules and can be added to one of the quizzes?")

    def __str__(self):
        return self.question


class Quiz(models.Model):
    description = models.CharField(max_length=300, default="Quiz description")
    category = models.ForeignKey(Category, to_field='name', on_delete=models.CASCADE, related_name="category_name")
    question = models.ManyToManyField(Question)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.description
