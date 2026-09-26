

import sys
import os
import re
import json
import math
import random
import socket
import threading
import urllib.error
import urllib.parse
import urllib.request


try:
    import tkinter as tk
    TKINTER_MEVCUT = True
except ImportError:
    tk = None
    TKINTER_MEVCUT = False



EGITIM_VERISI = [
    ("ileri git", "hedefli_hareket"),
    ("ileriye git", "hedefli_hareket"),
    ("ileriye 5 metre git", "hedefli_hareket"),
    ("ileri 2 metre", "hedefli_hareket"),
    ("düz git", "hedefli_hareket"),
    ("düz ilerle", "hedefli_hareket"),
    ("öne git", "hedefli_hareket"),
    ("öne doğru git", "hedefli_hareket"),
    ("git ileri", "hedefli_hareket"),
    ("ilerle", "hedefli_hareket"),
    ("yürü", "hedefli_hareket"),
    ("go forward", "hedefli_hareket"),
    ("move forward two meters", "hedefli_hareket"),
    ("sağa git", "hedefli_hareket"),
    ("sağa dön", "hedefli_hareket"),
    ("sağa doğru dön", "hedefli_hareket"),
    ("sağa 90 derece dön", "hedefli_hareket"),
    ("90 derece sağa dön", "hedefli_hareket"),
    ("yerinde sağa dön", "hedefli_hareket"),
    ("çeyrek tur sağa", "hedefli_hareket"),
    ("sağa 3 metre ilerle", "hedefli_hareket"),
    ("sağ tarafa 4 metre git", "hedefli_hareket"),
    ("sağa 5 metre sür", "hedefli_hareket"),
    ("turn right", "hedefli_hareket"),
    ("rotate right 45 degrees", "hedefli_hareket"),
    ("sola git", "hedefli_hareket"),
    ("sola dön", "hedefli_hareket"),
    ("sola doğru dön", "hedefli_hareket"),
    ("sola 90 derece dön", "hedefli_hareket"),
    ("sola 3 metre ilerle", "hedefli_hareket"),
    ("sol tarafa git", "hedefli_hareket"),
    ("2 metre sola git", "hedefli_hareket"),
    ("turn left", "hedefli_hareket"),
    ("geri git", "hedefli_hareket"),
    ("gerile", "hedefli_hareket"),
    ("geri çekil", "hedefli_hareket"),
    ("geri 1 metre", "hedefli_hareket"),
    ("geriye doğru yürü", "hedefli_hareket"),
    ("arkaya dön", "hedefli_hareket"),
    ("180 derece dön", "hedefli_hareket"),
    ("yarım tur dön", "hedefli_hareket"),
    ("tam tur dön", "hedefli_hareket"),
    ("yerinde dön", "hedefli_hareket"),
    ("dön", "hedefli_hareket"),
    ("dön dolaş", "rastgele_gezinme"),
    ("buralarda turla", "rastgele_gezinme"),
    ("etrafta gez", "rastgele_gezinme"),
    ("tur at", "rastgele_gezinme"),
    ("keşfet", "rastgele_gezinme"),
    ("etrafı keşfet", "rastgele_gezinme"),
    ("random gez", "rastgele_gezinme"),
    ("serbest dolaş", "rastgele_gezinme"),
    ("dolaş etrafta", "rastgele_gezinme"),
    ("boş boş gez", "rastgele_gezinme"),
    ("keşfe çık", "rastgele_gezinme"),
    ("serbest dolaşım", "rastgele_gezinme"),
    ("ortalıkta dolaş", "rastgele_gezinme"),
    ("otonom gez", "rastgele_gezinme"),
    ("wander around", "rastgele_gezinme"),
    ("explore the area", "rastgele_gezinme"),
]

# Yerleşik eşanlam / yabancı dil sözlüğü (internetsiz de çalışır)
YERLESİK_ESANLAM = {
    "right": "sağ", "left": "sol", "forward": "ileri", "back": "geri",
    "backward": "geri", "backwards": "geri", "ahead": "ileri",
    "straight": "ileri", "turn": "dön", "rotate": "dön", "spin": "dön",
    "go": "git", "move": "git", "walk": "yürü", "drive": "sür",
    "meter": "metre", "meters": "metre", "metre": "metre",
    "degree": "derece", "degrees": "derece",
    "starboard": "sağ", "port": "sol", "astern": "geri",
    "clockwise": "sağ dön", "counterclockwise": "sol dön",
    "anticlockwise": "sol dön",
    "wander": "dolaş", "explore": "keşfet", "patrol": "dolaş",
    "roam": "dolaş", "cruise": "dolaş",
    "ilerle": "ileri git", "yürü": "ileri git", "sür": "git",
    "ilerleyiş": "ileri", "ilerleme": "ileri git",
    "sağ taraf": "sağ", "sol taraf": "sol",
    "arkaya": "geri", "arkaya doğru": "geri", "geriye": "geri",
    "önüne": "ileri", "öne": "ileri", "düz": "ileri", "duz": "ileri",
    "çevir": "dön", "cevir": "dön", "döndür": "dön",
    "çeyrek": "90 derece", "ceyrek": "90 derece",
}

SAYI_KELIME = {
    "yarım": 0.5, "bucuk": 0.5, "buçuk": 0.5, "sıfır": 0, "sifir": 0,
    "bir": 1, "iki": 2, "üç": 3, "uc": 3, "dört": 4, "dort": 4,
    "beş": 5, "bes": 5, "altı": 6, "alti": 6, "yedi": 7, "sekiz": 8,
    "dokuz": 9, "on": 10, "on beş": 15, "onbes": 15, "onbeş": 15,
    "yirmi": 20, "otuz": 30, "kırk": 40, "kirk": 40, "elli": 50,
    "altmış": 60, "altmis": 60, "yetmiş": 70, "yetmis": 70,
    "seksen": 80, "doksan": 90, "yüz": 100, "yuz": 100,
}

DURDURMA = {
    "ve", "ile", "bir", "bu", "şu", "o", "da", "de", "mi", "mı",
    "mu", "mü", "the", "a", "an", "to", "for", "of", "in", "on",
    "at", "please", "lütfen", "lutfen", "robot", "pioneer",
}

GEZINME_DESEN = re.compile(
    r"dolaş|dolan|turla|tur\s*at|keşfet|kesfet|keşfe|kesfe|"
    r"serbest\s+dolaş|random\s+gez|otonom|ortalıkta|"
    r"buralarda|etrafta|etrafı|etrafi|wander|explore|patrol|roam",
    re.IGNORECASE,
)
DONUS_DESEN = re.compile(
    r"dön|don|dönme|donme|çevir|cevir|döndür|dondur|rotate|spin|\bturn\b",
    re.IGNORECASE,
)
YON_DESEN = re.compile(
    r"(sağa|saga|sola|ileriye|öne|one|geriye|arkaya|"
    r"sağ|sag|sol|ileri|geri|düz|duz|right|left|forward|"
    r"backwards|backward|back|starboard|port|astern)",
    re.IGNORECASE,
)


def _kucuk(metin):
    return (metin or "").strip().lower().replace("â", "a").replace("î", "i")


def _paket_yaz(adim):
    """(eylem, yon, mesafe, ilerle, aci_derece|None) -> protokol satırı."""
    e, y, m, il = adim[0], adim[1], adim[2], adim[3]
    aci = adim[4] if len(adim) > 4 else None
    taban = "%s,%s,%.3f,%s" % (e, y, m, "1" if il else "0")
    if aci is None:
        return taban
    return "%s,%.2f" % (taban, float(aci))


def _paket_oku(parcalar):
    e = parcalar[0].strip() if parcalar else "hedefli_hareket"
    y = parcalar[1].strip() if len(parcalar) > 1 else "ileri"
    try:
        m = float(parcalar[2].strip())
    except (ValueError, IndexError, AttributeError):
        m = 1.0
    il = (len(parcalar) > 3 and str(parcalar[3]).strip() == "1")
    aci = None
    if len(parcalar) > 4:
        try:
            aci = float(str(parcalar[4]).strip())
        except (ValueError, TypeError):
            aci = None
    return e, y, m, il, aci


