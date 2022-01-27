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
> git clone https://github.com/jaugustyn/quizapp.git \
> ***Stwórz środowisko wirtualne: [LINK](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)*** \
> pip install -r requirements.txt \
> ***Wygeneruj secret_key:*** python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())' \
> ***Stwórz plik ".env" i dodaj w nim:*** SECRET_KEY = < generated_key > \
> py manage.py makemigrations quiz, accounts \
> py manage.py migrate \
> py manage.py runserver

**Enjoy**