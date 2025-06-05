"""
Kedi Hikaye Görsel Üretici - Sahne Üretici Modülü
Geliştirici: @burakkocin
Oluşturma Tarihi: 2025-06-05 17:09:20 UTC
Versiyon: 3.0
"""

import json
import re
import random
from datetime import datetime

def ai_ile_sahneler_uret(baslik, sahne_sayisi=8):
    """
    Yapay zeka ile dinamik ve detaylı sahne üretici
    - Minimal ve sevimli stil
    - Chibi tarzı karakterler
    - Pastel renk paleti
    - Basit ve temiz kompozisyonlar
    """
    print(f"🤖 '{baslik}' için {sahne_sayisi} sahne üretiliyor...")
    
    # Hikaye analizi
    hikaye_detaylari = hikayeyi_analiz_et(baslik)
    
    # Sahne üretimi
    sahneler = detayli_sahne_uret(hikaye_detaylari, sahne_sayisi)
    
    return sahneler

def hikayeyi_analiz_et(baslik):
    """Hikayeyi analiz edip detayları çıkarır"""
    baslik_lower = baslik.lower()
    kelimeler = baslik_lower.split()
    
    detaylar = {
        "ana_eylem": kelimeler[-1],
        "mekan": mekan_belirle(baslik_lower),
        "zaman": zaman_belirle(baslik_lower),
        "hava_durumu": random.choice(["sunny", "with soft clouds", "with gentle rain", "with snowflakes"]),
        "ruh_hali": ruh_hali_belirle(baslik_lower),
        "ekipmanlar": ekipman_belirle(baslik_lower),
        "kiyafetler": kiyafet_belirle(baslik_lower),
        "tema": tema_belirle(baslik_lower)
    }
    
    return detaylar

def mekan_belirle(baslik):
    """Minimal ve sevimli mekanlar"""
    mekanlar = {
        "okul": [
            "cute classroom with pastel walls and tiny desks",
            "kawaii school garden with pink cherry blossoms",
            "adorable library with floating books",
            "sweet playground with colorful equipment",
            "magical school corridor with pastel lockers"
        ],
        "ev": [
            "cozy pastel room with floating stars",
            "cute kitchen with magical appliances",
            "sweet garden with rainbow flowers",
            "adorable living room with floating cushions",
            "magical bedroom with twinkling lights"
        ],
        "doğa": [
            "cute forest with pastel mushrooms",
            "kawaii park with rainbow slides",
            "sweet lake with heart-shaped clouds",
            "adorable meadow with dancing flowers",
            "magical garden with glowing butterflies"
        ],
        "şehir": [
            "cute street with candy-colored buildings",
            "kawaii cafe with floating sweets",
            "sweet shop with magical items",
            "adorable plaza with musical fountains",
            "magical city with rainbow paths"
        ]
    }
    
    if "okul" in baslik:
        return mekanlar["okul"]
    elif "ev" in baslik:
        return mekanlar["ev"]
    elif any(kelime in baslik for kelime in ["orman", "doğa", "park", "bahçe"]):
        return mekanlar["doğa"]
    else:
        return mekanlar["şehir"]

def zaman_belirle(baslik):
    """Hikayeye uygun zaman belirler"""
    if "sabah" in baslik:
        return "with morning sparkles"
    elif "akşam" in baslik or "gece" in baslik:
        return "with twinkling stars"
    else:
        return random.choice([
            "with morning sparkles",
            "with afternoon glow",
            "with sunset colors",
            "with twinkling stars"
        ])

def ruh_hali_belirle(baslik):
    """Kedinin ruh halini belirler"""
    if any(kelime in baslik for kelime in ["mutlu", "sevinç", "eğlen"]):
        return "super happy with sparkling eyes"
    elif any(kelime in baslik for kelime in ["üzgün", "mutsuz"]):
        return "thoughtful with gentle smile"
    else:
        return random.choice([
            "excited with bouncing joy",
            "curious with twinkling eyes",
            "happy with flowing energy",
            "peaceful with soft smile"
        ])

def ekipman_belirle(baslik):
    """Hikayeye uygun minimal sevimli ekipmanları belirler"""
    ekipman_setleri = {
        "okul": [
            "magical floating pencils",
            "glowing notebook",
            "rainbow backpack",
            "star-shaped books",
            "heart-shaped tablet"
        ],
        "spor": [
            "bouncing magical ball",
            "rainbow water bottle",
            "star-shaped towel",
            "glowing sports shoes"
        ],
        "sanat": [
            "floating paint brushes",
            "rainbow palette",
            "magical canvas",
            "glowing art supplies"
        ],
        "macera": [
            "magical adventure map",
            "glowing compass",
            "rainbow backpack",
            "star-shaped flashlight"
        ],
        "parti": [
            "floating party balloons",
            "magical party hat",
            "rainbow gift box",
            "glowing decorations"
        ]
    }
    
    for tema, ekipmanlar in ekipman_setleri.items():
        if tema in baslik:
            return ekipmanlar
    return ekipman_setleri["macera"]