LLM_SISTEM = (
    "Sen bir Pioneer 3-DX gezgin robotun komut planlayıcısısın. "
    "Kullanıcı Türkçe veya İngilizce, kısa ya da karmaşık cümle yazabilir. "
    "Sadece JSON döndür, başka yazı yazma. Şema:\n"
    '{"niyet":"hedefli_hareket|rastgele_gezinme|lidar_tara|dur",'
    '"adimlar":[{"eylem":"don|git|tara|gez|dur","yon":"ileri|geri|sag|sol",'
    '"metre":0,"aci":90}]}\n'
    "Kurallar: sağa/sola dön = eylem don, aci yoksa 90. "
    "geri dön = don yon sag aci 180. tam tur = 360. "
    "sağa X metre git = önce don sag 90 sonra git ileri X. "
    "Lidar/tara/nesne/etrafı tarama = tara. "
    "dolaş/keşfet/tur at = gez. dur/stop = dur. "
    "Birden fazla istek varsa adımları sırayla yaz."
)


class LlmYorumcu:
    """Ollama veya OpenAI uyumlu büyük dil modeli. Yoksa None döner."""

    def __init__(self):
        self.kaynak = None
        self.model = (
            os.environ.get("LLM_MODEL")
            or os.environ.get("OLLAMA_MODEL")
            or ""
        )
        self._openai_key = (
            os.environ.get("OPENAI_API_KEY")
            or os.environ.get("GROQ_API_KEY")
            or ""
        )
        self._openai_url = os.environ.get(
            "OPENAI_BASE_URL",
            "https://api.openai.com/v1" if os.environ.get("OPENAI_API_KEY")
            else "https://api.groq.com/openai/v1",
        )
        self._ollama = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
        self._kesfet()

    def _kesfet(self):
        if self._openai_key:
            if not self.model:
                self.model = os.environ.get(
                    "LLM_MODEL",
                    "llama-3.3-70b-versatile" if "groq" in self._openai_url
                    else "gpt-4o-mini",
                )
            self.kaynak = "openai-uyumlu"
            return
        try:
            ham = self._http(self._ollama.rstrip("/") + "/api/tags",
                             metod="GET", zaman=1.2)
            modeller = [m.get("name") for m in (ham.get("models") or [])
                        if m.get("name")]
            if modeller:
                if self.model and self.model in modeller:
                    pass
                else:
                    tercih = ("llama3.1", "llama3.2", "llama3", "qwen2.5",
                              "qwen2", "mistral", "gemma2", "phi3")
                    self.model = modeller[0]
                    for p in tercih:
                        for ad in modeller:
                            if p in ad.lower():
                                self.model = ad
                                break
                self.kaynak = "ollama"
        except Exception:
            self.kaynak = None

    def aciklama(self):
        if self.kaynak == "ollama":
            return "LLM: Ollama (%s)" % self.model
        if self.kaynak == "openai-uyumlu":
            return "LLM: API (%s)" % self.model
        return ("LLM yok — Ollama kur (ollama pull llama3.1) veya "
                "OPENAI_API_KEY / GROQ_API_KEY ver")

    def coz(self, metin):
        if not self.kaynak:
            return None
        try:
            ham = self._iste(metin)
        except Exception:
            return None
        if not ham:
            return None
        return self._json_ayikla(ham)

    def _iste(self, metin):
        if self.kaynak == "ollama":
            url = self._ollama.rstrip("/") + "/api/chat"
            govde = {
                "model": self.model,
                "stream": False,
                "format": "json",
                "messages": [
                    {"role": "system", "content": LLM_SISTEM},
                    {"role": "user", "content": metin},
                ],
            }
            veri = self._http(url, govde, zaman=25)
            return ((veri.get("message") or {}).get("content") or "")
        url = self._openai_url.rstrip("/") + "/chat/completions"
        govde = {
            "model": self.model,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": LLM_SISTEM},
                {"role": "user", "content": metin},
            ],
        }
        veri = self._http(
            url, govde, zaman=25,
            basliklar={"Authorization": "Bearer " + self._openai_key},
        )
        sec = (veri.get("choices") or [{}])[0]
        return ((sec.get("message") or {}).get("content") or "")

    def _http(self, url, govde=None, metod=None, zaman=8, basliklar=None):
        hdr = {"Content-Type": "application/json", "User-Agent": "PioneerLLM/2.0"}
        if basliklar:
            hdr.update(basliklar)
        data = None if govde is None else json.dumps(govde).encode("utf-8")
        istek = urllib.request.Request(
            url, data=data, headers=hdr,
            method=metod or ("POST" if data else "GET"),
        )
        with urllib.request.urlopen(istek, timeout=zaman) as yanit:
            return json.loads(yanit.read().decode("utf-8", "replace"))

    def _json_ayikla(self, ham):
        metin = ham.strip()
        es = re.search(r"\{.*\}", metin, re.DOTALL)
        if not es:
            return None
        try:
            veri = json.loads(es.group(0))
        except json.JSONDecodeError:
            return None
        adimlar = []
        for a in veri.get("adimlar") or []:
            if not isinstance(a, dict):
                continue
            ey = _kucuk(str(a.get("eylem") or ""))
            yon = _kucuk(str(a.get("yon") or "ileri"))
            if yon in ("sağ", "saga", "sağa", "right"):
                yon = "sag"
            elif yon in ("sola", "left"):
                yon = "sol"
            elif yon in ("back", "arka", "geriye"):
                yon = "geri"
            elif yon not in ("ileri", "geri", "sag", "sol"):
                yon = "ileri"
            try:
                metre = float(a.get("metre") if a.get("metre") is not None else 0)
            except (TypeError, ValueError):
                metre = 0.0
            try:
                aci = a.get("aci")
                aci = None if aci is None else float(aci)
            except (TypeError, ValueError):
                aci = None
            if ey in ("tara", "lidar", "tarama", "lidar_tara", "scan"):
                adimlar.append(("lidar_tara", "-", 0.0, False, None))
            elif ey in ("gez", "dolas", "dolaş", "wander", "rastgele"):
                adimlar.append(("rastgele_gezinme", "-", 0.0, False, None))
            elif ey in ("dur", "stop", "bekle"):
                adimlar.append(("dur", "-", 0.0, False, None))
            elif ey in ("don", "dön", "turn", "rotate"):
                if yon == "ileri":
                    yon = "sag"
                adimlar.append(("hedefli_hareket", yon, 0.0, False,
                                90.0 if aci is None else aci))
            else:
                if yon == "geri" and metre <= 0:
                    metre = 1.0
                if yon in ("sag", "sol") and metre > 0:
                    adimlar.append(("hedefli_hareket", yon, metre, True,
                                    90.0 if aci is None else aci))
                else:
                    adimlar.append(("hedefli_hareket", yon,
                                    metre if metre > 0 else 1.0, True, aci))
        niyet = _kucuk(str(veri.get("niyet") or ""))
        if not adimlar:
            if "lidar" in niyet or "tara" in niyet:
                adimlar = [("lidar_tara", "-", 0.0, False, None)]
            elif "gez" in niyet or "rastgele" in niyet:
                adimlar = [("rastgele_gezinme", "-", 0.0, False, None)]
            elif "dur" in niyet:
                adimlar = [("dur", "-", 0.0, False, None)]
        if not adimlar:
            return None
        if adimlar[0][0] == "rastgele_gezinme" and len(adimlar) == 1:
            niyet = "rastgele_gezinme"
        elif adimlar[0][0] == "lidar_tara" and len(adimlar) == 1:
            niyet = "lidar_tara"
        elif adimlar[0][0] == "dur" and len(adimlar) == 1:
            niyet = "dur"
        else:
            niyet = "hedefli_hareket"
        return {
            "ham": "",
            "genis": "",
            "niyet": niyet,
            "adimlar": adimlar,
            "web": [],
            "llm": True,
        }


