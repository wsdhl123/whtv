"""
导航:   https://www.qiushui.vip   
           https://www.qiushuitv.cn
           https://www.qiushuiying.cn
由「影视py源生成器」自动生成 2026-09-18 08:31
站点: https://www.5o5k.com
"""
import re
import json
import time
import base64
import hashlib
try:
    import threading
except ImportError:
    threading = None
import html as html_lib
import zlib
from urllib.parse import quote, urljoin, unquote

import requests
from bs4 import BeautifulSoup

try:
    from base.spider import Spider as _BaseSpider
except ImportError:
    class _BaseSpider(object):
        pass


def _unq(v):
    try:
        return unquote(v)
    except Exception:
        return v


class Spider(_BaseSpider):
    name = "蘑菇影视-最新免费电影电视剧在线观看"
    base_url = "https://www.5o5k.com"
    site_url = "https://www.5o5k.com"
    prefix = ""
    encoding = "utf-8"

    class_name = ['连续剧', '电影', '综艺节目', '短剧', '动漫', '影视解说', '预告片']
    class_url = ['35', '20', '43', '55', '48', '54', '63']

    cat_pattern = 'https://www.5o5k.com/vodshow/{cid}--------{pg}---.html'
    search_pattern = 'https://www.5o5k.com/vodsearch/-------------.html?wd={key}&page={pg}'

    _filter_mode = 'html'
    _filter_data = {'35': {'seg3': [('全部', ''), ('喜剧', '喜剧'), ('爱情', '爱情'), ('恐怖', '恐怖'), ('动作', '动作'), ('科幻', '科幻'), ('剧情', '剧情'), ('战争', '战争'), ('警匪', '警匪'), ('犯罪', '犯罪'), ('古装', '古装'), ('青春偶像', '青春偶像'), ('家庭', '家庭'), ('奇幻', '奇幻'), ('历史', '历史'), ('经典', '经典'), ('乡村', '乡村'), ('情景', '情景'), ('商战', '商战')], 'seg1': [('全部', ''), ('中国', '中国'), ('韩国', '韩国'), ('香港', '香港'), ('台湾', '台湾'), ('日本', '日本'), ('美国', '美国'), ('泰国', '泰国'), ('英国', '英国'), ('新加坡', '新加坡'), ('其他', '其他')], 'seg4': [('全部', ''), ('国语', '国语'), ('英语', '英语'), ('粤语', '粤语'), ('闽南语', '闽南语'), ('韩语', '韩语'), ('日语', '日语'), ('法语', '法语'), ('德语', '德语'), ('泰语', '泰语'), ('其它', '其它')], 'seg11': [('全部', ''), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009')], 'seg5': [('全部', ''), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], 'seg2': [('全部', ''), ('时间排序', 'time'), ('人气排序', 'hits'), ('评分排序', 'score')]}, '20': {'seg3': [('全部', ''), ('喜剧', '喜剧'), ('爱情', '爱情'), ('恐怖', '恐怖'), ('动作', '动作'), ('科幻', '科幻'), ('剧情', '剧情'), ('战争', '战争'), ('警匪', '警匪'), ('犯罪', '犯罪'), ('动画', '动画'), ('奇幻', '奇幻'), ('武侠', '武侠'), ('冒险', '冒险'), ('枪战', '枪战'), ('悬疑', '悬疑'), ('惊悚', '惊悚'), ('经典', '经典'), ('青春', '青春')], 'seg1': [('全部', ''), ('中国', '中国'), ('香港', '香港'), ('台湾', '台湾'), ('美国', '美国'), ('法国', '法国'), ('英国', '英国'), ('日本', '日本'), ('韩国', '韩国'), ('德国', '德国'), ('泰国', '泰国'), ('印度', '印度'), ('意大利', '意大利'), ('西班牙', '西班牙'), ('加拿大', '加拿大'), ('其他', '其他')], 'seg4': [('全部', ''), ('国语', '国语'), ('英语', '英语'), ('粤语', '粤语'), ('闽南语', '闽南语'), ('韩语', '韩语'), ('日语', '日语'), ('法语', '法语'), ('德语', '德语'), ('泰语', '泰语'), ('其它', '其它')], 'seg11': [('全部', ''), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009')], 'seg5': [('全部', ''), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], 'seg2': [('全部', ''), ('时间排序', 'time'), ('人气排序', 'hits'), ('评分排序', 'score')]}, '43': {'seg3': [('全部', ''), ('选秀', '选秀'), ('情感', '情感'), ('访谈', '访谈'), ('播报', '播报'), ('旅游', '旅游'), ('音乐', '音乐'), ('美食', '美食'), ('纪实', '纪实'), ('曲艺', '曲艺'), ('生活', '生活'), ('游戏互动', '游戏互动'), ('财经', '财经'), ('求职', '求职')], 'seg1': [('全部', ''), ('内地', '内地'), ('港台', '港台'), ('日韩', '日韩'), ('欧美', '欧美')], 'seg4': [('全部', ''), ('国语', '国语'), ('英语', '英语'), ('粤语', '粤语'), ('闽南语', '闽南语'), ('韩语', '韩语'), ('日语', '日语'), ('其它', '其它')], 'seg11': [('全部', ''), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009')], 'seg5': [('全部', ''), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], 'seg2': [('全部', ''), ('时间排序', 'time'), ('人气排序', 'hits'), ('评分排序', 'score')]}, '55': {'seg5': [('全部', ''), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], 'seg2': [('全部', ''), ('时间排序', 'time'), ('人气排序', 'hits'), ('评分排序', 'score')]}, '48': {'seg4': [('全部', ''), ('国语', '国语'), ('英语', '英语'), ('粤语', '粤语'), ('闽南语', '闽南语'), ('韩语', '韩语'), ('日语', '日语'), ('其它', '其它')], 'seg11': [('全部', ''), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009')], 'seg5': [('全部', ''), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], 'seg2': [('全部', ''), ('时间排序', 'time'), ('人气排序', 'hits'), ('评分排序', 'score')]}, '54': {'seg5': [('全部', ''), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], 'seg2': [('全部', ''), ('时间排序', 'time'), ('人气排序', 'hits'), ('评分排序', 'score')]}, '63': {'seg5': [('全部', ''), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], 'seg2': [('全部', ''), ('时间排序', 'time'), ('人气排序', 'hits'), ('评分排序', 'score')]}}
    _filter_names = {
        "class": "类型", "area": "地区", "lang": "语言",
        "year": "年份", "letter": "字母", "by": "排序",
    }
    _filter_names.update({'seg3': '剧情', 'seg1': '地区', 'seg4': '语言', 'seg11': '年份', 'seg5': '字母', 'seg2': '排序'})

    _show_mode = 'seg'
    _show_tpl = '/vodshow/{id}-{seg1}-{seg2}-{seg3}-{seg4}-{seg5}---{pg}---{seg11}.html'
    _show_total = 12
    _seg_prefix = '/vodshow/'
    _seg_pos = {'seg3': 3, 'seg1': 1, 'seg4': 4, 'seg11': 11, 'seg5': 5, 'seg2': 2}
    _seg_sep = '-'

    _path_tpl = ''
    _path_dim = ""
    _kv_prefix = "/"
    _kv_segs = []

    detail_route = "voddetail"
    sections = []
    det_tpl = ''
    det_rx = None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.5o5k.com/",
    }
    timeout = 15
    page_size = 20

    _session = None

    def getName(self):
        return self.name

    def init(self, extend=""):
        return ""

    def getHeaders(self):
        return self.headers

    def _get_session(self):
        if self._session is None:
            s = _PowSession()
            s.trust_env = False
            s.headers.update(self.headers)
            self._session = s
        return self._session

    @staticmethod
    def _decode(r):
        raw = r.content
        head = raw[:4096].decode("ascii", errors="ignore")
        enc = ""
        m = re.search(r'<meta[^>]+charset=["\']?\s*([\w\-]+)', head, re.I)
        if m:
            enc = m.group(1).lower()
        if not enc:
            m = re.search(r'charset=["\']?([\w\-]+)', r.headers.get("Content-Type", ""), re.I)
            if m:
                enc = m.group(1).lower()
        if not enc:
            try:
                enc = (r.apparent_encoding or "utf-8").lower()
            except Exception:
                enc = "utf-8"
        try:
            text = raw.decode(enc, errors="replace")
        except LookupError:
            text = raw.decode("utf-8", errors="replace")
        if text.count("\ufffd") > 20:
            best, bad = text, text.count("\ufffd")
            for e in ("utf-8", "gb18030", "gbk", "big5"):
                try:
                    t = raw.decode(e, errors="replace")
                    if t.count("\ufffd") < bad:
                        best, bad = t, t.count("\ufffd")
                except Exception:
                    continue
            text = best
        return text

    _slider_domains = []
    _slider_idx = 0
    _slider_sessions = {}
    _slider_verified = {}
    try:
        _slider_lock = threading.Lock()
    except Exception:
        class _slider_lock(object):
            def __enter__(self):
                return self
            def __exit__(self, *a):
                return False

    def _slider_session(self, domain):
        with self._slider_lock:
            sess = self._slider_sessions.get(domain)
            if sess is None:
                sess = _PowSession()
                sess.trust_env = False
                sess.headers.update(self.headers)
                self._slider_sessions[domain] = sess
            return sess

    def _slider_handshake(self, domain):
        try:
            sess = self._slider_session(domain)
            h = {"Referer": domain + "/"}
            r = sess.get(domain + "/", timeout=self.timeout)
            m = re.search(r'src=["\']([^"\']*huadong[^"\']*\.js[^"\']*)["\']',
                          r.text or "", re.I)
            if not m:
                with self._slider_lock:
                    self._slider_verified[domain] = True
                return True
            jsu = urljoin(domain + "/", m.group(1).split("?")[0])
            js = sess.get(jsu, headers=h, timeout=self.timeout).text or ""
            km = re.search(r'key="([^"]+)"', js)
            vm = re.search(r'value="([^"]+)"', js)
            pm = re.search(r'(/[^\s"\']+\.php)\?type=([0-9a-f]+)', js)
            if not (km and vm and pm):
                print(f"[{self.name}] 滑块JS缺少 key/value/verify 参数({domain})")
                return False
            hexval = "".join(str(ord(ch) + 1) for ch in vm.group(1))
            md5val = hashlib.md5(hexval.encode()).hexdigest()
            u = (domain + pm.group(1) + "?type=" + pm.group(2)
                 + "&key=" + quote(km.group(1)) + "&value=" + md5val)
            sess.get(u, headers=h, timeout=self.timeout)
            with self._slider_lock:
                self._slider_verified[domain] = True
            return True
        except Exception as e:
            print(f"[{self.name}] 滑块握手异常({domain})：{e}")
            return False

    def _webview_header(self):
        hdr = {"User-Agent": self.headers["User-Agent"],
               "Referer": self.base_url + "/"}
        try:
            sess = (self._slider_sessions.get(self.base_url)
                    or next(iter(self._slider_sessions.values()), None))
            if sess is not None:
                ck = "; ".join(f"{c.name}={c.value}" for c in sess.cookies)
                if ck:
                    hdr["Cookie"] = ck
        except Exception:
            pass
        return hdr

    def _slider_get(self, url, retries=4):
        from urllib.parse import urlparse as _urlparse
        retriable = (403, 429, 500, 502, 503, 504, 520, 521, 522, 850)
        delay = 0.6
        if url.startswith("http://") or url.startswith("https://"):
            host = _urlparse(url).netloc
            domain = ""
            for d in self._slider_domains:
                if host and host in d:
                    domain = d
                    break
            if not domain:
                try:
                    r = self._get_session().get(url, timeout=self.timeout)
                    return self._decode(r) if r.status_code == 200 and r.content                         else ""
                except Exception as e:
                    print(f"[{self.name}] GET 异常: {url} -> {e}")
                    return ""
            sess = self._slider_session(domain)
            if not self._slider_verified.get(domain):
                self._slider_handshake(domain)
            for i in range(retries):
                try:
                    r = sess.get(url, timeout=self.timeout)
                    if r.status_code == 200 and r.content:
                        return self._decode(r)
                    if r.status_code == 404:
                        return ""
                    if r.status_code == 403:
                        self._slider_verified[domain] = False
                        self._slider_handshake(domain)
                    elif r.status_code in retriable and i + 1 < retries:
                        time.sleep(delay)
                        delay = min(delay * 2, 3.0)
                except Exception as e:
                    print(f"[{self.name}] 滑块GET异常({i + 1}/{retries})："
                          f"{url} -> {e}")
            self._slider_idx = (self._slider_domains.index(domain) + 1) % len(self._slider_domains)
            _up = _urlparse(url)
            url = _up.path + (("?" + _up.query) if _up.query else "")
            if not url:
                return ""
        for _ in range(len(self._slider_domains)):
            domain = self._slider_domains[self._slider_idx]
            sess = self._slider_session(domain)
            if not self._slider_verified.get(domain):
                self._slider_handshake(domain)
            for i in range(retries):
                try:
                    r = sess.get(domain + url, timeout=self.timeout)
                    if r.status_code == 200 and r.content:
                        if type(self).base_url != domain:
                            type(self).base_url = domain
                            type(self).site_url = domain
                        return self._decode(r)
                    if r.status_code == 404:
                        break
                    if r.status_code == 403:
                        self._slider_verified[domain] = False
                        self._slider_handshake(domain)
                        continue
                    if r.status_code in retriable and i + 1 < retries:
                        time.sleep(delay)
                        delay = min(delay * 2, 3.0)
                except Exception as e:
                    print(f"[{self.name}] 滑块GET异常({i + 1}/{retries})："
                          f"{domain}{url} -> {e}")
            self._slider_idx = (self._slider_idx + 1) % len(self._slider_domains)
        return ""

    def _get(self, url, retries=4, timeout=None):
        if self._slider_domains:
            return self._slider_get(url, retries)
        retriable = (403, 429, 500, 502, 503, 504, 520, 521, 522, 850)
        delay = 0.6
        for i in range(retries):
            try:
                r = self._get_session().get(url, timeout=timeout or self.timeout)
                html = self._decode(r) if r.content else ""
                if r.status_code == 200 and html:
                    return html
                if html and self._has_detail(html):
                    return html
                print(f"[{self.name}] GET {url} 状态码={r.status_code}")
                if r.status_code == 404:
                    return ""
                if r.status_code in retriable and i + 1 < retries:
                    time.sleep(delay)
                    delay = min(delay * 2, 3.0)
            except Exception as e:
                print(f"[{self.name}] GET 异常({i + 1}/{retries}): {url} -> {e}")
                if i + 1 < retries:
                    time.sleep(delay)
                    delay = min(delay * 2, 3.0)
        return ""

    def _soup(self, html):
        return BeautifulSoup(html, "html.parser")

    def _clean(self, text):
        if not text:
            return ""
        text = re.sub(r"<[^>]+>", "", str(text))
        text = text.replace("&nbsp;", " ").replace("&amp;", "&")
        return re.sub(r"\s+", " ", text).strip()

    def _abs(self, u):
        if not u:
            return ""
        if u.startswith("//"):
            return "https:" + u
        if u.startswith("/"):
            return urljoin(self.base_url, u)
        return u

    _DETAIL_RX = [
        re.compile(r"/vod/detail/id/(\d+)"),
        re.compile(r"/voddetail\d*/(\d+)"),
        re.compile(r"/voddetail(\d+)\.html"),
        re.compile(r"/detail/id/(\d+)"),
        re.compile(r"/detail/(\d+)\.html"),
        re.compile(r"/detail/\?(\d+)"),
    ]

    def _match_detail(self, href):
        href = href or ""
        if self.detail_route == "custom" and self.det_rx is not None:
            m = self.det_rx.search(href)
            if m:
                return m.group(1)
        if self.detail_route == "pathslug" and self.det_rx is not None:
            m = self.det_rx.search(href)
            if m:
                return m.group(1)
        elif self.detail_route == "pathslug" and self.sections:
            m = re.match(r"^/([a-z][a-z0-9_-]{1,20})/([^/?#\"]+)\.html?$", href)
            if m and m.group(1) in self.sections:
                return m.group(1) + "/" + m.group(2)
        for rx in self._DETAIL_RX:
            m = rx.search(href)
            if m:
                return m.group(1)
        if self.detail_route and self.detail_route != "maccms":
            m = re.search(
                r"/(?:voddetail\d*|detail(?:/id)?)/([^/?#\"]{1,160}?)(?:\.html?)?(?:[?#].*)?$",
                href)
            if m:
                return m.group(1)
        return ""

    def _has_detail(self, html):
        if self.detail_route == "custom" and self.det_rx is not None:
            return bool(self.det_rx.search(html or ""))
        if self.detail_route == "pathslug":
            if self.det_rx is not None:
                if self.det_rx.search(html or ""):
                    return True
            if self.sections:
                secs = "|".join(re.escape(s) for s in self.sections)
                if re.search(rf"/({secs})/[^/?#\"]+\.html", html or ""):
                    return True
        return bool(re.search(
            r"/(?:vod/detail/id/|voddetail\d*/?\d|detail/id/\d|detail/[\w-]{4,})",
            html or ""))

    def _extract_cards(self, soup, limit=40):
        seen, seen_url, items = set(), set(), []
        for a in soup.find_all("a", href=True):
            vid = self._match_detail(a.get("href", ""))
            if not vid or vid in seen:
                continue
            seen.add(vid)
            seen_url.add(urljoin(self.base_url, a.get("href", "")))
            img = a.find(["img", "amp-img"]) or (a.parent.find(["img", "amp-img"])
                                                  if a.parent else None)
            pic = ""
            nodes = [img, a] + ([a.parent] if a.parent is not None else []) \
                + list(a.find_all(True)[:8])
            for cand in nodes:
                if cand is None or not hasattr(cand, "get"):
                    continue
                for at in ("data-original", "data-src", "data-lazy",
                           "data-lazy-src", "data-background", "data-echo"):
                    v = (cand.get(at) or "").strip()
                    if v and ("." in v or v.startswith("/")):
                        pic = v
                        break
                if pic:
                    break
                mbg = re.search(
                    r"background-image\s*:\s*url\(['\"]?([^'\")]+)",
                    cand.get("style") or "", re.I)
                if mbg:
                    pic = mbg.group(1).strip()
                    break
                pic = (cand.get("imgtag") or "").strip()
                if pic:
                    break
            if not pic:
                for cand in nodes:
                    if cand is None or not hasattr(cand, "get"):
                        continue
                    v = (cand.get("src") or "").strip()
                    if v and "." in v and not v.startswith("data:"):
                        pic = v
                        break
            if pic:
                pic = urljoin(self.base_url, pic)
            name = (a.get("title") or "").strip()
            if not name and img is not None:
                name = (img.get("alt") or "").strip()
            if not name or len(name) > 40:
                t2 = ""
                for cand in a.find_all(["h1", "h2", "h3", "h4", "span",
                                        "p", "strong", "em"]):
                    t = cand.get_text(strip=True)
                    if 1 < len(t) <= 40:
                        t2 = t
                        break
                if t2:
                    name = t2
                elif len(name) > 40:
                    name = name[:40]
            if not name and img is None:
                continue
            remarks = ""
            box = a.parent
            for _ in range(3):
                if box is None:
                    break
                t = box.get_text(" ", strip=True)
                if name and name in t:
                    t = t.replace(name, " ").strip()
                if t:
                    remarks = t[:30]
                    break
                box = box.parent
            items.append({
                "vod_id": vid,
                "vod_name": name,
                "vod_pic": self._abs(pic),
                "vod_remarks": remarks,
            })
            if len(items) >= limit:
                break
        if len(items) < 5:
            for it in self._cards_heuristic(soup, limit):
                if it["vod_id"] not in seen:
                    seen.add(it["vod_id"])
                    items.append(it)
        return items

    def _cards_heuristic(self, soup, limit=40):
        best, best_score = None, 0
        for tag in soup.find_all(["ul", "div", "section", "dl", "tbody"]):
            children = tag.find_all(recursive=False)
            if len(children) < 3:
                continue
            cnt = 0
            for c in children:
                a = c if c.name == "a" else c.find("a", href=True)
                if a is not None and c.find(["img", "amp-img"]) is not None:
                    cnt += 1
            if cnt < 3:
                continue
            score = cnt
            cls = " ".join(tag.get("class") or []).lower()
            if any(k in cls for k in ("list", "item", "video", "grid", "movie",
                                      "vod", "pic", "module", "content")):
                score = int(score * 1.6)
            if score > best_score:
                best_score, best = score, tag
        rows = (best.find_all(recursive=False) if best is not None
                else [a for a in soup.find_all("a", href=True)
                      if a.find(["img", "amp-img"])])
        items, seen = [], set()
        for row in rows:
            try:
                a = row if row.name == "a" else row.find("a", href=True)
                if a is None:
                    continue
                href = a.get("href") or ""
                if not href or href.startswith(("javascript:", "#", "mailto:")):
                    continue
                full = urljoin(self.base_url, href)
                if full in seen or full in seen_url \
                        or full.rstrip("/") == self.base_url.rstrip("/"):
                    continue
                seen.add(full)
                img = row.find(["img", "amp-img"])
                pic = ""
                if img:
                    pic = (img.get("data-src") or img.get("data-original")
                           or img.get("data-echo") or img.get("src") or "")
                title = (a.get("title") or "").strip()
                if not title and img:
                    title = (img.get("alt") or "").strip()
                if not title:
                    for cand in row.find_all(["h1", "h2", "h3", "h4", "a", "span", "p"]):
                        t = cand.get_text(strip=True)
                        if 1 < len(t) <= 40:
                            title = t
                            break
                if not title and not pic:
                    continue
                remark = ""
                for cand in row.find_all(["span", "em", "p", "div"]):
                    t = cand.get_text(strip=True)
                    if t and len(t) <= 14 and re.search(r"(更新|全|集|HD|BD|第|期|完结)", t):
                        remark = t
                        break
                items.append({
                    "vod_id": full,
                    "vod_name": title or "未知",
                    "vod_pic": self._abs(pic),
                    "vod_remarks": remark,
                })
                if len(items) >= limit:
                    break
            except Exception:
                continue
        return items

    def homeContent(self, filter=False):
        result = {"class": [{"type_id": t, "type_name": n}
                            for t, n in zip(self.class_url, self.class_name)],
                  "filters": self._build_filters() if self._filter_mode else {}, "list": []}
        try:
            html = self._get(self.base_url + "/", retries=1, timeout=8)
            if not html or len(html) < 500:
                html = self._get(self.base_url + "/index.php", retries=1, timeout=8)
            if html:
                result["list"] = self._extract_cards(self._soup(html), limit=30)
        except Exception as e:
            print(f"[{self.name}] 首页异常: {e}")
        return result

    def homeVideoContent(self):
        return self.homeContent()

    def categoryContent(self, tid, pg, filter=False, extend=None, content=None):
        page = int(pg) if str(pg).isdigit() and int(pg) > 0 else 1
        result = {"list": [], "page": page, "pagecount": 1,
                  "limit": self.page_size, "total": 0}
        try:
            tid_s = str(tid)
            ext = self._ext_dict(extend, content)
            ext = {k: str(v) for k, v in ext.items()
                   if str(v) and k in (self._filter_data.get(tid_s) or {})}
            cands = []
            if tid_s == "home":
                cands.append(self.base_url + "/")
            else:
                if ext or not self.cat_pattern:
                    if self._show_mode == "path" and self._path_tpl:
                        cands.append(self._build_show_url(tid_s, page, ext))
                    elif self._show_mode == "kvseg" and self._kv_segs:
                        cands.append(self._build_show_url(tid_s, page, ext))
                    elif self._show_mode == "seg" and self._show_tpl:
                        cands.append(self._build_show_url(tid_s, page, ext))
                    elif self._filter_mode:
                        cands.append(self._build_show_url(tid_s, page, ext))
                if self.cat_pattern:
                    u = (self.cat_pattern
                         .replace("{cid}", tid_s).replace("{pg}", str(page)))
                    if not re.match(r"^https?://", u):
                        u = urljoin(self.base_url, u)
                    cands.append(u)
                    if page <= 1:
                        v = re.sub(r"-1\.html$", ".html", u)
                        if v != u:
                            cands.append(v)
                else:
                    if self.detail_route == "pathslug" and tid_s in (self.sections or []):
                        cands.append(self.base_url + f"/{tid_s}/")
                        if page > 1:
                            cands.append(self.base_url + f"/{tid_s}/?page={page}")
                        cands.append(self.base_url + f"/{tid_s}/index{page}.html"
                                     if page > 1 else self.base_url + f"/{tid_s}/index.html")
                    cands.append(self.base_url + f"/vodtype/{tid_s}.html")
                    if page > 1:
                        cands.append(self.base_url + f"/vodtype/{tid_s}-{page}.html")
                    for style in ("show", "type"):
                        path = f"{self.prefix}/vod/{style}/id/{tid_s}"
                        if page > 1:
                            path += f"/page/{page}"
                        cands.append(self.base_url + path + ".html")
                cands.append(self.base_url + "/")
            html = ""
            cands = list(dict.fromkeys(cands))
            for i, u in enumerate(cands):
                got = self._get(u, retries=2)
                if ext and got and i == 0:
                    html = got
                    break
                if got and (self._has_detail(got) or i == len(cands) - 1):
                    html = got
                    break
                if got and not html:
                    html = got
            if not html:
                return result
            soup = self._soup(html)
            items = self._extract_cards(soup, limit=60)
            if not items and page <= 1 and not ext:
                try:
                    home = self._get(self.base_url + "/", retries=1) or \
                        self._get(self.base_url + "/index.php", retries=1)
                    if home and self._has_detail(home):
                        items = self._extract_cards(self._soup(home), limit=60)
                except Exception:
                    pass
            result["list"] = items
            result["total"] = len(items)
            maxpg = self._scan_pagecount(html)
            if maxpg > page:
                result["pagecount"] = maxpg
            elif len(items) >= self.page_size:
                result["pagecount"] = page + 1
        except Exception as e:
            print(f"[{self.name}] 分类异常: {e}")
        return result

    def _page_rx_list(self):
        rxs = []
        sep = self._seg_sep or "-"
        seg_noc = r"[^_]" if sep == "_" else r"[^-]"
        _ids = [str(c) for c in (self.class_url or []) if str(c or "")]
        idpat = r"\d+" if (not _ids or all(x.isdigit() for x in _ids)) else r"[^/\-]+"
        for tpl in (self.cat_pattern, self._show_tpl, self._path_tpl):
            if not tpl or "{pg}" not in tpl or "{qs}" in tpl:
                continue
            t = re.sub(r"^https?://[^/]+", "", tpl)
            rx = re.escape(t)
            rx = rx.replace(re.escape("{cid}"), idpat)
            rx = rx.replace(re.escape("{id}"), idpat)
            rx = rx.replace(re.escape("{val}"), r"[^/?#]*")
            rx = rx.replace(re.escape("{pg}"), r"(\d+)")
            for k in (self._seg_pos or {}):
                rx = rx.replace(re.escape("{%s}" % k), seg_noc + r"*")
            rx = re.sub(r"\\{[^{}]+?\\}", seg_noc + r"*", rx)
            rxs.append(rx)
        if self._kv_segs and any(t == "{pg}" for t in self._kv_segs):
            toks = []
            for tk in self._kv_segs:
                if tk == "{pg}":
                    toks.append(r"(\d+)")
                elif tk == "{id}":
                    toks.append(r"\d+")
                elif tk and tk[0] == "{" and tk[-1] == "}":
                    toks.append(seg_noc + r"*")
                else:
                    toks.append(re.escape(tk))
            rxs.append(re.escape(self._kv_prefix or "/")
                       + "-".join(toks) + r"\.html?")
        return rxs

    def _scan_pagecount(self, html):
        maxpg = 0
        for rx in self._page_rx_list():
            try:
                for m in re.finditer(rx, html):
                    v = int(m.group(1))
                    if maxpg < v <= 20000:
                        maxpg = v
            except re.error:
                continue
        for m in re.finditer(r'[\?&](?:page|p)=(\d+)', html):
            v = int(m.group(1))
            if maxpg < v <= 20000:
                maxpg = v
        for m in re.finditer(r'href="[^"]*[-/](\d+)(?:\.html)?"[^>]*>[^<]*下一', html):
            v = int(m.group(1))
            if maxpg < v <= 20000:
                maxpg = v
        return maxpg


    _ORDER = ("class", "area", "lang", "year", "letter", "by", "status", "plot")

    def _build_filters(self):
        filters = {}
        allow = (self._path_dim,) if (self._show_mode == "path" and self._path_dim) else None
        for tid, dims in self._filter_data.items():
            arr = []
            keys = [k for k in self._ORDER if k in dims]
            keys += [k for k in dims if k not in keys]
            for param in keys:
                if allow is not None and param not in allow:
                    continue
                arr.append({
                    "key": param,
                    "name": self._filter_names.get(param, param),
                    "init": "",
                    "value": [{"n": label, "v": val} for label, val in dims[param]],
                })
            if arr:
                filters[tid] = arr
        return filters

    @staticmethod
    def _ext_dict(extend, content=None):
        ext = extend if extend is not None else content
        if isinstance(ext, str) and ext:
            try:
                import json as _json
                ext = _json.loads(ext)
            except Exception:
                ext = {}
        return ext if isinstance(ext, dict) else {}

    def _build_seg_url(self, tid, pg, ext):
        total = self._show_total or (max(self._seg_pos.values()) + 2 if self._seg_pos else 12)
        seg = [""] * total
        seg[0] = str(tid)
        for key, pos in self._seg_pos.items():
            v = str(ext.get(key, "") or "")
            if v and 0 <= pos < total:
                seg[pos] = v
        pg_pos = 8 if 8 < total else (total - 1)
        for key, pos in self._seg_pos.items():
            if key == "page":
                pg_pos = pos
        if int(pg) > 1:
            seg[pg_pos] = str(pg)
        prefix = self._seg_prefix or "/vodshow/"
        if not prefix.startswith("/"):
            prefix = "/" + prefix
        sep = self._seg_sep or "-"
        return self.base_url.rstrip("/") + prefix + sep.join(
            quote(s, safe="") for s in seg) + ".html"

    def _build_query_url(self, tid, pg, ext):
        tpl = self._show_tpl or "/?{qs}"
        params = []
        dims = self._filter_data.get(str(tid)) or {}
        for key in dims:
            v = ext.get(key, "")
            if v:
                params.append("%s=%s" % (key, quote(str(v), safe="")))
        if int(pg) > 1:
            params.append("page=%s" % pg)
        base = tpl.replace("{id}", str(tid)).replace("{qs}", "&".join(params))
        return self.base_url + base

    def _build_kvseg_url(self, tid, pg, ext):
        segs = getattr(self, "_kv_segs", None) or []
        if not segs:
            return self._cat_url(tid, pg)
        out = []
        for s in segs:
            if len(s) > 2 and s[0] == "{" and s[-1] == "}":
                k = s[1:-1]
                if k == "id":
                    v = str(tid)
                elif k == "pg":
                    v = str(pg)
                else:
                    v = str(ext.get(k, "") or "")
                out.append(quote(v, safe="") if v else "")
            else:
                out.append(s)
        prefix = self._kv_prefix or "/"
        if not prefix.startswith("/"):
            prefix = "/" + prefix
        return self.base_url.rstrip("/") + prefix + "-".join(out) + ".html"

    def _cat_url(self, tid, pg):
        if self.cat_pattern:
            u = self.cat_pattern.replace("{cid}", str(tid)).replace("{pg}", str(pg))
            if not re.match(r"^https?://", u):
                u = urljoin(self.base_url, u)
            if str(pg) == "1":
                u = re.sub(r"-1\.html$", ".html", u)
            return u
        return self.base_url.rstrip("/") + "%s/vod/type/id/%s.html" % (self.prefix, tid)

    def _build_show_url(self, tid, pg, extend):
        ext = extend or {}
        if self._show_mode == "seg" and self._show_tpl:
            return self._build_seg_url(tid, pg, ext)
        if self._show_mode == "query" and self._show_tpl:
            return self._build_query_url(tid, pg, ext)
        if self._show_mode == "path" and self._path_tpl:
            v = str(ext.get(self._path_dim, "") or "")
            if v:
                url = self.base_url.rstrip("/") + self._path_tpl.replace(
                    "{val}", quote(str(v), safe=""))
                if int(pg) > 1:
                    url += "/page/%s" % pg
                return url + ".html"
            return self._cat_url(tid, pg)
        if self._show_mode == "kvseg" and self._kv_segs:
            return self._build_kvseg_url(tid, pg, ext)
        """苹果CMS筛选页路径：{prefix}/vod/show/by/../area/../class/../id/{tid}/lang/../year/../letter/../page/{pg}.html"""
        by = ext.get("by", "")
        area = ext.get("area", "")
        cls = ext.get("class", "")
        lang = ext.get("lang", "")
        year = ext.get("year", "")
        letter = ext.get("letter", "")
        path = f"{self.prefix}/vod/show/"
        if by:
            path += f"by/{by}/"
        if area:
            path += "area/%s/" % quote(str(area))
        if cls:
            path += "class/%s/" % quote(str(cls))
        path += "id/%s" % tid
        if lang:
            path += "/lang/%s" % quote(str(lang))
        if year:
            path += "/year/%s" % quote(str(year))
        if letter:
            path += "/letter/%s" % quote(str(letter))
        if pg and int(pg) > 1:
            path += "/page/%s.html" % pg
        else:
            path += ".html"
        return self.base_url + path

    def _detail_urls(self, vid):
        b = self.base_url
        if self.detail_route == "custom" and self.det_tpl:
            return [self.base_url + self.det_tpl.replace("{vid}", str(vid))]
        if self.detail_route == "voddetail":
            return [f"{b}/voddetail/{vid}.html", f"{b}/voddetail{vid}.html",
                    f"{b}/voddetail2/{vid}.html"]
        if self.detail_route == "seacms":
            return [f"{b}/detail/id/{vid}.html", f"{b}/detail/?{vid}.html"]
        if self.detail_route == "detail":
            return [f"{b}/detail/{vid}.html", f"{b}/detail/{vid}",
                    f"{b}/detail/?{vid}.html", f"{b}/detail/id/{vid}.html",
                    f"{b}/voddetail/{vid}.html"]
        if self.detail_route == "pathslug":
            if self.det_tpl:
                return [self.base_url + self.det_tpl.replace("{vid}", str(vid))]
            return [f"{b}/{vid}", f"{b}/{vid}.html"]
        return [f"{b}{self.prefix}/vod/detail/id/{vid}.html"]

    _ERR_MARKS = ("could not be found", "page not found", "404 not found",
                  "页面不存在", "内容不存在", "您访问的页面", "无法找到",
                  "内容正在审核", "参数错误")

    @classmethod
    def _looks_error(cls, html):
        low = (html or "")[:4000].lower()
        return any(m in low for m in cls._ERR_MARKS)

    def detailContent(self, ids):
        result = {"list": []}
        vid = ""
        if isinstance(ids, (list, tuple)):
            vid = str(ids[0]) if ids else ""
        elif isinstance(ids, dict):
            vid = str(ids.get("vod_id") or ids.get("id") or "")
        elif ids is not None:
            vid = str(ids)
        vid = str(vid)
        try:
            if re.match(r"^https?://", vid):
                url = vid
                html = self._get(url)
            else:
                vid = vid.strip().strip("/")
                if not vid:
                    return result
                if "/" in vid and self.detail_route != "pathslug":
                    return result
                html = ""
                for u in self._detail_urls(vid):
                    got = self._get(u)
                    if got and len(got) > 500 and not self._looks_error(got):
                        html = got
                        break
            if not html:
                return result
            soup = self._soup(html)

            node = (soup.select_one(".stui-content__detail .title")
                    or soup.select_one(".module-info-name")
                    or soup.select_one(".module-info-heading h1")
                    or soup.select_one(".video-info-header .title")
                    or soup.select_one(".detail-content .title")
                    or soup.select_one("h1") or soup.select_one("h2"))
            if node is None:
                for cand in soup.select("[class*=title]"):
                    t = cand.get_text(strip=True)
                    if not t or len(t) > 40:
                        continue
                    anc, ok = cand, False
                    for _ in range(4):
                        anc = anc.parent
                        if anc is None:
                            break
                        pt = anc.get_text(" ", strip=True)
                        if any(w in pt for w in ("主演", "导演", "简介", "类型", "地区")):
                            ok = True
                            break
                    if ok:
                        node = cand
                        break
            vod_name = node.get_text(strip=True) if node else ""

            pic_node = (soup.select_one(".module-item-pic img")
                        or soup.select_one(".stui-content__thumb img")
                        or soup.select_one(".content_thumb img")
                        or soup.select_one("img[data-original]")
                        or soup.select_one("img[data-src]")
                        or soup.select_one("amp-img[src]")
                        or soup.select_one("[style*='background-image']"))
            vod_pic = ""
            if pic_node:
                vod_pic = (pic_node.get("data-src") or pic_node.get("data-original")
                           or pic_node.get("src") or "")
                if not vod_pic:
                    style = pic_node.get("style") or ""
                    mbg = re.search(r"background-image\s*:\s*url\(['\"]?([^'\")]+)",
                                    style, re.I)
                    if mbg:
                        vod_pic = mbg.group(1).strip()
                if not vod_pic:
                    vod_pic = pic_node.get("imgtag") or ""
                if vod_pic:
                    vod_pic = urljoin(self.base_url, vod_pic)

            info = {}
            for row in soup.select(".video-info-items"):
                t = row.select_one(".video-info-itemtitle")
                if not t:
                    continue
                key = re.sub(r"[：:]", "", t.get_text(strip=True))
                val = row.select_one(".video-info-item")
                if val:
                    info[key] = val.get_text(" ", strip=True)
            if not info:
                full = soup.get_text(" ", strip=True)
                for key, pat in (("导演", r"导演[：:]\s*([^ ]{1,40})"),
                                 ("主演", r"主演[：:]\s*([^ ]{1,60})"),
                                 ("年份", r"(?:年代|年份)[：:]\s*(\d{4})"),
                                 ("地区", r"地区[：:]\s*(\S{1,10})"),
                                 ("类型", r"类型[：:]\s*(\S{1,10})"),
                                 ("状态", r"(?:状态|备注|更新)[：:]\s*(\S{1,20})")):
                    m = re.search(pat, full)
                    if m:
                        info[key] = m.group(1).strip()

            desc = (soup.select_one(".video-info-content") or soup.select_one(".sqjj_a")
                    or soup.select_one(".stui-content__desc") or soup.select_one(".vodplayinfo"))
            vod_content = self._clean(desc.get_text(" ", strip=True)) if desc else ""

            groups = {}
            cp_names = {}
            _cp_rx = re.compile(r"^copy_([A-Za-z0-9_\-]+)\[\]$")
            _cp_inputs = [i for i in soup.find_all("input")
                          if _cp_rx.match(i.get("name") or "")]
            if _cp_inputs:
                _seq = {}
                for inp in _cp_inputs:
                    ck = _cp_rx.match(inp.get("name") or "").group(1)
                    val = (inp.get("value") or "").strip()
                    if not val:
                        continue
                    if ck not in _seq:
                        _seq[ck] = str(len(_seq) + 1)
                        csid = _seq[ck]
                        ul = inp.find_parent("ul")
                        box = ul.parent if ul is not None else inp.find_parent("div")
                        cnm = ""
                        if box is not None:
                            h = box.find(["h4", "h3", "h2", "h5"])
                            if h is not None:
                                cnm = re.sub(r"\s+", "", h.get_text(" ", strip=True))
                                cnm = re.sub(r"(地址|线路|播放)$", "", cnm) or cnm
                        if not cnm and ul is not None:
                            cls = [c for c in (ul.get("class") or [])
                                   if c not in ("playlist", "wbox")]
                            cnm = cls[0] if cls else ""
                        cp_names[csid] = cnm or ck
                    csid = _seq[ck]
                    if "$" in val:
                        epname, _, link = val.partition("$")
                    else:
                        epname, link = "", val
                    link = link.strip()
                    if not link:
                        continue
                    if not link.startswith("http"):
                        link = urljoin(self.base_url, link)
                    groups.setdefault(csid, {})
                    cnid = str(len(groups[csid]) + 1)
                    groups[csid][cnid] = (epname.strip() or f"第{cnid}集", link)
            for a in ([] if groups else soup.select("a[href]")):
                href = a.get("href", "")
                m = re.search(r"/vod/play/id/(\d+)/sid/(\d+)/nid/(\d+)", href)
                if m:
                    ref_vid, sid, nid = m.groups()
                    ref = f"{ref_vid}-{sid}-{nid}"
                else:
                    m = re.search(r"/(?:vodplay|v_play|vplay)/(\d+)-(\d+)-(\d+)\.html", href)
                    if m:
                        sid, nid = m.group(2), m.group(3)
                        ref = urljoin(self.base_url, href)
                    else:
                        m = re.search(r"/[a-z0-9_-]{1,30}/(\d+)-(\d+)-(\d+)\.html?$", href)
                        if m:
                            sid, nid = m.group(2), m.group(3)
                            ref = urljoin(self.base_url, href)
                        else:
                            m2 = re.search(r"^/(?:play|v|watch)/[^/?#]+-(\d+)\.html?$", href)
                            if m2:
                                sid, nid = "1", m2.group(1)
                                ref = urljoin(self.base_url, href)
                            else:
                                seg = (href or "").strip().strip("/")
                                seg = seg.split("?")[0].split("#")[0]
                                if not seg.endswith(".html") or "/" in seg:
                                    continue
                                kv = {}
                                parts = seg[:-5].split("-")
                                for i in range(len(parts) - 1):
                                    if parts[i] in ("src", "sid", "num", "nid", "ep",
                                                    "episode", "server", "line", "pid"):
                                        kv[parts[i]] = parts[i + 1]
                                nid2 = (kv.get("num") or kv.get("nid")
                                        or kv.get("ep") or kv.get("episode") or "")
                                if not nid2.isdigit():
                                    continue
                                sid = (kv.get("src") or kv.get("sid")
                                       or kv.get("server") or kv.get("line") or "1")
                                nid = nid2
                                ref = urljoin(self.base_url, href)
                ep = a.get_text(strip=True) or f"第{nid}集"
                groups.setdefault(sid, {})[nid] = (ep, ref)

            try:
                _pan_rx = re.compile(
                    r"^https?://[\w.-]*("
                    r"pan\.quark\.cn|quark\.cn|pan\.xunlei\.com|xlshare|"
                    r"pan\.baidu\.com|115\.com|alipan\.com|aliyundrive\.com|"
                    r"123pan\.com|123865\.com|123684\.com|wopan189\.cn|"
                    r"cloud\.189\.cn|caiyun\.139\.cn|pikpako|lanzou[a-z]*\.com)",
                    re.I)
                _pan_groups = {}
                for a in soup.find_all("a", href=True):
                    href = (a.get("href") or "").strip()
                    if not _pan_rx.match(href):
                        continue
                    box, pname = a.parent, ""
                    for _ in range(8):
                        if box is None:
                            break
                        h = box.find(["h2", "h3", "h4", "h5"])
                        if h is not None:
                            t = re.sub(r"\s+", " ", h.get_text(strip=True))
                            if t and len(t) <= 24:
                                pname = t
                                break
                        box = box.parent
                    if not pname:
                        continue
                    sp = a.find(class_="netdisk-name")
                    if sp is not None:
                        label = sp.get_text(strip=True)
                    else:
                        label = a.get_text(" ", strip=True)
                    label = re.sub(r"\s+", " ", label or "").strip()
                    epsd = _pan_groups.setdefault(pname, {})
                    if len(epsd) >= 100:
                        continue
                    key = label or ("资源%d" % (len(epsd) + 1))
                    while key in epsd:
                        key = "%s·%d" % (key, len(epsd) + 1)
                    epsd[key] = href
                if _pan_groups:
                    _mx = 0
                    for k in groups:
                        try:
                            _mx = max(_mx, int(k))
                        except Exception:
                            pass
                    for _i, (pn, eps) in enumerate(_pan_groups.items()):
                        sid = str(_mx + 1 + _i)
                        groups[sid] = {str(j + 1): (nm, uu)
                                       for j, (nm, uu) in enumerate(eps.items())}
                        cp_names[sid] = pn
            except Exception:
                pass

            try:
                if len(groups) > 1:
                    _cta_rx = re.compile(
                        r"^(?:立即|马上|开始|点击|在线|免费|高速|极速)?"
                        r"(?:播放|观看|看片)$")
                    for s_ in [k for k in groups if len(groups[k]) <= 4]:
                        labels = [t for t, _u in groups[s_].values()]
                        if labels and all(_cta_rx.match(re.sub(r"\s+", "", t))
                                          for t in labels):
                            del groups[s_]
            except Exception:
                pass

            line_names, line_urls = [], []
            tabs = (soup.select(".module-player-tab .module-tab-item")
                    or soup.select(".module-tab-item[data-dropdown-value]")
                    or soup.select("[id*='playList'] .module-tab-item")
                    or soup.select(".player-tab-btn, .tab-btn"))

            def _container_name(sid, eps=None):
                rx = re.compile(r"playlist[_-]?(\d+)$", re.I)
                for pt in soup.select(".playtitle[tag]"):
                    if (pt.get("tag") or "").strip() == str(sid):
                        t = pt.get_text(strip=True)
                        if t and len(t) <= 20:
                            return t
                for box in soup.find_all(id=rx):
                    m = rx.search(box.get("id") or "")
                    if not m or m.group(1) != str(sid):
                        continue
                    h = box.find(["h2", "h3", "h4"])
                    if h is None:
                        dt = box.find(class_=re.compile(r"down-title|title", re.I))
                        h = dt.find(["h2", "h3", "h4", "strong"]) if dt else None
                    t = h.get_text(strip=True) if h else ""
                    if t and len(t) <= 20:
                        return t
                    anc = box
                    for _ in range(5):
                        anc = anc.parent
                        if anc is None:
                            break
                        if len(anc.find_all(id=rx)) > 1:
                            continue
                        pt = anc.select_one(".playtitle")
                        if pt is not None:
                            t2 = pt.get_text(strip=True)
                            if t2 and len(t2) <= 20:
                                return t2
                        h2 = anc.find(class_=re.compile(r"pannel__head|panel__head"))
                        if h2 is not None:
                            t3 = h2.get_text(strip=True)
                            if t3 and len(t3) <= 20:
                                return t3
                if eps:
                    hrefs = set()
                    for _n, (_t, _u) in eps.items():
                        hrefs.add(_u)
                    anchors = []
                    for a in soup.find_all("a", href=True):
                        hu = (a.get("href") or "").strip()
                        if hu in hrefs or urljoin(self.base_url, hu) in hrefs:
                            anchors.append(a)
                    anc = anchors[0].parent if anchors else None
                    for _ in range(10):
                        if anc is None:
                            break
                        if all(x in anc.descendants for x in anchors):
                            links = anc.find_all("a", href=True)
                            if len(links) > len(anchors) + 4:
                                break
                            h = anc.find(["h2", "h3", "h4", "h5"])
                            if h is None:
                                h = anc.find(
                                    class_=re.compile(r"panel__?head|playtitle", re.I))
                            t = re.sub(r"\s+", " ", h.get_text(strip=True)) if h else ""
                            if t and len(t) <= 24:
                                return t
                        anc = anc.parent
                    if anchors:
                        t = re.sub(r"\s+", "", anchors[0].get_text(strip=True))
                        if (1 < len(t) <= 12
                                and not re.match(
                                    r"^[\d一二两三四五六七八九十百千]+$", t)
                                and not re.match(
                                    r"^第?[\d一二三四五六七八九十百]+"
                                    r"[集期话章节]$", t)
                                and not re.search(
                                    r"(更新|完结|全\d+[集期]|预告|彩蛋)$", t)):
                            return t
                return ""

            fb_names = {}
            if not groups and self.detail_route in ("maccms", "voddetail", "detail"):
                groups, fb_names = self._play_fallback_vodplay(vid)
            if groups:
                for i, sid in enumerate(sorted(groups, key=lambda x: int(x))):
                    name = ""
                    if len(tabs) == len(groups):
                        name = tabs[i].get("data-dropdown-value") or tabs[i].get_text(strip=True)
                    name = (name or cp_names.get(sid, "")
                            or _container_name(sid, groups[sid]) or fb_names.get(sid, ""))
                    name = name or f"线路{sid}"
                    if name in line_names:
                        name = f"{name}{sid}"
                    line_names.append(name)
                    eps = groups[sid]
                    line_urls.append("#".join(
                        f"{eps[n][0]}${eps[n][1]}" for n in sorted(eps, key=lambda x: int(x))))
            else:
                for name, eps in self._play_groups_heuristic(soup):
                    line_names.append(name)
                    line_urls.append("#".join(eps))

            vod = {
                "vod_id": str(vid),
                "vod_name": vod_name,
                "vod_pic": self._abs(vod_pic),
                "vod_year": info.get("年份", info.get("年代", "")),
                "vod_area": info.get("地区", ""),
                "vod_actor": info.get("主演", info.get("演员", "")),
                "vod_director": info.get("导演", ""),
                "vod_type": info.get("类型", ""),
                "vod_remarks": info.get("状态", info.get("备注", "")),
                "vod_content": vod_content,
                "vod_play_from": "$$$".join(line_names) or "默认线路",
                "vod_play_url": "$$$".join(line_urls),
            }
            result["list"].append(vod)
        except Exception as e:
            import traceback
            print(f"[{self.name}] 详情异常: {e}")
            traceback.print_exc()
        return result

    def searchContent(self, key, quick=None, pg="1"):
        page = int(pg) if str(pg).isdigit() and int(pg) > 0 else 1
        result = {"list": [], "page": page, "pagecount": 1,
                  "limit": self.page_size, "total": 0}
        if not key:
            return result
        kw = quote(str(key), safe="")
        urls = []
        if self.search_pattern:
            u = (self.search_pattern
                 .replace("{key}", kw).replace("{pg}", str(page)))
            if not re.match(r"^https?://", u):
                u = urljoin(self.base_url, u)
            urls.append(u)
        urls += [
            f"{self.base_url}{self.prefix}/vod/search/page/{page}/wd/{kw}.html",
            f"{self.base_url}{self.prefix}/vod/search.html?wd={kw}"
            + (f"&page={page}" if page > 1 else ""),
            f"{self.base_url}/vodsearch/{kw}----------{page}---.html",
            f"{self.base_url}/vodsearch/{kw}-------------.html",
            f"{self.base_url}/search/?keyword={kw}&page={page}",
            f"{self.base_url}/search?wd={kw}&page={page}",
        ]
        for u in urls:
            try:
                html = self._get(u)
                if not html:
                    continue
                items = self._extract_cards(self._soup(html), limit=60)
                if items:
                    result["list"] = items
                    result["total"] = len(items)
                    result["pagecount"] = page + 1 if len(items) >= self.page_size else page
                    break
            except Exception as e:
                print(f"[{self.name}] 搜索异常: {e}")
        return result

    def searchContentPage(self, key, quick, pg):
        return self.searchContent(key, quick, pg)

    @staticmethod
    def _is_play_link(a):
        href = (a.get("href") or "").lower()
        if not href or href.startswith(("javascript:", "#", "mailto:")):
            return False
        text = a.get_text(strip=True)
        if re.search(r"/(vodplay|vplay|play|watch|v)/", href):
            return True
        if re.search(r"第\s*\d+\s*[集话期]", text):
            return True
        if re.match(r"^\d{1,4}$", text) and "?" not in href \
                and not re.search(r"(?:year|area|class|lang|letter|page|cateid)=", href) \
                and not re.search(r"/(?:show|vodshow|type|vodtype|label|vtype)/", href):
            return True
        if re.search(r"\d+-\d+-\d+\.html", href):
            return True
        if re.search(r"\.(m3u8|mp4)(\?|$)", href):
            return True
        return False

    @staticmethod
    def _is_ancestor(a, b):
        p = b
        while p is not None:
            if p is a:
                return True
            p = getattr(p, "parent", None)
        return False

    @staticmethod
    def _guess_group_name(tag, idx):
        prev = tag.find_previous(["h1", "h2", "h3", "h4", "strong", "span", "a"])
        if prev is not None:
            t = prev.get_text(strip=True)
            if 0 < len(t) <= 12:
                return t
        return "线路%d" % (idx + 1)

    def _play_groups_heuristic(self, soup):
        groups = []
        cands = []
        for tag in soup.find_all(["ul", "div", "ol"]):
            links = tag.find_all("a", href=True)
            if len(links) < 2:
                continue
            play_links = [a for a in links if self._is_play_link(a)]
            if len(play_links) >= 2:
                cands.append((tag, play_links))
        cands.sort(key=lambda x: -len(x[1]))
        picked = []
        for tag, links in cands:
            if any(self._is_ancestor(t, tag) for t, _ in picked):
                continue
            picked.append((tag, links))
        for idx, (tag, links) in enumerate(picked):
            eps, seen = [], set()
            for a in links:
                href = a.get("href") or ""
                if not href or href.startswith("javascript:"):
                    continue
                full = urljoin(self.base_url, href)
                if full in seen:
                    continue
                seen.add(full)
                name = a.get_text(strip=True) or ("第%d集" % (len(eps) + 1))
                eps.append("%s$%s" % (name, full))
            if eps:
                groups.append((self._guess_group_name(tag, idx), eps))
        return groups

    @staticmethod
    def _extract_balanced(text, marker):
        if not text:
            return ""
        idx = text.find(marker)
        if idx < 0:
            return ""
        i = text.find("{", idx)
        if i < 0:
            return ""
        depth, in_str, esc, start, n = 0, False, False, i, len(text)
        while i < n:
            c = text[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        return text[start:i + 1]
            i += 1
        return ""

    @staticmethod
    def _js_unescape(s):
        if not s:
            return ""
        try:
            s = re.sub(r"%u([0-9a-fA-F]{4})",
                       lambda m: chr(int(m.group(1), 16)), s)
            return requests.utils.unquote(s)
        except Exception:
            return s

    @staticmethod
    def _looks_html(s):
        t = (s or "").lstrip("\ufeff \t\r\n")
        t = re.sub(r"^(?:<!--.*?-->\s*)+", "", t, flags=re.S)
        return bool(re.match(r"(?is)^(?:<!doctype\s+html\b|<html\b|<head\b|"
                             r"<body\b|<div\b|<script\b|<main\b|<section\b)", t))

    @staticmethod
    def _decode_page(html):
        if not html:
            return html
        try:
            m = re.search(r'atob\(atob\("([^"]+)"\)\)', html)
            if m:
                s1 = base64.b64decode(m.group(1)).decode("utf-8", "replace")
                s2 = base64.b64decode(s1).decode("utf-8", "replace")
                fin = requests.utils.unquote(s2)
                if not Spider._looks_html(fin):
                    try:
                        fin = requests.utils.unquote(
                            base64.b64decode(fin).decode("utf-8", "replace"))
                    except Exception:
                        pass
                return fin if Spider._looks_html(fin) else html
            m = re.search(r'atob\("([^"]+)"\)', html)
            if m:
                s1 = base64.b64decode(m.group(1)).decode("utf-8", "replace")
                if re.fullmatch(r"[0-9a-fA-F]+", (s1 or "")[:64] or "x") and len(s1) >= 8:
                    s1 = bytes.fromhex(s1).decode("utf-8", "replace")
                fin = requests.utils.unquote(s1)
                if not Spider._looks_html(fin):
                    try:
                        fin = requests.utils.unquote(
                            base64.b64decode(fin).decode("utf-8", "replace"))
                    except Exception:
                        pass
                return fin if Spider._looks_html(fin) else html
        except Exception:
            pass
        return html
    @staticmethod
    def _unpack_packer(html):
        try:
            m = re.search(r"eval\(function\(p,a,c,k,e,d\)\{.*?\}\("
                          r"['\"](.*?)['\"],(\d+),(\d+),['\"](.*?)['\"]\.split\(['\"]\|['\"]\)",
                          html, re.S)
            if not m:
                return ""
            payload, radix, cnt, keys = m.group(1), int(m.group(2)), int(m.group(3)),                 m.group(4).split("|")
            if len(keys) < cnt:
                return ""

            def _enc(num, base):
                out = ""
                while True:
                    out = ("0123456789abcdefghijklmnopqrstuvwxyz"[num % base]) + out
                    num //= base
                    if not num:
                        return out

            un = { _enc(i, radix): keys[i] for i in range(cnt) if i < len(keys) }
            def _sub(mo):
                w = mo.group(0)
                if w.isdigit():
                    return un.get(w, w)
                return un.get(w[1:], "") + w[0] if w[0] == "." and w[1:] in un else w
            text = re.sub(r"\b\w+\b", _sub, payload)
            text = text.replace("\\/", "/").replace("\\\\", "\\")
            return text
        except Exception:
            return ""

    @staticmethod
    def _decode_compressed(value):
        try:
            raw = base64.b64decode(value + "=" * (-len(value) % 4))
            data = zlib.decompressobj(-15).decompress(raw)
            return json.loads(data.decode("utf-8", "replace"))
        except Exception:
            return {}

    @staticmethod
    def _media_from_text(text):
        if not text:
            return ""
        m = re.search(r'"(?:videoSrc|hlsUrl|playUrl|play_url|video_url|url|m3u8)"'
                      r'\s*:\s*"(https?://[^"]+\.(?:m3u8|mp4|flv|mkv)[^"]*)"', text, re.I)
        if not m:
            m = re.search(r'"(https?://[^"\']+?\.(?:m3u8|mp4|flv|mkv)[^"\']*)"', text)
        if m:
            return m.group(1).replace("\\/", "/")
        return ""

    def _extract_play(self, html):
        if not html:
            return ""
        if "document.write" in html[:2000] and "<div" not in html and "<video" not in html:
            dec = Spider._decode_page(html)
            if dec is not html:
                html = dec
        m_mac = re.search(r"mac_url\s*=\s*unescape\('([^']*)'\)", html)
        if not m_mac:
            m_mac = re.search(r"mac_url\s*=\s*'([^']*)'", html)
        if m_mac:
            val = Spider._js_unescape(m_mac.group(1))
            for chunk in val.split("#"):
                parts = [p.strip() for p in chunk.split("$") if p.strip()]
                for p in reversed(parts):
                    if p.startswith("http") or any(
                            t in p for t in (".m3u8", ".mp4", ".flv", ".mkv")):
                        return p
        raw = Spider._extract_balanced(html, "player_aaaa=") \
            or Spider._extract_balanced(html, "player_data=")
        if not raw:
            dec = html_lib.unescape(html).replace("\\/", "/")
            raw = Spider._extract_balanced(dec, "player_aaaa=") \
                or Spider._extract_balanced(dec, '"player_aaaa":')
        if raw:
            try:
                data = json.loads(raw)
            except Exception:
                data = None
            if data:
                url = data.get("url", "") or ""
                enc = str(data.get("encrypt", 0))
                if enc == "1":
                    url = requests.utils.unquote(url)
                elif enc == "2":
                    try:
                        url = base64.b64decode(url).decode("utf-8", "ignore")
                    except Exception:
                        pass
                if url.startswith("http"):
                    return url
        for kv in re.findall(r'(?:play_data|player_data|playData|playerData)'
                             r'["\'=\s:]+["\']([A-Za-z0-9+/=]{80,})["\']', html):
            obj = Spider._decode_compressed(kv)
            if isinstance(obj, dict):
                got = Spider._media_from_text(json.dumps(obj, ensure_ascii=False))
                if got:
                    return got
        up = Spider._unpack_packer(html)
        if up:
            got = Spider._media_from_text(up)
            if got:
                return got
        m = re.search(r'<source[^>]+src="([^"]+\.(?:m3u8|mp4|flv|mkv)[^"]*)"', html, re.I)
        if not m:
            m = re.search(r'og:video"\s*content="([^"]+)"', html, re.I)
        if not m:
            m = re.search(r'"(https?://[^"\']+?\.(?:m3u8|mp4|flv|mkv)[^"\']*)"', html)
        if m:
            return m.group(1).replace("\\/", "/")
        mi = re.search(r'<iframe[^>]+src="((?:https?:)?//[^"\']+)"', html, re.I)
        if mi:
            u = mi.group(1).replace("\\/", "/")
            u = "https:" + u if u.startswith("//") else u
            try:
                ih = self._get(u)
            except Exception:
                ih = ""
            if ih:
                got = Spider._media_from_text(ih)
                if got:
                    return got
                mi2 = re.search(r'<iframe[^>]+src="((?:https?:)?//[^"\']+)"', ih, re.I)
                if mi2:
                    u2 = mi2.group(1).replace("\\/", "/")
                    u2 = "https:" + u2 if u2.startswith("//") else u2
                    ih2 = self._get(u2)
                    if ih2:
                        got = Spider._media_from_text(ih2)
                        if got:
                            return got
            return u
        return ""

    def _play_fallback_vodplay(self, vid):
        first = self._get(f"{self.base_url}/vodplay/{vid}-1-1.html")
        if not first or "player_aaaa" not in first:
            return {}, {}
        side = {}
        for m in re.finditer(r"/(?:vodplay|v_play|vplay)/(\d+)-(\d+)-(\d+)\.html", first):
            _v, sid, nid = m.groups()
            side.setdefault(sid, set()).add(nid)
        if not side:
            return {}, {}
        groups, names = {}, {}
        for sid in sorted(side, key=lambda x: int(x)):
            page = first if sid == "1" else \
                self._get(f"{self.base_url}/vodplay/{vid}-{sid}-1.html")
            if not page:
                continue
            fm = re.search(r'"from":"([^"]*)"', page)
            if fm and fm.group(1):
                names[sid] = fm.group(1)
            nids = set()
            for m in re.finditer(r"/(?:vodplay|v_play|vplay)/\d+-"
                                 + re.escape(sid) + r"-(\d+)\.html", page):
                nids.add(m.group(1))
            if not nids:
                nids = side.get(sid, set())
            single = len(nids) == 1
            eps = {}
            for nid in sorted(nids, key=lambda x: int(x)):
                epname = "正片" if single else ("第%s集" % nid)
                eps[nid] = (epname, f"{self.base_url}/vodplay/{vid}-{sid}-{nid}.html")
            if eps:
                groups[sid] = eps
        return groups, names

    def playerContent(self, flag, id, vipFlags=None):
        try:
            play_url = id
            if play_url and self.isVideoFormat(play_url):
                return {"parse": 0, "url": play_url,
                        "header": {"User-Agent": self.headers["User-Agent"],
                                   "Referer": self.base_url + "/"}}
            if re.search(r"//[^/]+/(?:share|s|file|disk)/[0-9a-zA-Z]{8,}",
                         str(play_url or "")):
                return {"parse": 1, "url": play_url,
                        "header": {"User-Agent": self.headers["User-Agent"]}}
            m_ref = re.match(r"^(.+)-(\d+)-(\d+)$", str(play_url or ""))
            if m_ref:
                vid, sid, nid = m_ref.groups()
                dyn = (f"{self.base_url}{self.prefix}"
                       f"/vod/play/id/{vid}/sid/{sid}/nid/{nid}.html")
                fei = f"{self.base_url}/vodplay/{vid}-{sid}-{nid}.html"
                sea = f"{self.base_url}/v_play/{vid}-{sid}-{nid}.html"
                if self.detail_route == "voddetail":
                    cands = [fei, dyn, sea]
                elif self.detail_route == "seacms":
                    cands = [sea, dyn, fei]
                else:
                    cands = [dyn, fei, sea]
                html = ""
                got_url = ""
                for u in cands:
                    got = self._get(u)
                    if got:
                        html = got
                        got_url = u
                        if "player_aaaa" in got:
                            break
                if not html:
                    return {"parse": 1, "url": cands[0],
                            "header": self._webview_header()}
                real = self._extract_play(html)
                if not real:
                    return {"parse": 1, "url": got_url or cands[0],
                        "header": self._webview_header()}
                direct = any(t in real for t in (".m3u8", ".mp4", ".flv", ".mkv"))
                return {
                    "parse": 0 if direct else 1,
                    "url": real,
                    "header": {"User-Agent": self.headers["User-Agent"],
                               "Referer": self.base_url + "/"},
                }

            if not str(play_url).startswith("http"):
                if str(play_url).startswith("/"):
                    play_url = self.base_url + play_url
                else:
                    return {"parse": 1, "url": self.base_url + "/",
                            "header": self._webview_header()}

            html = self._get(play_url)
            real = self._extract_play(html)
            if not real and html:
                m_eq = re.search(r"/(?:vplay|vodplay|v_play)/(\d+)-(\d+)-(\d+)\.html",
                                 str(play_url))
                if m_eq:
                    vid, sid, nid = m_eq.groups()
                    alts = [
                        f"{self.base_url}{self.prefix}"
                        f"/vod/play/id/{vid}/sid/{sid}/nid/{nid}.html",
                        f"{self.base_url}/vodplay/{vid}-{sid}-{nid}.html",
                        f"{self.base_url}/v_play/{vid}-{sid}-{nid}.html",
                    ]
                    for u2 in alts:
                        if u2 == str(play_url):
                            continue
                        real = self._extract_play(self._get(u2))
                        if real:
                            break
            if not real:
                return {"parse": 1, "url": play_url,
                        "header": self._webview_header()}
            direct = any(t in real for t in (".m3u8", ".mp4", ".flv", ".mkv"))
            return {
                "parse": 0 if direct else 1,
                "url": real,
                "header": {"User-Agent": self.headers["User-Agent"],
                           "Referer": self.base_url + "/"},
            }
        except Exception as e:
            print(f"[{self.name}] 播放解析异常: {e}")
            return {"parse": 1, "url": self.base_url + "/",
                    "header": self._webview_header()}

    def isVideoFormat(self, url):
        return any(t in url for t in (".m3u8", ".mp4", ".flv", ".mkv"))

    def manualVideoCheck(self):
        return False

    def destroy(self):
        pass

    def localProxy(self, param):
        return None


import requests as _rq
from urllib.parse import urlparse as _up


def _pow_params(text):
    if not text:
        return None
    if not ("正在验证您的浏览器" in text or "__cdn_pow" in text):
        return None
    import re as _re
    m = _re.search(r'var\s+TS\s*=\s*"([^"]+)"\s*,\s*SIG\s*=\s*"([^"]+)"\s*,'
                   r'\s*DIFF\s*=\s*"([^"]+)"\s*(?:,\s*MODE\s*=\s*"([^"]*)")?',
                   text)
    if not m:
        return None
    mc = _re.search(r'var\s+POW\s*=\s*"([^"]+)"', text)
    return {"ts": m.group(1), "sig": m.group(2),
            "diff": m.group(3) or "0000", "mode": m.group(4) or "auto",
            "cookie": mc.group(1) if mc else "__cdn_pow"}


def _pow_solve(sig, diff, mx=4000000):
    import hashlib as _hl
    import time as _t
    t0 = _t.time()
    n = 0
    while n < mx:
        if _hl.sha256((sig + str(n)).encode()).hexdigest().startswith(diff):
            return n
        n += 1
        if n % 50000 == 0 and _t.time() - t0 > 8:
            return None
    return None


try:
    class _PowSession(_rq.Session):

        def request(self, method, url, *a, **kw):
            r = _rq.Session.request(self, method, url, *a, **kw)
            try:
                txt = r.text or ""
            except Exception:
                return r
            for _i in range(2):
                p = _pow_params(txt)
                if not p:
                    break
                n = _pow_solve(p["sig"], p["diff"])
                if n is None:
                    break
                self.cookies.set(p["cookie"],
                                 "%s_%s_%s_%s" % (p["ts"], p["mode"], n, p["sig"]),
                                 domain=_up(url).netloc, path="/")
                r = _rq.Session.request(self, method, url, *a, **kw)
                try:
                    txt = r.text or ""
                except Exception:
                    break
            return r
except Exception:
    _PowSession = _rq.Session