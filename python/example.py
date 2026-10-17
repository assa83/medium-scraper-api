"""Export Medium articles to Markdown files for RAG / LLM knowledge bases.

Usage: python example.py --tag rag --max 20
       python example.py --user @dhh
       python example.py --search "langgraph agents"
Writes one .md file per article (YAML front matter + body) in ./medium_md/
"""
import argparse
import os
import re
import sys

from apify_client import ApifyClient

ACTOR = "lagenuina_agency/medium-scraper"
TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tag", action="append", default=[], help="Medium tag, e.g. rag")
    p.add_argument("--user", action="append", default=[], help="Medium username, e.g. @dhh")
    p.add_argument("--publication", action="append", default=[], help="publication slug, e.g. towards-data-science")
    p.add_argument("--search", action="append", default=[], help="keyword search")
    p.add_argument("--max", type=int, default=20, help="max articles per source")
    p.add_argument("--out", default="medium_md")
    a = p.parse_args()
    if not (a.tag or a.user or a.publication or a.search):
        a.tag = ["rag"]

    client = ApifyClient(TOKEN)
    run = client.actor(ACTOR).call(run_input={
        "tags": a.tag, "users": a.user, "publications": a.publication, "searchQueries": a.search,
        "maxItemsPerFeed": a.max,
    })
    os.makedirs(a.out, exist_ok=True)
    n = 0
    for it in client.dataset(run["defaultDatasetId"]).iterate_items():
        slug = re.sub(r"[^a-z0-9]+", "-", (it["title"] or it["id"]).lower()).strip("-")[:80]
        front = "\n".join([
            "---",
            f"title: {json_str(it['title'])}",
            f"author: {json_str(it['author'])}",
            f"url: {it['url']}",
            f"published: {it['publishedAt']}",
            f"claps: {it['claps']}",
            f"tags: [{', '.join(it['tags'])}]",
            f"paywalled: {str(it['isPaywalled']).lower()}",
            "---",
        ])
        with open(os.path.join(a.out, f"{slug}-{it['id']}.md"), "w", encoding="utf-8") as f:
            f.write(f"{front}\n\n# {it['title']}\n\n{it['markdown'] or ''}\n")
        n += 1
    print(f"{n} articles -> {a.out}/")


def json_str(s):
    return '"' + (s or "").replace("\\", "\\\\").replace('"', '\\"') + '"'


if __name__ == "__main__":
    main()
