# Medium API in Python – scrape Medium articles to Markdown (working example)

Scrape **Medium articles** by **tag**, **author**, **publication** or **keyword search** from Python, JavaScript or n8n: title, subtitle, author, date, **claps**, **responses**, **reading time**, tags and the **full text as clean Markdown**, ready for RAG pipelines and AI agents. Member-only stories are flagged (`isPaywalled`) and return only the public preview.

Powered by the [medium-scraper](https://apify.com/lagenuina_agency/medium-scraper) actor on Apify. No Medium account, no API key from Medium, no browser.

## Example output (real result, shortened)

```json
{
  "id": "c2d91ecfdf77",
  "url": "https://medium.com/data-science/improving-agent-systems-ai-reasoning-c2d91ecfdf77",
  "title": "Improving Agent Systems & AI Reasoning",
  "author": "Tula Masterman",
  "publication": "TDS Archive",
  "publishedAt": "2025-02-02T14:32:00.159Z",
  "claps": 166,
  "responses": 4,
  "readingTimeMinutes": 8.9,
  "tags": ["aireasoning", "generative-ai-tools", "ai-agent", "llm", "editors-pick"],
  "isPaywalled": false,
  "markdown": "### DeepSeek-R1, OpenAI o1 & o3, Test-Time Compute Scaling...\n\n![Image by author](https://miro.medium.com/v2/resize:fit:1400/1*oI0lijofursOtYkoEZqtrw.png)\n\n..."
}
```

## Quickstart (3 steps)

1. Create a free Apify account and copy your API token from [Settings → Integrations](https://console.apify.com/settings/integrations).
2. Put it in an environment variable (never in code): `export APIFY_TOKEN=your_token`
3. Run the example:

```bash
pip install -r python/requirements.txt
python python/example.py --tag rag --max 20
```

JavaScript: `cd js && npm install && node example.mjs rag`

## Examples

**Python** (`pip install "apify-client<2"`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("lagenuina_agency/medium-scraper").call(run_input={
    "tags": ["rag"],
    "users": ["@dhh"],
    "searchQueries": ["langgraph agents"],
    "maxItemsPerFeed": 20,
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["title"], item["claps"], item["url"])
```

**JavaScript / Node.js** (`npm install apify-client`)

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('lagenuina_agency/medium-scraper').call({ tags: ['rag'], maxItemsPerFeed: 20 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

**cURL / any language** – one HTTP call, results in the response:

```bash
curl -X POST "https://api.apify.com/v2/acts/lagenuina_agency~medium-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"publications": ["towards-data-science"], "maxItemsPerFeed": 10}'
```

All input fields are documented on the [actor page](https://apify.com/lagenuina_agency/medium-scraper) (Input tab).

## Use case: Medium articles to Markdown files for RAG

`python/example.py` writes one `.md` file per article (YAML front matter with title, author, URL, date, claps, tags, paywall flag + the body in Markdown) into `./medium_md/`. Point LlamaIndex `SimpleDirectoryReader`, LangChain `DirectoryLoader` or your vector database loader at that folder.

## n8n workflow

[`n8n/workflow.json`](n8n/workflow.json): every day 08:00 → latest Medium articles for your tags → one row per article (date, title, author, claps, responses, reading time, member-only, tags, URL) → append to Google Sheets.

1. In n8n: **Workflows → Import from File** and pick `n8n/workflow.json`.
2. Create a **Header Auth** credential named `Apify API token` with name `Authorization` and value `Bearer <your token>`, and select it in the *Run Apify actor* node.
3. Edit the JSON body (your tags, authors, publications), set your Google Sheet ID and activate.

The `run-sync-get-dataset-items` endpoint waits up to 300 s; for bigger runs use `/runs` plus a webhook.

## Use with AI agents (MCP)

Give Claude, ChatGPT, Cursor or any MCP client this actor as a tool:

```json
{
  "mcpServers": {
    "medium-scraper": {
      "url": "https://mcp.apify.com/?actors=lagenuina_agency/medium-scraper"
    }
  }
}
```

Sign in with Apify OAuth when asked, or send `Authorization: Bearer <APIFY_TOKEN>`.

## Pricing

$8 per 1,000 articles ($0.008 each) on every Apify plan (Free, Bronze, Silver, Gold, Platinum, Diamond), platform usage included, no start fee, pay only for articles returned – see [lagenuina_agency/medium-scraper](https://apify.com/lagenuina_agency/medium-scraper).

## Disclaimer

Independent, not affiliated with or endorsed by A Medium Corporation. It reads only publicly available data and never bypasses the paywall. Articles are copyrighted by their authors: use them in line with the applicable terms and laws.

## License

[MIT](LICENSE) © Quelli di Carne Genuina
