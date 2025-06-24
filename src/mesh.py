import requests
import urllib.parse
import typing

def search_mesh_terms(base: str, 
                      match: typing.Literal["exact", "contains", "startswith"],
                      num: int):
    response = requests.get("https://id.nlm.nih.gov/mesh/lookup/term?"
                            +
                            "label="
                            +
                            urllib.parse.quote_plus(base)
                            +
                            "&match="
                            +
                            match
                            +
                            "&limit="
                            +
                            f"{num}")
    if response.status_code != 200:
        raise Exception(f"search_mesh_term: Fail to search {repr(base)}(status code: {response.status_code})")
    results = []
    for record in response.json():
        results.append(record["label"])
    return results