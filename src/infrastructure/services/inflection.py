import re
from typing import Dict
import morfeusz2


class InflectionService:
    """
    Serwis odpowiedzialny za personalizację i odmianę tekstu przy użyciu biblioteki Morfeusz2.
    """

    CASE_MAP = {
        "mianownik": "nom", "nom": "nom",
        "dopelniacz": "gen", "dopełniacz": "gen", "gen": "gen",
        "celownik": "dat", "dat": "dat",
        "biernik": "acc", "acc": "acc",
        "narzednik": "inst", "narzędnik": "inst", "inst": "inst",
        "miejscownik": "loc", "loc": "loc",
        "wolacz": "voc", "wołacz": "voc", "voc": "voc",
    }

    def __init__(self):
        self.morfeusz = morfeusz2.Morfeusz()

    def _inflect_name(self, name: str, case_key: str) -> str:
        """
        Pomocnicza metoda generująca odmienioną formę słowa.
        """
        target_case_tag = self.CASE_MAP.get(case_key.lower(), case_key)
        analyses = self.morfeusz.generate(name)

        for form, _, tags, _, _ in analyses:
            if target_case_tag in tags.split(":"):
                return form

        return name

    def personalize_text(self, text: str, names: Dict[str, str]) -> str:
        """
        Podmienia placeholdery w formacie {klucz:przypadek} na odmienione imiona.
        """
        if not text:
            return ""

        # np. {child_name:inst} lub {grandfather:narzędnik}
        pattern = r"\{(\w+):(\w+)\}"

        def replacer(match):
            key = match.group(1)
            case_req = match.group(2)
            original_name = names.get(key)

            if not original_name:
                return match.group(0)

            inflected = self._inflect_name(original_name, case_req)
            return inflected

        result_text = re.sub(pattern, replacer, text)

        """
        for key, value in names.items():
            simple_placeholder = f"{{{key}}}"
            if simple_placeholder in result_text:
                result_text = result_text.replace(simple_placeholder, str(value))
        """

        return result_text