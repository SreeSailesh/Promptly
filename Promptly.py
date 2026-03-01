"""
PROMPTLY — Smart Reminder Assistant
Precision Scheduling · Enterprise Reliability
Version 1.0 | Windows 10 / 11 | Python 3.11+
"""
from __future__ import annotations

import base64, heapq, json, os, struct, sys, uuid
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Optional, List, Dict, Literal

from PyQt6.QtCore import Qt, QTimer, QObject, pyqtSignal, QDateTime, QSize
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QAction, QFont, QPen, QBrush, QPainterPath
from PyQt6.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QWidget, QDialog,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTextEdit, QComboBox, QSpinBox, QDateTimeEdit,
    QScrollArea, QFrame, QMessageBox, QGraphicsDropShadowEffect
)

try:
    from windows_toasts import Toast, WindowsToaster
    TOAST_AVAILABLE = True
except ImportError:
    TOAST_AVAILABLE = False


# ══════════════════════════════════════════════════════════════════════
#  EMBEDDED ICON  (replaced by inject script — DO NOT EDIT THIS LINE)
# ══════════════════════════════════════════════════════════════════════
PROMPTLY_ICON_B64 = (
    "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"
)


# ══════════════════════════════════════════════════════════════════════
#  THEME SYSTEM
# ══════════════════════════════════════════════════════════════════════

class Theme:
    DARK = "dark"
    LIGHT = "light"

# ── Dark palette — CSS design tokens (.dark class) ────────────────────
DARK = {
    "bg":           "#000000",   # --background
    "surface":      "#17181C",   # --card
    "surface2":     "#181818",   # --muted
    "surface3":     "#22303C",   # --input
    "border":       "#242628",   # --border
    "border_focus": "#1DA1F2",   # --ring
    "text":         "#E7E9EA",   # --foreground
    "text2":        "#D9D9D9",   # --card-foreground
    "text3":        "#72767A",   # --muted-foreground
    "accent":       "#1C9CF0",   # --primary
    "accent_h":     "#3DB0FA",   # lighter hover
    "accent_p":     "#1580C8",   # pressed
    "success":      "#17BF63",   # --chart-4
    "success_bg":   "#061A0E",
    "warning":      "#F7B928",   # --chart-3
    "warning_bg":   "#1A1200",
    "danger":       "#F4212E",   # --destructive
    "danger_bg":    "#1A0406",
    "purple":       "#B39DDB",
    "purple_bg":    "#120E20",
    "teal":         "#00B87A",   # --chart-2
    "teal_bg":      "#001A10",
    "scrollbar":    "#17181C",
    "scrollthumb":  "#38444D",   # --sidebar-border
    "header_bg":    "#000000",
    "filter_bg":    "#0A0A0A",
    "status_bg":    "#000000",
    "card_hover":   "#1E2024",
    "shadow":       "#000000",
}

# ── Light palette — CSS design tokens (:root) ─────────────────────────
LIGHT = {
    "bg":           "#FFFFFF",   # --background
    "surface":      "#F7F8F8",   # --card
    "surface2":     "#E5E5E6",   # --muted
    "surface3":     "#E3ECF6",   # --accent
    "border":       "#E1EAF0",   # --border
    "border_focus": "#1DA1F2",   # --ring
    "text":         "#0F1419",   # --foreground
    "text2":        "#536471",   # secondary (Twitter gray)
    "text3":        "#8B98A5",   # muted
    "accent":       "#1E9DF1",   # --primary
    "accent_h":     "#1A8CD8",   # hover (slightly darker)
    "accent_p":     "#1670B0",   # pressed
    "success":      "#17BF63",   # --chart-4
    "success_bg":   "#E8F8EF",
    "warning":      "#F7B928",   # --chart-3
    "warning_bg":   "#FEF9E7",
    "danger":       "#F4212E",   # --destructive
    "danger_bg":    "#FEE8E9",
    "purple":       "#7856FF",
    "purple_bg":    "#F0EEFF",
    "teal":         "#00B87A",   # --chart-2
    "teal_bg":      "#E6F9F3",
    "scrollbar":    "#E5E5E6",
    "scrollthumb":  "#1E9DF1",
    "header_bg":    "#FFFFFF",
    "filter_bg":    "#F7F9FA",   # --input
    "status_bg":    "#F7F8F8",
    "card_hover":   "#F7F9FA",
    "shadow":       "#E1EAF0",
}