def kiyafet_belirle(baslik):
    """Hikayeye uygun kıyafetleri belirler"""
    kiyafet_setleri = {
        "okul": [
            "fitted white t-shirt with school logo, dark blue jeans, leather backpack",
            "smart casual blazer, crisp white shirt, tailored pants",
            "varsity jacket, comfortable jeans, sports sneakers",
            "professional looking suit with school tie, polished shoes"
        ],
        "spor": [
            "fitted workout tank top showing muscles, athletic shorts",
            "modern track suit with brand logos, premium sports shoes",
            "sleeveless training shirt, compression pants, gym gloves",
            "professional sports uniform, high-end running shoes"
        ],
        "günlük": [
            "tight-fitting white t-shirt showing muscular build, ripped jeans",
            "stylish casual shirt with rolled sleeves, designer jeans",
            "form-fitting polo shirt, premium chinos, leather belt",
            "trendy streetwear with modern urban style"
        ],
        "macera": [
            "rugged adventure vest with many pockets, cargo pants",
            "durable hiking outfit with protective gear",
            "tactical clothing with utility belt, sturdy boots",
            "explorer outfit with weather-resistant materials"
        ]
    }
    
    for tema, kiyafetler in kiyafet_setleri.items():
        if tema in baslik:
            return kiyafetler
    return kiyafet_setleri["günlük"]

def sahne_formati_olustur(karakter, mekan, kiyafet, ekipman, ruh_hali, hava, zaman, eylem):
    """3D gerçekçi sahne formatı"""
    return f"3D render of {karakter}, {ruh_hali}, wearing {kiyafet}, in a {mekan} {hava} {zaman}, with {ekipman}, {eylem}, Pixar style animation, modern CGI, cinematic lighting, photorealistic textures, high end character design, depth of field, dramatic composition"

def tema_belirle(baslik):
    """Hikayenin ana temasını belirler"""
    if "okul" in baslik:
        return "magical school life"
    elif any(kelime in baslik for kelime in ["macera", "keşif", "yolculuk"]):
        return "magical adventure"
    elif any(kelime in baslik for kelime in ["parti", "kutlama", "eğlence"]):
        return "magical celebration"
    elif any(kelime in baslik for kelime in ["yardım", "destek", "iyilik"]):
        return "magical helping"
    else:
        return "magical daily life"

def detayli_sahne_uret(detaylar, sahne_sayisi):
    """Detaylı sahne üretimi yapar"""
    sahneler = []
    
    # Giriş sahnesi
    giris_sahnesi = sahne_formati_olustur(
        "cute chibi orange cat",
        detaylar["mekan"][0],
        detaylar["kiyafetler"][0],
        detaylar["ekipmanlar"][0],
        detaylar["ruh_hali"],
        detaylar["hava_durumu"],
        detaylar["zaman"],
        "starting the story"
    )
    sahneler.append(giris_sahnesi)
    
    # Gelişme sahneleri
    for i in range(sahne_sayisi - 2):
        mekan = random.choice(detaylar["mekan"])
        kiyafet = random.choice(detaylar["kiyafetler"])
        ekipman = random.choice(detaylar["ekipmanlar"])
        
        sahne = sahne_formati_olustur(
            "cute chibi orange cat",
            mekan,
            kiyafet,
            ekipman,
            detaylar["ruh_hali"],
            detaylar["hava_durumu"],
            detaylar["zaman"],
            detaylar["ana_eylem"]
        )
        sahneler.append(sahne)
    
    # Sonuç sahnesi
    sonuc_sahnesi = sahne_formati_olustur(
        "cute chibi orange cat",
        detaylar["mekan"][-1],
        detaylar["kiyafetler"][-1],
        detaylar["ekipmanlar"][-1],
        "super happy with sparkling eyes",
        detaylar["hava_durumu"],
        "with magical evening glow",
        "completing the story with joy"
    )
    sahneler.append(sonuc_sahnesi)
    
    return sahneler

def sahne_formati_olustur(karakter, mekan, kiyafet, ekipman, ruh_hali, hava, zaman, eylem):
    """Minimal sevimli sahne formatı"""
    return f"flat 2D illustration of a {karakter}, {ruh_hali}, {kiyafet}, {eylem}, {mekan}, {hava}, vector art style, kawaii mascot design, simple geometric background shapes, pastel color palette, clean minimalist design, Japanese illustration style, perfect symmetry, soft gradients"