class AnlamArastirici:
    """Bilinmeyen kelimeleri Wiktionary / Vikipedi özetinden çözer.

    Eğitim setine bağlı kalmamak için tanımı robot sözlüğüne çevirir.
    Ağ yoksa sessizce atlanır; sonuçlar bellekte önbelleğe alınır.
    """

    _UA = "PioneerNLP/1.0 (Webots egitim projesi; dogal dil robot kontrolu)"

    def __init__(self):
        self._onbellek = {}
        self._kilit = threading.Lock()

    def zenginlestir(self, metin):
        """Metni yerleşik eşanlam + internet tanımlarıyla genişletir."""
        notlar = []
        genis = _kucuk(metin)
        for kaynak, hedef in sorted(YERLESİK_ESANLAM.items(),
                                    key=lambda kv: -len(kv[0])):
            if kaynak in genis:
                genis = genis.replace(kaynak, "%s %s" % (kaynak, hedef))

        bilinmeyen = []
        for ham in re.findall(r"[a-zA-ZçğıöşüÇĞİÖŞÜâîû]+", genis):
            kelime = _kucuk(ham)
            if len(kelime) < 3 or kelime in DURDURMA:
                continue
            if kelime in YERLESİK_ESANLAM or kelime in SAYI_KELIME:
                continue
            if re.search(r"sağ|sag|sol|ileri|geri|dön|don|metre|git|"
                         r"gez|dolaş|derece", kelime):
                continue
            bilinmeyen.append(kelime)

        # Tekrarları koru ama en fazla 4 kelime ara (gecikme)
        uniq = []
        for k in bilinmeyen:
            if k not in uniq:
                uniq.append(k)
        for kelime in uniq[:4]:
            tanim, kaynak = self._anlam_bul(kelime)
            if tanim:
                genis += " " + tanim
                notlar.append("%s [%s]: %s" % (kelime, kaynak, tanim[:80]))
        return genis, notlar

    def _anlam_bul(self, kelime):
        with self._kilit:
            if kelime in self._onbellek:
                return self._onbellek[kelime]
        sonuc = ("", "")
        for fn in (self._wiktionary, self._wikipedia):
            try:
                sonuc = fn(kelime)
            except (urllib.error.URLError, urllib.error.HTTPError,
                    TimeoutError, ValueError, OSError, json.JSONDecodeError):
                sonuc = ("", "")
            if sonuc[0]:
                break
        with self._kilit:
            self._onbellek[kelime] = sonuc
        return sonuc

    def _indir(self, url):
        istek = urllib.request.Request(url, headers={"User-Agent": self._UA})
        with urllib.request.urlopen(istek, timeout=3.5) as yanit:
            return yanit.read().decode("utf-8", "replace")

    def _wiktionary(self, kelime):
        q = urllib.parse.quote(kelime)
        for dil in ("tr", "en"):
            url = (
                "https://%s.wiktionary.org/w/api.php?action=query"
                "&format=json&prop=extracts&exintro=1&explaintext=1"
                "&redirects=1&titles=%s" % (dil, q)
            )
            veri = json.loads(self._indir(url))
            sayfalar = (veri.get("query") or {}).get("pages") or {}
            for sayfa in sayfalar.values():
                if int(sayfa.get("pageid") or 0) < 0:
                    continue
                extract = (sayfa.get("extract") or "").strip()
                if extract:
                    return self._tanimi_sadele(extract), "wiktionary-%s" % dil
        return "", ""

    def _wikipedia(self, kelime):
        q = urllib.parse.quote(kelime)
        url = "https://tr.wikipedia.org/api/rest_v1/page/summary/" + q
        veri = json.loads(self._indir(url))
        ozet = (veri.get("extract") or veri.get("description") or "").strip()
        if ozet:
            return self._tanimi_sadele(ozet), "wikipedia-tr"
        return "", ""

    def _tanimi_sadele(self, metin):
        metin = re.sub(r"<[^>]+>", " ", metin)
        metin = re.sub(r"\s+", " ", metin).strip().lower()
        # Tanımdan robotun anlayacağı ipuçlarını öne çıkar
        ipuclari = []
        eslesmeler = [
            (r"sağ|right|starboard", " sağ dön "),
            (r"sol\b|left|port side", " sol dön "),
            (r"ileri|forward|ahead", " ileri git "),
            (r"geri|back(ward)?s?|astern", " geri git "),
            (r"dön|rotate|turn|spin", " dön "),
            (r"dolaş|gez|wander|explore|roam", " dolaş keşfet "),
            (r"metre|meter", " metre "),
            (r"derece|degree", " derece "),
        ]
        for desen, ek in eslesmeler:
            if re.search(desen, metin, re.IGNORECASE):
                ipuclari.append(ek)
        if ipuclari:
            return " ".join(ipuclari) + " " + metin[:180]
        return metin[:220]


