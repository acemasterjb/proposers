from asyncio import run as asyncio_run
from os import getenv
from pprint import PrettyPrinter
from typing import Any

from dotenv import load_dotenv
from graphql import DocumentNode
from gql import dsl, Client
from gql.transport.aiohttp import AIOHTTPTransport


def proposers_query(
        schema: dsl.DSLSchema,
        space: str,
        author: str,
        limit: int = 100,
        skip: int = 0
) -> DocumentNode:
    where = {
        "space": space,
        "author": author,
        "flagged": False} if author else {
            "space": space,
            "flagged": False
        }

    query = dsl.DSLQuery(
        schema.Query.proposals(
            where=where,
            first=limit, skip=skip
        ).select(
            schema.Proposal.id,
            schema.Proposal.author,
            schema.Proposal.flagged,
        )
    )

    return dsl.dsl_gql(query)


async def get_proposals_from_space(space_name: str, proposal_author: str = ""):
    load_dotenv()

    headers = {"x-api-key": getenv("SNAPSHOT_API")}
    transport = AIOHTTPTransport(
        url="https://hub.snapshot.org/graphql",
        headers=headers,
        timeout=120
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    session = await client.connect_async(reconnecting=True)
    ds = dsl.DSLSchema(client.schema)
    query = proposers_query(ds, space_name, proposal_author)

    response = await session.execute(query)
    await client.close_async()

    if not response.get("proposals"):
        return {"proposals": []}
    return response


def get_proposals_by(
        proposal_author: str, proposals: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    return [
        proposal for proposal in proposals if proposal["author"] == proposal_author
    ]


def get_proposal_statistics_for(space_name: str) -> dict[str, int]:
    all_proposals = asyncio_run(get_proposals_from_space(space_name))

    all_authors = set(
        proposal["author"] for proposal in all_proposals["proposals"]
    )

    return {
        author: len(get_proposals_by(author, all_proposals["proposals"]))
        for author in all_authors
    }


def hop_proposers_stats() -> dict[str, int]:
    space = input("Enter the space name: ")
    stats = get_proposal_statistics_for(space)

    pp = PrettyPrinter(indent=2)

    pp.pprint(stats)


if __name__ == "__main__":
    hop_proposers_stats()


def hello():
    return "Hello from proposers!"