def make_stylesheet(p: dict) -> str:
    return f"""
/* ════════════════════════════════════════════
   ROOT — all widgets inherit this baseline
   ════════════════════════════════════════════ */
QWidget {{
    background-color: {p["bg"]};
    color: {p["text"]};
    font-family: 'Segoe UI', 'Inter', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
}}

/* Dialogs and top-level windows */
QDialog  {{ background-color: {p["bg"]}; }}

/* Named containers — MUST be explicit so Qt doesn't fall
   through to the OS native white background */
QWidget#form_body   {{ background-color: {p["bg"]}; }}
QWidget#form_footer {{ background-color: {p["header_bg"]}; border-top: 1px solid {p["border"]}; }}
QWidget#header_widget {{ background-color: {p["header_bg"]}; border-bottom: 1px solid {p["border"]}; }}
QWidget#filter_widget {{ background-color: {p["filter_bg"]}; border-bottom: 1px solid {p["border"]}; }}
QWidget#status_bar_widget {{ background-color: {p["status_bg"]}; border-top: 1px solid {p["border"]}; }}

/* ════════════════════════════════
   BUTTONS
   ════════════════════════════════ */
QPushButton {{
    background-color: {p["accent"]};
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 10px 22px;
    font-weight: 700;
    font-size: 13px;
    min-height: 18px;
}}
QPushButton:hover    {{ background-color: {p["accent_h"]}; }}
QPushButton:pressed  {{ background-color: {p["accent_p"]}; }}
QPushButton:disabled {{ background-color: {p["surface3"]}; color: {p["text3"]}; }}

QPushButton#btn_secondary {{
    background-color: {p["surface2"]};
    color: {p["text2"]};
    border: 1.5px solid {p["border"]};
}}
QPushButton#btn_secondary:hover {{
    background-color: {p["surface3"]};
    color: {p["text"]};
    border-color: {p["border_focus"]};
}}

QPushButton#btn_ghost {{
    background: transparent;
    padding: 6px 8px;
    border-radius: 7px;
    font-size: 15px;
    color: {p["text2"]};
    border: none;
}}
QPushButton#btn_ghost:hover {{
    background-color: {p["surface2"]};
    color: {p["text"]};
}}

QPushButton#btn_theme {{
    background-color: {p["surface2"]};
    color: {p["text2"]};
    border: 1.5px solid {p["border"]};
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 600;
    min-height: 14px;
}}
QPushButton#btn_theme:hover {{
    background-color: {p["surface3"]};
    color: {p["text"]};
}}

/* ════════════════════════════════
   INPUTS — line / text / spin / datetime
   ════════════════════════════════ */
QLineEdit, QTextEdit, QSpinBox, QDateTimeEdit {{
    background-color: {p["surface"]};
    border: 1.5px solid {p["border"]};
    border-radius: 8px;
    padding: 9px 13px;
    color: {p["text"]};
    selection-background-color: {p["accent"]};
    selection-color: #FFFFFF;
}}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDateTimeEdit:focus {{
    border: 1.5px solid {p["border_focus"]};
    background-color: {p["surface"]};
}}
QLineEdit:read-only {{ color: {p["text2"]}; }}

QSpinBox::up-button, QSpinBox::down-button {{
    width: 20px; border: none; background: transparent;
    color: {p["text2"]};
}}

/* ════════════════════════════════
   COMBOBOX — the tricky one
   Every state must be explicit to avoid OS bleed-through
   ════════════════════════════════ */
QComboBox {{
    background-color: {p["surface"]};
    border: 1.5px solid {p["border"]};
    border-radius: 8px;
    padding: 9px 36px 9px 13px;
    color: {p["text"]};
    selection-background-color: {p["accent"]};
    min-height: 18px;
}}
QComboBox:focus {{
    border: 1.5px solid {p["border_focus"]};
}}
QComboBox:hover {{
    border: 1.5px solid {p["border_focus"]};
}}
QComboBox::drop-down {{
    border: none;
    width: 30px;
    subcontrol-origin: padding;
    subcontrol-position: right center;
}}
QComboBox::down-arrow {{
    width: 10px;
    height: 10px;
}}

/* The floating popup list */
QComboBox QAbstractItemView {{
    background-color: {p["surface"]};
    border: 1.5px solid {p["border"]};
    border-radius: 10px;
    padding: 6px;
    outline: none;
    /* CRITICAL: explicit text color so it never inherits OS white */
    color: {p["text"]};
}}

/* Every individual item — explicit in ALL states */
QComboBox QAbstractItemView::item {{
    background-color: transparent;
    color: {p["text"]};          /* visible in light AND dark */
    padding: 9px 12px;
    border-radius: 6px;
    min-height: 26px;
}}
QComboBox QAbstractItemView::item:hover {{
    background-color: {p["surface2"]};
    color: {p["text"]};          /* stays readable — NOT white on white */
}}
QComboBox QAbstractItemView::item:selected {{
    background-color: {p["accent"]};
    color: #FFFFFF;              /* white on accent is always fine */
}}
QComboBox QAbstractItemView::item:selected:hover {{
    background-color: {p["accent_h"]};
    color: #FFFFFF;
}}

/* ════════════════════════════════
   SCROLL BARS
   ════════════════════════════════ */
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{
    background: {p["scrollbar"]};
    width: 6px;
    border-radius: 3px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {p["scrollthumb"]};
    border-radius: 3px;
    min-height: 28px;
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{ height: 0; }}

/* ════════════════════════════════
   NAMED LABELS
   ════════════════════════════════ */
QLabel#lbl_heading {{
    font-size: 20px;
    font-weight: 800;
    color: {p["text"]};
    letter-spacing: 0.3px;
    background: transparent;
}}
QLabel#lbl_section {{
    font-size: 11px;
    font-weight: 700;
    color: {p["text3"]};
    letter-spacing: 1.4px;
    background: transparent;
}}
QLabel#lbl_tagline {{
    font-size: 11px;
    color: {p["accent"]};
    font-weight: 600;
    letter-spacing: 0.4px;
    background: transparent;
}}
QLabel#lbl_app_name {{
    font-size: 18px;
    font-weight: 800;
    color: {p["text"]};
    letter-spacing: 2px;
    background: transparent;
}}
QLabel#lbl_status {{
    color: {p["text3"]};
    font-size: 11px;
    background: transparent;
}}
QLabel#lbl_state_running {{
    color: {p["success"]};
    font-size: 12px;
    font-weight: 700;
    background: transparent;
}}
QLabel#lbl_state_paused {{
    color: {p["warning"]};
    font-size: 12px;
    font-weight: 700;
    background: transparent;
}}
QLabel#lbl_empty {{
    color: {p["text3"]};
    font-size: 14px;
    background: transparent;
}}
QLabel#lbl_count {{
    background-color: {p["surface2"]};
    color: {p["text2"]};
    border-radius: 10px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 600;
}}

/* ════════════════════════════════
   STRUCTURAL FRAMES
   ════════════════════════════════ */
QFrame#divider {{
    background: {p["border"]};
    max-height: 1px;
    border: none;
}}
QFrame#task_card {{
    background-color: {p["surface"]};
    border: 1px solid {p["border"]};
    border-radius: 12px;
}}
QFrame#task_card:hover {{
    background-color: {p["card_hover"]};
    border: 1.5px solid {p["border_focus"]};
}}

/* ════════════════════════════════
   BADGES
   ════════════════════════════════ */
QLabel#badge_active   {{
    background: {p["teal_bg"]}; color: {p["teal"]};
    border-radius: 10px; padding: 3px 10px;
    font-size: 11px; font-weight: 700;
}}
QLabel#badge_interval {{
    background: {p["purple_bg"]}; color: {p["purple"]};
    border-radius: 10px; padding: 3px 10px;
    font-size: 11px; font-weight: 700;
}}
QLabel#badge_daily    {{
    background: {p["success_bg"]}; color: {p["success"]};
    border-radius: 10px; padding: 3px 10px;
    font-size: 11px; font-weight: 700;
}}
QLabel#badge_paused   {{
    background: {p["warning_bg"]}; color: {p["warning"]};
    border-radius: 10px; padding: 3px 10px;
    font-size: 11px; font-weight: 700;
}}
QLabel#badge_done     {{
    background: {p["surface2"]}; color: {p["text3"]};
    border-radius: 10px; padding: 3px 10px;
    font-size: 11px; font-weight: 700;
}}
"""


