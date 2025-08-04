import json
import time
import urllib
import urllib.request

from nntool.utils.utils_module import read_toml_file
from typing import List
from dataclasses import dataclass
from urllib.parse import quote


@dataclass
class BioOntologyDecoderConfig:
    api_key: str
    rest_url: str = "http://data.bioontology.org"
    time_interval: float = 1.0


def get_json(url, API_KEY):
    opener = urllib.request.build_opener()
    opener.addheaders = [("Authorization", "apikey token=" + API_KEY)]
    return json.loads(opener.open(url).read())


class BioOntologyDecoder:
    def __init__(self, config: BioOntologyDecoderConfig):
        self.config = config
        self.api_key = config.api_key
        self.rest_url = config.rest_url

    def query_cell(self, cell_name: str, top_k: int = 1):
        # Do a search for every term
        results = get_json(
            self.rest_url + "/search?q=" + quote(cell_name) + "&ontologies=CL",
            API_KEY=self.api_key,
        )

        # each result with dict_keys(['prefLabel', 'synonym', 'definition', 'obsolete', 'matchType', 'ontologyType', 'provisional', '@id', '@type', 'links', '@context'])
        # each links with dict_keys(['self', 'ontology', 'children', 'parents', 'descendants', 'ancestors', 'instances', 'tree', 'notes', 'mappings', 'ui', '@context'])
        search_results = results["collection"]
        top_search_results = search_results[:top_k]

        # query the parent cell
        top_results = []
        for result in top_search_results:
            parents_result = []
            if "parents" in result["links"]:
                parents_result = get_json(result["links"]["parents"], API_KEY=self.api_key)
            top_results.append({"result": result, "parents": parents_result})

        return top_results

    def decode(self, cell_list: List[str], top_k: int = 1, *args, **kwargs) -> List[List[dict[str, str]]]:
        results = []
        for cell in cell_list:
            time.sleep(self.config.time_interval)
            results.append(self.decode_one(cell, top_k=top_k, *args, **kwargs))

        return results

    def decode_one(self, cell: str, top_k: int = 1, *args, **kwargs) -> List[dict[str, str]]:
        top_results = self.query_cell(cell, top_k=top_k)
        decoded_results = []

        # if there is no result, return the original cell name
        if top_results:
            for result in top_results:
                decoded_result = {}
                decoded_result["prefLabel"] = result["result"]["prefLabel"]
                decoded_result["synonym"] = result["result"].get("synonym", [])
                decoded_result["definition"] = result["result"].get("definition", "")
                decoded_result["parents"] = []

                for parent in result["parents"]:
                    parent_result = {}
                    parent_result["prefLabel"] = parent["prefLabel"]
                    parent_result["synonym"] = parent.get("synonym", [])
                    parent_result["definition"] = parent.get("definition", "")
                    decoded_result["parents"].append(parent_result)

                decoded_results.append(decoded_result)
        else:
            decoded_results.append({"prefLabel": cell, "synonym": [], "definition": ""})
        return decoded_results


if __name__ == "__main__":
    api_key = read_toml_file("env.toml")["bioportal"]["token"]
    config = BioOntologyDecoderConfig(api_key=api_key)
    decoder = BioOntologyDecoder(config)

    result = decoder.decode(["Conventional Dendritic Cell 2"], top_k=1)
    print(result)
