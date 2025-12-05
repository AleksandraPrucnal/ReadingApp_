from pydantic import BaseModel, Field

class InflectionRequest(BaseModel):
    text: str = Field(..., description="Tekst bazowy do personalizacji/odmiany")
    names: dict[str, str] = Field(
        ...,
        description="Słownik imion, np. {'child_name': 'Ola', 'grandfather': 'Dziadek Paweł'}",
        example={
            "child_name": "Ola",
            "grandfather": "Dziadek Paweł",
            "grandmother": "Babcia"
        }
    )

class InflectionResponse(BaseModel):
    original_text: str
    inflected_text: str