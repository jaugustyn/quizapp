from django.contrib import admin
from .views import Category, Question, Quiz, Answer

# Register your models here.

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


admin.site.register(Category, CategoryAdmin)
