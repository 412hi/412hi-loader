import sys
import os
import requests
import random
from datetime import datetime, timedelta

# 1. ÇALIŞMA DİZİNİNİ SABİTLE (Hataları önlemek için en üstte olmalı)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 2. KEYAUTH KÜTÜPHANESİNİ İÇE AKTAR
try:
    from keyauth import api
except ImportError:
    print("HATA: 'keyauth.py' bulunamadı! Lütfen aynı klasörde olduğundan emin olun.")
    sys.exit()

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QStackedWidget,
    QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve,
    QTimer, QPoint, QEvent
)
from PyQt6.QtGui import (
    QColor, QPainter, QPen, QBrush,
    QLinearGradient, QPalette, QPixmap, QIcon
)

print(f"Şu anki dizin: {os.getcwd()}")
print(f"Klasördeki dosyalar: {os.listdir()}")

# KEYAUTH KÜTÜPHANESİ
try:
    from keyauth import api
except ImportError:
    print("HATA: 'keyauth.py' dosyası bulunamadı! Lütfen KeyAuth GitHub'dan indirip aynı klasöre koyun.")
    sys.exit()

# ─────────────────────────────────────────────────────────────
#  KEYAUTH CONFIG (Kendi panelinden alacağın bilgiler)
# ─────────────────────────────────────────────────────────────
keyauthapp = api(
    name = "UYGULAMA_ADINIZ",   # KeyAuth panelindeki Application Name
    ownerid = "OWNER_ID",       # KeyAuth panelindeki Owner ID
    version = "1.0",            # Versiyon
    hash_to_check = None
)

# DEMO BYPASS (Test için)
DEMO_KEY     = "412HI-DEMO*2026"
DEMO_ACCOUNT = {
    "expiry":     (datetime.now() + timedelta(days=27)).strftime("%Y-%m-%d"),
    "days_left":  27,
    "plan":       "Premium",
    "features":   ["Örnek Özellik 1", "Örnek Özellik 2"],
}

TR = {
    "en": {
        "key_placeholder":  "Enter your license key...",
        "validate_btn":     "VALIDATE KEY",
        "invalid_key":      "INVALID KEY — TRY AGAIN",
        "checking":         "CHECKING...",
        "announcements":    "Announcements",
        "ann_text":         "Welcome to 412hi Loader v1.0.",
        "spoofer_menu":     "Products",
        "account_status":   "Account Status",
        "exit":             "EXIT",
        "spoofer_panel":    "Products",
        "coming_soon":      "Coming Soon",
        "expiry_label":     "Expiry Date",
        "days_label":       "Days Remaining",
        "plan_label":       "Plan",
        "features_label":   "Included Features",
        "product_title":    "Product",
        "product_desc":     "Detailed information about this product will be available soon.",
        "window_title":     "412hi Loader",
    },
    "tr": {
        "key_placeholder":  "Lisans anahtarınızı girin...",
        "validate_btn":     "DOĞRULA",
        "invalid_key":      "GEÇERSİZ ANAHTAR — TEKRAR DENEYİN",
        "checking":         "KONTROL EDİLİYOR...",
        "announcements":    "Duyurular",
        "ann_text":         "412hi Loader v.0'a hoş geldiniz.",
        "spoofer_menu":     "Ürünler",
        "account_status":   "Hesap Durumu",
        "exit":             "ÇIKIŞ",
        "spoofer_panel":    "Ürünler",
        "coming_soon":      "Çok Yakında",
        "expiry_label":     "Son Kullanma Tarihi",
        "days_label":       "Kalan Gün",
        "plan_label":       "Plan",
        "features_label":   "Dahil Özellikler",
        "product_title":    "Ürün",
        "product_desc":     "Bu ürün hakkında detaylı bilgi yakında eklenecektir.",
        "window_title":     "412hi Yükleyici",
    }
}

C = {
    "bg":         "#0A0A0F",
    "bg2":        "#111118",
    "bg3":        "#1A1A24",
    "card":       "#16161F",
    "border":     "#2A2A3A",
    "border2":    "#3F3F5A",
    "navy":       "#4A6CFF",
    "navy_light": "#6E8EFF",
    "navy_dark":  "#2E4AD9",
    "accent":     "#00D4FF",
    "white":      "#FFFFFF",
    "text":       "#E0E4FF",
    "text2":      "#A0A8CC",
    "text3":      "#70789E",
    "yellow":     "#FFD740",
    "badge_off":  "#1F2333",
    "error":      "#FF4D6B",
}

