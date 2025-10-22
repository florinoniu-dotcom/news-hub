import json, time, feedparser
from pathlib import Path

SOURCES = [
  {"name":"MacRumors","url":"https://www.macrumors.com/mac/rss/"},
  {"name":"9to5Mac","url":"https://9to5mac.com/feed/"},
  {"name":"Macworld","url":"https://www.macworld.com/feed"},
  {"name":"MacDailyNews","url":"https://macdailynews.com/feed/"},
  {"name":"Go4IT","url":"https://www.go4it.ro/feed/"},
  {"name":"Playtech.ro","url":"https://playtech.ro/stiri/feed/"},
  {"name":"iDevice.ro","url":"https://www.idevice.ro/feed/"}
]

items = []
now = int(time.time())

for s in SOURCES:
    d = feedparser.parse(s["url"])
    for e in d.entries[:15]:
        items.append({
            "source": s["name"],
            "title": getattr(e, "title", ""),
            "link": getattr(e, "link", ""),
            "published": getattr(e, "published", getattr(e, "updated", "")),
            "ts": int(time.mktime(getattr(e, "published_parsed", getattr(e, "updated_parsed", time.gmtime(0))))),
        })

items.sort(key=lambda x: x["ts"], reverse=True)
Path(\"docs\").mkdir(exist_ok=True)
Path(\"docs/feed.json\").write_text(json.dumps({\"generated\":now,\"items\":items[:150]}, ensure_ascii=False, indent=2))
print(f\"Wrote {len(items)} items\")
