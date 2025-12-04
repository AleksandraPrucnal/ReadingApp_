import re
import morfeusz2

# Inicjalizacja morfeusza raz (jest to kosztowne operacyjnie)
morfeusz = morfeusz2.Morfeusz()


class InflectionService:
    def __init__(self):
        # Domyślne imiona, gdyby użytkownik ich nie ustawił
        self.defaults = {
            "child_name": "Jasiu",
            "mom_name": "Mama",
            "dad_name": "Tata",
            "grandfather": "Dziadek",
            "grandmother": "Babcia"
        }

    def _inflect_word(self, name: str, case_tag: str) -> str:
        """
        Próbuje odmienić słowo. Jeśli się nie uda lub imię jest nieznane,
        zwraca formę podstawową.
        """
        try:
            analyses = morfeusz.generate(name)
            for form, _, tags, _, _ in analyses:
                # Sprawdzamy czy tag przypadku (np. 'inst') znajduje się w tagach morfeusza
                # Tagi morfeusza są złożone, np. 'subst:sg:inst:m1'
                if case_tag in tags.split(":"):
                    return form
        except Exception:
            pass  # W razie błędu biblioteki

        return name

    def personalize_text(self, text: str, user_names: dict) -> str:
        """
        Główna funkcja podmieniająca placeholdery w tekście.
        """
        # Łączymy domyślne imiona z tymi podanymi przez użytkownika
        # (user_names nadpisują defaults)
        names_map = {**self.defaults, **user_names}

        pattern = r"\{(\w+):(\w+)\}"

        def replacement(match):
            key = match.group(1)  # np. child_name
            case = match.group(2)  # np. inst (narzędnik)

            name_to_inflect = names_map.get(key, self.defaults.get(key, key))

            # Odmieniamy imię
            inflected = self._inflect_word(name_to_inflect, case)

            # Jeśli to początek zdania (nie dotyczy środka tekstu, ale warto mieć na uwadze),
            # można dodać logikę .capitalize(), ale tu zostawiamy prosto.
            return inflected

        return re.sub(pattern, replacement, text)


# Instancja singleton (opcjonalnie)
inflector = InflectionService()