class NlpMotor:
    """Kural tabanlı niyet + RegEx slot doldurma + isteğe bağlı sklearn +
    internet anlam araştırması. Eğitim seti tek kaynak değildir."""

    def __init__(self):
        self._model = None
        self.arastirici = AnlamArastirici()
        self.llm = LlmYorumcu()
        self.yontem = "kural + sözlük + internet"
        if self.llm.kaynak:
            self.yontem = self.llm.aciklama() + " + kural yedek"
        self._kur()

    def _kur(self):
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.pipeline import Pipeline
            from sklearn.svm import LinearSVC

            metinler = [metin for metin, _ in EGITIM_VERISI]
            niyetler = [niyet for _, niyet in EGITIM_VERISI]
            self._model = Pipeline([
                ("vektor", TfidfVectorizer(ngram_range=(1, 2))),
                ("sinif", LinearSVC()),
            ])
            self._model.fit(metinler, niyetler)
            self.yontem = ("kural + sözlük + internet + scikit-learn "
                           "(Tfidf + LinearSVC)")
            if self.llm.kaynak:
                self.yontem = self.llm.aciklama() + " + sklearn yedek"
        except ImportError:
            self._model = None

    def cozumle(self, metin):
        """Önce büyük LLM, olmazsa kural/sözlük/sklearn."""
        ham = (metin or "").strip()
        llm_sonuc = self.llm.coz(ham)
        if llm_sonuc:
            llm_sonuc["ham"] = ham
            llm_sonuc["web"] = ["LLM (%s / %s)" % (self.llm.kaynak, self.llm.model)]
            return llm_sonuc

        genis, web_notlar = self.arastirici.zenginlestir(ham)
        niyet = self.niyet(ham, genis)
        if niyet == "rastgele_gezinme":
            adimlar = [("rastgele_gezinme", "-", 0.0, False, None)]
        elif niyet == "lidar_tara":
            adimlar = [("lidar_tara", "-", 0.0, False, None)]
        elif niyet == "dur":
            adimlar = [("dur", "-", 0.0, False, None)]
        else:
            adimlar = self.komutlar(genis if genis else ham)
            if not adimlar:
                adimlar = [("hedefli_hareket", "ileri", 1.0, True, None)]
        return {
            "ham": ham,
            "genis": genis,
            "niyet": niyet,
            "adimlar": adimlar,
            "web": web_notlar + ["yedek ayrıştırıcı (LLM bağlı değil)"],
        }

    def niyet(self, ham, genis=None):
        metin = _kucuk(genis or ham)
        kural = self._kural_niyet(metin)
        if kural is not None:
            return kural
        if self._model is not None:
            try:
                return self._model.predict([metin])[0]
            except Exception:
                pass
        return "hedefli_hareket"

    def _kural_niyet(self, metin):
        if re.search(r"\bdur\b|stop|bekle|fren", metin) and not re.search(
                r"git|dön|ilerle|metre", metin):
            return "dur"
        if re.search(r"lidar|tarama|\btara\b|nesne|engelleri\s*gör|"
                     r"etrafı\s*tara|scan", metin):
            if not re.search(r"dön|metre git|ilerle", metin):
                return "lidar_tara"
        gez = bool(GEZINME_DESEN.search(metin))
        don = bool(DONUS_DESEN.search(metin))
        yon_var = bool(YON_DESEN.search(metin))
        derece = bool(re.search(r"derece|°|çeyrek|ceyrek|yarım tur|yarim tur|"
                                r"tam tur", metin, re.IGNORECASE))
        if don and (yon_var or derece) and not re.search(
                r"dolaş|dolan|gez\b|keşfet|wander", metin):
            return "hedefli_hareket"
        if gez:
            return "rastgele_gezinme"
        if don:
            return "hedefli_hareket"
        return None

    def yon(self, metin):
        eslesme = YON_DESEN.search(metin)
        if not eslesme:
            if re.search(r"clockwise|saat\s*yön", metin, re.IGNORECASE):
                return "sag"
            if re.search(r"counter|anti\s*clockwise|tersi", metin, re.IGNORECASE):
                return "sol"
            return "ileri"
        kelime = eslesme.group(1).lower()
        if any(k in kelime for k in ("sağ", "sag", "right", "starboard")):
            return "sag"
        if any(k in kelime for k in ("sol", "left", "port")):
            return "sol"
        if any(k in kelime for k in ("geri", "back", "arka", "astern")):
            return "geri"
        return "ileri"

    def _sayi_kelime(self, metin):
        t = _kucuk(metin)
        for kelime, deger in sorted(SAYI_KELIME.items(),
                                    key=lambda kv: -len(kv[0])):
            if re.search(r"\b%s\b" % re.escape(kelime), t):
                return float(deger)
        return None

    def mesafe(self, metin, varsayilan=1.0):
        eslesme = re.search(
            r"(\d+(?:[.,]\d+)?)\s*(?:metre|mt|(?<![a-zA-Z])m)\b",
            metin, re.IGNORECASE,
        )
        if eslesme:
            return float(eslesme.group(1).replace(",", "."))
        kelime = self._sayi_kelime(metin)
        if kelime is not None and re.search(r"metre|mt|\bm\b", metin, re.I):
            return kelime
        # Dönüş cümlesindeki derece sayısı mesafe değildir
        if DONUS_DESEN.search(metin) or re.search(r"derece|°", metin):
            return varsayilan
        eslesme = re.search(r"(\d+(?:[.,]\d+)?)", metin)
        if eslesme:
            return float(eslesme.group(1).replace(",", "."))
        if kelime is not None:
            return kelime
        return varsayilan

    def aci_derece(self, metin, yon):
        """Yerinde dönüş açısı (derece). Yoksa yönün varsayılanı."""
        t = _kucuk(metin)
        if re.search(r"tam\s*tur|bir\s*tur|360", t):
            return 360.0
        if re.search(r"yarım\s*tur|yarim\s*tur|180", t):
            return 180.0
        if re.search(r"çeyrek|ceyrek", t):
            return 90.0
        eslesme = re.search(
            r"(\d+(?:[.,]\d+)?)\s*(?:derece|°|deg)",
            metin, re.IGNORECASE,
        )
        if eslesme:
            return float(eslesme.group(1).replace(",", "."))
        kelime = self._sayi_kelime(metin)
        if kelime is not None and re.search(r"derece|°", t):
            return float(kelime)
        if yon == "geri":
            return 180.0
        if yon in ("sag", "sol"):
            return 90.0
        return 90.0

    def _sadece_donus(self, parca):
        t = _kucuk(parca)
        if not DONUS_DESEN.search(t):
            return False
        # "sağa 3 metre dönerek git" gibi: mesafe varsa ilerle
        if re.search(r"metre|mt|\bm\b", t) and not re.search(
                r"derece|°", t):
            return False
        return True

    def komutlar(self, metin):
        """Cümleyi ardışık adımlara böler.

        Her adım (eylem, yon, mesafe, ilerle, aci_derece) beşlisidir.
        """
        mt = metin.strip()
        if not mt:
            return []

        ayirici = re.compile(
            r"\s*(?:ondan\s+sonra|daha\s+sonra|ve\s+sonra|veya\s+da|"
            r"ardından|ardindan|daha|sonra|önce|once|veya|ya\s+da|"
            r"ve|[,.;])\s+",
            re.IGNORECASE,
        )
        parcalar = [p for p in ayirici.split(mt) if p and p.strip()]
        if not parcalar:
            parcalar = [mt]

        adimlar = []
        for parca in parcalar:
            parca = parca.strip(" ,.;")
            if not parca:
                continue
            yon = self.yon(parca)
            if self._sadece_donus(parca):
                aci = self.aci_derece(parca, yon)
                if yon == "ileri" and not YON_DESEN.search(parca):
                    yon = "sag"
                adimlar.append(("hedefli_hareket", yon, 0.0, False, aci))
            else:
                adimlar.append(("hedefli_hareket", yon,
                                self.mesafe(parca), True, None))
        return adimlar


# ============================================================================
# 2) SOKET SUNUCUSU (GUI tarafı, localhost:5555)
# ============================================================================

class RobotSunucusu:
    """Webots denetleyicisini dinleyen, tek istemcili TCP sunucusu.
    Dinleme işlemi daemon bir thread içinde yürütülür; GUI thread'i asla
    bloklanmaz."""

    def __init__(self, host="127.0.0.1", port=5555,
                 baglanti_cb=None, log_cb=None):
        self.host = host
        self.port = port
        self._soket = None          # dinleyen sunucu soketi
        self._istemci = None        # bağlı Webots istemcisi
        self.bagli = False
        self.dur = False
        self._baglanti_cb = baglanti_cb   # bağlantı durumu değişince çağrılır
        self._log_cb = log_cb             # log satırı için geri çağrı

    # -- dış arayüz ---------------------------------------------------------
    def baslat(self):
        """Sunucuyu arka plan thread'inde başlatır."""
        threading.Thread(target=self._dinle, daemon=True).start()

    def kapat(self):
        """Sunucu ve istemci soketlerini kapatır."""
        self.dur = True
        for soket in (self._istemci, self._soket):
            try:
                if soket is not None:
                    soket.close()
            except OSError:
                pass

    def komut_gonder(self, komut):
        """Çözümlenen komutu Webots'a gönderir. Başarılıysa True döner."""
        if self._istemci is None:
            return False
        try:
            self._istemci.sendall((komut + "\n").encode("utf-8"))
            self._log("-> Webots'a gönderildi: " + komut)
            return True
        except OSError:
            self._baglanti_degistir(False)
            return False

    # -- iç yardımcılar ------------------------------------------------------
    def _log(self, mesaj):
        if self._log_cb:
            self._log_cb(mesaj)

    def _baglanti_degistir(self, bagli):
        self.bagli = bagli
        if self._baglanti_cb:
            self._baglanti_cb(bagli)

    def _dinle(self):
        """Ana dinleme döngüsü (daemon thread içinde çalışır)."""
        self._soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._soket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._soket.bind((self.host, self.port))
            self._soket.listen(1)
        except OSError as hata:
            self._log("[HATA] Sunucu başlatılamadı: %s" % hata)
            return
        self._log("Sunucu dinliyor: %s:%d" % (self.host, self.port))

        while not self.dur:
            # Bir istemci bağlantısını kabul et (0.5 sn zaman aşımlı)
            try:
                self._soket.settimeout(0.5)
                istemci, adres = self._soket.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            self._istemci = istemci
            self._baglanti_degistir(True)
            self._log("Webots bağlandı: %s:%d" % adres)

            # Bağlı istemciyi dinle; kopunca tekrar accept döngüsüne dön
            try:
                istemci.settimeout(0.5)
                while not self.dur:
                    try:
                        veri = istemci.recv(1024)
                    except socket.timeout:
                        continue
                    except OSError:
                        break
                    if not veri:
                        break
                    self._log("<- Webots'tan: %s"
                              % veri.decode("utf-8", "replace").strip())
            except OSError:
                pass
            finally:
                if self._istemci is istemci:
                    self._istemci = None
                    self._baglanti_degistir(False)
                try:
                    istemci.close()
                except OSError:
                    pass
                self._log("Webots bağlantısı kesildi.")


