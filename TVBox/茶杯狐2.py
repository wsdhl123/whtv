# -*- coding: utf-8 -*-
"""
茶杯狐 - TVBox 爬虫源
由「TVBox Py源生成器」自动生成
站点: https://www.cupb.cc
生成时间: 2026/9/21上午11:35:15

如解析失败，请按注释手动调整上方 CARD_SELECTOR / LINK_PATTERN 等配置。
"""

import re
import json
import time
import threading
from urllib.parse import quote, unquote, urljoin

import requests
from requests.adapters import HTTPAdapter

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    import urllib3
    urllib3.disable_warnings()
except Exception:
    pass

try:
    import sys
    sys.path.append('..')
    from base.spider import Spider as _BaseSpider
except ImportError:
    _BaseSpider = None


# ============================================================
# 站点配置（自动识别结果）
# ============================================================
HOST = 'https://www.cupb.cc'
UA = ("Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36")

CARD_SELECTOR   = 'div.myci-vodlist__box a'
TITLE_SELECTOR  = ''
PIC_SELECTOR    = ''
REMARK_SELECTOR = ''
LINK_PATTERN    = r'/v/(\\d+)/40'

SEARCH_URL = ''

CATEGORIES = [
    {'id': '1', 'name': '电影', 'url': '/vod/1/39/0/0/0/0/0/0'},
    {'id': '2', 'name': '电视剧', 'url': '/vod/1/40/0/0/0/0/0/0'},
    {'id': '3', 'name': '综艺', 'url': '/vod/1/41/0/0/0/0/0/0'},
    {'id': '4', 'name': '动漫', 'url': '/vod/1/42/0/0/0/0/0/0'},
    {'id': '5', 'name': '短剧', 'url': '/vod/1/195/0/0/0/0/0/0'},
    {'id': '6', 'name': '动作片', 'url': '/vod/1/39/47/0/0/0/0/0'},
    {'id': '7', 'name': '喜剧片', 'url': '/vod/1/39/48/0/0/0/0/0'},
    {'id': '8', 'name': '爱情片', 'url': '/vod/1/39/49/0/0/0/0/0'},
    {'id': '9', 'name': '恐怖片', 'url': '/vod/1/39/50/0/0/0/0/0'},
    {'id': '10', 'name': '剧情片', 'url': '/vod/1/39/51/0/0/0/0/0'},
    {'id': '11', 'name': '科幻片', 'url': '/vod/1/39/52/0/0/0/0/0'},
    {'id': '12', 'name': '惊悚片', 'url': '/vod/1/39/53/0/0/0/0/0'},
    {'id': '13', 'name': '国产剧', 'url': '/vod/1/40/60/0/0/0/0/0'},
    {'id': '14', 'name': '奈飞电视剧', 'url': '/vod/1/40/192/0/0/0/0/0'},
    {'id': '15', 'name': '韩国剧', 'url': '/vod/1/40/65/0/0/0/0/0'},
    {'id': '16', 'name': '欧美剧', 'url': '/vod/1/40/63/0/0/0/0/0'},
    {'id': '17', 'name': '日本剧', 'url': '/vod/1/40/64/0/0/0/0/0'},
    {'id': '18', 'name': '香港剧', 'url': '/vod/1/40/61/0/0/0/0/0'},
    {'id': '19', 'name': '台湾剧', 'url': '/vod/1/40/62/0/0/0/0/0'},
    {'id': '20', 'name': '国内综艺', 'url': '/vod/1/41/68/0/0/0/0/0'},
    {'id': '21', 'name': '港台综艺', 'url': '/vod/1/41/69/0/0/0/0/0'},
    {'id': '22', 'name': '日韩综艺', 'url': '/vod/1/41/70/0/0/0/0/0'},
    {'id': '23', 'name': '欧美综艺', 'url': '/vod/1/41/71/0/0/0/0/0'},
    {'id': '24', 'name': '海外综艺', 'url': '/vod/1/41/72/0/0/0/0/0'},
]

TIMEOUT_PAGE = 8
TIMEOUT_API  = 6
TTL_LIST     = 300
TTL_DETAIL   = 600

_Base = _BaseSpider if _BaseSpider is not None else object