# ══════════════════════════════════════════════════════════════════════
#  ICON HELPERS
# ══════════════════════════════════════════════════════════════════════

def _load_icon() -> QIcon:
    try:
        raw = base64.b64decode(PROMPTLY_ICON_B64)
        pix = QPixmap(); pix.loadFromData(raw, "ICO")
        if not pix.isNull():
            return QIcon(pix)
    except Exception:
        pass
    return _painted_icon("#5B7BFF")


def _painted_icon(accent="#5B7BFF") -> QIcon:
    """Fallback painted eye icon."""
    sz = 32
    pix = QPixmap(sz, sz); pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix); p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor("#0F1221")); p.setPen(Qt.PenStyle.NoPen)
    path = QPainterPath(); path.addRoundedRect(1,1,sz-2,sz-2, sz*0.22, sz*0.22)
    p.drawPath(path)
    cx, cy = sz/2, sz/2; ew, eh = sz*0.38, sz*0.20
    pen = QPen(QColor(accent), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
    p.setPen(pen)
    p.drawArc(int(cx-ew), int(cy-eh), int(ew*2), int(eh*2), 200*16, 140*16)
    p.drawArc(int(cx-ew), int(cy-eh), int(ew*2), int(eh*2), 20*16,  140*16)
    ir = eh*0.65; p.setBrush(QColor(accent)); p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(int(cx-ir), int(cy-ir), int(ir*2), int(ir*2))
    pr = ir*0.5; p.setBrush(QColor("#0F1221"))
    p.drawEllipse(int(cx-pr), int(cy-pr), int(pr*2), int(pr*2))
    hr = pr*0.4; p.setBrush(QColor(255,255,255,220))
    p.drawEllipse(int(cx+pr*0.3-hr), int(cy-pr*0.5-hr), int(hr*2), int(hr*2))
    p.end()
    return QIcon(pix)


def _tray_icon_paused() -> QIcon:
    return _painted_icon("#F59E0B")


# ══════════════════════════════════════════════════════════════════════
#  DOMAIN MODEL
# ══════════════════════════════════════════════════════════════════════

class AppState(Enum):
    RUNNING       = 1
    PAUSED        = 2
    SHUTTING_DOWN = 3
    RECOVERING    = 4


class Task:
    VALID_TYPES = {"one_time", "interval", "daily"}

    def __init__(self, id, title, notes, contact_name, contact_info,
                 reminder_type, interval_minutes, scheduled_time,
                 next_trigger_utc, last_trigger_utc, created_utc,
                 completed, paused):
        self.id = id; self.title = title; self.notes = notes
        self.contact_name = contact_name; self.contact_info = contact_info
        self.reminder_type = reminder_type; self.interval_minutes = interval_minutes
        self.scheduled_time = scheduled_time; self.next_trigger_utc = next_trigger_utc
        self.last_trigger_utc = last_trigger_utc; self.created_utc = created_utc
        self.completed = completed; self.paused = paused

    def __lt__(self, o): return self.next_trigger_utc < o.next_trigger_utc
    def __eq__(self, o): return isinstance(o, Task) and self.id == o.id

    def to_dict(self):
        return {"id":self.id,"title":self.title,"notes":self.notes,
                "contact_name":self.contact_name,"contact_info":self.contact_info,
                "reminder_type":self.reminder_type,"interval_minutes":self.interval_minutes,
                "scheduled_time":self.scheduled_time.isoformat() if self.scheduled_time else None,
                "next_trigger_utc":self.next_trigger_utc.isoformat(),
                "last_trigger_utc":self.last_trigger_utc.isoformat() if self.last_trigger_utc else None,
                "created_utc":self.created_utc.isoformat(),
                "completed":self.completed,"paused":self.paused}

    @classmethod
    def from_dict(cls, d):
        def _dt(v):
            if not v: return None
            try:
                t = datetime.fromisoformat(v)
                return t if t.tzinfo else t.replace(tzinfo=timezone.utc)
            except: return None
        rt = d.get("reminder_type","one_time")
        if rt not in cls.VALID_TYPES: rt = "one_time"
        iv = d.get("interval_minutes")
        if iv is not None:
            try: iv = max(1,int(iv))
            except: iv = 60
        now = datetime.now(timezone.utc)
        tid = d.get("id","")
        try: uuid.UUID(tid)
        except: tid = str(uuid.uuid4())
        return cls(id=tid,title=str(d.get("title",""))[:200],
                   notes=str(d.get("notes",""))[:2000],
                   contact_name=str(d.get("contact_name",""))[:100],
                   contact_info=str(d.get("contact_info",""))[:200],
                   reminder_type=rt,interval_minutes=iv,
                   scheduled_time=_dt(d.get("scheduled_time")),
                   next_trigger_utc=_dt(d.get("next_trigger_utc")) or now,
                   last_trigger_utc=_dt(d.get("last_trigger_utc")),
                   created_utc=_dt(d.get("created_utc")) or now,
                   completed=bool(d.get("completed",False)),
                   paused=bool(d.get("paused",False)))

    def compute_next_trigger(self, after):
        if self.completed or self.reminder_type=="one_time": return None
        if self.reminder_type=="interval":
            return after+timedelta(minutes=self.interval_minutes or 60)
        sched=(self.scheduled_time or after).astimezone(timezone.utc)
        c=after.replace(hour=sched.hour,minute=sched.minute,second=0,microsecond=0)
        if c<=after: c+=timedelta(days=1)
        return c


# ══════════════════════════════════════════════════════════════════════
#  INFRASTRUCTURE — JSON STORAGE
# ══════════════════════════════════════════════════════════════════════

class JsonStorage:
    SCHEMA_VERSION = 1
    def __init__(self, path):
        self.path=path; self._tmp=path+".tmp"
    def load(self):
        if not os.path.exists(self.path): return []
        try:
            with open(self.path,"r",encoding="utf-8") as f: data=json.loads(f.read())
            tasks,seen=[],set()
            for t in data.get("tasks",[]):
                try:
                    task=Task.from_dict(t)
                    if task.id in seen: task.id=str(uuid.uuid4())
                    seen.add(task.id); tasks.append(task)
                except: continue
            return tasks
        except (json.JSONDecodeError,ValueError): self._quarantine(); return []
        except OSError: return []
    def save(self,tasks):
        try:
            payload={"schema_version":self.SCHEMA_VERSION,"app":"Promptly",
                     "saved_utc":datetime.now(timezone.utc).isoformat(),
                     "tasks":[t.to_dict() for t in tasks]}
            with open(self._tmp,"w",encoding="utf-8") as f:
                f.write(json.dumps(payload,indent=2,ensure_ascii=False))
            os.replace(self._tmp,self.path); return True
        except: return False
    def _quarantine(self):
        try:
            ts=datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            os.rename(self.path,self.path+f".corrupted_{ts}")
        except: pass


# ══════════════════════════════════════════════════════════════════════
#  INFRASTRUCTURE — NOTIFICATION SERVICE
# ══════════════════════════════════════════════════════════════════════

class NotificationService:
    def __init__(self):
        self._toaster=None; self._tray=None
        if TOAST_AVAILABLE:
            try: self._toaster=WindowsToaster("Promptly")
            except: pass
    def set_fallback(self,tray): self._tray=tray
    def send(self,task):
        parts=[]
        if task.notes: parts.append(task.notes[:80])
        if task.contact_name: parts.append(f"Contact: {task.contact_name}")
        if task.contact_info: parts.append(task.contact_info)
        body="\n".join(parts).strip() or "Reminder triggered"
        if self._toaster and TOAST_AVAILABLE:
            try:
                t=Toast(); t.text_fields=[task.title,body]
                self._toaster.show_toast(t); return
            except: pass
        if self._tray:
            self._tray.showMessage(task.title,body,QSystemTrayIcon.MessageIcon.Information,6000)


# ══════════════════════════════════════════════════════════════════════
#  SCHEDULER ENGINE
# ══════════════════════════════════════════════════════════════════════

class SchedulerEngine(QObject):
    task_triggered = pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__(parent)
        self._queue=[]; self._tasks={}
        self._timer=QTimer(self); self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._on_timer)
        self._state=AppState.RUNNING
    def load_tasks(self,tasks):
        self._tasks.clear(); self._queue.clear()
        now=datetime.now(timezone.utc)
        for t in tasks:
            self._tasks[t.id]=t
            if not t.completed and not t.paused:
                self._recover(t,now); heapq.heappush(self._queue,(t.next_trigger_utc,t.id))
        self._arm()
    def add_task(self,t):
        self._tasks[t.id]=t
        if not t.completed and not t.paused:
            heapq.heappush(self._queue,(t.next_trigger_utc,t.id)); self._arm()
    def update_task(self,t):
        self._tasks[t.id]=t
        if not t.completed and not t.paused:
            heapq.heappush(self._queue,(t.next_trigger_utc,t.id)); self._arm()
    def remove_task(self,tid): self._tasks.pop(tid,None)
    def get_all_tasks(self): return list(self._tasks.values())
    def set_state(self,s):
        self._state=s
        if s==AppState.RUNNING: self._arm()
        elif s==AppState.PAUSED: self._timer.stop()
    def _recover(self,t,now):
        if t.next_trigger_utc<=now and t.reminder_type!="one_time":
            n=t.compute_next_trigger(now)
            if n: t.next_trigger_utc=n
    def _arm(self):
        if self._state!=AppState.RUNNING: return
        self._timer.stop()
        while self._queue:
            dt,tid=self._queue[0]; t=self._tasks.get(tid)
            if not t or t.completed or t.paused: heapq.heappop(self._queue); continue
            if t.next_trigger_utc!=dt: heapq.heappop(self._queue); continue
            now=datetime.now(timezone.utc)
            ms=max(0,min(int((dt-now).total_seconds()*1000),86_400_000))
            self._timer.start(ms); return
    def _on_timer(self):
        if self._state!=AppState.RUNNING: return
        now=datetime.now(timezone.utc); fired=[]
        while self._queue:
            dt,tid=self._queue[0]; t=self._tasks.get(tid)
            if not t or t.completed or t.paused: heapq.heappop(self._queue); continue
            if t.next_trigger_utc!=dt: heapq.heappop(self._queue); continue
            if dt>now: break
            heapq.heappop(self._queue)
            if t.last_trigger_utc and (now-t.last_trigger_utc).total_seconds()<10: continue
            fired.append(t.id); t.last_trigger_utc=now
            if t.reminder_type=="one_time": t.completed=True
            else:
                nxt=t.compute_next_trigger(now)
                if nxt: t.next_trigger_utc=nxt; heapq.heappush(self._queue,(nxt,t.id))
        for tid in fired: self.task_triggered.emit(tid)
        self._arm()


