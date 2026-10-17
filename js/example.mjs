// Most-clapped recent Medium articles for a tag.
// Usage: node example.mjs rag
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set APIFY_TOKEN first: https://console.apify.com/settings/integrations');
    process.exit(1);
}

const tag = process.argv[2] ?? 'rag';
const client = new ApifyClient({ token });
const run = await client.actor('lagenuina_agency/medium-scraper').call({ tags: [tag], maxItemsPerFeed: 30 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
items.sort((a, b) => b.claps - a.claps);
for (const it of items.slice(0, 10)) {
    console.log(`${it.claps} claps | ${it.readingTimeMinutes} min | ${it.isPaywalled ? 'member-only' : 'free'} | ${it.title}\n  ${it.url}`);
}
