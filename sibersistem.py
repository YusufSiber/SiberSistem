import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import turtle
import json
import random
import time
import os
import string
import importlib
import wikipedia 
import urllib.request 
import webbrowser 

wikipedia.set_lang("tr")

# SİSTEMİN MEVCUT SÜRÜMÜ
SISTEM_SURUMU = "5.0" 

# ==========================================
# DOSYA YOLU AYARLARI
# ==========================================
BELGELER_KLASORU = os.path.join(os.path.expanduser("~"), "Documents")
REHBER_DOSYASI = os.path.join(BELGELER_KLASORU, "rehber.json")
GOREV_DOSYASI = os.path.join(BELGELER_KLASORU, "gorevler.json")
SKOR_DOSYASI = os.path.join(BELGELER_KLASORU, "yilan_skor.json")
SIFRE_DOSYASI = os.path.join(BELGELER_KLASORU, "sistem_sifresi.json") 

# ==========================================
# ŞİFRE OKUMA VE YAZMA SİSTEMİ
# ==========================================
def sifre_dosyasi_var_mi():
    return os.path.exists(SIFRE_DOSYASI)

def sifre_getir():
    try:
        with open(SIFRE_DOSYASI, "r", encoding="utf-8") as d: 
            return json.load(d).get("sifre", "")
    except: 
        return "" 

def sifre_kaydet(yeni_sifre):
    with open(SIFRE_DOSYASI, "w", encoding="utf-8") as d: 
        json.dump({"sifre": yeni_sifre}, d)

# ==========================================
# ÖZEL VE BÜYÜK ARAYÜZ MOTORU
# ==========================================
def ozel_mesaj_kutusu(baslik, mesaj):
    pencere = tk.Toplevel(root)
    pencere.title(baslik)
    w, h = 550, 350
    x = (pencere.winfo_screenwidth() // 2) - (w // 2)
    y = (pencere.winfo_screenheight() // 2) - (h // 2)
    pencere.geometry(f"{w}x{h}+{x}+{y}")
    pencere.configure(bg="#2c3e50")
    pencere.grab_set() 
    frame = tk.Frame(pencere, bg="#2c3e50")
    frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))
    metin = tk.Text(frame, wrap="word", font=("Arial", 14), bg="#34495e", fg="white", relief="flat", padx=15, pady=15)
    metin.insert("1.0", mesaj)
    metin.config(state="disabled")
    metin.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(frame, command=metin.yview)
    scrollbar.pack(side="right", fill="y")
    metin.config(yscrollcommand=scrollbar.set)
    tk.Button(pencere, text="TAMAM", command=pencere.destroy, font=("Arial", 12, "bold"), bg="#1ebca1", fg="white", width=15).pack(pady=(0, 20))
    pencere.wait_window()

