# QUIZAPP RESTAPI

### O projekcie:
Aplikacja stworzona w Django Rest Framework do sprawdzania swojej wiedzy w quizach z języków
programowania, umożliwia proponowanie nowych pytań przez użytkowników,
zweryfikowane przez administatora sugestie mogą zostać dodane do określonego quizu lub odrzucone
Rozwiązywać quizy można anonimowo, jeśli chcemy zasugerować nowe pytanie do quizy należy
się zarejestrować.\
Aplikacja ma testy jednostkowe do pytań, kategorii i rejestracji użytkowników.

> *Podgląd aplikacji: **[LINK](https://quiz-app-restapi.herokuapp.com/)***


### Użyte technologie:
- Django
- DRF

### Instalacja:

**1. Pobranie projektu**
```
git clone https://github.com/jaugustyn/quizapp.git
```

**2. Stwórz i aktywuj środowisko wirtualne:**
```
virtualenv env
```

**3. Instalacja potrzebnych bibliotek:**
```
pip install -r requirements.txt
```

**4. Wygeneruj secret_key:**
```
python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
```

**5. Stwórz plik ".env" i dodaj w nim:** 
```
SECRET_KEY = "generated_key"
```

**6. Stworzenie migracji i uruchomienie serwera:**  
```
bash  python manage.py makemigrations quiz, accounts \  python manage.py migrate \  python manage.py runserver
```

**Enjoy**
