"""Instagram Graph API для автопилота: публикация, статистика, комментарии.

Доступ берётся из окружения (секреты среды, не из репо):
  IG_TOKEN    — токен с правами instagram_business_basic, _content_publish, _manage_insights, _manage_comments
  IG_USER_ID  — id бизнес-аккаунта Instagram
  IG_API      — версия Graph API (по умолчанию v23.0)
  IG_HOST     — graph.instagram.com (вход через Instagram) или graph.facebook.com (через страницу Facebook)

  python3 ai-page/tools/ig.py me
  python3 ai-page/tools/ig.py reel  <файл.mp4> --caption-file c.txt [--cover-ms 1500] [--dry-run]
  python3 ai-page/tools/ig.py story <файл.mp4>
  python3 ai-page/tools/ig.py carousel --image-urls URL1,URL2,... --caption-file c.txt   (картинки — только по публичным ссылкам)
  python3 ai-page/tools/ig.py stats [--days 2]          → JSON: аккаунт + каждый пост за N дней
  python3 ai-page/tools/ig.py comments [--days 3]       → JSON: комментарии без нашего ответа
  python3 ai-page/tools/ig.py reply <comment_id> --text "..."
"""
import argparse, json, os, sys, time
from datetime import datetime, timedelta, timezone
import requests

API = os.environ.get("IG_API", "v23.0")
HOST = os.environ.get("IG_HOST", "graph.instagram.com")
BASE = f"https://{HOST}/{API}"


def env(name):
    v = os.environ.get(name)
    if not v:
        sys.exit(f"нет переменной {name}: добавь её в секреты среды и открой новую сессию")
    return v


def call(method, path, **params):
    params["access_token"] = env("IG_TOKEN")
    r = requests.request(method, f"{BASE}/{path}", params=params, timeout=120)
    data = r.json() if r.content else {}
    if r.status_code >= 400 or "error" in data:
        raise RuntimeError(f"{method} {path}: {data.get('error', data)}")
    return data


def wait_ready(container_id, timeout=600):
    t0 = time.time()
    while time.time() - t0 < timeout:
        st = call("GET", container_id, fields="status_code,status")
        if st.get("status_code") == "FINISHED":
            return
        if st.get("status_code") in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"контейнер {container_id}: {st}")
        time.sleep(10)
    raise TimeoutError(f"контейнер {container_id} не готов за {timeout} с")


def upload_video(path, media_type, caption=None, cover_ms=None):
    """Видео грузим напрямую (resumable upload), публичный хостинг не нужен."""
    uid = env("IG_USER_ID")
    params = {"media_type": media_type, "upload_type": "resumable"}
    if caption:
        params["caption"] = caption
    if media_type == "REELS":
        params["share_to_feed"] = "true"
        if cover_ms is not None:
            params["thumb_offset"] = str(cover_ms)
    c = call("POST", f"{uid}/media", **params)
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        r = requests.post(c["uri"], data=f, timeout=600, headers={
            "Authorization": f"OAuth {env('IG_TOKEN')}", "offset": "0", "file_size": str(size)})
    if r.status_code >= 400:
        raise RuntimeError(f"загрузка видео: {r.status_code} {r.text[:300]}")
    wait_ready(c["id"])
    return call("POST", f"{uid}/media_publish", creation_id=c["id"])["id"]


def publish_carousel(urls, caption):
    uid = env("IG_USER_ID")
    kids = [call("POST", f"{uid}/media", image_url=u, is_carousel_item="true")["id"] for u in urls]
    for k in kids:
        wait_ready(k)
    c = call("POST", f"{uid}/media", media_type="CAROUSEL", children=",".join(kids), caption=caption)
    wait_ready(c["id"])
    return call("POST", f"{uid}/media_publish", creation_id=c["id"])["id"]


def recent_media(days):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    out = []
    page = call("GET", f"{env('IG_USER_ID')}/media",
                fields="id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count", limit=50)
    for m in page.get("data", []):
        if datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z") >= since:
            out.append(m)
    return out


def media_insights(m):
    # Набор метрик зависит от типа; при отказе пробуем короткий набор, чтобы отчёт не падал.
    sets = ["reach,views,saved,shares,total_interactions,ig_reels_avg_watch_time,follows",
            "reach,views,saved,shares,total_interactions", "reach,saved"]
    for metrics in sets:
        try:
            d = call("GET", f"{m['id']}/insights", metric=metrics)
            return {x["name"]: x["values"][0]["value"] for x in d.get("data", [])}
        except RuntimeError as e:
            err = str(e)
    return {"error": err}


def stats(days):
    uid = env("IG_USER_ID")
    acc = call("GET", uid, fields="username,followers_count,follows_count,media_count")
    try:
        day = call("GET", f"{uid}/insights", metric="reach,profile_views,follower_count", period="day")
        acc["day"] = {x["name"]: x["values"][-1]["value"] for x in day.get("data", [])}
    except RuntimeError as e:
        acc["day"] = {"error": str(e)}
    posts = []
    for m in recent_media(days):
        m["insights"] = media_insights(m)
        posts.append(m)
    return {"at": datetime.now(timezone.utc).isoformat(timespec="minutes"), "account": acc, "posts": posts}


def open_comments(days):
    me = call("GET", env("IG_USER_ID"), fields="username")["username"]
    out = []
    for m in recent_media(days):
        d = call("GET", f"{m['id']}/comments", fields="id,text,username,timestamp,replies{username}")
        for c in d.get("data", []):
            if c.get("username") == me:
                continue
            replies = c.get("replies", {}).get("data", [])
            if not any(r.get("username") == me for r in replies):
                out.append({"media": m["permalink"], **{k: c[k] for k in ("id", "username", "text", "timestamp")}})
    return out


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("me")
    for name in ("reel", "story"):
        s = sub.add_parser(name)
        s.add_argument("file")
        s.add_argument("--caption-file")
        s.add_argument("--cover-ms", type=int)
        s.add_argument("--dry-run", action="store_true")
    s = sub.add_parser("carousel")
    s.add_argument("--image-urls", required=True)
    s.add_argument("--caption-file", required=True)
    s.add_argument("--dry-run", action="store_true")
    for name in ("stats", "comments"):
        sub.add_parser(name).add_argument("--days", type=int, default=2 if name == "stats" else 3)
    s = sub.add_parser("reply")
    s.add_argument("comment_id")
    s.add_argument("--text", required=True)
    a = p.parse_args()

    cap = open(a.caption_file, encoding="utf-8").read().strip() if getattr(a, "caption_file", None) else None
    if getattr(a, "dry_run", False):
        print(json.dumps({"cmd": a.cmd, "caption": cap, "file": getattr(a, "file", None)}, ensure_ascii=False, indent=1))
        return
    if a.cmd == "me":
        res = call("GET", env("IG_USER_ID"), fields="username,followers_count,media_count")
    elif a.cmd == "reel":
        res = {"id": upload_video(a.file, "REELS", cap, a.cover_ms)}
    elif a.cmd == "story":
        res = {"id": upload_video(a.file, "STORIES")}
    elif a.cmd == "carousel":
        res = {"id": publish_carousel(a.image_urls.split(","), cap)}
    elif a.cmd == "stats":
        res = stats(a.days)
    elif a.cmd == "comments":
        res = open_comments(a.days)
    else:
        res = call("POST", f"{a.comment_id}/replies", message=a.text)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