class Spider(_Base):
    siteUrl = HOST
    headers = {
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': HOST + '/',
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.verify = False
        adapter = HTTPAdapter(pool_connections=20, pool_maxsize=40, max_retries=0)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self._lock = threading.Lock()
        self._cache = {}

    def init(self, extend=""):
        self.extend = extend or ""

    # ---------------- 网络 ----------------
    def _get_text(self, url, referer='', timeout=TIMEOUT_PAGE):
        if not url:
            return ""
        if not url.startswith('http'):
            url = urljoin(HOST, url)
        headers = {}
        if referer:
            headers['Referer'] = referer
        for i in range(2):
            try:
                r = self.session.get(url, timeout=timeout, headers=headers)
                if r.status_code == 429:
                    time.sleep(1.5)
                    continue
                r.raise_for_status()
                r.encoding = r.apparent_encoding or 'utf-8'
                return r.text
            except Exception:
                if i == 0:
                    time.sleep(0.3)
        return ""

    def _soup(self, html):
        if BeautifulSoup is None or not html:
            return None
        try:
            return BeautifulSoup(html, 'html.parser')
        except Exception:
            return None

    # ---------------- 缓存 ----------------
    def _cget(self, key, ttl):
        item = self._cache.get(key)
        if item and time.time() - item[0] < ttl:
            return item[1]
        return None

    def _cset(self, key, value, ttl):
        if len(self._cache) > 400:
            self._cache.clear()
        self._cache[key] = (time.time(), value, ttl)

    # ---------------- 列表解析 ----------------
    def _parse_cards(self, html):
        soup = self._soup(html)
        if soup is None:
            return []
        out = []
        seen = set()
        try:
            nodes = soup.select(CARD_SELECTOR)
        except Exception:
            nodes = []

        for a in nodes:
            href = a.get('href') or ''
            if not href:
                continue
            m = re.search(LINK_PATTERN, href)
            if not m:
                continue
            key = m.group(1)
            if not key or key in seen:
                continue

            title = ''
            if TITLE_SELECTOR:
                try:
                    el = a.select_one(TITLE_SELECTOR)
                    if el is not None:
                        title = el.get_text(strip=True)
                except Exception:
                    pass
            if not title:
                title = (a.get('title') or '').strip()
            if not title:
                title = a.get_text(strip=True)
            if not title:
                continue

            pic = ''
            if PIC_SELECTOR:
                try:
                    img = a.select_one(PIC_SELECTOR)
                except Exception:
                    img = None
                if img is not None:
                    pic = (img.get('src') or img.get('data-src') or
                           img.get('data-original') or img.get('data-lazy') or '').strip()
                    if pic.startswith('//'):
                        pic = 'https:' + pic
                    elif pic and not pic.startswith('http'):
                        pic = urljoin(HOST, pic)

            remark = ''
            if REMARK_SELECTOR:
                try:
                    el = a.select_one(REMARK_SELECTOR)
                    if el is not None:
                        remark = el.get_text(strip=True)
                except Exception:
                    pass

            seen.add(key)
            out.append({
                'vod_id': urljoin(HOST, href),
                'vod_name': title,
                'vod_pic': pic,
                'vod_remarks': remark,
            })
        return out

    # ---------------- 首页 ----------------
    def homeContent(self, filter=False):
        classes = [{'type_id': c['id'], 'type_name': c['name']} for c in CATEGORIES]
        if not classes:
            classes = [{'type_id': '1', 'type_name': '首页'}]
        return {'class': classes}

    def homeVideoContent(self):
        cached = self._cget('home', TTL_LIST)
        if cached is not None:
            return cached
        html = self._get_text(HOST + '/')
        result = {'list': self._parse_cards(html) if html else []}
        self._cset('home', result, TTL_LIST)
        return result

    # ---------------- 分类 ----------------
    def categoryContent(self, tid, pg, filter, extend):
        page = max(1, int(pg or 1))
        url = None
        for c in CATEGORIES:
            if str(c['id']) == str(tid):
                url = c['url']
                break
        if not url:
            return {'list': [], 'page': page, 'pagecount': 1, 'limit': 36, 'total': 0}

        if '{pg}' in url:
            url = url.replace('{pg}', str(page))
        elif page > 1:
            url = url + ('&' if '?' in url else '?') + 'page=' + str(page)

        ckey = 'cat:%s:%s' % (tid, page)
        cached = self._cget(ckey, TTL_LIST)
        if cached is not None:
            return cached

        html = self._get_text(url, referer=HOST + '/')
        cards = self._parse_cards(html) if html else []
        result = {
            'list': cards,
            'page': page,
            'pagecount': 9999 if cards else page,
            'limit': 36,
            'total': 999999 if cards else 0,
        }
        self._cset(ckey, result, TTL_LIST)
        return result

    # ---------------- 详情 ----------------
    def detailContent(self, ids):
        if isinstance(ids, str):
            ids = [ids]
        raw = str(ids[0]).split(',')[0].strip()
        if not raw:
            return {'list': []}
        url = raw if raw.startswith('http') else urljoin(HOST, raw)

        ckey = 'detail:' + url
        cached = self._cget(ckey, TTL_DETAIL)
        if cached is not None:
            return cached

        html = self._get_text(url, referer=HOST + '/')
        detail = self._parse_detail(html, url) if html else None
        result = {'list': [detail]} if detail else {'list': []}
        self._cset(ckey, result, TTL_DETAIL)
        return result

    def _parse_detail(self, html, url):
        soup = self._soup(html)
        if soup is None:
            return None

        name = pic = content = year = area = type_name = director = actor = ''

        # 1) ld+json 结构化数据
        for script in soup.find_all('script', type='application/ld+json'):
            txt = script.string or script.get_text() or ''
            if not txt.strip():
                continue
            try:
                d = json.loads(txt)
            except Exception:
                continue
            if isinstance(d, list):
                d = d[0] if d else {}
            if not isinstance(d, dict):
                continue

            name = name or str(d.get('name') or '').strip()
            img = d.get('image')
            if isinstance(img, list):
                img = img[0] if img else ''
            if isinstance(img, dict):
                img = img.get('url') or ''
            pic = pic or str(img or '').strip()
            content = content or str(d.get('description') or '').strip()
            year = year or str(d.get('dateCreated') or '')[:4]
            area = area or str(d.get('countryOfOrigin') or '').strip()

            g = d.get('genre')
            if isinstance(g, list):
                g = '、'.join([str(x) for x in g if x])
            type_name = type_name or str(g or '').strip()

            dr = d.get('director')
            if isinstance(dr, list):
                dr = dr[0] if dr else {}
            if isinstance(dr, dict):
                director = director or str(dr.get('name') or '').strip()

            ac = d.get('actor')
            if isinstance(ac, list):
                names = [str(x.get('name') or '').strip() for x in ac
                         if isinstance(x, dict) and x.get('name')]
                if names:
                    actor = actor or '、'.join(names)

        # 2) 兜底：og / title / h1
        if not pic:
            og = soup.find('meta', property='og:image')
            if og:
                pic = (og.get('content') or '').strip()
        if not name:
            h1 = soup.find('h1')
            if h1:
                name = h1.get_text(strip=True)
        if not name:
            t = soup.find('title')
            if t:
                name = re.split(r'[-_|]', t.get_text(strip=True))[0].strip()
        if not content:
            og = soup.find('meta', {'name': 'description'})
            if og:
                content = (og.get('content') or '').strip()

        if not name:
            return None

        # 3) 播放地址
        eps = []
        seen = set()
        # 3a) JSON 里的 url 字段
        for m in re.finditer(r'"url"\s*:\s*"([^"]+?\.(?:m3u8|mp4)[^"]*)"', html):
            u = m.group(1).replace('\\/', '/').strip()
            if u and u not in seen:
                seen.add(u)
                eps.append(u)
        # 3b) 正文中的裸链接
        if not eps:
            for m in re.finditer(r'https?://[^"\'<>\s\\]+\.(?:m3u8|mp4)[^"\'<>\s\\]*', html):
                u = m.group(0).replace('\\/', '/').strip()
                if u and u not in seen:
                    seen.add(u)
                    eps.append(u)

        if not eps:
            # 没有直链，交给 TVBox 的嗅探
            return {
                'vod_id': url,
                'vod_name': name,
                'vod_pic': pic,
                'type_name': type_name,
                'vod_year': year,
                'vod_area': area,
                'vod_remarks': '',
                'vod_director': director,
                'vod_actor': actor,
                'vod_content': content[:500],
                'vod_play_from': '默认线路',
                'vod_play_url': '播放$' + url,
            }

        play_items = []
        for i, u in enumerate(eps):
            label = '播放' if len(eps) == 1 else '第%d集' % (i + 1)
            play_items.append(label + '$' + u)

        return {
            'vod_id': url,
            'vod_name': name,
            'vod_pic': pic,
            'type_name': type_name,
            'vod_year': year,
            'vod_area': area,
            'vod_remarks': ('共%d集' % len(eps)) if len(eps) > 1 else '',
            'vod_director': director,
            'vod_actor': actor,
            'vod_content': content[:500],
            'vod_play_from': '默认线路',
            'vod_play_url': '#'.join(play_items),
        }

    # ---------------- 搜索 ----------------
    def searchContent(self, keyword, quick=False, pg=1):
        kw = (keyword or '').strip()
        if not kw:
            return {'list': [], 'msg': '请输入搜索关键词'}

        if SEARCH_URL:
            url = SEARCH_URL.replace('{kw}', quote(kw))
        else:
            url = '/?wd=' + quote(kw)
        if not url.startswith('http'):
            url = urljoin(HOST, url)

        ckey = 'search:%s' % kw
        cached = self._cget(ckey, TTL_LIST)
        if cached is not None:
            return cached

        html = self._get_text(url, referer=HOST + '/')
        cards = self._parse_cards(html) if html else []
        result = {'list': cards, 'msg': '' if cards else '未找到相关内容'}
        self._cset(ckey, result, TTL_LIST)
        return result

    # ---------------- 播放 ----------------
    def playerContent(self, flag, id, vipFlags):
        u = unquote(str(id or '').strip())
        if not u:
            return {'parse': 0, 'url': ''}
        if u.startswith('//'):
            u = 'https:' + u
        elif not u.startswith('http'):
            u = urljoin(HOST, u)

        low = u.lower()
        if '.m3u8' in low or '.mp4' in low or '.flv' in low:
            return {
                'parse': 0,
                'url': u,
                'header': {'User-Agent': UA, 'Referer': HOST + '/'},
            }
        return {
            'parse': 1,
            'url': u,
            'header': {'User-Agent': UA, 'Referer': HOST + '/'},
        }

    def localProxy(self, param):
        return [200, 'video/MP2T', b'', '']

    def destroy(self):
        try:
            self.session.close()
        except Exception:
            pass

    def close(self):
        self.destroy()


if __name__ == '__main__':
    s = Spider()
    print(s.homeContent())
