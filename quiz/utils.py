import random
from .models import Question

def get_random_question(name):
    questions = []
    max_id = Question.objects.all().filter(category_id=name).aggregate(max_id=Max("id"))['max_id']
    pk = random.sample(range(1, max_id), k=5)
    print(pk)
    for pk_idx in pk:  
        category = Question.objects.filter(id=pk_idx).first()
        if category:
            questions.append(category)
    return questions