BASE_SS = f"""
QWidget {{ background:transparent; color:{C['text']}; font-family:'Segoe UI',Arial,sans-serif; }}
QScrollBar:vertical {{ background:{C['bg2']}; width:5px; border-radius:2px; }}
QScrollBar::handle:vertical {{ background:{C['navy_dark']}; border-radius:2px; min-height:20px; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}
"""

def create_412hi_box(size_font=14, padding="6px 30px"):
    box = QLabel("412hi")
    box.setAlignment(Qt.AlignmentFlag.AlignCenter)
    box.setStyleSheet(f"""
        background: {C['bg3']};
        color: {C['white']};
        border: 1.5px solid {C['navy']};
        border-radius: 6px;
        font-weight: 800;
        font-size: {size_font}px;
        padding: {padding};
        letter-spacing: 3px;
    """)
    return box

# ─────────────────────────────────────────────────────────────
#  AUTH WORKER
# ─────────────────────────────────────────────────────────────
class AuthWorker(QThread):
    result = pyqtSignal(bool, dict)
    
    def __init__(self, key):
        super().__init__()
        self.key = key
        
    def run(self):
        if self.key.strip().upper() == DEMO_KEY:
            self.msleep(900)
            self.result.emit(True, DEMO_ACCOUNT)
            return
            
        try:
            status = keyauthapp.license(self.key)
            if status:
                try:
                    expiry_ts = int(keyauthapp.user_data.expires)
                    expiry_date = datetime.fromtimestamp(expiry_ts)
                    days_left = max(0, (expiry_date - datetime.now()).days)
                    expiry_str = expiry_date.strftime("%Y-%m-%d")
                except:
                    expiry_str = "Unknown"
                    days_left = 0

                user_data = {
                    "expiry": expiry_str,
                    "days_left": days_left,
                    "plan": keyauthapp.user_data.subscription if hasattr(keyauthapp.user_data, 'subscription') else "Default",
                    "features": ["KeyAuth Verified"],
                }
                self.result.emit(True, user_data)
            else:
                self.result.emit(False, {})
        except Exception as e:
            print(f"KeyAuth Hatası: {e}")
            self.result.emit(False, {})

