#!/usr/bin/env python3
"""抓取高公局(tisvcloud)路段即時路況,依 route.json 篩出你行駛的路段,輸出 data/traffic.json"""
import gzip, json, os, urllib.error, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

BASE = "https://tisvcloud.freeway.gov.tw/history/motc20/"
TW = timezone(timedelta(hours=8))
DIR_MAP = {"N": ("N", "北"), "S": ("S", "南"), "E": ("E", "東"), "W": ("W", "西")}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=10).read()
    return gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data


def first_ok(urls):
    last = None
    for u in urls:
        try:
            return get(u), u
        except urllib.error.HTTPError as e:  # 檔案不存在等,換下一個網址
            last = f"{u} -> HTTP {e.code}"
        except Exception as e:  # 逾時/連不上:不必再試其他網址
            raise RuntimeError(f"無法連線到高公局({u}):{e}。可能是對方擋海外 IP 或網站暫時無回應。")
    raise RuntimeError("全部來源都失敗,最後一個:" + str(last))


def records(xml_bytes):
    """取出所有含 SectionID 的記錄,回傳 {欄位: 文字, '_text': 全部文字}"""
    out = []
    for el in ET.fromstring(xml_bytes).iter():
        leaf = {c.tag.split("}")[-1]: (c.text or "").strip() for c in el if len(c) == 0}
        if "SectionID" in leaf:
            leaf["_text"] = " ".join(t.strip() for t in el.itertext() if t.strip())
            out.append(leaf)
    return out


def num(v, default=-99.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def build(cfg, static, live):
    live_by_id = {r["SectionID"]: r for r in live}
    result = []
    for rt in cfg["routes"]:
        d = DIR_MAP.get(rt.get("direction", ""), ())
        secs = []
        for s in static:
            if rt["road"] not in s["_text"]:
                continue
            sd = s.get("RoadDirection", "")
            if d and sd and not sd.startswith(d):
                continue
            kws = rt.get("keywords") or []
            if kws and not any(k in s["_text"] for k in kws):
                continue
            lv = live_by_id.get(s["SectionID"])
            if not lv:
                continue
            secs.append({
                "id": s["SectionID"],
                "name": s.get("SectionName") or s["_text"][:40],
                "speed": num(lv.get("TravelSpeed")),
                "time": num(lv.get("TravelTime")),
                "level": lv.get("CongestionLevel", ""),
            })
        item = {"name": rt["name"], "road": rt["road"], "sections": secs}
        if not secs:
            names = [s.get("SectionName") or s["_text"][:40] for s in static if rt["road"] in s["_text"]]
            item["hint"] = "沒有符合的路段,請調整 route.json 的 keywords。該道路可用路段範例:" + "、".join(names[:40])
        result.append(item)
    return result


def main():
    cfg = json.load(open("route.json", encoding="utf-8"))
    now = datetime.now(TW)
    out = {"updated": now.isoformat(timespec="seconds"), "routes": [], "error": None}
    try:
        stamps = [(now - timedelta(minutes=m)) for m in range(2, 14)]
        live_urls = [BASE + "LiveTraffic.xml"] + [
            BASE + f"Section/{t:%Y%m%d}/LiveTraffic_{t:%H%M}.xml.gz" for t in stamps]
        static_urls = [BASE + "Section.xml", BASE + f"Section/{now:%Y%m%d}/Section_0000.xml.gz"]
        live_bytes, lu = first_ok(live_urls)
        static_bytes, su = first_ok(static_urls)
        print("live:", lu, "| static:", su)
        out["routes"] = build(cfg, records(static_bytes), records(live_bytes))
    except Exception as e:
        out["error"] = f"抓取失敗:{e}"
        print(out["error"])
    os.makedirs("data", exist_ok=True)
    json.dump(out, open("data/traffic.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
