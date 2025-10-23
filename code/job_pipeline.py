import dlt
import requests
import json
from pathlib import Path
import os

query = ""

# Yrken med social inriktning, "Yrken med teknisk inriktning", "Chefer och verksamhetsledare"
occupation_fields = ("GazW_2TU_kJw", "6Hq3_tKo_V57", "bh3H_Y3h_5eD")

def _get_ads(url_for_search, params):
    headers = {"accept": "application/json"}
    response = requests.get(url_for_search, headers=headers, params=params)
    response.raise_for_status()  # check for http errors
    return json.loads(response.content.decode("utf8"))


@dlt.resource(table_name ="job_ads",write_disposition="merge", primary_key="id")
def jobsearch_resource(params):
    """
    params should include at least:
      - "q": your query
      - "limit": page size (e.g. 100)
    """
    url = "https://jobsearch.api.jobtechdev.se"
    url_for_search = f"{url}/search"
    limit = params.get("limit", 100)
    offset = 0

    while True:
        # build this page’s params
        page_params = dict(params, offset=offset)
        data = _get_ads(url_for_search, page_params)

        hits = data.get("hits", [])
        if not hits:
            # no more results
            break

        # yield each ad on this page
        for ad in hits:
            yield ad

        # if fewer than a full page was returned, we’re done
        if len(hits) < limit or offset > 1900:
            break

        offset += limit


@dlt.source
def jobads_source():
    for occupation_field in occupation_fields:
        params = {"q": query, "limit": 100, "occupation-field": occupation_field}
        return jobsearch_resource(params=params)
        
