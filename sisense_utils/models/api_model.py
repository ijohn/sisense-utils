from pydantic import BaseModel


def camelize(string: str) -> str:
    if "_" not in string:
        return string
    words = string.split("_")
    words = [words[0]] + [word.capitalize() for word in words[1:]]
    return "".join(words)


class APIModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True