# ─────────────────────────────────────────────────────────────
#  UI BİLEŞENLERİ
# ─────────────────────────────────────────────────────────────
class GlowFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pulse = 0; self._inc = 1
        t = QTimer(self); t.timeout.connect(self._anim); t.start(45)
    def _anim(self):
        self._pulse += self._inc
        if self._pulse >= 50: self._inc = -1
        if self._pulse <= 0:  self._inc =  1
        self.update()
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().adjusted(1,1,-1,-1)
        p.setBrush(QBrush(QColor(C['bg']))); p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(r,14,14)
        p.setPen(QPen(QColor(10, 17, 114, 70+self._pulse*2), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r,14,14); p.end()

class LanguageScreen(QWidget):
    selected = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(30); lay.setContentsMargins(80,80,80,80)
        title = QLabel("SELECT LANGUAGE  /  DİL SEÇİN")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color:{C['text2']}; font-size:11px; letter-spacing:4px; font-weight:600;")
        lay.addWidget(title)
        div = QFrame(); div.setFixedHeight(1)
        div.setStyleSheet(f"background:{C['border2']};"); lay.addWidget(div)
        row = QHBoxLayout(); row.setSpacing(20)
        row.addWidget(self._btn("🇬🇧", "English", "en"))
        row.addWidget(self._btn("🇹🇷", "Türkçe",  "tr"))
        lay.addLayout(row)
    def _btn(self, flag, label, lang):
        b = QPushButton(f"{flag}   {label}")
        b.setFixedSize(170,58)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setStyleSheet(f"""
            QPushButton {{
                background:{C['card']}; color:{C['white']};
                border:1px solid {C['border2']}; border-radius:10px;
                font-size:14px; font-weight:600; letter-spacing:1px;
            }}
            QPushButton:hover {{ background:{C['navy_dark']}; border-color:{C['navy']}; color:{C['white']}; }}
            QPushButton:pressed {{ background:{C['navy']}; color:{C['white']}; }}
        """)
        b.clicked.connect(lambda: self.selected.emit(lang))
        return b

class LoginScreen(QWidget):
    auth_success = pyqtSignal(dict)
    def __init__(self, lang="en"):
        super().__init__()
        self.lang = lang; self.t = TR[lang]; self._worker = None
        self._build()
    def _build(self):
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter); lay.setContentsMargins(0,0,0,0)
        card = GlowFrame(); card.setFixedSize(400,320)
        cl = QVBoxLayout(card)
        cl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cl.setSpacing(16); cl.setContentsMargins(40,30,40,30)
        self.logo_box = create_412hi_box(size_font=18, padding="8px 50px")
        cl.addWidget(self.logo_box)
        dv = QFrame(); dv.setFixedHeight(1)
        dv.setStyleSheet(f"background:{C['border2']};"); cl.addWidget(dv)
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText(self.t["key_placeholder"])
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setFixedHeight(42)
        self.key_input.setStyleSheet(f"""
            QLineEdit {{ background:{C['bg3']}; border:1px solid {C['border2']}; border-radius:8px; padding:0 14px; color:{C['text']}; font-size:13px; letter-spacing:1px; }}
            QLineEdit:focus {{ border-color:{C['navy']}; }}
        """)
        self.key_input.returnPressed.connect(self._validate)
        cl.addWidget(self.key_input)
        self.status_lbl = QLabel("")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_lbl.setFixedHeight(16)
        self.status_lbl.setStyleSheet(f"color:{C['yellow']}; font-size:10px; letter-spacing:2px; font-weight:600;")
        cl.addWidget(self.status_lbl)
        self.validate_btn = QPushButton(self.t["validate_btn"])
        self.validate_btn.setFixedHeight(42)
        self.validate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.validate_btn.setStyleSheet(f"""
            QPushButton {{ background:{C['navy_dark']}; color:{C['white']}; border:1px solid {C['navy']}; border-radius:8px; font-size:12px; font-weight:700; letter-spacing:3px; }}
            QPushButton:hover {{ background:{C['navy']}; color:{C['white']}; border-color:{C['navy_light']}; }}
            QPushButton:pressed {{ background:{C['navy_dark']}; color:{C['text3']}; }}
            QPushButton:disabled {{ background:{C['bg3']}; color:{C['text3']}; border-color:{C['border']}; }}
        """)
        self.validate_btn.clicked.connect(self._validate)
        cl.addWidget(self.validate_btn)
        lay.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        ft = QLabel("412hi.shop")
        ft.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ft.setStyleSheet(f"color:{C['text3']}; font-size:10px; letter-spacing:2px; margin-top:12px;")
        lay.addWidget(ft)
    def _validate(self):
        key = self.key_input.text().strip()
        if not key:
            self._shake(); self.status_lbl.setText(self.t["invalid_key"]); return
        self.validate_btn.setEnabled(False)
        self.validate_btn.setText(self.t["checking"])
        self.status_lbl.setText("")
        self._worker = AuthWorker(key)
        self._worker.result.connect(self._on_result)
        self._worker.start()
    def _on_result(self, ok, data):
        if ok: self.auth_success.emit(data)
        else:
            self.validate_btn.setEnabled(True)
            self.validate_btn.setText(self.t["validate_btn"])
            self.status_lbl.setText(self.t["invalid_key"])
            self._shake()
    def _shake(self):
        inp = self.key_input; orig = inp.pos()
        a = QPropertyAnimation(inp, b"pos"); a.setDuration(280)
        for pct, dx in [(0.0,0),(0.1,-7),(0.3,7),(0.5,-5),(0.7,5),(1.0,0)]:
            a.setKeyValueAt(pct, QPoint(orig.x()+dx, orig.y()))
        a.setEasingCurve(QEasingCurve.Type.Linear)
        a.start(); self._anim = a

