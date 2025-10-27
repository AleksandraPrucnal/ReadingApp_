import re
import morfeusz2

morfeusz = morfeusz2.Morfeusz()

def inflect_name(name: str, case: str) -> str:
    analyses = morfeusz.generate(name)
    for form, _, tags, _, _ in analyses:
        if case in tags.split(":"):
            return form
    return name

def inflect_in_text(text: str, favourite_names: dict) -> str:
    pattern = r"\{(\w+):(\w+)\}"
    return re.sub(pattern, lambda m: inflect_name(favourite_names.get(m.group(1), ""), m.group(2)) or m.group(0), text)

text = "Dziadek {grandfather:nom} piecze ciasto z {child_name:inst}."
favourite_names = {
    "child_name": "Ola",
    "grandfather": "Paweł"
}

result = inflect_in_text(text, favourite_names)
print(result)
