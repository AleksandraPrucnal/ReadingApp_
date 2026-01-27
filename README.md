# Backend API

## O projekcie

Backend dla innowacyjnej aplikacji mobilnej wspierającej naukę czytania ze zrozumieniem u dzieci. System rozwiązuje problem braku zaangażowania uczniów poprzez **personalizację treści w czasie rzeczywistym**.

Kluczową funkcjonalnością jest implementacja mechanizmu personalizacji opartego na przetwarzaniu języka naturalnego (NLP). Dynamicznie wplata imiona bliskich dziecka (rodziny, zwierząt) w treść zadań, dbając o **poprawną odmianę gramatyczną (fleksję) w języku polskim**.

### Kluczowe funkcjonalności
* **RESTful API:** Wydajne, asynchroniczne endpointy zbudowane w oparciu o framework FastAPI.
* **Zaawansowana personalizacja (NLP):** Wykorzystanie biblioteki `Morfeusz2` do morfologicznej analizy i odmiany imion przez przypadki.
* **Generowanie treści:** System dynamicznie uzupełnia szablony czytanek, zachowując poprawność językową (np. zamiana "Ola" na "Olą" w narzędniku).
* **Zarządzanie użytkownikami:** Autentykacja (JWT), role użytkowników.
* **Ćwiczenia:** Dwa typy ćwiczeń- dopasuj obrazek i quiz.
* **Progres:** Śledzenie postępów i zapisywanie wyników.

## Tech Stack

* **Core:** Python, FastAPI, Pydantic
* **Database:** PostgreSQL, SQLAlchemy
* **NLP:** Morfeusz2
* **Architecture:** Onion Architecture
* **DevOps:** Docker, Docker Compose

## Proces tworzenia

Projekt realizowany był zgodnie z podejściem **API-First / Backend-First**, co pozwoliło na stabilny rozwój systemu:

1.  **Domain & Data Modeling:** Prace rozpoczęto od zaprojektowania modeli domenowych oraz struktury bazy danych.
2.  **Backend Implementation:** Implementacja logiki biznesowej oraz wystawienie endpointów REST API.
3.  **Parallel UI/UX Design:** Równolegle do prac backendowych trwało projektowanie interfejsów i makiety aplikacji mobilnej. (portfolio z projektem: https://bit.ly/portfolio-prucnal)
4.  **Mobile Integration:** Finalnym etapem była implementacja warstwy wizualnej we Flutterze i integracja z przygotowanym wcześniej, przetestowanym API. (frontend: https://github.com/AleksandraPrucnal/frontend_ReadingApp)

## Architektura

W projekcie zastosowano wzorzec **Onion Architecture**, aby zapewnić separację logiki biznesowej od zewnętrznych frameworków i bazy danych.

```text
src/
|-- api/                        # Warstwa PREZENTACJI
|   |-- deps/
|   |   |-- auth.py
|   |-- routers/                # Endpointy (kontrolery)
|   |   |-- exercise.py
|   |   |-- inflection.py
|   |   |-- ...
|   |-- dependencies.py         # Zależności (np. get_current_user)
|
|-- core/                       # Warstwa DOMENY 
|   |-- domain/
|   |   |-- exercises/          # Modele domenowe
|   |   |-- user.py
|   |   |-- ...
|   |-- repositories/           # Interfejsy (Kontrakty)
|       |-- iexercise_repository.py
|       |-- ...
|
|-- infrastructure/             # Warstwa INFRASTRUKTURY
|   |-- dto/                    # Obiekty Transferu Danych (Pydantic)
|   |   |-- exerciseDTO.py
|   |   |-- ...
|   |-- repositories/           # Implementacja dostępu do bazy
|   |   |-- exercise_repository.py
|   |   |-- ...
|   |-- services/               # Logika biznesowa
|       |-- exercise.py
|       |-- inflection.py       # Logika Morfeusza
|       |-- ...
|
|-- config.py                   # Konfiguracja bazy danych
|-- container.py                # Konfiguracja Dependency Injection
|-- db.py                       # Schematy i połączenie z bazą danych
|-- main.py                     # Punkt startowy aplikacji
|-- data.sql                    # Zainicjalizowane obiekty początkowe w bazie danych