def ozel_girdi_al(baslik, mesaj, gizli=False):
    pencere = tk.Toplevel(root)
    pencere.title(baslik)
    w, h = 500, 300
    x = (pencere.winfo_screenwidth() // 2) - (w // 2)
    y = (pencere.winfo_screenheight() // 2) - (h // 2)
    pencere.geometry(f"{w}x{h}+{x}+{y}")
    pencere.configure(bg="#2c3e50")
    pencere.grab_set()
    cevap = {"deger": None}
    tk.Label(pencere, text=mesaj, font=("Arial", 14), bg="#2c3e50", fg="white", wraplength=450, justify="center").pack(pady=(30, 15))
    
    if gizli: girdi = tk.Entry(pencere, font=("Arial", 16), justify="center", width=25, bg="#ecf0f1", fg="black", show="*")
    else: girdi = tk.Entry(pencere, font=("Arial", 16), justify="center", width=25, bg="#ecf0f1", fg="black")
    
    girdi.pack(pady=10)
    girdi.focus()
    def kaydet(event=None):
        cevap["deger"] = girdi.get()
        pencere.destroy()
    pencere.bind('<Return>', kaydet)
    tk.Button(pencere, text="ONAYLA", command=kaydet, font=("Arial", 12, "bold"), bg="#f39c12", fg="white", width=15).pack(pady=15)
    pencere.wait_window()
    return cevap["deger"]

# ==========================================
# 1-20 TÜM OYUNLAR VE ARAÇLAR 
# ==========================================
def baslat_turtle_oyunu():
    ozel_mesaj_kutusu("Bilgi", "Yılan oyunu açılıyor...\n\nKapatmak için çarpıdan (X) kapatın.")
    turtle.TurtleScreen._RUNNING = True 
    def skor_yukle():
        try:
            with open(SKOR_DOSYASI, "r", encoding="utf-8") as d: return json.load(d)
        except: return 0
    def skor_kaydet(yeni_skor):
        with open(SKOR_DOSYASI, "w", encoding="utf-8") as d: json.dump(yeni_skor, d)
    ekran = turtle.Screen(); ekran.clear(); ekran.title("Siber Yılan Oyunu"); ekran.bgcolor("black"); ekran.setup(600, 600); ekran.tracer(0) 
    oyuncu = turtle.Turtle(); oyuncu.speed(0); oyuncu.shape("square"); oyuncu.color("white"); oyuncu.penup(); oyuncu.goto(0, 0); oyuncu.yon = "dur" 
    elma = turtle.Turtle(); elma.speed(0); elma.shape("circle"); elma.color("red"); elma.penup(); elma.goto(0, 100) 
    kuyruklar = []; global skor; skor = 0; en_yuksek_skor = skor_yukle() 
    kalem = turtle.Turtle(); kalem.speed(0); kalem.color("white"); kalem.penup(); kalem.hideturtle(); kalem.goto(0, 260)
    kalem.write(f"Skor: {skor}  En Yüksek Skor: {en_yuksek_skor}", align="center", font=("Courier", 16, "normal"))
    def yukari():
        if oyuncu.yon != "asagi": oyuncu.yon = "yukari"
    def asagi():
        if oyuncu.yon != "yukari": oyuncu.yon = "asagi"
    def sola():
        if oyuncu.yon != "saga": oyuncu.yon = "sola"
    def saga():
        if oyuncu.yon != "sola": oyuncu.yon = "saga"
    ekran.listen(); ekran.onkeypress(yukari, "Up"); ekran.onkeypress(asagi, "Down"); ekran.onkeypress(sola, "Left"); ekran.onkeypress(saga, "Right")
    def hareket():
        if oyuncu.yon == "yukari": oyuncu.sety(oyuncu.ycor() + 20)
        if oyuncu.yon == "asagi": oyuncu.sety(oyuncu.ycor() - 20)
        if oyuncu.yon == "sola": oyuncu.setx(oyuncu.xcor() - 20)
        if oyuncu.yon == "saga": oyuncu.setx(oyuncu.xcor() + 20)
    while True:
        try:
            ekran.update() 
            if oyuncu.xcor() > 290 or oyuncu.xcor() < -290 or oyuncu.ycor() > 290 or oyuncu.ycor() < -290:
                time.sleep(1); oyuncu.goto(0, 0); oyuncu.yon = "dur"
                for parca in kuyruklar: parca.goto(1000, 1000)
                kuyruklar.clear(); skor = 0; kalem.clear()
                kalem.write(f"Skor: {skor}  En Yüksek Skor: {en_yuksek_skor}", align="center", font=("Courier", 16, "normal"))
            if oyuncu.distance(elma) < 20:
                elma.goto(random.randint(-270, 270), random.randint(-270, 270)) 
                yeni_kuyruk = turtle.Turtle(); yeni_kuyruk.speed(0); yeni_kuyruk.shape("square"); yeni_kuyruk.color("gray"); yeni_kuyruk.penup(); kuyruklar.append(yeni_kuyruk)
                skor += 10
                if skor > en_yuksek_skor: en_yuksek_skor = skor; skor_kaydet(en_yuksek_skor) 
                kalem.clear(); kalem.write(f"Skor: {skor}  En Yüksek Skor: {en_yuksek_skor}", align="center", font=("Courier", 16, "normal"))
            for i in range(len(kuyruklar) - 1, 0, -1):
                kuyruklar[i].goto(kuyruklar[i - 1].xcor(), kuyruklar[i - 1].ycor())
            if len(kuyruklar) > 0: kuyruklar[0].goto(oyuncu.xcor(), oyuncu.ycor())
            hareket() 
            for parca in kuyruklar:
                if parca.distance(oyuncu) < 20:
                    time.sleep(1); oyuncu.goto(0,0); oyuncu.yon = "dur"
                    for p in kuyruklar: p.goto(1000, 1000)
                    kuyruklar.clear(); skor = 0; kalem.clear()
                    kalem.write(f"Skor: {skor}  En Yüksek Skor: {en_yuksek_skor}", align="center", font=("Courier", 16, "normal"))
            time.sleep(0.1) 
        except turtle.Terminator: break 
    importlib.reload(turtle)

def baslat_hesap_makinesi():
    secim = ozel_girdi_al("Hesap Makinesi", "İşlem Seçin:\n\n1: Topla | 2: Çıkar | 3: Çarp | 4: Böl")
    if secim in ['1', '2', '3', '4']:
        s1_str = ozel_girdi_al("1. Sayı", "Birinci sayıyı girin:")
        s2_str = ozel_girdi_al("2. Sayı", "İkinci sayıyı girin:")
        if s1_str and s2_str:
            try:
                s1, s2 = float(s1_str), float(s2_str)
                if secim == '1': sonuc = s1 + s2
                elif secim == '2': sonuc = s1 - s2
                elif secim == '3': sonuc = s1 * s2
                elif secim == '4': 
                    if s2 == 0: ozel_mesaj_kutusu("Hata", "Sıfıra bölünemez!"); return
                    sonuc = s1 / s2
                ozel_mesaj_kutusu("Sonuç", f"İşlem Sonucu:\n\n{sonuc}")
            except: ozel_mesaj_kutusu("Hata", "Geçersiz giriş!")

def baslat_rehber():
    try:
        with open(REHBER_DOSYASI, "r", encoding="utf-8") as d: rehber = json.load(d)
    except: rehber = {}
    secim = ozel_girdi_al("Rehber", "İşlem: (ekle / sil / listele)")
    if secim:
        secim = secim.lower().strip()
        if secim == "ekle":
            isim = ozel_girdi_al("Ekle", "Kişi İsmi:")
            num = ozel_girdi_al("Ekle", "Telefon Numarası:")
            if isim and num:
                rehber[isim] = num; json.dump(rehber, open(REHBER_DOSYASI, "w", encoding="utf-8")); ozel_mesaj_kutusu("Başarılı", f"[{isim}] eklendi!")
        elif secim == "sil":
            isim = ozel_girdi_al("Sil", "Silinecek İsim:")
            if isim in rehber: del rehber[isim]; json.dump(rehber, open(REHBER_DOSYASI, "w", encoding="utf-8")); ozel_mesaj_kutusu("Başarılı", f"[{isim}] silindi.")
        elif secim == "listele":
            if not rehber: ozel_mesaj_kutusu("Rehber", "Rehber boş.")
            else: ozel_mesaj_kutusu("Kayıtlı Kişiler", "\n".join([f"👤 {k}: 📞 {v}" for k, v in rehber.items()]))

def baslat_sayi_tahmin():
    gizli_sayi = random.randint(1, 100); deneme = 0
    ozel_mesaj_kutusu("Oyun Başlıyor", "Aklımdan 1 ile 100 arasında bir sayı tuttum. Hadi bil!")
    while True:
        t_str = ozel_girdi_al("Tahmin", f"Tahminin nedir? (Deneme: {deneme})")
        if not t_str: break 
        try:
            t = int(t_str); deneme += 1
            if t < gizli_sayi: ozel_mesaj_kutusu("İpucu", "Daha BÜYÜK bir sayı söyle! ⬆️")
            elif t > gizli_sayi: ozel_mesaj_kutusu("İpucu", "Daha KÜÇÜK bir sayı söyle! ⬇️")
            else: ozel_mesaj_kutusu("Kazandın!", f"🎉 {deneme}. denemede doğru bildin!"); break
        except: pass

def baslat_tas_kagit_makas():
    sec = ["taş", "kağıt", "makas"]; kul = ozel_girdi_al("Seçim", "Taş / Kağıt / Makas")
    if kul:
        kul = kul.lower().strip()
        if kul in sec:
            pc = random.choice(sec)
            if kul == pc: s = "BERABERE! 🤝"
            elif (kul=="taş" and pc=="makas") or (kul=="kağıt" and pc=="taş") or (kul=="makas" and pc=="kağıt"): s = "KAZANDIN! 🏆"
            else: s = "KAYBETTİN! 💀"
            ozel_mesaj_kutusu("Sonuç", f"Sen: {kul.upper()}\nPC: {pc.upper()}\n\n{s}")

def baslat_adam_asmaca():
    k = {"python": "YAZILIM", "klavye": "DONANIM", "sistem": "BİLGİSAYAR", "algoritma": "YAZILIM", "hacker": "TEKNOLOJİ"}
    sec = random.choice(list(k.keys())); ipucu = k[sec]; bilinen = []; can = 6
    while can > 0:
        ekran = "".join([h + " " if h in bilinen else "_ " for h in sec])
        if "_" not in ekran: ozel_mesaj_kutusu("Kazandın", f"Kelime: {sec.upper()}"); return
        t = ozel_girdi_al("Adam Asmaca", f"💡 {ipucu}  |  ❤️ {can}\nKelime: {ekran}\nHarf gir:")
        if not t: return 
        t = t.lower().strip()
        if len(t) == 1 and t.isalpha():
            if t not in bilinen:
                bilinen.append(t)
                if t not in sec:
                    can -= 1
                    if can > 0: ozel_mesaj_kutusu("Yanlış", f"Yanlış harf! Kalan Can: {can}")
        else: ozel_mesaj_kutusu("Hata", "Tek harf gir!")
    ozel_mesaj_kutusu("Kaybettin", f"💀 Adam Asıldı!\nDoğru kelime: {sec.upper()}")

def baslat_sifre_olusturucu():
    uz_str = ozel_girdi_al("Şifre", "Kaç karakter olsun?")
    if uz_str:
        try:
            uz = int(uz_str); h = string.ascii_letters + string.digits + string.punctuation
            s = "".join(random.choice(h) for _ in range(uz)); ozel_mesaj_kutusu("Oluşturuldu", f"Şifren:\n\n{s}")
        except: pass

def baslat_gorev_yoneticisi():
    try:
        with open(GOREV_DOSYASI, "r", encoding="utf-8") as d: g = json.load(d)
    except: g = []
    secim = ozel_girdi_al("Görev", "1: Ekle | 2: Listele | 3: Tamamla | 4: Sil")
    if secim == '1':
        y = ozel_girdi_al("Yeni Görev", "Görev nedir?")
        if y: g.append({"gorev": y, "durum": False}); json.dump(g, open(GOREV_DOSYASI, "w")); ozel_mesaj_kutusu("Başarılı", "Eklendi!")
    elif secim == '2':
        l = "\n".join([f"{i+1}. [{'✓' if x['durum'] else ' '}] {x['gorev']}" for i, x in enumerate(g)])
        ozel_mesaj_kutusu("Görevlerin", l if l else "Görev yok!")
    elif secim in ['3', '4']:
        no = ozel_girdi_al("İşlem", "Görev numarası?")
        try:
            no = int(no)
            if 0 < no <= len(g):
                if secim == '3': g[no-1]["durum"] = True
                if secim == '4': g.pop(no-1)
                json.dump(g, open(GOREV_DOSYASI, "w")); ozel_mesaj_kutusu("Başarılı", "İşlem yapıldı!")
        except: pass

def baslat_xox():
    mod = ozel_girdi_al("XOX", "1: Yapay Zeka\n2: İki Kişi")
    if mod not in ['1', '2']: return
    turtle.TurtleScreen._RUNNING = True 
    ekran = turtle.Screen(); ekran.clear(); ekran.bgcolor("#1ebca1"); ekran.setup(600, 600); ekran.tracer(0)
    cizer = turtle.Turtle(); cizer.speed(0); cizer.hideturtle(); cizer.width(12)
    def tahtayi_ciz():
        cizer.color("#158a75") 
        cizer.penup(); cizer.goto(-100, 300); cizer.pendown(); cizer.goto(-100, -300)
        cizer.penup(); cizer.goto(100, 300); cizer.pendown(); cizer.goto(100, -300)
        cizer.penup(); cizer.goto(-300, 100); cizer.pendown(); cizer.goto(300, 100)
        cizer.penup(); cizer.goto(-300, -100); cizer.pendown(); cizer.goto(300, -100)
        cizer.penup(); cizer.goto(-300, 300); cizer.pendown(); cizer.goto(300, 300); cizer.goto(300, -300); cizer.goto(-300, -300); cizer.goto(-300, 300)
        ekran.update()
    tahtayi_ciz(); tahta = [' '] * 9; durum = {"aktif": True, "sira": "X"}
    def k(t, h): return ((t[0]==h and t[1]==h and t[2]==h) or (t[3]==h and t[4]==h and t[5]==h) or (t[6]==h and t[7]==h and t[8]==h) or (t[0]==h and t[3]==h and t[6]==h) or (t[1]==h and t[4]==h and t[7]==h) or (t[2]==h and t[5]==h and t[8]==h) or (t[0]==h and t[4]==h and t[8]==h) or (t[2]==h and t[4]==h and t[6]==h))
    def tık(x, y):
        if not durum["aktif"]: return
        sat = 0 if y>100 else (1 if y>-100 else 2); sut = 0 if x<-100 else (1 if x<100 else 2)
        kutu = sat*3+sut; my = 200 if sat==0 else (0 if sat==1 else -200); mx = -200 if sut==0 else (0 if sut==1 else 200)
        if tahta[kutu] == ' ':
            tahta[kutu] = durum["sira"]; cizer.color("#545454" if durum["sira"]=='X' else "#f2ebd3")
            if durum["sira"]=='X': cizer.penup(); cizer.goto(mx-50, my+50); cizer.pendown(); cizer.goto(mx+50, my-50); cizer.penup(); cizer.goto(mx+50, my+50); cizer.pendown(); cizer.goto(mx-50, my-50)
            else: cizer.penup(); cizer.goto(mx, my-50); cizer.pendown(); cizer.circle(50)
            ekran.update()
            if k(tahta, durum["sira"]): durum["aktif"]=False; ozel_mesaj_kutusu("Oyun Bitti", f"🏆 {durum['sira']} KAZANDI!"); ekran.bye(); return
            if ' ' not in tahta: durum["aktif"]=False; ozel_mesaj_kutusu("Oyun Bitti", "🤝 BERABERE!"); ekran.bye(); return
            if mod=='1':
                b = [i for i, v in enumerate(tahta) if v==' ']; pc = random.choice(b)
                for h in b: 
                    k_t = tahta[:]; k_t[h] = 'O'
                    if k(k_t, 'O'): pc = h
                for h in b: 
                    k_t = tahta[:]; k_t[h] = 'X'
                    if k(k_t, 'X'): pc = h
                tahta[pc] = 'O'; py = 200 if pc//3==0 else (0 if pc//3==1 else -200); px = -200 if pc%3==0 else (0 if pc%3==1 else 200)
                time.sleep(0.3); cizer.color("#f2ebd3"); cizer.penup(); cizer.goto(px, py-50); cizer.pendown(); cizer.circle(50); ekran.update()
                if k(tahta, 'O'): durum["aktif"]=False; ozel_mesaj_kutusu("Bitti", "💀 PC KAZANDI!"); ekran.bye()
            else: durum["sira"] = 'O' if durum["sira"]=='X' else 'X'
    ekran.onclick(tık)
    while True:
        try: ekran.update(); time.sleep(0.1)
        except: break
    importlib.reload(turtle)

def baslat_klavye_testi():
    h = " ".join(random.sample(["yazılım", "hacker", "klavye", "veri", "sistem", "oyun"], 4)); ozel_mesaj_kutusu("Hazır", f"Yaz:\n\n{h}")
    s = time.time(); y = ozel_girdi_al("YAZ!", h); e = time.time()
    if y and y.strip().lower() == h.lower(): ozel_mesaj_kutusu("Harika!", f"Süre: {round(e-s, 2)} s\nHız: {round((4/(e-s))*60)} WPM")
    else: ozel_mesaj_kutusu("Hata", "Yanlış yazdın!")

def baslat_uzay_savasi():
    ozel_mesaj_kutusu("Başlıyor", "🚀 UZAY SAVAŞI\nSağ/Sol: Hareket\nYukarı: Ateş")
    turtle.TurtleScreen._RUNNING=True; e=turtle.Screen(); e.clear(); e.bgcolor("black"); e.setup(600,600); e.tracer(0)
    o=turtle.Turtle(); o.color("#3498db"); o.shape("triangle"); o.penup(); o.speed(0); o.setheading(90); o.goto(0,-250); o.shapesize(1.5,1.5)
    o.h_s = False; o.h_g = False
    def s_b(): o.h_s=True
    def s_d(): o.h_s=False
    def g_b(): o.h_g=True
    def g_d(): o.h_g=False
    l = []; d = []
    for _ in range(3): x = turtle.Turtle(); x.color("#e74c3c"); x.shape("circle"); x.penup(); x.speed(0); x.goto(random.randint(-270,270), random.randint(100,250)); d.append(x)
    p = 0; y=turtle.Turtle(); y.speed(0); y.color("white"); y.penup(); y.hideturtle(); y.goto(0,260); y.write(f"Puan: {p}", align="center", font=("Courier", 18, "bold"))
    def at():
        if len([i for i in l if i.isvisible()])<3: z=turtle.Turtle(); z.color("yellow"); z.shape("square"); z.penup(); z.speed(0); z.shapesize(0.8,0.2); z.setheading(90); z.goto(o.xcor(), o.ycor()+20); l.append(z)
    e.listen(); e.onkeypress(s_b,"Left"); e.onkeyrelease(s_d,"Left"); e.onkeypress(g_b,"Right"); e.onkeyrelease(g_d,"Right"); e.onkeypress(at,"Up")
    ak = True; dh=3
    while ak:
        try:
            e.update()
            if o.h_s and o.xcor()>-270: o.setx(o.xcor()-8)
            if o.h_g and o.xcor()<270: o.setx(o.xcor()+8)
            for z in l:
                if z.isvisible():
                    z.sety(z.ycor()+25)
                    if z.ycor()>280: z.hideturtle()
            for x in d:
                x.sety(x.ycor()-dh)
                if x.ycor()<-280 or o.distance(x)<25: ak=False; break
                for z in l:
                    if z.isvisible() and z.distance(x)<25:
                        z.hideturtle(); z.goto(1000,1000); x.goto(random.randint(-270,270), random.randint(100,250))
                        p+=10; dh+=0.2; y.clear(); y.write(f"Puan: {p}", align="center", font=("Courier", 18, "bold"))
            time.sleep(0.02)
        except: break
    try:
        if not ak: y.goto(0,0); y.color("red"); y.write("OYUN BİTTİ!", align="center", font=("Courier", 30, "bold")); time.sleep(2); e.bye()
    except: pass
    importlib.reload(turtle)

def baslat_aim_trainer():
    ozel_mesaj_kutusu("Aim", "Kırmızı hedeflere hızlıca tıkla! 30sn.")
    turtle.TurtleScreen._RUNNING=True; e=turtle.Screen(); e.clear(); e.bgcolor("#2c3e50"); e.setup(600,600); e.tracer(0)
    h=turtle.Turtle(); h.shape("circle"); h.color("#e74c3c"); h.shapesize(2.5,2.5); h.penup(); h.speed(0)
    d={"p":0, "s":30, "a":True}; y=turtle.Turtle(); y.hideturtle(); y.penup(); y.color("white"); y.goto(0,260)
    def yz(): y.clear(); y.write(f"Skor: {d['p']} | Süre: {d['s']}", align="center", font=("Courier", 16, "bold"))
    def ts(): h.goto(random.randint(-250,250), random.randint(-230,230)); e.update()
    def vr(x,y):
        if d["a"]: d["p"]+=1; yz(); ts()
    h.onclick(vr); ts(); b = time.time()
    while True:
        try:
            d["s"] = max(0, 30-int(time.time()-b)); yz()
            if d["s"]<=0: d["a"]=False; h.hideturtle(); y.goto(0,0); y.color("yellow"); y.write(f"BİTTİ!\nSkor: {d['p']}", align="center", font=("Courier",24,"bold")); e.update(); time.sleep(3); e.bye(); break
            e.update(); time.sleep(0.1)
        except: break
    importlib.reload(turtle)

def baslat_hacker_sim():
    if not messagebox.askyesno("Troll", "Emin misiniz?"): return
    w=tk.Toplevel(root); w.attributes('-fullscreen',True); w.configure(bg="black"); w.attributes("-topmost",True)
    t=tk.Text(w, bg="black", fg="#00FF00", font=("Courier",16,"bold"), borderwidth=0); t.pack(fill="both", expand=True, padx=40, pady=40)
    s = ["Sistem Kırılıyor...","Şifreler Çekildi...","Tüm Veriler Dark Web'te.","SİSTEM32 SİLİNİYOR!"]
    def y(i=0):
        if i<len(s): t.insert(tk.END, s[i]+"\n\n"); t.see(tk.END); w.after(1000, y, i+1)
        else: w.after(1500, b)
    def p():
        if w.winfo_exists():
            x=tk.Toplevel(w); x.geometry(f"300x100+{random.randint(0,1000)}+{random.randint(0,700)}"); x.configure(bg="red")
            tk.Label(x, text="ÇÖKÜŞ!", font=("Arial",14,"bold"), bg="red", fg="white").pack(expand=True); w.after(500, p)
    def b(): t.delete('1.0',tk.END); t.configure(fg="red", font=("Courier",40,"bold")); t.insert(tk.END,"\n\n\n\tSİSTEM TARAFINDAN TROLLENDİNİZ 😎"); w.after(4000, w.destroy)
    y(); w.after(2000, p)

def baslat_ping_pong():
    ozel_mesaj_kutusu("Ping Pong", "🏓 PING PONG\nSol: W/S\nSağ: Yukarı/Aşağı")
    turtle.TurtleScreen._RUNNING=True; e=turtle.Screen(); e.clear(); e.bgcolor("black"); e.setup(800,600); e.tracer(0)
    rs=turtle.Turtle(); rs.shape("square"); rs.color("red"); rs.shapesize(5,1); rs.penup(); rs.goto(-350,0)
    rg=turtle.Turtle(); rg.shape("square"); rg.color("blue"); rg.shapesize(5,1); rg.penup(); rg.goto(350,0)
    t=turtle.Turtle(); t.shape("circle"); t.color("white"); t.penup(); t.goto(0,0); t.dx=6; t.dy=6
    p={"sol":0, "sag":0}; y=turtle.Turtle(); y.speed(0); y.color("white"); y.penup(); y.hideturtle(); y.goto(0,260); y.write("Sol: 0 | Sağ: 0", align="center", font=("Courier",18,"bold"))
    def su(): rs.sety(rs.ycor()+30) if rs.ycor()<240 else None
    def sa(): rs.sety(rs.ycor()-30) if rs.ycor()>-240 else None
    def gu(): rg.sety(rg.ycor()+30) if rg.ycor()<240 else None
    def ga(): rg.sety(rg.ycor()-30) if rg.ycor()>-240 else None
    e.listen(); e.onkeypress(su,"w"); e.onkeypress(sa,"s"); e.onkeypress(gu,"Up"); e.onkeypress(ga,"Down")
    while True:
        try:
            e.update(); t.setx(t.xcor()+t.dx); t.sety(t.ycor()+t.dy)
            if t.ycor()>290 or t.ycor()<-290: t.dy*=-1
            if t.xcor()>390: t.goto(0,0); t.dx*=-1; p["sol"]+=1; y.clear(); y.write(f"Sol: {p['sol']} | Sağ: {p['sag']}", align="center", font=("Courier",18,"bold"))
            if t.xcor()<-390: t.goto(0,0); t.dx*=-1; p["sag"]+=1; y.clear(); y.write(f"Sol: {p['sol']} | Sağ: {p['sag']}", align="center", font=("Courier",18,"bold"))
            if (340<t.xcor()<350) and (rg.ycor()-50<t.ycor()<rg.ycor()+50): t.setx(340); t.dx*=-1.05
            elif (-350<t.xcor()<-340) and (rs.ycor()-50<t.ycor()<rs.ycor()+50): t.setx(-340); t.dx*=-1.05
            if p["sol"]==5 or p["sag"]==5:
                y.goto(0,0); y.color("yellow"); y.write(f"BİTTİ! KAZANAN: {'SOL' if p['sol']==5 else 'SAĞ'}", align="center", font=("Courier",24,"bold")); time.sleep(3); e.bye(); break
            time.sleep(0.02)
        except: break
    importlib.reload(turtle)

def baslat_flappy():
    ozel_mesaj_kutusu("Flappy", "🚁 FLAPPY HELİKOPTER\nBoşluk tuşu ile zıpla. Borulara çarpma!")
    turtle.TurtleScreen._RUNNING=True; e=turtle.Screen(); e.clear(); e.bgcolor("#87CEEB"); e.setup(600,600); e.tracer(0)
    o=turtle.Turtle(); o.shape("square"); o.color("yellow"); o.penup(); o.goto(-200,0); o.dy=0
    bu=turtle.Turtle(); bu.shape("square"); bu.color("green"); bu.shapesize(15,3); bu.penup(); bu.goto(300,250)
    ba=turtle.Turtle(); ba.shape("square"); ba.color("green"); ba.shapesize(15,3); ba.penup(); ba.goto(300,-250)
    p=0; y=turtle.Turtle(); y.speed(0); y.color("black"); y.penup(); y.hideturtle(); y.goto(0,260); y.write(f"Puan: {p}", align="center", font=("Courier",18,"bold"))
    def zp(): o.dy=8
    e.listen(); e.onkeypress(zp,"space"); ak=True; bh=-5
    while ak:
        try:
            o.dy-=0.6; o.sety(o.ycor()+o.dy); bu.setx(bu.xcor()+bh); ba.setx(ba.xcor()+bh)
            if bu.xcor()<-350:
                bu.setx(350); ba.setx(350); yf=random.randint(-80,80); bu.sety(280+yf); ba.sety(-280+yf)
                p+=1; y.clear(); y.write(f"Puan: {p}", align="center", font=("Courier",18,"bold")); bh-=0.1
            if o.ycor()>290 or o.ycor()<-290: ak=False
            if (o.xcor()+10>bu.xcor()-30) and (o.xcor()-10<bu.xcor()+30):
                if (o.ycor()+10>bu.ycor()-150) or (o.ycor()-10<ba.ycor()+150): ak=False
            e.update(); time.sleep(0.02)
        except: break
    try:
        if not ak: y.goto(0,0); y.color("red"); y.write("ÇAKILDIN!", align="center", font=("Courier",30,"bold")); time.sleep(2); e.bye()
    except: pass
    importlib.reload(turtle)

def baslat_kaplumbaga_yarisi():
    renkler = ["red", "blue", "green", "yellow"]; turkce = {"red": "Kırmızı", "blue": "Mavi", "green": "Yeşil", "yellow": "Sarı"}
    sec = ozel_girdi_al("Bahis Yap", "Hangi renk kazanır?\nKırmızı | Mavi | Yeşil | Sarı")
    if not sec: return
    sec = sec.lower().strip(); b = ""
    if sec=="kırmızı": b="red"
    elif sec=="mavi": b="blue"
    elif sec=="yeşil": b="green"
    elif sec=="sarı": b="yellow"
    else: ozel_mesaj_kutusu("Hata", "Geçersiz renk!"); return
    turtle.TurtleScreen._RUNNING = True; e = turtle.Screen(); e.clear(); e.title("Siber Yarış"); e.bgcolor("#2c3e50"); e.setup(600,400)
    bitis = turtle.Turtle(); bitis.penup(); bitis.goto(200, 150); bitis.right(90); bitis.pendown(); bitis.color("white"); bitis.pensize(5); bitis.forward(300); bitis.hideturtle()
    yl = []; yp = [100, 40, -20, -80]
    for i in range(4): k = turtle.Turtle(shape="turtle"); k.color(renkler[i]); k.penup(); k.goto(-250, yp[i]); yl.append(k)
    kr = ""; ak = True
    while ak:
        try:
            for k in yl:
                if k.xcor() > 200: kr = k.pencolor(); ak = False; break
                k.forward(random.randint(1, 5))
            e.update(); time.sleep(0.02)
        except: return
    try:
        if kr == b: ozel_mesaj_kutusu("KAZANDIN!", f"🎉 Bildin! {turkce[kr]} kazandı!")
        else: ozel_mesaj_kutusu("KAYBETTİN!", f"Siz {turkce[b]} dediniz ama {turkce[kr]} kazandı.")
        e.bye()
    except: pass
    importlib.reload(turtle)

def baslat_cizim_tahtasi():
    pencere = tk.Toplevel(root); pencere.title("🎨 Profesyonel Çizim Tahtası"); pencere.geometry("800x600"); pencere.configure(bg="#2c3e50"); pencere.grab_set()
    kalem_rengi = ["black"]; kalem_kalinligi = tk.IntVar(value=3); eski_x, eski_y = [None], [None]
    ust_frame = tk.Frame(pencere, bg="#34495e", pady=10); ust_frame.pack(fill="x")
    def renk_sec():
        secilen = colorchooser.askcolor(color=kalem_rengi[0], title="Renk Seçin")
        if secilen[1]: kalem_rengi[0] = secilen[1]; renk_btn.config(bg=secilen[1])
    def temizle(): tuval.delete("all")
    renk_btn = tk.Button(ust_frame, text="🎨 Renk Seç", font=("Arial", 10, "bold"), command=renk_sec, bg=kalem_rengi[0], fg="white", width=15); renk_btn.pack(side="left", padx=20)
    tk.Label(ust_frame, text="Kalınlık:", bg="#34495e", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)
    tk.Scale(ust_frame, from_=1, to=30, orient="horizontal", variable=kalem_kalinligi, bg="#34495e", fg="white", highlightthickness=0, length=150).pack(side="left", padx=10)
    tk.Button(ust_frame, text="🧹 Temizle", font=("Arial", 10, "bold"), command=temizle, bg="#e74c3c", fg="white", width=15).pack(side="right", padx=20)
    tuval = tk.Canvas(pencere, bg="white", cursor="crosshair"); tuval.pack(fill="both", expand=True, padx=15, pady=15)
    def basla(e): eski_x[0], eski_y[0] = e.x, e.y
    def ciz(e):
        if eski_x[0] and eski_y[0]:
            tuval.create_line(eski_x[0], eski_y[0], e.x, e.y, width=kalem_kalinligi.get(), fill=kalem_rengi[0], capstyle=tk.ROUND, smooth=True); eski_x[0], eski_y[0] = e.x, e.y
    def bitir(e): eski_x[0], eski_y[0] = None, None
    tuval.bind("<Button-1>", basla); tuval.bind("<B1-Motion>", ciz); tuval.bind("<ButtonRelease-1>", bitir)

def baslat_hafiza_oyunu():
    ozel_mesaj_kutusu("Hafıza", "🧠 HAFIZA TESTİ\nEkranda kısacık görünen sayıları aklında tut ve sonra yaz!")
    seviye = 1; uz = 3
    while True:
        h = "".join([str(random.randint(0,9)) for _ in range(uz)])
        w = tk.Toplevel(root); w.title("Ezberle!"); w.geometry("300x150"); w.configure(bg="#2c3e50")
        tk.Label(w, text="Aklında Tut!", font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=10)
        tk.Label(w, text=h, font=("Courier", 35, "bold"), bg="#2c3e50", fg="#f1c40f").pack(pady=10)
        w.update(); time.sleep(1.5); w.destroy()
        c = ozel_girdi_al("Hafıza", "Hangi sayıyı gördün?")
        if c == h: ozel_mesaj_kutusu("Doğru", f"Harika! Seviye {seviye+1} başlıyor."); seviye+=1; uz+=1
        else: ozel_mesaj_kutusu("Yanlış", f"Maalesef!\nDoğrusu: {h}\nUlaştığın Seviye: {seviye}"); break

def baslat_yakala_beni():
    ozel_mesaj_kutusu("Refleks", "⚡ YAKALA BENİ\nKaçan kırmızı butona 20 saniye boyunca tıklamaya çalış!")
    w = tk.Toplevel(root); w.title("Siber Yakala Beni"); w.geometry("500x500"); w.configure(bg="#2c3e50")
    d = {"s":0, "k":20, "a":True}
    lbl = tk.Label(w, text="Skor: 0 | Süre: 20", font=("Arial",14,"bold"), bg="#2c3e50", fg="white"); lbl.pack(pady=10)
    btn = tk.Button(w, text="BANA TIKLA!", font=("Arial",10,"bold"), bg="#e74c3c", fg="white")
    def tkla(e):
        if d["a"]: d["s"]+=1; lbl.config(text=f"Skor: {d['s']} | Süre: {d['k']}"); btn.place(x=random.randint(50,400), y=random.randint(50,400))
    btn.place(x=200, y=200); btn.bind("<Button-1>", tkla)
    def s_say():
        if d["k"]>0 and w.winfo_exists(): d["k"]-=1; lbl.config(text=f"Skor: {d['s']} | Süre: {d['k']}"); w.after(1000, s_say)
        elif w.winfo_exists(): d["a"]=False; btn.destroy(); ozel_mesaj_kutusu("Bitti", f"Süre doldu!\nSkorunuz: {d['s']}"); w.destroy()
    w.after(1000, s_say)

def baslat_elma_yakalama():
    ozel_mesaj_kutusu("Elma", "🍎 ELMA YAKALAMA\nSağ/Sol oklarla sepeti yönet. 3 elma kaçırırsan yanarsın!")
    turtle.TurtleScreen._RUNNING = True; e = turtle.Screen(); e.clear(); e.bgcolor("lightgreen"); e.title("Siber Elma"); e.setup(600,600); e.tracer(0)
    s = turtle.Turtle(); s.shape("square"); s.color("brown"); s.shapesize(1,4); s.penup(); s.goto(0,-250)
    el = [turtle.Turtle() for _ in range(5)]
    for x in el: x.shape("circle"); x.color("red"); x.penup(); x.goto(random.randint(-280,280), random.randint(100,300))
    d = {"p":0, "k":0, "h":3}; y = turtle.Turtle(); y.hideturtle(); y.penup(); y.goto(0,260)
    def sol(): s.setx(s.xcor()-30) if s.xcor()>-240 else None
    def sag(): s.setx(s.xcor()+30) if s.xcor()<240 else None
    e.listen(); e.onkeypress(sol,"Left"); e.onkeypress(sag,"Right")
    ak = True
    while ak:
        try:
            e.update()
            for x in el:
                x.sety(x.ycor()-d["h"])
                if (s.ycor()-20 < x.ycor() < s.ycor()+20) and (s.xcor()-50 < x.xcor() < s.xcor()+50):
                    x.goto(random.randint(-280,280), random.randint(250,300)); d["p"]+=10; d["h"]+=0.1
                    y.clear(); y.write(f"Skor: {d['p']} Kaçan: {d['k']}/3", align="center", font=("Arial", 16, "bold"))
                if x.ycor() < -290:
                    x.goto(random.randint(-280,280), random.randint(250,300)); d["k"]+=1
                    y.clear(); y.write(f"Skor: {d['p']} Kaçan: {d['k']}/3", align="center", font=("Arial", 16, "bold"))
                    if d["k"]>=3: ak=False; break
            time.sleep(0.02)
        except: break
    try:
        if not ak: y.goto(0,0); y.color("red"); y.write("OYUN BİTTİ!", align="center", font=("Arial",30,"bold")); time.sleep(2); e.bye()
    except: pass
    importlib.reload(turtle)

# ==========================================
# YAPAY ZEKA VE BULUT ASİSTANI
# ==========================================
def baslat_yapay_zeka():
    soru = ozel_girdi_al("Yapay Zeka Asistanı", "Bana ne sormak istersiniz?")
    if soru:
        try:
            ozel_mesaj_kutusu("Bekle", "Veriler internetten taranıyor...")
            cevap = wikipedia.summary(soru)
            ozel_mesaj_kutusu(f"🤖 Yapay Zeka: {soru}", cevap)
        except: ozel_mesaj_kutusu("Hata", "Sonuç bulunamadı veya bağlantı hatası!")

def baslat_sifre_degistir():
    p = tk.Toplevel(root); p.title("Şifre Değiştir"); p.geometry("350x300"); p.configure(bg="#2c3e50"); p.grab_set()
    tk.Label(p, text="Eski Şifreniz:", font=("Arial",12,"bold"), bg="#2c3e50", fg="#1ebca1").pack(pady=(20,5))
    e1 = tk.Entry(p, show="*", font=("Arial",14), justify="center"); e1.pack(pady=5)
    tk.Label(p, text="Yeni Şifreniz:", font=("Arial",12,"bold"), bg="#2c3e50", fg="#1ebca1").pack(pady=(15,5))
    e2 = tk.Entry(p, show="*", font=("Arial",14), justify="center"); e2.pack(pady=5)
    def dg():
        if e1.get() == sifre_getir():
            if len(e2.get())>0: sifre_kaydet(e2.get()); p.destroy(); ozel_mesaj_kutusu("Başarılı", "Şifreniz güncellendi!")
            else: ozel_mesaj_kutusu("Hata", "Boş bırakılamaz!")
        else: ozel_mesaj_kutusu("Hata", "Eski şifre yanlış!")
    tk.Button(p, text="KAYDET", command=dg, font=("Arial",12,"bold"), bg="#f39c12", fg="white").pack(pady=20)

def internet_var_mi():
    try:
        urllib.request.urlopen('http://google.com', timeout=3)
        return True
    except: return False

def sistemi_guncelle():
    if not internet_var_mi():
        ozel_mesaj_kutusu("Bağlantı Hatası", "İnternet bağlantısı bulunamadı!\nLütfen ağ bağlantınızı kontrol edin.")
        return
    
    w = tk.Toplevel(root); w.title("Bulut Sunucu"); w.geometry("400x200"); w.configure(bg="#2c3e50"); w.grab_set()
    tk.Label(w, text="Ana Sunuculara Bağlanılıyor...", font=("Arial", 12, "bold"), bg="#2c3e50", fg="#1ebca1").pack(pady=30)
    w.update(); time.sleep(1.5)
    tk.Label(w, text=f"Mevcut Sürüm: {SISTEM_SURUMU}\nGüncellemeler denetleniyor...", font=("Arial", 11), bg="#2c3e50", fg="white").pack(pady=10)
    w.update(); time.sleep(1.5)
    
    try:
        # GITHUB BAĞLANTISI (Burası sabit kalmalı)
        url = "https://raw.githubusercontent.com/YusufSiber/SiberSistem/main/version.txt"
        cevap = urllib.request.urlopen(url, timeout=5)
        sunucu_surumu = cevap.read().decode('utf-8').strip()
        w.destroy()
        
        if float(sunucu_surumu) > float(SISTEM_SURUMU):
            github_link = "https://github.com/YusufSiber/SiberSistem"
            mesaj = f"🚀 YENİ GÜNCELLEME BULUNDU!\n\nSunucudaki Sürüm: v{sunucu_surumu}\nSizin Sürümünüz: v{SISTEM_SURUMU}\n\nTamam'a bastığınızda indirme sayfasına yönlendirileceksiniz!"
            ozel_mesaj_kutusu("Güncelleme Mevcut!", mesaj)
            webbrowser.open(github_link) 
        else:
            ozel_mesaj_kutusu("Sistem Güncel", f"Harika! Şu anda sistemin en güncel versiyonunu (v{SISTEM_SURUMU}) kullanıyorsunuz.\n\nYeni bir güncelleme bulunmuyor.")
            
    except Exception as e:
        w.destroy(); ozel_mesaj_kutusu("Sunucu Hatası", "Ana sunuculara ulaşılamadı. Lütfen daha sonra tekrar deneyin.")

def guncelleme_yayinla():
    admin_pass = ozel_girdi_al("Yönetici Girişi", "GELİŞTİRİCİ ŞİFRESİ GEREKLİ:", gizli=True)
    if admin_pass != "2372": ozel_mesaj_kutusu("Erişim Engellendi", "Yanlış Şifre!"); return
    ozel_mesaj_kutusu("Geliştirici Paneli", "Sayın Geliştirici,\n\nKodlarınızı güncellemek için doğrudan github.com/YusufSiber/SiberSistem adresine gidip yeni dosyalarınızı yükleyin ve version.txt dosyasındaki sayıyı artırın.")


# ==========================================
# ANA UYGULAMA ARAYÜZÜ 
# ==========================================
root = tk.Tk()
root.title(f"Siber Sistem (v{SISTEM_SURUMU})")

window_w = 750; window_h = 550
x_center = (root.winfo_screenwidth() // 2) - (window_w // 2)
y_center = (root.winfo_screenheight() // 2) - (window_h // 2)
root.geometry(f"{window_w}x{window_h}+{x_center}+{y_center}"); root.configure(bg="#2c3e50"); root.resizable(False, False) 

ilk_kurulum_frame = tk.Frame(root, bg="#2c3e50")
login_frame = tk.Frame(root, bg="#2c3e50")
menu_frame = tk.Frame(root, bg="#2c3e50")

# ----- İLK KURULUM EKRANI -----
tk.Label(ilk_kurulum_frame, text="SİSTEME HOŞ GELDİNİZ", font=("Courier", 20, "bold"), bg="#2c3e50", fg="#1ebca1").pack(pady=(80, 20))
tk.Label(ilk_kurulum_frame, text="Lütfen sisteminiz için kalıcı bir giriş şifresi belirleyin:", font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=10)
yeni_sifre_entry = tk.Entry(ilk_kurulum_frame, font=("Arial", 18), show="*", justify="center", bg="#34495e", fg="white")
yeni_sifre_entry.pack(pady=10)

def ilk_sifreyi_kaydet():
    sifre = yeni_sifre_entry.get()
    if len(sifre) >= 3:
        sifre_kaydet(sifre)
        ozel_mesaj_kutusu("Kurulum Başarılı", "Şifreniz başarıyla sisteme kaydedildi!\n\nArtık programı her açtığınızda bu şifreyi kullanacaksınız.")
        ilk_kurulum_frame.pack_forget()
        login_frame.pack(fill="both", expand=True) 
        sifre_entry.focus()
    else:
        ozel_mesaj_kutusu("Hata", "Lütfen en az 3 karakterli bir şifre girin!")

tk.Button(ilk_kurulum_frame, text="ŞİFREYİ KAYDET", font=("Arial", 14, "bold"), bg="#27ae60", fg="white", command=ilk_sifreyi_kaydet, width=20).pack(pady=20)


# ----- GÜVENLİK DUVARI (GİRİŞ EKRANI) -----
tk.Label(login_frame, text="SİSTEME GİRİŞ YAPILMALI", font=("Courier", 20, "bold"), bg="#2c3e50", fg="#1ebca1").pack(pady=80)
tk.Label(login_frame, text="Güvenlik Şifresi:", font=("Arial", 14), bg="#2c3e50", fg="white").pack(pady=10)
sifre_entry = tk.Entry(login_frame, font=("Arial", 18), show="*", justify="center", bg="#34495e", fg="white")
sifre_entry.pack(pady=10)

def giris_kontrol():
    if sifre_entry.get() == sifre_getir(): 
        login_frame.pack_forget()
        menu_frame.pack(fill="both", expand=True)
        ozel_mesaj_kutusu("Başarılı", "Sisteme Hoş Geldiniz!")
    else: 
        sifre_entry.delete(0, tk.END)
        ozel_mesaj_kutusu("HATA", "Yanlış Şifre!")

tk.Button(login_frame, text="GİRİŞ YAP", font=("Arial", 14, "bold"), bg="#1ebca1", fg="white", command=giris_kontrol, width=15).pack(pady=20)

def enter_basildi(event):
    if login_frame.winfo_ismapped(): giris_kontrol()
    elif ilk_kurulum_frame.winfo_ismapped(): ilk_sifreyi_kaydet()

root.bind('<Return>', enter_basildi)

# ----- ÇİFT SÜTUNLU ANA MENÜ -----
tk.Label(menu_frame, text="SİBER KONTROL PANELİ", font=("Arial", 18, "bold"), bg="#2c3e50", fg="#1ebca1").pack(pady=5)
grid_frame = tk.Frame(menu_frame, bg="#2c3e50"); grid_frame.pack(pady=5)
btn_style = {"font": ("Arial", 11), "bg": "#34495e", "fg": "white", "width": 35, "pady": 2}

tk.Button(grid_frame, text="1. 🐍 Yılan Oyunu", command=baslat_turtle_oyunu, **btn_style).grid(row=0, column=0, padx=10, pady=2)
tk.Button(grid_frame, text="2. 🧮 Hesap Makinesi", command=baslat_hesap_makinesi, **btn_style).grid(row=1, column=0, padx=10, pady=2)
tk.Button(grid_frame, text="3. 📞 Akıllı Rehber", command=baslat_rehber, **btn_style).grid(row=2, column=0, padx=10, pady=2)
tk.Button(grid_frame, text="4. 🔮 Sayı Tahmin Oyunu", command=baslat_sayi_tahmin, **btn_style).grid(row=3, column=0, padx=10, pady=2)
tk.Button(grid_frame, text="5. ✌️ Taş-Kağıt-Makas", command=baslat_tas_kagit_makas, **btn_style).grid(row=4, column=0, padx=10, pady=2)
tk.Button(grid_frame, text="6. 🕵️ Adam Asmaca", command=baslat_adam_asmaca, **btn_style).grid(row=5, column=0, padx=10, pady=2)
tk.Button(grid_frame, text="7. 🔐 Şifre Oluşturucu", command=baslat_sifre_olusturucu, **btn_style).grid(row=6, column=0, padx=10, pady=2)
tk.Button(grid_frame, text="8. 📝 Görev Yöneticisi", command=baslat_gorev_yoneticisi, **btn_style).grid(row=7, column=0, padx=10, pady=2)
tk.Button(grid_frame, text="9. ❌ Görsel XOX", command=baslat_xox, **btn_style).grid(row=8, column=0, padx=10, pady=2)
tk.Button(grid_frame, text="10. ⌨️ Klavye Hız Testi", command=baslat_klavye_testi, **btn_style).grid(row=9, column=0, padx=10, pady=2)
tk.Button(grid_frame, text="11. 🚀 Uzay Gemisi Savaşı", command=baslat_uzay_savasi, **btn_style).grid(row=0, column=1, padx=10, pady=2)
tk.Button(grid_frame, text="12. 🎯 Nişancı (Aim) Trainer", command=baslat_aim_trainer, **btn_style).grid(row=1, column=1, padx=10, pady=2)
tk.Button(grid_frame, text="13. 💀 Hacker Simülatörü (Troll)", command=baslat_hacker_sim, **btn_style).grid(row=2, column=1, padx=10, pady=2)
tk.Button(grid_frame, text="14. 🏓 Retro Ping Pong", command=baslat_ping_pong, **btn_style).grid(row=3, column=1, padx=10, pady=2)
tk.Button(grid_frame, text="15. 🚁 Flappy Helikopter", command=baslat_flappy, **btn_style).grid(row=4, column=1, padx=10, pady=2)
tk.Button(grid_frame, text="16. 🏁 Kaplumbağa Yarışı", command=baslat_kaplumbaga_yarisi, **btn_style).grid(row=5, column=1, padx=10, pady=2)
tk.Button(grid_frame, text="17. 🎨 Çizim Tahtası", command=baslat_cizim_tahtasi, **btn_style).grid(row=6, column=1, padx=10, pady=2)
tk.Button(grid_frame, text="18. 🧠 Hafıza Testi", command=baslat_hafiza_oyunu, **btn_style).grid(row=7, column=1, padx=10, pady=2)
tk.Button(grid_frame, text="19. ⚡ Yakala Beni", command=baslat_yakala_beni, **btn_style).grid(row=8, column=1, padx=10, pady=2)
tk.Button(grid_frame, text="20. 🍎 Elma Yakalama", command=baslat_elma_yakalama, **btn_style).grid(row=9, column=1, padx=10, pady=2)

bulut_frame = tk.Frame(menu_frame, bg="#2c3e50"); bulut_frame.pack(fill="x", padx=30, pady=10)
tk.Button(bulut_frame, text="⬇️ Sistemi Güncelle", command=sistemi_guncelle, font=("Arial", 11, "bold"), bg="#3498db", fg="white", width=20).pack(side="left", padx=5)
tk.Button(bulut_frame, text="🤖 Yapay Zeka Asistanı", command=baslat_yapay_zeka, font=("Arial", 12, "bold"), bg="#27ae60", fg="white", width=25).pack(side="left", padx=10)
tk.Button(bulut_frame, text="☁️ Güncelleme Yayınla", command=guncelleme_yayinla, font=("Arial", 11, "bold"), bg="#9b59b6", fg="white", width=20).pack(side="right", padx=5)

alt_frame = tk.Frame(menu_frame, bg="#2c3e50"); alt_frame.pack(fill="x", padx=40, pady=(5, 0))
tk.Button(alt_frame, text="⚙️ Şifre Değiştir", command=baslat_sifre_degistir, font=("Arial", 10, "bold"), bg="#f39c12", fg="white", width=15).pack(side="left")
tk.Button(alt_frame, text="ÇIKIŞ", command=root.quit, font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", width=15).pack(side="right")

if sifre_dosyasi_var_mi():
    login_frame.pack(fill="both", expand=True)
    sifre_entry.focus()
else:
    ilk_kurulum_frame.pack(fill="both", expand=True)
    yeni_sifre_entry.focus()

root.mainloop()
