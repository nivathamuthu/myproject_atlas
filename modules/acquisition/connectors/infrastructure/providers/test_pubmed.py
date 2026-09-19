import asyncio

from modules.acquisition.connectors.infrastructure.providers.pubmed import (
    search_pubmed,
)


async def main() -> None:
    pmids = await search_pubmed("diabetes")
    print("Matching PMIDs:")
    for pmid in pmids:
        print(pmid)


if __name__ == "__main__":
    asyncio.run(main())