# ============================================================================
# 3) TKINTER GRAFİK ARAYÜZÜ
# ============================================================================

class PioneerGUI:
    """Tkinter tabanlı kontrol paneli. NLP analizi ve soket gönderimi arka
    plan thread'lerinde yapılır; arayüz asla donmaz."""

    def __init__(self, kok):
        self.kok = kok
        kok.title("Pioneer 3-DX | NLP Kontrol Paneli")
        kok.configure(bg="#2b2b2b")
        kok.geometry("760x620")
        kok.resizable(False, False)
        kok.protocol("WM_DELETE_WINDOW", self._kapat)

        self.nlp = NlpMotor()
        self.son_komut = ""

        self._arayuz_kur()
        self._log("[AI] NLP motoru: " + self.nlp.yontem)

        # Sunucuyu arka planda (daemon thread) başlat
        self.sunucu = RobotSunucusu(
            baglanti_cb=self._baglanti_cb,
            log_cb=self._log,
        )
        self.sunucu.baslat()

        # Bağlantı durumunu GUI thread'inde periyodik olarak yenile
        self.kok.after(200, self._durum_yenile)

    # -- arayüz kurulumu -----------------------------------------------------
    def _arayuz_kur(self):
        baslik = tk.Label(
            self.kok, text="Pioneer 3-DX | Doğal Dil Kontrol Paneli",
            font=("Segoe UI", 14, "bold"), bg="#2b2b2b", fg="#ffffff")
        baslik.pack(pady=(14, 4))

        aciklama = tk.Label(
            self.kok,
            text='Örn: "tam 90 derece sağa dön", "önce sola dön sonra 2 metre git '
                 'ardından etrafı tara", "dön dolaş"',
            font=("Segoe UI", 9), bg="#2b2b2b", fg="#bbbbbb")
        aciklama.pack()

        # Robot bağlantı durumu etiketi (yeşil = bağlı, kırmızı = değil)
        self.baglanti_etiketi = tk.Label(
            self.kok, text="Webots robotu BALI DEİL",
            font=("Segoe UI", 10, "bold"), bg="#cc3333", fg="white",
            padx=12, pady=6)
        self.baglanti_etiketi.pack(pady=10)

        # Komut girişi ve gönder butonu
        girdi_cubugu = tk.Frame(self.kok, bg="#2b2b2b")
        girdi_cubugu.pack(fill=tk.X, padx=18, pady=4)

        self.girdi = tk.Entry(girdi_cubugu, font=("Segoe UI", 12))
        self.girdi.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.girdi.bind("<Return>", self._gonder)   # Enter tuşu da çalışsın
        self.girdi.focus_set()

        self.gonder_butonu = tk.Button(
            girdi_cubugu, text="GÖNDER", font=("Segoe UI", 11, "bold"),
            bg="#4caf50", fg="white", padx=16, command=self._gonder)
        self.gonder_butonu.pack(side=tk.RIGHT, padx=(8, 0))

        # Son gönderilen komutun paket hali
        self.son_komut_etiketi = tk.Label(
            self.kok, text="Son komut: -", font=("Consolas", 10),
            bg="#1e1e1e", fg="#8bc34a", padx=10, pady=6)
        self.son_komut_etiketi.pack(fill=tk.X, padx=18, pady=4)

        # AI analizi ve bağlantı loglarını gösteren alan
        log_cubugu = tk.Frame(self.kok, bg="#2b2b2b")
        log_cubugu.pack(fill=tk.BOTH, expand=True, padx=18, pady=(4, 12))

        self.log = tk.Text(
            log_cubugu, height=12, font=("Consolas", 9),
            bg="#1e1e1e", fg="#dddddd", state=tk.DISABLED)
        kaydirma = tk.Scrollbar(log_cubugu, command=self.log.yview)
        self.log.configure(yscrollcommand=kaydirma.set)
        kaydirma.pack(side=tk.RIGHT, fill=tk.Y)
        self.log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # -- thread güvenli geri çağrılar (GUI thread'ine aktarım) ---------------
    def _log(self, mesaj):
        """Diğer thread'lerden gelen mesajları GUI thread'ine zamanlar."""
        try:
            self.kok.after(0, self._log_ekle, mesaj)
        except tk.TclError:
            pass

    def _log_ekle(self, mesaj):
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, mesaj + "\n")
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def _baglanti_cb(self, bagli):
        try:
            self.kok.after(0, self._baglanti_etiket, bagli)
        except tk.TclError:
            pass

    def _baglanti_etiket(self, bagli):
        if bagli:
            self.baglanti_etiketi.configure(
                text="Webots robotu BALI", bg="#2e7d32", fg="white")
            self.kok.title("Pioneer 3-DX | NLP Paneli - ROBOT BALI")
        else:
            self.baglanti_etiketi.configure(
                text="Webots robotu BALI DEİL", bg="#cc3333", fg="white")
            self.kok.title("Pioneer 3-DX | NLP Paneli - Robot BALI DEİL")

    def _durum_yenile(self):
        """Sunucu thread'i GUI'ye dokunmadığı için durum burada poll edilir."""
        self._baglanti_etiket(self.sunucu.bagli)
        self.kok.after(200, self._durum_yenile)

    # -- komut gönderme akışı ------------------------------------------------
    def _gonder(self, event=None):
        metin = self.girdi.get().strip()
        if not metin:
            return
        self.girdi.delete(0, tk.END)
        # NLP analizi ve soket gönderimi arka planda çalışır; GUI donmaz
        threading.Thread(target=self._isle_komut, args=(metin,),
                         daemon=True).start()

    def _isle_komut(self, metin):
        """Niyet tahmini + yön/mesafe/açı çıkarımı + paket gönderimi."""
        analiz = self.nlp.cozumle(metin)
        niyet = analiz["niyet"]
        adimlar = analiz["adimlar"] or []

        if (len(adimlar) == 1 and adimlar[0][0] == "rastgele_gezinme") or (
                not adimlar and niyet == "rastgele_gezinme"):
            komut = "rastgele_gezinme,-,0"
        elif not adimlar:
            komut = _paket_yaz(("hedefli_hareket", "ileri", 1.0, True, None))
        elif len(adimlar) == 1:
            komut = _paket_yaz(adimlar[0])
        else:
            komut = "sira:" + ";".join(_paket_yaz(a) for a in adimlar)

        self._log("[AI] Metin  : " + analiz["ham"])
        if analiz["genis"] and analiz["genis"] != _kucuk(analiz["ham"]):
            self._log("[AI] Geniş  : " + analiz["genis"][:220])
        for not_satir in analiz["web"]:
            self._log("[NET] " + not_satir)
        self._log("[AI] Niyet  : " + niyet)
        self._log("[AI] Adım   : " + komut)
        self._log("[AI] Paket  : " + komut)

        self.son_komut = komut
        try:
            self.kok.after(0, self._son_komut_etiketi)
        except tk.TclError:
            pass

        if not self.sunucu.komut_gonder(komut):
            self._log("[HATA] Webots bağlı değil; komut gönderilemedi.")

    def _son_komut_etiketi(self):
        self.son_komut_etiketi.configure(text="Son komut: %s" % self.son_komut)

    def _kapat(self):
        self.sunucu.kapat()
        self.kok.destroy()


# ============================================================================
# 4) WEBOTS DENETLEYİCİ (Pioneer 3-DX)
# ============================================================================

# Pioneer 3-DX fiziksel parametreleri
TEKERLEK_YARICAPI = 0.0975      # tekerlek yarıçapı (metre)
TEKERLEK_ARASI   = 0.381        # aks açıklığı (metre)
MAX_HIZ          = 6.28         # tekerlek max rad/s
V_MAX            = 0.35         # doğrusal hız m/s (kaymasız)
W_MAX            = 0.9          # yerinde dönüş rad/s (~51 deg/s)
YAW_TOL          = math.radians(1.0)
MESAFE_TOL       = 0.03         # metre

