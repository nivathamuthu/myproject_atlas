# import httpx


# NCBI_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"


# async def search_pubmed(term: str) -> list[str]:
#     params = {
#         "db": "pubmed",
#         "term": term,
#         "retmode": "json",
#         "retmax": 10,
#     }

#     async with httpx.AsyncClient(timeout=30.0) as client:
#         response = await client.get(NCBI_ESEARCH_URL, params=params)
#         response.raise_for_status()

#     data = response.json()
#     return data["esearchresult"]["idlist"]