# ══════════════════════════════════════════════════════════════════════
#  UI HELPERS
# ══════════════════════════════════════════════════════════════════════

def _divider(parent=None) -> QFrame:
    f = QFrame(parent)
    f.setObjectName("divider")
    f.setFrameShape(QFrame.Shape.HLine)
    f.setFixedHeight(1)
    return f


def _section_label(text: str) -> QLabel:
    l = QLabel(text.upper())
    l.setObjectName("lbl_section")
    return l


def _field(label: str, widget: QWidget) -> QVBoxLayout:
    col = QVBoxLayout()
    col.setSpacing(6)
    col.addWidget(_section_label(label))
    col.addWidget(widget)
    return col


# ══════════════════════════════════════════════════════════════════════
#  TASK CARD
# ══════════════════════════════════════════════════════════════════════

class TaskCard(QFrame):
    edit_requested   = pyqtSignal(str)
    delete_requested = pyqtSignal(str)
    pause_toggled    = pyqtSignal(str, bool)

    def __init__(self, task: Task, palette: dict, parent=None):
        super().__init__(parent)
        self.task_id = task.id
        self._pal = palette
        self.setObjectName("task_card")
        self.setMinimumHeight(96)
        self._build(task)

    def _build(self, t: Task):
        root = QHBoxLayout(self)
        root.setContentsMargins(20, 16, 16, 16)
        root.setSpacing(0)

        # ── Left accent bar ────────────────────────────────────
        bar = QFrame(self)
        bar.setFixedWidth(3)
        bar.setStyleSheet(f"background:{self._bar_color(t)};border-radius:2px;")
        root.addWidget(bar)
        root.addSpacing(16)

        # ── Info column ────────────────────────────────────────
        info = QVBoxLayout()
        info.setSpacing(6)

        # Row 1: title + badges
        r1 = QHBoxLayout(); r1.setSpacing(8); r1.setContentsMargins(0,0,0,0)

        title = QLabel(t.title or "(Untitled)")
        title.setStyleSheet(
            f"font-size:14px;font-weight:700;color:{self._pal['text']};"
            "background:transparent;border:none;"
        )
        r1.addWidget(title)

        type_badge = QLabel({"one_time":"One Time","interval":"Interval","daily":"Daily"}.get(t.reminder_type, t.reminder_type))
        type_badge.setObjectName(
            "badge_done" if t.completed else
            {"one_time":"badge_active","interval":"badge_interval","daily":"badge_daily"}.get(t.reminder_type,"badge_active")
        )
        r1.addWidget(type_badge)

        if t.paused and not t.completed:
            pb = QLabel("Paused"); pb.setObjectName("badge_paused"); r1.addWidget(pb)

        r1.addStretch()
        info.addLayout(r1)

        # Row 2: time + contact
        ts = t.next_trigger_utc.astimezone().strftime("%a, %d %b %Y  ·  %I:%M %p")
        r2_parts = [f"🕐  {ts}"]
        if t.contact_name: r2_parts.append(f"👤  {t.contact_name}")
        r2 = QLabel("     ".join(r2_parts))
        r2.setStyleSheet(f"font-size:12px;color:{self._pal['text2']};background:transparent;border:none;")
        info.addWidget(r2)

        # Row 3: notes preview
        if t.notes:
            n = QLabel(t.notes[:100] + ("…" if len(t.notes) > 100 else ""))
            n.setStyleSheet(f"font-size:12px;color:{self._pal['text3']};background:transparent;border:none;")
            info.addWidget(n)

        root.addLayout(info, stretch=1)
        root.addSpacing(12)

        # ── Action buttons ─────────────────────────────────────
        btns = QVBoxLayout(); btns.setSpacing(2)
        btns.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        if not t.completed:
            pb2 = QPushButton("▶" if t.paused else "⏸")
            pb2.setObjectName("btn_ghost"); pb2.setFixedSize(32, 32)
            pb2.setToolTip("Resume" if t.paused else "Pause")
            pb2.clicked.connect(lambda: self.pause_toggled.emit(self.task_id, not t.paused))
            btns.addWidget(pb2)

        eb = QPushButton("✎"); eb.setObjectName("btn_ghost"); eb.setFixedSize(32, 32)
        eb.setToolTip("Edit reminder"); eb.clicked.connect(lambda: self.edit_requested.emit(self.task_id))
        btns.addWidget(eb)

        db = QPushButton("✕"); db.setObjectName("btn_ghost"); db.setFixedSize(32, 32)
        db.setToolTip("Delete reminder"); db.clicked.connect(lambda: self.delete_requested.emit(self.task_id))
        btns.addWidget(db)

        root.addLayout(btns)

    def _bar_color(self, t: Task) -> str:
        if t.completed: return self._pal["text3"]
        if t.paused:    return self._pal["warning"]
        return {"one_time":self._pal["teal"],"interval":self._pal["purple"],"daily":self._pal["success"]}.get(t.reminder_type, self._pal["accent"])