ENGEL_MESAFESI   = 0.55
KACMA_GUCU       = 2.5
GEZINME_TABAN_HIZ = 2.2

# Ön sonarların (indeks 0..7; R2025a'da so0..so7, eski sürümlerde ds0..ds7)
# yaklaşık yerleşim açıları (derece; negatif = robotun sol tarafı,
# pozitif = sağ tarafı).
ON_ACILAR = {0: -90, 1: -50, 2: -30, 3: -10, 4: 10, 5: 30, 6: 50, 7: 90}


def _aci_sar(a):
    """Açıyı [-pi, pi] aralığına sarar."""
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def _sinirla(deger, alt, ust):
    """Değeri [alt, ust] aralığına sıkıştırır."""
    return max(alt, min(ust, deger))


def _cihaz_bul(robot, adaylar):
    """Robot üzerinde verilen aday isimlerden ilk var olan cihazı bulur.

    Webots sürümüne göre cihaz adları değişebilir (ör. "left wheel motor" vs
    "left wheel", "ds0" vs "so0"). Hiçbiri yoksa (None, None) döner.
    """
    for ad in adaylar:
        cihaz = robot.getDevice(ad)
        if cihaz is not None:
            return ad, cihaz
    return None, None


class TekerlekOdometri:
    """Klasik diferansiyel sürüş odometrisi (unicycle)."""

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self._l0 = None
        self._r0 = None

    def sifirla_poz(self):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self._l0 = None
        self._r0 = None

    def guncelle(self, sol_enc, sag_enc, yaw_imu=None):
        if self._l0 is None:
            self._l0 = sol_enc
            self._r0 = sag_enc
            if yaw_imu is not None:
                self.theta = yaw_imu
            return
        if any(math.isinf(v) or math.isnan(v) for v in (sol_enc, sag_enc)):
            return
        ds = (sol_enc - self._l0) * TEKERLEK_YARICAPI
        dd = (sag_enc - self._r0) * TEKERLEK_YARICAPI
        self._l0 = sol_enc
        self._r0 = sag_enc
        delta = (ds + dd) / 2.0
        dth = (dd - ds) / TEKERLEK_ARASI
        orta = self.theta + dth / 2.0
        self.x += delta * math.cos(orta)
        self.y += delta * math.sin(orta)
        if yaw_imu is not None and not (math.isnan(yaw_imu) or math.isinf(yaw_imu)):
            self.theta = yaw_imu
        else:
            self.theta = _aci_sar(self.theta + dth)


class HareketKontrolcu:
    """IMU/GPS kapalı döngü + diferansiyel inverse kinematics.

    Dönüş tekerlek yayına değil yaw hatasına bakarak biter (tam 90°).
    İlerleme GPS (yoksa odometri) mesafesi + heading tutma ile gider.
    """

    def __init__(self, sol_teker, sag_teker, sol_encoder, sag_encoder,
                 imu=None, gps=None, gyro=None, dt=0.032):
        self.sol_teker = sol_teker
        self.sag_teker = sag_teker
        self.sol_encoder = sol_encoder
        self.sag_encoder = sag_encoder
        self.imu = imu
        self.gps = gps
        self.gyro = gyro
        self.dt = dt
        self.odo = TekerlekOdometri()
        self.durum = "bekle"
        self._oturma = 0
        self.hedef_yaw = 0.0
        self.tutulan_yaw = 0.0
        self.hedef_mesafe = 0.0
        self.bas_xy = (0.0, 0.0)
        self.don_ilerle = False
        self.sonraki_mesafe = 0.0
        try:
            sol_teker.setAcceleration(8.0)
            sag_teker.setAcceleration(8.0)
        except Exception:
            pass

    def _vw(self, v, w):
        """v (m/s), w (rad/s) -> tekerlek rad/s."""
        v = _sinirla(v, -V_MAX, V_MAX)
        w = _sinirla(w, -W_MAX, W_MAX)
        wr = (v + w * TEKERLEK_ARASI / 2.0) / TEKERLEK_YARICAPI
        wl = (v - w * TEKERLEK_ARASI / 2.0) / TEKERLEK_YARICAPI
        wr = _sinirla(wr, -MAX_HIZ, MAX_HIZ)
        wl = _sinirla(wl, -MAX_HIZ, MAX_HIZ)
        self.sol_teker.setVelocity(wl)
        self.sag_teker.setVelocity(wr)

    def yaw(self):
        if self.imu is not None:
            try:
                rpy = self.imu.getRollPitchYaw()
                if rpy and not math.isnan(rpy[2]):
                    return rpy[2]
            except Exception:
                pass
        return self.odo.theta

    def konum(self):
        if self.gps is not None:
            try:
                g = self.gps.getValues()
                if g and len(g) >= 3 and not math.isnan(g[0]):
                    x, y, z = float(g[0]), float(g[1]), float(g[2])
                    if abs(z) > 0.5 and abs(y) < 0.35:
                        return x, z
                    return x, y
            except Exception:
                pass
        return self.odo.x, self.odo.y

    def durdur(self):
        self._vw(0.0, 0.0)
        self.durum = "bekle"
        self._oturma = 0
        self.don_ilerle = False
        self.sonraki_mesafe = 0.0

    def hedefli_hareket(self, yon, mesafe, ilerle=True, aci_derece=None):
        mesafe = max(0.0, min(float(mesafe), 20.0))
        self.durdur()
        if aci_derece is not None:
            aci = math.radians(max(0.0, min(abs(float(aci_derece)), 720.0)))
        elif yon == "geri":
            aci = math.pi
        elif yon in ("sag", "sol"):
            aci = math.pi / 2.0
        else:
            aci = 0.0

        sadece_don = (not ilerle) or mesafe <= 0.0
        isaret = -1.0 if yon == "sol" else 1.0
        simdi = self.yaw()

        if yon == "ileri" and not sadece_don:
            self._ilerlemeye_basla(mesafe, simdi)
            return
        if yon == "ileri" and sadece_don:
            if aci > math.radians(2):
                self._donmeye_basla(simdi + isaret * aci, 0.0, False)
            return
        if aci <= math.radians(1):
            if ilerle and mesafe > 0:
                self._ilerlemeye_basla(mesafe, simdi)
            return
        self._donmeye_basla(simdi + isaret * aci,
                            mesafe if (ilerle and mesafe > 0) else 0.0,
                            ilerle and mesafe > 0)

    def _donmeye_basla(self, hedef_yaw, sonraki_mesafe, ilerle):
        self.hedef_yaw = hedef_yaw
        self.sonraki_mesafe = sonraki_mesafe
        self.don_ilerle = bool(ilerle)
        self.durum = "don"
        self._oturma = 0

    def _ilerlemeye_basla(self, mesafe, tut_yaw):
        self.hedef_mesafe = max(0.0, mesafe)
        self.tutulan_yaw = tut_yaw
        self.bas_xy = self.konum()
        self.durum = "ilerle"
        self._oturma = 0

    def adim(self):
        yaw_i = None
        if self.imu is not None:
            try:
                yaw_i = self.imu.getRollPitchYaw()[2]
            except Exception:
                yaw_i = None
        self.odo.guncelle(self.sol_encoder.getValue(),
                          self.sag_encoder.getValue(), yaw_i)
        if self.durum == "don":
            self._don_adim()
        elif self.durum == "ilerle":
            self._ilerleme_adim()

    def _don_adim(self):
        hata = _aci_sar(self.hedef_yaw - self.yaw())
        if abs(hata) <= YAW_TOL:
            self._oturma += 1
            self._vw(0.0, 0.0)
            if self._oturma >= 4:
                if self.don_ilerle:
                    self._ilerlemeye_basla(self.sonraki_mesafe, self.hedef_yaw)
                else:
                    self.durdur()
            return
        self._oturma = 0
        w = 2.8 * hata
        if abs(hata) < math.radians(12):
            w = 1.6 * hata
        self._vw(0.0, w)

    def _ilerleme_adim(self):
        x, y = self.konum()
        dx = x - self.bas_xy[0]
        dy = y - self.bas_xy[1]
        katedilen = math.hypot(dx, dy)
        kalan = self.hedef_mesafe - katedilen
        if kalan <= MESAFE_TOL:
            self.durdur()
            return
        hata = _aci_sar(self.tutulan_yaw - self.yaw())
        w = 2.2 * hata
        v = V_MAX
        if kalan < 0.35:
            v = max(0.06, V_MAX * (kalan / 0.35))
        self._vw(v, w)


