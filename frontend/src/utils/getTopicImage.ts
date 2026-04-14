import log from "loglevel";

const PICSUM_FALLBACK = (name: string) =>
  `https://upload.wikimedia.org/wikipedia/commons/a/af/Bananas_%28Alabama_Extension%29.jpg`;

export async function getTopicImage(name: string): Promise<string> {
  // 1. Try Wikipedia
  try {
    const slug = encodeURIComponent(name.replace(/ /g, "_"));
    const res = await fetch(
      `https://en.wikipedia.org/api/rest_v1/page/summary/${slug}`,
    );
    if (res.ok) {
      const data = await res.json();
      if (data.thumbnail?.source) return data.thumbnail.source;
      log.debug(`thumbnail for ${name}, using wikipedia`);
    }
  } catch {}
  log.debug(`thumbnail for ${name}, using picsum fallback`);

  log.debug(PICSUM_FALLBACK(""));
  // 2. Picsum fallback
  return PICSUM_FALLBACK(name);
}