# ══════════════════════════════════════════════════════════════════════
#  TASK FORM DIALOG
# ══════════════════════════════════════════════════════════════════════

class TaskFormDialog(QDialog):
    task_saved = pyqtSignal(object)

    def __init__(self, app_icon, task: Optional[Task] = None, parent=None):
        super().__init__(parent)
        self._editing = task
        self.setWindowTitle("New Reminder" if not task else "Edit Reminder")
        self.setWindowIcon(app_icon)
        self.setModal(True)
        self.setMinimumWidth(520)
        self.setFixedWidth(540)
        self._build()
        if task: self._populate(task)

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header strip
        hdr = QWidget(); hdr.setObjectName("header_widget")
        hdr_l = QHBoxLayout(hdr); hdr_l.setContentsMargins(28, 22, 28, 22)
        hl = QLabel("New Reminder" if not self._editing else "Edit Reminder")
        hl.setObjectName("lbl_heading"); hdr_l.addWidget(hl); hdr_l.addStretch()
        root.addWidget(hdr)
        root.addWidget(_divider())

        # Form body — MUST have objectName so stylesheet can target it explicitly
        body = QWidget(); body.setObjectName("form_body")
        bl = QVBoxLayout(body); bl.setContentsMargins(28, 24, 28, 24); bl.setSpacing(18)

        self._title_in = QLineEdit()
        self._title_in.setPlaceholderText("e.g. Weekly team sync, Call Dr. Mehta…")
        bl.addLayout(_field("Reminder Title *", self._title_in))

        self._notes_in = QTextEdit()
        self._notes_in.setPlaceholderText("Optional description or notes…")
        self._notes_in.setFixedHeight(74)
        bl.addLayout(_field("Notes", self._notes_in))

        # Contact row
        cr = QHBoxLayout(); cr.setSpacing(16)
        self._cname = QLineEdit(); self._cname.setPlaceholderText("Full name")
        cn = QVBoxLayout(); cn.setSpacing(6)
        cn.addWidget(_section_label("Contact Name")); cn.addWidget(self._cname)
        cr.addLayout(cn)
        self._cinfo = QLineEdit(); self._cinfo.setPlaceholderText("Phone or email")
        ci = QVBoxLayout(); ci.setSpacing(6)
        ci.addWidget(_section_label("Contact Info")); ci.addWidget(self._cinfo)
        cr.addLayout(ci)
        bl.addLayout(cr)

        # Type — short, clean labels (no long descriptions that bleed out)
        self._type = QComboBox()
        self._type.addItems(["One Time", "Interval", "Daily"])
        self._type.currentIndexChanged.connect(self._on_type)

        # Hint label that updates with the selection
        self._type_hint = QLabel("Fires once at a scheduled date and time.")
        self._type_hint.setObjectName("lbl_section")
        self._type_hint.setStyleSheet("letter-spacing:0;font-size:12px;")

        type_col = QVBoxLayout(); type_col.setSpacing(6)
        type_col.addWidget(_section_label("Reminder Type"))
        type_col.addWidget(self._type)
        type_col.addWidget(self._type_hint)
        bl.addLayout(type_col)

        # Date/time
        self._dt = QDateTimeEdit()
        self._dt.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self._dt.setCalendarPopup(True)
        self._dt.setDisplayFormat("ddd, dd MMM yyyy   hh:mm AP")
        self._dt_col = _field("Date & Time", self._dt)
        bl.addLayout(self._dt_col)

        # Interval
        self._iv = QSpinBox()
        self._iv.setRange(1, 43200); self._iv.setValue(60)
        self._iv.setSuffix("  minutes")
        self._iv_col = _field("Repeat Every", self._iv)
        bl.addLayout(self._iv_col)

        self._on_type(0)
        root.addWidget(body)
        root.addWidget(_divider())

        # Footer — named so stylesheet targets it, not generic header_widget
        ftr = QWidget(); ftr.setObjectName("form_footer")
        ftl = QHBoxLayout(ftr); ftl.setContentsMargins(28, 16, 28, 16); ftl.setSpacing(10)
        ftl.addStretch()
        cb = QPushButton("Cancel"); cb.setObjectName("btn_secondary")
        cb.clicked.connect(self.reject); ftl.addWidget(cb)
        sb = QPushButton("  Save Reminder  "); sb.clicked.connect(self._save)
        ftl.addWidget(sb)
        root.addWidget(ftr)

    def _on_type(self, idx):
        _hints = [
            "Fires once at the scheduled date and time, then marks as complete.",
            "Fires repeatedly every N minutes until paused or deleted.",
            "Fires every day at the same time you set below.",
        ]
        if hasattr(self, "_type_hint"):
            self._type_hint.setText(_hints[idx])
        is_iv = (idx == 1)
        for col, visible in [(self._dt_col, not is_iv), (self._iv_col, is_iv)]:
            for i in range(col.count()):
                item = col.itemAt(i)
                if item and item.widget():
                    item.widget().setVisible(visible)

    def _populate(self, t: Task):
        self._title_in.setText(t.title); self._notes_in.setPlainText(t.notes)
        self._cname.setText(t.contact_name); self._cinfo.setText(t.contact_info)
        self._type.setCurrentIndex({"one_time":0,"interval":1,"daily":2}.get(t.reminder_type, 0))
        if t.scheduled_time:
            qdt = QDateTime.fromString(t.scheduled_time.astimezone().strftime("%Y-%m-%d %H:%M:%S"), "yyyy-MM-dd HH:mm:ss")
            if qdt.isValid(): self._dt.setDateTime(qdt)
        if t.interval_minutes: self._iv.setValue(t.interval_minutes)

    def _save(self):
        title = self._title_in.text().strip()
        if not title:
            self._title_in.setFocus(); return
        types = ["one_time","interval","daily"]; rt = types[self._type.currentIndex()]
        now = datetime.now(timezone.utc)
        py_dt = self._dt.dateTime().toPyDateTime()
        if py_dt.tzinfo is None: py_dt = py_dt.astimezone(timezone.utc)
        sched = py_dt.astimezone(timezone.utc)
        iv = self._iv.value() if rt=="interval" else None
        if rt=="one_time": nt=sched
        elif rt=="interval": nt=now+timedelta(minutes=iv or 60)
        else: nt=sched if sched>now else sched+timedelta(days=1)
        task = Task(
            id=self._editing.id if self._editing else str(uuid.uuid4()),
            title=title[:200], notes=self._notes_in.toPlainText()[:2000],
            contact_name=self._cname.text().strip()[:100],
            contact_info=self._cinfo.text().strip()[:200],
            reminder_type=rt, interval_minutes=iv, scheduled_time=sched,
            next_trigger_utc=nt,
            last_trigger_utc=self._editing.last_trigger_utc if self._editing else None,
            created_utc=self._editing.created_utc if self._editing else now,
            completed=False, paused=False,
        )
        self.task_saved.emit(task); self.accept()