def _otonom_gezin(sol_teker, sag_teker, on_sonarlar, taban_hiz, sapma,
                  lidar_sektor=None):
    """Braitenberg + isteğe bağlı lidar sektörleri."""
    sol_hiz = taban_hiz
    sag_hiz = taban_hiz

    if lidar_sektor:
        on, sol, sag = lidar_sektor
        if 0.0 < on < 0.7:
            sol_hiz -= 2.0
            sag_hiz -= 2.0
        if 0.0 < sol < 0.8:
            sag_hiz -= 1.6
        if 0.0 < sag < 0.8:
            sol_hiz -= 1.6

    for index, cihaz in on_sonarlar:
        okunan = cihaz.getValue()
        if 0.0 <= okunan < ENGEL_MESAFESI:
            kuvvet = 1.0 - okunan / ENGEL_MESAFESI
            aci = ON_ACILAR.get(index, 0.0)
            if aci < 0:
                sag_hiz -= kuvvet * KACMA_GUCU
            elif aci > 0:
                sol_hiz -= kuvvet * KACMA_GUCU
            else:
                sol_hiz -= kuvvet * 1.0
                sag_hiz -= kuvvet * 1.0

    sol_hiz = _sinirla(sol_hiz - sapma, -MAX_HIZ, MAX_HIZ)
    sag_hiz = _sinirla(sag_hiz + sapma, -MAX_HIZ, MAX_HIZ)
    sol_teker.setVelocity(sol_hiz)
    sag_teker.setVelocity(sag_hiz)


def _lidar_sektorler(lidar):
    if lidar is None:
        return None
    try:
        img = lidar.getRangeImage()
    except Exception:
        return None
    if not img:
        return None
    n = len(img)
    # sol | ön | sağ  — Webots: ilk ışın FOV'un sol ucu
    def _min_aralik(a, b):
        degerler = []
        for i in range(a, b):
            d = img[i % n]
            if d is None:
                continue
            if math.isinf(d) or math.isnan(d) or d <= 0.05:
                continue
            degerler.append(d)
        return min(degerler) if degerler else 99.0

    on = _min_aralik(int(n * 0.42), int(n * 0.58))
    sol = _min_aralik(int(n * 0.70), int(n * 0.95))
    sag = _min_aralik(int(n * 0.05), int(n * 0.30))
    return on, sol, sag


def _lidar_tara_metin(lidar, max_r=10.0):
    """360° taramayı kümeler; GUI'ye insan okur özet döner."""
    if lidar is None:
        return "LIDAR yok (dünya dosyasında lidar eklendi mi?)"
    try:
        img = list(lidar.getRangeImage())
        fov = float(lidar.getFov())
    except Exception as hata:
        return "LIDAR okunamadı: %s" % hata
    n = len(img)
    if n < 8:
        return "LIDAR veri yok"
    kume = []
    aktif = None
    for i, d in enumerate(img):
        gecerli = (d is not None and not math.isinf(d) and not math.isnan(d)
                   and 0.12 < d < max_r * 0.98)
        aci = -fov / 2.0 + (i + 0.5) * fov / n
        if gecerli:
            if aktif is None:
                aktif = [aci, aci, d, d, 1]
            else:
                aktif[1] = aci
                aktif[2] = min(aktif[2], d)
                aktif[3] += d
                aktif[4] += 1
        elif aktif is not None:
            kume.append(aktif)
            aktif = None
    if aktif is not None:
        kume.append(aktif)
    if not kume:
        return "LIDAR: etrafta nesne yok (menzil %.0f m)." % max_r

    def _yon_ad(a):
        d = math.degrees(_aci_sar(a))
        if -30 <= d <= 30:
            return "ön"
        if 30 < d <= 120:
            return "sol"
        if -120 <= d < -30:
            return "sağ"
        return "arka"

    satirlar = ["LIDAR tarama: %d nesne kümesi" % len(kume)]
    kume.sort(key=lambda k: k[2])
    for i, (a0, a1, dmin, dtoplam, adet) in enumerate(kume[:8], 1):
        orta = (a0 + a1) / 2.0
        genislik = abs(math.degrees(_aci_sar(a1 - a0)))
        satirlar.append(
            "  %d) %s  min=%.2fm  orta=%.0f°  genişlik=%.0f°  ışın=%d"
            % (i, _yon_ad(orta), dmin, math.degrees(_aci_sar(orta)),
               genislik, adet)
        )
    return " | ".join(satirlar) if len(satirlar) == 1 else "\n".join(satirlar)


def _sunucuya_baglan(host="127.0.0.1", port=5555):
    """GUI sunucusuna bağlanır; başarısızsa None döner."""
    try:
        istemci = socket.create_connection((host, port), timeout=1.0)
        istemci.setblocking(False)           # recv hiçbir zaman bloklanmasın
        try:
            istemci.sendall(b"hazirim\n")    # GUI'ye "hazır" mesajı gönder
        except OSError:
            pass
        print("[Webots] GUI sunucusuna bağlandı: %s:%d" % (host, port))
        return istemci
    except OSError:
        print("[Webots] GUI sunucusu bulunamadı (%s:%d)." % (host, port))
        return None


def _guiyi_otomatik_baslat():
    """GUI açık değilse kontrol panelini ayrı bir süreç olarak başlatır.

    Böylece sıralama önemli olmaz: Webots başlatıldığında GUI kapalıysa
    panel kendiliğinden açılır; GUI açıksa zaten bağlantı kurulur.
    """
    import subprocess
    script = os.path.abspath(__file__)
    # Konsolsuz (pythonw) tercih edilir, olmazsa python / py / Webots python'u.
    denenecekler = ["pythonw", "pyw", "python", "py", sys.executable]
    for calistirici in denenecekler:
        if not calistirici:
            continue
        try:
            subprocess.Popen([calistirici, script, "gui"])
            return True
        except OSError:
            continue
    return False


