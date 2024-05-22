// these urls are filtered because they are often behind a paywall
const filteredUrls = ['twitter.com', 'bloomberg.com', 'nytimes.com', 'wsj.com', 'ft.com', 'economist.com', 'reuters.com', 'washingtonpost.com', 'filtered'];
const filteredTerms = ['trump', 'roe', 'abortion', 'shooting', 'gun', 'first mover', 'elon', 'musk', 'deal', 'deals', 'hiring', 'price', 'bitcoin', 'NFT', 'best', 'only', 'most', 'every', 'bull', 'bulls', 'defi'];

function newsfeed(topic) {
  let urls;
  if (topic === 'finance') {
    // a list of sources used to pull in engineering news
    // source: https://hnrss.github.io/ (a hacker news rss feed)
    urls = [
      'https://www.cnbc.com/id/100727362/device/rss/rss.html',
      'https://feeds.bbci.co.uk/news/business/rss.xml',
      'https://techcrunch.com/feed/'
    ];
  } else if (topic === 'engineering') {
    // a list of sources used to pull in technology news
    urls = [
      'https://www.theverge.com/rss/index.xml',
      'https://hnrss.org/frontpage'
    ];
  } else if (topic === 'web3') {
    // a list of sources used to pull in world news
    urls = ['https://decrypt.co/feed'];
  }

  const fetchFeed = async (url) => {
    try {
      const response = await fetch(url);
      const data = await response.text();
      const parser = new DOMParser();
      const xml = parser.parseFromString(data, 'application/xml');
      const items = xml.querySelectorAll('item');
      return Array.from(items).map(item => {
        const title = item.querySelector('title').textContent;
        const link = item.querySelector('link').textContent;
        const published = item.querySelector('pubDate').textContent;
        return { title, link, published };
      });
    } catch (error) {
      console.error(`Error fetching feed from ${url}:`, error);
      return [];
    }
  };

  const fetchFeeds = async () => {
    const feeds = await Promise.all(urls.map(fetchFeed));
    const feed = feeds.flat();
    feed.sort((a, b) => new Date(b.published) - new Date(a.published));

    for (const item of feed) {
      // remove the timestamp from the date
      item.published = item.published.slice(0, -15);

      // instructions: https://stackoverflow.com/questions/1521592/get-root-domain-of-link
      const parsedUri = new URL(item.link);
      let domain = parsedUri.hostname;
      domain = domain.replace('www.', '');
      item.domain = domain;

      for (const term of filteredTerms) {
        if (item.title.toLowerCase().includes(term.toLowerCase())) {
          item.domain = 'filtered';
        }
      }
    }

    return feed.slice(0, 30);
  };

  return fetchFeeds();
}