class SpooferCard(QWidget):
    def __init__(self, number, title, desc, badges, parent=None):
        super().__init__(parent)
        self.setFixedHeight(128)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._hov = False
        lay = QVBoxLayout(self); lay.setContentsMargins(16,12,16,12); lay.setSpacing(5)
        lay.addWidget(QLabel(f"[ {number:02d} ]", styleSheet=f"color:{C['text3']}; font-size:10px; letter-spacing:1px;"))
        lay.addWidget(QLabel(title, styleSheet=f"color:{C['white']}; font-size:14px; font-weight:700; letter-spacing:1px;"))
        dl = QLabel(desc); dl.setWordWrap(True)
        dl.setStyleSheet(f"color:{C['text2']}; font-size:10px;"); lay.addWidget(dl)
        br = QHBoxLayout(); br.setSpacing(6)
        for text, active in badges:
            b = QLabel(text)
            if active: b.setStyleSheet(f"background:{C['navy_dark']}; color:{C['white']}; border:1px solid {C['navy']}; border-radius:4px; font-size:9px; font-weight:700; padding:2px 7px; letter-spacing:1px;")
            else: b.setStyleSheet(f"background:{C['badge_off']}; color:{C['text3']}; border:1px solid {C['border']}; border-radius:4px; font-size:9px; font-weight:700; padding:2px 7px; letter-spacing:1px;")
            br.addWidget(b)
        br.addStretch(); lay.addLayout(br)
    def enterEvent(self, event): self._hov = True; self.update(); super().enterEvent(event)
    def leaveEvent(self, event): self._hov = False; self.update(); super().leaveEvent(event)
    def paintEvent(self, e):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().adjusted(0,0,-1,-1)
        p.setBrush(QBrush(QColor(C['bg3'] if self._hov else C['card'])))
        p.setPen(QPen(QColor(C['navy'] if self._hov else C['border']), 1))
        p.drawRoundedRect(r,10,10); p.end()