def webots_kontrolcu_calistir():
    """Webots simülasyonu içinde çalıştırılan ana denetleyici döngüsü."""
    try:
        from controller import Robot
    except ImportError:
        print("[HATA] 'controller' modülü bulunamadı.")
        print("[HATA] Bu mod yalnızca Webots içinde çalışır. Webots'ta robotun")
        print("[HATA] controller alanına 'yapayzekalpioneer.py' yazın, ya da")
        print("[HATA] GUI modu için:  python yapayzekalpioneer.py gui")
        return

    # DİKKAT: Robot() Webots çalışmazsa (extern controller beklerken) ~50 sn
    # bloklanır. Webots'u açıp simülasyonu çalıştırmadan buraya gelmemelisiniz.
    try:
        robot = Robot()
    except Exception as hata:
        print("[HATA] Robot başlatılamadı: %s" % hata)
        return

    zaman_adimi = 32          # ms cinsinden simülasyon adımı

    # --- tekerlek motorları (velocity kontrol modu) ---
    # Pioneer 3-DX cihaz adları: "left wheel" / "right wheel",
    # konum algılayıcıları "left wheel sensor" / "right wheel sensor".
    _, sol_teker = _cihaz_bul(robot, ["left wheel", "left wheel motor"])
    _, sag_teker = _cihaz_bul(robot, ["right wheel", "right wheel motor"])
    if sol_teker is None or sag_teker is None:
        print("[HATA] Tekerlek motorları bulunamadı.")
        print("[HATA] Webots sürümünüzdeki Pioneer cihaz adlarını kontrol edin:")
        print("[HATA]   left wheel / right wheel")
        return
    sol_teker.setPosition(float("inf"))   # Webots'ta velocity kontrolü için şart
    sag_teker.setPosition(float("inf"))
    sol_teker.setVelocity(0.0)
    sag_teker.setVelocity(0.0)

    # --- tekerlek konum sensörleri (encoder) ---
    _, sol_encoder = _cihaz_bul(robot, ["left wheel sensor"])
    _, sag_encoder = _cihaz_bul(robot, ["right wheel sensor"])
    if sol_encoder is None or sag_encoder is None:
        print("[HATA] Tekerlek konum sensörleri (encoder) bulunamadı.")
        return
    sol_encoder.enable(zaman_adimi)
    sag_encoder.enable(zaman_adimi)

    # --- 16 ultrasonik sonar (R2025a: so0..so15, eski: ds0..ds15) ---
    on_sonarlar = []
    arka_sonarlar = []
    for i in range(16):
        _, cihaz = _cihaz_bul(robot, ["so%d" % i, "ds%d" % i])
        if cihaz is not None:
            cihaz.enable(zaman_adimi)
            (on_sonarlar if i <= 7 else arka_sonarlar).append((i, cihaz))
    if not on_sonarlar:
        print("[HATA] Hiçbir sonar bulunamadı (so0..so15 / ds0..ds15).")
        print("[HATA] Webots sürümünüzdeki sonar adlarını kontrol edin.")
        return
    print("[Webots] Sonar algılandı: %d ön, %d arka"
          % (len(on_sonarlar), len(arka_sonarlar)))

    hareket = HareketKontrolcu(sol_teker, sag_teker, sol_encoder, sag_encoder)
    otonom = False
    sapma = 0.0
    arabellek = b""
    yeniden_baglanma = 0.0
    komut_kuyrugu = []   # "sira:" paketlerinden gelen bekleyen adımlar

    print("[Webots] Pioneer 3-DX kontrolcüsü hazır.")
    print("[Webots] GUI açık değilse kontrol paneli otomatik açılacak...")
    print("[Webots] NOT: Webots simülasyonu durdurulduysa (Pause) robot "
          "hareket etmez; üstteki 'Run' tuşuna basın.")

    # GUI sunucusuna bağlan (istemci modu); açık değilse otomatik başlat
    istemci = _sunucuya_baglan()
    if istemci is None:
        if _guiyi_otomatik_baslat():
            print("[Webots] Kontrol paneli (GUI) otomatik başlatıldı; "
                  "bağlantı kurulmaya çalışılıyor...")
        else:
            print("[Webots] GUI otomatik başlatılamadı; elle açın:")
            print("[Webots]   python yapayzekalpioneer.py gui")

    while robot.step(zaman_adimi) != -1:
        # ---------------------------------------------------------------
        # 1) Soketten gelen verileri BLOKLAMADAN oku
        # ---------------------------------------------------------------
        if istemci is not None:
            try:
                veri = istemci.recv(1024)
            except OSError as hata:
                # WSAEWOULDBLOCK / EAGAIN -> veri yok, döngüye devam
                if getattr(hata, "errno", None) not in (
                        socket.EWOULDBLOCK, socket.EAGAIN):
                    print("[Webots] GUI bağlantı hatası: %s" % hata)
                    try:
                        istemci.close()
                    except OSError:
                        pass
                    istemci = None
            else:
                if veri:
                    arabellek += veri
                else:
                    print("[Webots] GUI bağlantısı kapatıldı.")
                    try:
                        istemci.close()
                    except OSError:
                        pass
                    istemci = None

            # Tamamlanan satırları tek tek işle
            while b"\n" in arabellek:
                satir, arabellek = arabellek.split(b"\n", 1)
                komut = satir.decode("utf-8", "replace").strip()
                if not komut:
                    continue

                print("[Webots] Komut alındı: " + komut)

                # ---------- "sira:" ok adımlı paket ----------
                if komut.startswith("sira:"):
                    komut_kuyrugu = []
                    for alt in komut[5:].split(";"):
                        alt = alt.strip()
                        if not alt:
                            continue
                        _e, y, m, il, aci = _paket_oku(alt.split(","))
                        komut_kuyrugu.append((y, m, il, aci))
                    otonom = False
                    hareket.durdur()
                    continue

                parcalar = komut.split(",")
                eylem = parcalar[0].strip()

                if eylem == "hedefli_hareket":
                    _e, yon, mesafe, ilerle, aci = _paket_oku(parcalar)
                    otonom = False
                    komut_kuyrugu = []
                    hareket.hedefli_hareket(yon, mesafe, ilerle, aci)

                elif eylem == "rastgele_gezinme":
                    hareket.durdur()
                    komut_kuyrugu = []
                    otonom = True

        else:
            # Bağlantı kopmuşsa saniyede bir yeniden bağlanmayı dene
            yeniden_baglanma -= zaman_adimi / 1000.0
            if yeniden_baglanma <= 0.0:
                yeniden_baglanma = 1.0
                istemci = _sunucuya_baglan()

        # ---------------------------------------------------------------
        # 2) Hareket mantığını güncelle
        # ---------------------------------------------------------------
        if otonom:
            # Rastgele gezinme: zaman zaman sapma yönünü değiştir
            if random.random() < 0.02:
                sapma = random.uniform(-1.2, 1.2)
            _otonom_gezin(sol_teker, sag_teker, on_sonarlar,
                          GEZINME_TABAN_HIZ, sapma)
        else:
            hareket.adim()
            # Sıralı komut zinciri: mevcut adım bittiğinde sıradakine geç
            if hareket.durum == "bekle" and komut_kuyrugu:
                y, m, il, aci = komut_kuyrugu.pop(0)
                hareket.hedefli_hareket(y, m, il, aci)

    # Simülasyon sona erdi
    if istemci is not None:
        try:
            istemci.close()
        except OSError:
            pass


# ============================================================================
# 5) GİRİ NOKTASI (GUI / Controller seçimi)
# ============================================================================

def _webots_kontrolcu_import_edilebilir():
    """Webots bizi mi çalıştırıyor? Webots, kendi python'una controller
    modülünü ekler; normal Python'da bu import hızlıca başarısız olur."""
    try:
        import controller
        return True
    except Exception:
        return False


def gui_calistir():
    """Tkinter arayüzünü başlatır."""
    if not TKINTER_MEVCUT or tk is None:
        print("[HATA] tkinter bulunamadı. GUI modu çalıştırılamıyor.")
        return
    print("[GUI] Kontrol paneli başlatılıyor...")
    print("[GUI] Sunucu 127.0.0.1:5555 üzerinde dinlemeye başlayacak.")
    print("[GUI] Webots'ta robotun controller'ı 'yapayzekalpioneer.py' "
          "olmalı ve simülasyon çalıştırılmalı.")
    kok = tk.Tk()
    PioneerGUI(kok)
    kok.mainloop()


def main():
    mod = sys.argv[1].lower() if len(sys.argv) > 1 else ""

    if mod in ("gui", "arayuz"):
        gui_calistir()
    elif mod in ("controller", "robot", "webots"):
        webots_kontrolcu_calistir()
    else:
        # Argümansız çalıştırma:
        #   - Webots içindeysek (controller import edilebiliyorsa) -> controller
        #   - Değilse -> GUI
        # NOT: WEBOTS_HOME bu makinede global tanımlı olduğu için bu değişkene
        # güvenmek yanlış mod seçimine ve donmaya yol açardı; o yüzden
        # controller import'u test ediliyor.
        if _webots_kontrolcu_import_edilebilir():
            webots_kontrolcu_calistir()
        else:
            gui_calistir()


if __name__ == "__main__":
    main()
