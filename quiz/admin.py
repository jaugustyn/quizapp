from django.contrib.auth import get_user_model
from django.contrib import admin
from .views import Category, Question, Quiz, Answer
from accounts.views import User

# Register your models here.

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)


user = get_user_model()
admin.site.register(user)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


admin.site.register(Category, CategoryAdmin)