class MainPanel(QWidget):
    def __init__(self, lang, account):
        super().__init__()
        self.lang=lang; self.t=TR[lang]; self.account=account
        self._build()
    def _build(self):
        root = QHBoxLayout(self); root.setContentsMargins(0,0,0,0); root.setSpacing(0)
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background:{C['bg2']};")
        self.stack.addWidget(self._ann_page())
        self.stack.addWidget(self._spoofer_page())
        self.stack.addWidget(self._account_page())
        sidebar_widget = self._sidebar()
        root.addWidget(sidebar_widget)
        sep = QFrame(); sep.setFixedWidth(1); sep.setStyleSheet(f"background:{C['border']};")
        root.addWidget(sep)
        root.addWidget(self.stack, 1)
        self._sel(0)
    def _sidebar(self):
        sb = QWidget(); sb.setFixedWidth(200); sb.setStyleSheet(f"background:{C['bg']};")
        lay = QVBoxLayout(sb); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        lw = QWidget(); lw.setFixedHeight(80)
        ll = QHBoxLayout(lw); ll.setContentsMargins(14,0,14,0)
        logo_sidebar = create_412hi_box(size_font=15, padding="6px 15px")
        ll.addWidget(logo_sidebar); ll.addStretch(); lay.addWidget(lw)
        dv = QFrame(); dv.setFixedHeight(1); dv.setStyleSheet(f"background:{C['border']};")
        lay.addWidget(dv); lay.addSpacing(10)
        self._nav_btns = []
        for label, idx in [(self.t["announcements"], 0), (self.t["spoofer_menu"], 1), (self.t["account_status"],2)]:
            b = QPushButton(label); b.setFixedHeight(42)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setStyleSheet(self._ns(False))
            b.clicked.connect(lambda _, i=idx: self._sel(i))
            lay.addWidget(b); self._nav_btns.append((b, idx))
        lay.addStretch()
        ex = QPushButton(self.t["exit"]); ex.setFixedHeight(50); ex.setFixedWidth(200)
        ex.setCursor(Qt.CursorShape.PointingHandCursor)
        ex.setStyleSheet(f"""
            QPushButton {{ background:transparent; color:{C['text3']}; border:1px solid {C['border']}; border-radius:15px; margin: 5px 20px; font-size:11px; font-weight:700; letter-spacing:3px; }}
            QPushButton:hover {{ background:{C['navy_dark']}; color:{C['white']}; border-color:{C['navy']}; }}
        """)
        ex.clicked.connect(QApplication.instance().quit)
        lay.addWidget(ex)
        return sb
    def _ns(self, active):
        if active: return f"QPushButton {{ background:{C['navy_dark']}; color:{C['white']}; border:none; border-left:3px solid {C['navy']}; text-align:left; padding-left:20px; font-size:13px; font-weight:600; letter-spacing:1px; }}"
        return f"QPushButton {{ background:transparent; color:{C['text2']}; border:none; border-left:3px solid transparent; text-align:left; padding-left:20px; font-size:13px; font-weight:500; letter-spacing:1px; }} QPushButton:hover {{ background:{C['bg3']}; color:{C['text']}; border-left:3px solid {C['border2']}; }}"
    def _sel(self, idx):
        if hasattr(self, 'stack') and self.stack:
            for b, i in self._nav_btns: b.setStyleSheet(self._ns(i==idx))
            self.stack.setCurrentIndex(idx)
    def _hdr(self, text):
        l = QLabel(text)
        l.setStyleSheet(f"color:{C['white']}; font-size:18px; font-weight:700; letter-spacing:2px;")
        return l
    def _div(self):
        d = QFrame(); d.setFixedHeight(1); d.setStyleSheet(f"background:{C['border']};")
        return d
    def _page_base(self):
        page = QWidget(); page.setStyleSheet(f"background:{C['bg2']};")
        lay = QVBoxLayout(page); lay.setContentsMargins(28,24,28,24); lay.setSpacing(14)
        return page, lay
    def _ann_page(self):
        page, lay = self._page_base()
        lay.addWidget(self._hdr(self.t["announcements"])); lay.addWidget(self._div())
        card = QWidget()
        card.setStyleSheet(f"background:{C['card']}; border:1px solid {C['border2']}; border-left:3px solid {C['navy']}; border-radius:8px;")
        cl = QVBoxLayout(card); cl.setContentsMargins(16,14,16,14); cl.setSpacing(8)
        badge = QLabel("   NEW   ")
        badge.setFixedWidth(46)
        badge.setStyleSheet(f"background:{C['navy_dark']}; color:{C['white']}; border:1px solid {C['navy']}; border-radius:4px; font-size:9px; font-weight:700; padding:2px 6px; letter-spacing:1px;")
        cl.addWidget(badge)
        txt = QLabel(self.t["ann_text"]); txt.setWordWrap(True)
        txt.setStyleSheet(f"color:{C['text']}; font-size:13px;"); cl.addWidget(txt)
        lay.addWidget(card); lay.addStretch()
        return page
    def _spoofer_page(self):
        page, lay = self._page_base()
        lay.addWidget(self._hdr(self.t["spoofer_panel"])); lay.addWidget(self._div())
        # Basit ürün kartı - rozet yok, açıklama genel
        cards_data = [
            (1, self.t["product_title"], self.t["product_desc"], []),
        ]
        main_content = QVBoxLayout(); main_content.setSpacing(22); main_content.setContentsMargins(0, 10, 0, 0)
        for num, title, desc, badges in cards_data:
            main_content.addWidget(SpooferCard(num, title, desc, badges))
        coming_box = self._create_coming_soon_banner(); main_content.addWidget(coming_box)
        main_content.addStretch(); lay.addLayout(main_content)
        return page
    def _create_coming_soon_banner(self):
        banner = QWidget(); banner.setFixedHeight(68)
        banner.setStyleSheet(f"QWidget {{ background: {C['card']}; border: 1px dashed {C['navy']}; border-radius: 10px; }}")
        layout = QHBoxLayout(banner); layout.setContentsMargins(24, 0, 24, 0); layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label = QLabel(self.t["coming_soon"])
        text_label.setStyleSheet(f"color: {C['text3']}; font-size: 14px; font-weight: 600; letter-spacing: 1.5px;")
        layout.addWidget(text_label)
        return banner
    def _account_page(self):
        page, lay = self._page_base()
        lay.addWidget(self._hdr(self.t["account_status"])); lay.addWidget(self._div())
        for label, value in [
            (self.t["expiry_label"], self.account.get("expiry", "N/A")),
            (self.t["days_label"],   str(self.account.get("days_left", "N/A"))),
            (self.t["plan_label"],   self.account.get("plan", "N/A")),
        ]:
            w = QWidget(); w.setFixedHeight(52)
            w.setStyleSheet(f"background: {C['card']}; border: 1px solid {C['border']}; border-radius: 10px;")
            rl = QHBoxLayout(w); rl.setContentsMargins(20, 0, 20, 0); rl.setSpacing(12)
            rl.addWidget(QLabel(label, styleSheet=f"color:{C['text2']}; font-size:13px; letter-spacing:1px;"))
            rl.addStretch()
            rl.addWidget(QLabel(value, styleSheet=f"color:{C['white']}; font-size:14px; font-weight:700; letter-spacing:1px;"))
            lay.addWidget(w)
        features_widget = QWidget(); features_widget.setStyleSheet(f"background: {C['card']}; border: 1px solid {C['border']}; border-radius: 10px;")
        fl = QVBoxLayout(features_widget); fl.setContentsMargins(20, 18, 20, 18); fl.setSpacing(8)
        fl.addWidget(QLabel(self.t["features_label"], styleSheet=f"color: {C['text2']}; font-size: 13px; font-weight: 600; letter-spacing: 1px;"))
        # Örnek özellikler
        for feat in self.account.get("features", ["Örnek özellik 1", "Örnek özellik 2"]):
            fl.addWidget(QLabel(f"• {feat}", styleSheet=f"color: {C['text']}; font-size: 12px;"))
        lay.addWidget(features_widget); lay.addStretch()
        return page

class LoaderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("412hi Loader")
        self.setFixedSize(780,500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        sc = QApplication.primaryScreen().geometry()
        self.move((sc.width()-780)//2, (sc.height()-500)//2)
        self._drag_pos = None
        self._setup_ui()
    def _setup_ui(self):
        outer = QWidget(); outer.setObjectName("outer")
        outer.setStyleSheet(f"#outer {{ background:{C['bg']}; border:1px solid {C['border2']}; border-radius:14px; }}")
        self.setCentralWidget(outer)
        ol = QVBoxLayout(outer); ol.setContentsMargins(0,0,0,0)
        ol.addWidget(self._title_bar())
        self.stack = QStackedWidget(); ol.addWidget(self.stack)
        ls = LanguageScreen(); ls.selected.connect(self._on_lang)
        self.stack.addWidget(ls); self.setStyleSheet(BASE_SS)
    def _title_bar(self):
        bar = QWidget(); bar.setFixedHeight(36)
        bar.setStyleSheet(f"background:{C['bg']}; border-bottom:1px solid {C['border']}; border-radius:14px 14px 0 0;")
        l = QHBoxLayout(bar); l.setContentsMargins(14,0,10,0)
        l.addWidget(QLabel("412hi  LOADER", styleSheet=f"color:{C['text3']}; font-size:10px; letter-spacing:4px; font-weight:600;"))
        l.addStretch()
        cb = QPushButton("✕"); cb.setFixedSize(24,24)
        cb.setCursor(Qt.CursorShape.PointingHandCursor)
        cb.setStyleSheet(f"QPushButton {{ background:{C['badge_off']}; color:{C['text3']}; border:1px solid {C['border']}; border-radius:12px; font-size:10px; font-weight:700; }} QPushButton:hover {{ background:{C['navy_dark']}; color:{C['white']}; border-color:{C['navy']}; }}")
        cb.clicked.connect(QApplication.instance().quit)
        l.addWidget(cb)
        bar.mousePressEvent = lambda e: setattr(self,'_drag_pos', e.globalPosition().toPoint()-self.frameGeometry().topLeft() if e.button()==Qt.MouseButton.LeftButton else self._drag_pos)
        bar.mouseMoveEvent = lambda e: self.move(e.globalPosition().toPoint()-self._drag_pos) if self._drag_pos and e.buttons()==Qt.MouseButton.LeftButton else None
        return bar
    def _on_lang(self, lang):
        self.lang = lang
        ls = LoginScreen(lang); ls.auth_success.connect(self._on_auth)
        self.stack.addWidget(ls); self.stack.setCurrentIndex(1)
    def _on_auth(self, account):
        panel = MainPanel(self.lang, account)
        self.stack.addWidget(panel); self.stack.setCurrentIndex(2)
        self.setWindowTitle(TR[self.lang]["window_title"])

# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        pass
    except Exception as e:
        print(f"KeyAuth Sunucusuna Bağlanılamadı! {e}")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window,          QColor(C['bg']))
    pal.setColor(QPalette.ColorRole.WindowText,      QColor(C['text']))
    pal.setColor(QPalette.ColorRole.Base,            QColor(C['bg3']))
    pal.setColor(QPalette.ColorRole.Text,            QColor(C['text']))
    pal.setColor(QPalette.ColorRole.Button,          QColor(C['card']))
    pal.setColor(QPalette.ColorRole.ButtonText,      QColor(C['text']))
    pal.setColor(QPalette.ColorRole.Highlight,       QColor(C['navy']))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor(C['white']))
    app.setPalette(pal)
    win = LoaderWindow(); win.show()
    sys.exit(app.exec())