# ══════════════════════════════════════════════════════════════════════
#  DASHBOARD WINDOW
# ══════════════════════════════════════════════════════════════════════

class DashboardWindow(QWidget):
    task_add_requested    = pyqtSignal()
    task_edit_requested   = pyqtSignal(str)
    task_delete_requested = pyqtSignal(str)
    task_pause_toggled    = pyqtSignal(str, bool)
    theme_toggle_requested = pyqtSignal()

    def __init__(self, app_icon: QIcon, parent=None):
        super().__init__(parent)
        self._app_icon = app_icon
        self._all_tasks: List[Task] = []
        self._palette = DARK
        self.setObjectName("promptly_dash")
        self.setWindowTitle("Promptly")
        self.setWindowIcon(app_icon)
        self.setMinimumSize(680, 580)
        self.resize(760, 620)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ────────────────────────────────────────────────
        self._hdr = QWidget(); self._hdr.setObjectName("header_widget")
        hl = QHBoxLayout(self._hdr); hl.setContentsMargins(24, 18, 20, 18); hl.setSpacing(0)

        # Logo block
        logo_col = QVBoxLayout(); logo_col.setSpacing(3)
        app_lbl = QLabel("PROMPTLY"); app_lbl.setObjectName("lbl_app_name")
        tag_lbl = QLabel("Smart Reminders  ·  Never Miss a Moment")
        tag_lbl.setObjectName("lbl_tagline")
        logo_col.addWidget(app_lbl); logo_col.addWidget(tag_lbl)
        hl.addLayout(logo_col); hl.addStretch()

        # State indicator
        self._state_lbl = QLabel("● Active")
        self._state_lbl.setObjectName("lbl_state_running")
        self._state_lbl.setContentsMargins(0, 0, 16, 0)
        hl.addWidget(self._state_lbl)

        # Theme toggle
        self._theme_btn = QPushButton("☀  Light")
        self._theme_btn.setObjectName("btn_theme")
        self._theme_btn.setFixedHeight(34)
        self._theme_btn.clicked.connect(self.theme_toggle_requested.emit)
        hl.addWidget(self._theme_btn)
        hl.addSpacing(12)

        # Add button
        self._add_btn = QPushButton("＋  Add Reminder")
        self._add_btn.setFixedHeight(36)
        self._add_btn.clicked.connect(self.task_add_requested.emit)
        hl.addWidget(self._add_btn)

        root.addWidget(self._hdr)
        root.addWidget(_divider())

        # ── Stats bar ─────────────────────────────────────────────
        self._stats_bar = QWidget(); self._stats_bar.setObjectName("filter_widget")
        sb = QHBoxLayout(self._stats_bar); sb.setContentsMargins(24, 0, 24, 0); sb.setSpacing(0)
        sb.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._stat_active   = self._stat_pill("Active", "0",   "stat_active")
        self._stat_interval = self._stat_pill("Interval", "0", "stat_interval")
        self._stat_daily    = self._stat_pill("Daily", "0",    "stat_daily")
        self._stat_done     = self._stat_pill("Done", "0",     "stat_done")
        sb.addWidget(self._stat_active); sb.addSpacing(6)
        sb.addWidget(self._stat_interval); sb.addSpacing(6)
        sb.addWidget(self._stat_daily); sb.addSpacing(6)
        sb.addWidget(self._stat_done)
        self._stats_bar.setFixedHeight(52)
        root.addWidget(self._stats_bar)
        root.addWidget(_divider())

        # ── Filter bar ────────────────────────────────────────────
        self._fbar = QWidget(); self._fbar.setObjectName("filter_widget")
        fl = QHBoxLayout(self._fbar); fl.setContentsMargins(20, 10, 20, 10); fl.setSpacing(10)

        self._filter = QComboBox()
        self._filter.addItems(["All Reminders", "Active", "Paused", "Completed"])
        self._filter.setFixedWidth(160); self._filter.setFixedHeight(34)
        self._filter.currentIndexChanged.connect(self._refresh_view)
        fl.addWidget(self._filter)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Search by title, notes, or contact…")
        self._search.setFixedHeight(34)
        self._search.textChanged.connect(self._refresh_view)
        fl.addWidget(self._search)

        self._count_lbl = QLabel(""); self._count_lbl.setObjectName("lbl_count")
        fl.addWidget(self._count_lbl)
        root.addWidget(self._fbar)
        root.addWidget(_divider())

        # ── Scroll area ───────────────────────────────────────────
        self._scroll = QScrollArea(); self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._container = QWidget()
        self._cards_l = QVBoxLayout(self._container)
        self._cards_l.setContentsMargins(20, 16, 20, 16)
        self._cards_l.setSpacing(10)
        self._cards_l.addStretch()
        self._scroll.setWidget(self._container)
        root.addWidget(self._scroll, stretch=1)

        # ── Status bar ────────────────────────────────────────────
        self._sb_widget = QWidget(); self._sb_widget.setObjectName("status_bar_widget")
        sbl = QHBoxLayout(self._sb_widget)
        sbl.setContentsMargins(20, 6, 20, 6); sbl.setSpacing(0)
        self._status_lbl = QLabel("Promptly ready."); self._status_lbl.setObjectName("lbl_status")
        sbl.addWidget(self._status_lbl); sbl.addStretch()
        self._ver_lbl = QLabel("v1.0  Enterprise"); self._ver_lbl.setObjectName("lbl_status")
        sbl.addWidget(self._ver_lbl)
        root.addWidget(self._sb_widget)

    def _stat_pill(self, label, value, name) -> QWidget:
        w = QFrame(); w.setFixedHeight(36)
        l = QHBoxLayout(w); l.setContentsMargins(12, 0, 12, 0); l.setSpacing(6)
        vl = QLabel(value); vl.setObjectName(f"_{name}_val")
        vl.setStyleSheet(f"font-size:15px;font-weight:800;background:transparent;border:none;")
        ll = QLabel(label); ll.setObjectName(f"_{name}_lbl")
        ll.setStyleSheet("font-size:11px;font-weight:600;background:transparent;border:none;")
        l.addWidget(vl); l.addWidget(ll)
        return w

    def _update_stat_pill(self, pill, value, val_color, lbl_color):
        val_lbl = pill.findChild(QLabel, [c.objectName() for c in pill.findChildren(QLabel) if "_val" in c.objectName()][0] if pill.findChildren(QLabel) else "")
        for child in pill.findChildren(QLabel):
            if "_val" in child.objectName():
                child.setText(str(value))
                child.setStyleSheet(f"font-size:15px;font-weight:800;color:{val_color};background:transparent;border:none;")
            elif "_lbl" in child.objectName():
                child.setStyleSheet(f"font-size:11px;font-weight:600;color:{lbl_color};background:transparent;border:none;")

    def apply_theme(self, palette: dict, theme_name: str):
        self._palette = palette
        QApplication.instance().setStyleSheet(make_stylesheet(palette))
        moon_sun = "☀  Light" if theme_name == Theme.DARK else "🌙  Dark"
        self._theme_btn.setText(moon_sun)

    def refresh_tasks(self, tasks: List[Task]):
        self._all_tasks = tasks
        # Update stat pills
        p = self._palette
        active   = [t for t in tasks if not t.completed and not t.paused and t.reminder_type=="one_time"]
        interval = [t for t in tasks if not t.completed and not t.paused and t.reminder_type=="interval"]
        daily    = [t for t in tasks if not t.completed and not t.paused and t.reminder_type=="daily"]
        done     = [t for t in tasks if t.completed]
        self._update_stat_pill(self._stat_active,   len(active),   p["teal"],    p["text2"])
        self._update_stat_pill(self._stat_interval, len(interval), p["purple"],  p["text2"])
        self._update_stat_pill(self._stat_daily,    len(daily),    p["success"], p["text2"])
        self._update_stat_pill(self._stat_done,     len(done),     p["text3"],   p["text3"])
        self._refresh_view()

    def _refresh_view(self):
        fi = self._filter.currentIndex(); q = self._search.text().strip().lower()
        def vis(t):
            if fi==1 and (t.completed or t.paused): return False
            if fi==2 and not t.paused: return False
            if fi==3 and not t.completed: return False
            if q and q not in f"{t.title} {t.notes} {t.contact_name} {t.contact_info}".lower(): return False
            return True
        tasks = sorted([t for t in self._all_tasks if vis(t)],
                       key=lambda t: (t.completed, t.paused, t.next_trigger_utc))

        while self._cards_l.count() > 1:
            item = self._cards_l.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        if not tasks:
            el = QLabel("No reminders found.\nClick  ＋ Add Reminder  to schedule your first reminder.")
            el.setObjectName("lbl_empty")
            el.setAlignment(Qt.AlignmentFlag.AlignCenter)
            el.setWordWrap(True)
            self._cards_l.insertWidget(0, el)
        else:
            for t in tasks:
                card = TaskCard(t, self._palette)
                card.edit_requested.connect(self.task_edit_requested.emit)
                card.delete_requested.connect(self.task_delete_requested.emit)
                card.pause_toggled.connect(self.task_pause_toggled.emit)
                self._cards_l.insertWidget(self._cards_l.count()-1, card)

        n = len(tasks)
        self._count_lbl.setText(f"{n} reminder{'s' if n != 1 else ''}")
        self._count_lbl.setVisible(True)

    def set_app_state(self, state: AppState):
        if state == AppState.RUNNING:
            self._state_lbl.setText("● Active")
            self._state_lbl.setObjectName("lbl_state_running")
        elif state == AppState.PAUSED:
            self._state_lbl.setText("⏸ Paused")
            self._state_lbl.setObjectName("lbl_state_paused")
        self._state_lbl.style().unpolish(self._state_lbl)
        self._state_lbl.style().polish(self._state_lbl)

    def set_status(self, msg: str):
        self._status_lbl.setText(msg)

    def closeEvent(self, e):
        e.ignore(); self.hide()


