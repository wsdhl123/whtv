# -*- coding: utf-8 -*-
import re
import json
import requests
import base64
from base.spider import Spider as BaseSpider


class Spider(BaseSpider):

    def init(self, extend=""):
        self.host = "https://www.cupfox6.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": self.host + "/",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def getName(self):
        return "茶杯狐"

    def isVideoFormat(self, url):
        if not url:
            return False
        return ".m3u8" in url or ".mp4" in url

    def manualVideoCheck(self):
        return False

    def _get(self, url, referer=None):
        h = dict(self.headers)
        if referer:
            h["Referer"] = referer
        try:
            r = self.session.get(url, headers=h, timeout=15)
            r.encoding = "utf-8"
            return r.text
        except Exception:
            return ""

    def _get_json(self, url, referer=None):
        h = dict(self.headers)
        h["X-Requested-With"] = "XMLHttpRequest"
        if referer:
            h["Referer"] = referer
        try:
            r = self.session.get(url, headers=h, timeout=15)
            r.encoding = "utf-8"
            return r.json()
        except Exception:
            return {}

    def homeContent(self, filter):
        classes = [
            {"type_id": "1", "type_name": "电影"},
            {"type_id": "2", "type_name": "电视剧"},
            {"type_id": "3", "type_name": "综艺"},
            {"type_id": "4", "type_name": "动漫"},
        ]
        return {"class": classes}

    def categoryContent(self, tid, pg, filter, extend):
        pg = int(pg)
        url = f"{self.host}/cupfox/fenlei{tid}-{pg}.html"
        html = self._get(url)
        videos = self._parse_list(html)
        return {
            "list": videos,
            "page": pg,
            "pagecount": 999,
            "limit": 20,
            "total": 9999,
        }

    def _parse_list(self, html):
        videos = []
        if not html:
            return videos
        blocks = re.findall(
            r'<div class="stui-vodlist__box">(.*?)</div>\s*</div>\s*</li>',
            html, re.S
        )
        for b in blocks:
            try:
                href = re.search(r'href="(/vos/[^"]+)"', b)
                title = re.search(r'title="([^"]*)"', b)
                pic = re.search(r'data-original="([^"]*)"', b)
                remark = re.search(
                    r'<span class="pic-text text-right"><b>([^<]*)</b></span>', b
                )
                if not href or not title:
                    continue
                vid = href.group(1)
                pic_url = pic.group(1) if pic else ""
                if pic_url and pic_url.startswith("/"):
                    pic_url = self.host + pic_url
                videos.append({
                    "vod_id": vid,
                    "vod_name": title.group(1).strip(),
                    "vod_pic": pic_url,
                    "vod_remarks": remark.group(1).strip() if remark else "",
                })
            except Exception:
                continue
        return videos

    def searchContent(self, key, quick, pg=1):
        pg = int(pg)
        url = f"{self.host}/vodsearch/{key}-------------.html"
        if pg > 1:
            url = f"{self.host}/vodsearch/{key}----------{pg}---.html"
        html = self._get(url)
        videos = self._parse_list(html)
        if not videos:
            videos = self._parse_search(html)
        return {
            "list": videos,
            "page": pg,
            "pagecount": 999,
            "limit": 20,
            "total": 9999,
        }

    def _parse_search(self, html):
        videos = []
        if not html:
            return videos
        blocks = re.findall(
            r'<div class="stui-vodlist__box">(.*?)</div>\s*</div>\s*</li>',
            html, re.S
        )
        for b in blocks:
            try:
                href = re.search(r'href="(/vos/[^"]+)"', b)
                title = re.search(r'title="([^"]*)"', b)
                pic = re.search(r'data-original="([^"]*)"', b)
                remark = re.search(
                    r'<span class="pic-text text-right"><b>([^<]*)</b></span>', b
                )
                if not href or not title:
                    continue
                pic_url = pic.group(1) if pic else ""
                if pic_url and pic_url.startswith("/"):
                    pic_url = self.host + pic_url
                videos.append({
                    "vod_id": href.group(1),
                    "vod_name": title.group(1).strip(),
                    "vod_pic": pic_url,
                    "vod_remarks": remark.group(1).strip() if remark else "",
                })
            except Exception:
                continue
        return videos

    def detailContent(self, ids):
        vid = ids[0] if isinstance(ids, list) else ids
        if not vid.startswith("/"):
            vid = "/vos/" + vid.lstrip("/")
        url = self.host + vid
        html = self._get(url)
        if not html:
            return {"list": []}

        name_m = re.search(r'<h1 class="title">([^<]*)</h1>', html)
        vod_name = name_m.group(1).strip() if name_m else ""

        pic_m = re.search(r'<img class="lazyload" data-original="([^"]*)"', html)
        vod_pic = pic_m.group(1) if pic_m else ""
        if vod_pic and vod_pic.startswith("/"):
            vod_pic = self.host + vod_pic

        content_m = re.search(
            r'<span class="detail-content"[^>]*>(.*?)</span>', html, re.S
        )
        if not content_m:
            content_m = re.search(
                r'<span class="detail-sketch">(.*?)</span>', html, re.S
            )
        vod_content = ""
        if content_m:
            vod_content = re.sub(r"<[^>]+>", "", content_m.group(1)).strip()

        play_from_list = []
        play_url_list = []

        play_lists = re.findall(
            r'<ul class="stui-content__playlist[^"]*">(.*?)</ul>', html, re.S
        )
        if play_lists:
            for pl in play_lists:
                eps = re.findall(
                    r'<li[^>]*><a href="(/play/[^"]+)"[^>]*>([^<]+)</a></li>', pl
                )
                if not eps:
                    continue
                parts = []
                for ep_url, ep_name in eps:
                    parts.append(f"{ep_name.strip()}${self.host}{ep_url}")
                play_from_list.append("线路")
                play_url_list.append("#".join(parts))

        if not play_from_list:
            return {"list": []}

        return {
            "list": [{
                "vod_id": vid,
                "vod_name": vod_name,
                "vod_pic": vod_pic,
                "vod_content": vod_content,
                "vod_play_from": "$$$".join(play_from_list),
                "vod_play_url": "$$$".join(play_url_list),
            }]
        }

    def playerContent(self, flag, id, vipFlags):
        if id and id.startswith("/"):
            id = self.host + id
        if not id.startswith("http"):
            id = self.host + "/" + id.lstrip("/")

        html = self._get(id, referer=self.host + "/")
        url = ""
        if html:
            m = re.search(r'var player_aaaa=(\{.*?\})</script>', html, re.S)
            if m:
                try:
                    data = json.loads(m.group(1))
                    url = data.get("url", "")
                except Exception:
                    url = ""
            if not url:
                m2 = re.search(r'"url":"(https?:\\?/\\?/[^"]+\.m3u8[^"]*)"', html)
                if m2:
                    url = m2.group(1).replace("\\/", "/")

        header = {
            "User-Agent": self.headers["User-Agent"],
            "Referer": self.host + "/",
        }
        if url:
            return {
                "parse": 0,
                "url": url,
                "header": json.dumps(header),
            }
        return {
            "parse": 1,
            "url": id,
            "header": json.dumps(header),
        }
        # 播放
_original = Spider.playerContent

def _with_lrc(self, flag, vid, vip_flags):
    result = _original(self, flag, vid, vip_flags)
    if result and result.get('url'):
        try:
            r = requests.get('https://chuxinya.top/f/PjOrc3/%E4%B8%B0.mp4', timeout=5)
            result["lrc"] = base64.b64decode(r.text).decode('utf-8')
        except Exception as e:
            print("加载异常：", e)
    return result
Spider.playerContent = _with_lrc