# ══════════════════════════════════════════════════════════════════════
#  APPLICATION CONTROLLER
# ══════════════════════════════════════════════════════════════════════

class AppController(QObject):
    def __init__(self):
        super().__init__()
        self._theme = Theme.DARK
        self._palette = DARK
        self._state = AppState.RUNNING
        self._data_path = self._resolve_path()
        self._storage = JsonStorage(self._data_path)
        self._notif   = NotificationService()
        self._sched   = SchedulerEngine()
        self._sched.task_triggered.connect(self._on_triggered)
        self._icon = _load_icon()
        self._tray: Optional[QSystemTrayIcon] = None
        self._dash: Optional[DashboardWindow] = None
        self._boot()

    def _resolve_path(self):
        base = os.path.dirname(sys.executable if getattr(sys,"frozen",False) else os.path.abspath(__file__))
        return os.path.join(base, "data.json")

    def _boot(self):
        self._setup_tray()
        self._dash = DashboardWindow(self._icon)
        self._dash.task_add_requested.connect(self._add)
        self._dash.task_edit_requested.connect(self._edit)
        self._dash.task_delete_requested.connect(self._delete)
        self._dash.task_pause_toggled.connect(self._pause_task)
        self._dash.theme_toggle_requested.connect(self._toggle_theme)
        # Apply initial theme
        QApplication.instance().setStyleSheet(make_stylesheet(self._palette))
        self._dash.apply_theme(self._palette, self._theme)
        self._set_state(AppState.RECOVERING)
        self._sched.load_tasks(self._storage.load())
        self._set_state(AppState.RUNNING)
        self._refresh()

    def _setup_tray(self):
        self._tray = QSystemTrayIcon()
        self._tray.setIcon(self._icon)
        self._tray.setToolTip("Promptly — Smart Reminders")
        self._notif.set_fallback(self._tray)
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background:#1E2444; border:1px solid #2A3060;
                border-radius:10px; padding:6px; font-size:13px;
            }
            QMenu::item { padding:10px 24px; color:#FFFFFF; border-radius:6px; }
            QMenu::item:selected { background:#5B7BFF; }
            QMenu::separator { height:1px; background:#2A3060; margin:5px 12px; }
        """)
        for label, slot in [
            ("Open Promptly",    self._show_dash),
            ("Add Reminder",  self._add),
        ]: a=QAction(label,menu); a.triggered.connect(slot); menu.addAction(a)
        menu.addSeparator()
        self._act_pause = QAction("Pause Notifications", menu)
        self._act_pause.triggered.connect(self._toggle_pause); menu.addAction(self._act_pause)
        menu.addSeparator()
        a_exit = QAction("Exit Promptly", menu); a_exit.triggered.connect(self._shutdown)
        menu.addAction(a_exit)
        self._tray.setContextMenu(menu)
        self._tray.activated.connect(
            lambda r: self._show_dash() if r==QSystemTrayIcon.ActivationReason.DoubleClick else None
        )
        self._tray.show()

    def _show_dash(self):
        self._refresh()
        self._dash.show(); self._dash.raise_(); self._dash.activateWindow()

    def _refresh(self):
        tasks = self._sched.get_all_tasks()
        self._dash.refresh_tasks(tasks)
        self._dash.set_app_state(self._state)
        active = sum(1 for t in tasks if not t.completed and not t.paused)
        self._dash.set_status(f"Promptly running  ·  {active} active reminder{'s' if active != 1 else ''}")

    def _toggle_theme(self):
        self._theme = Theme.LIGHT if self._theme == Theme.DARK else Theme.DARK
        self._palette = LIGHT if self._theme == Theme.LIGHT else DARK
        self._dash.apply_theme(self._palette, self._theme)
        self._refresh()

    def _add(self):
        d = TaskFormDialog(self._icon, parent=self._dash)
        d.task_saved.connect(self._saved); d.exec()

    def _edit(self, tid):
        t = next((x for x in self._sched.get_all_tasks() if x.id==tid), None)
        if not t: return
        d = TaskFormDialog(self._icon, task=t, parent=self._dash)
        d.task_saved.connect(self._saved); d.exec()

    def _saved(self, task):
        self._sched.add_task(task); self._persist(); self._refresh()

    def _delete(self, tid):
        self._sched.remove_task(tid); self._persist(); self._refresh()

    def _pause_task(self, tid, paused):
        t = next((x for x in self._sched.get_all_tasks() if x.id==tid), None)
        if not t: return
        t.paused=paused; self._sched.update_task(t); self._persist(); self._refresh()

    def _toggle_pause(self):
        self._set_state(AppState.RUNNING if self._state==AppState.PAUSED else AppState.PAUSED)

    def _set_state(self, s):
        self._state=s; self._sched.set_state(s)
        if s==AppState.RUNNING:
            self._tray.setIcon(self._icon)
            self._tray.setToolTip("Promptly — Active")
            self._act_pause.setText("Pause Notifications")
        elif s==AppState.PAUSED:
            self._tray.setIcon(_tray_icon_paused())
            self._tray.setToolTip("Promptly — Paused")
            self._act_pause.setText("Resume Notifications")
        elif s==AppState.RECOVERING:
            self._tray.setToolTip("Promptly — Loading…")
        if self._dash: self._dash.set_app_state(s)

    def _on_triggered(self, tid):
        if self._state!=AppState.RUNNING: return
        t = next((x for x in self._sched.get_all_tasks() if x.id==tid), None)
        if t: self._notif.send(t); self._persist(); self._refresh()

    def _persist(self): self._storage.save(self._sched.get_all_tasks())

    def _shutdown(self):
        self._set_state(AppState.SHUTTING_DOWN)
        self._persist(); self._tray.hide()
        QApplication.instance().quit()


# ══════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════

def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setApplicationName("Promptly")
    app.setApplicationDisplayName("Promptly")
    app.setOrganizationName("Promptly")
    app.setApplicationVersion("1.0")
    app.setQuitOnLastWindowClosed(False)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Promptly", "System tray is not available.")
        sys.exit(1)

    controller = AppController()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
