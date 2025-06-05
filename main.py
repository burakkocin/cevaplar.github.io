"""
Kedi Video Sistemi
Geliştirici: @burakkocin
Oluşturma Tarihi: 2025-06-05 21:07:15
Versiyon: 6.0
"""

import json
import requests
from datetime import datetime

# Sistem sabitleri
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:latest"
SYSTEM_PROMPT = """You are a creative storyteller specialized in creating Pixar/Disney/Zootopia style stories."""

# Stil ayarları - Optimizasyon yapıldı
STIL = """
(anthropomorphic:1.4), (3d character:1.4), (zootopia style:1.4), (cat character:1.4),
detailed fur, muscular build, high detail face, atmospheric lighting, 
cinematic composition, professional lighting, high end character design,
unreal engine 5, octane render, ray tracing, subsurface scattering
"""

SABIT_KEDI = """
muscular orange tabby cat, anthropomorphic cat character, strong feline features,
cat face with cat nose and whiskers, pointed cat ears, emerald green eyes,
athletic physique, broad shoulders, detailed fur grooming, disney character appeal,
NO HUMAN FACE, NO ANIME STYLE, professional 3D modeling, pixar quality rendering
"""

NEGATIVE_PROMPT = """
(human:1.6), (human face:1.6), (anime:1.6), (manga:1.6),
text, watermark, signature, blurry, low quality, bad art,
deformed, distorted, disfigured, bad anatomy, bad proportions,
extra limbs, duplicate, morbid, photorealistic face, human features
"""

class HikayeGenerator:
    def __init__(self):
        self.model = MODEL_NAME
        self.creation_time = "2025-06-05 21:07:15"
        self.user = "burakkocin"

    def sahnelere_cevir(self, hikaye_json):
        """JSON hikayeyi görsel üretim için sahne formatına çevirir"""
        sahneler = []
        
        for sahne in hikaye_json:
            # Props listesini düz metne çevir
            props = sahne['props']
            if isinstance(props, list):
                props = ', '.join(props)
                
            # Daha detaylı prompt yapısı
            prompt = f"""
(masterpiece:1.4), (best quality:1.4), (ultra detailed:1.3),
{SABIT_KEDI},
(detailed environment): {sahne['mekan']},
(character action): {sahne['eylem']},
(wearing): {sahne['kiyafet']},
(character expression): {sahne['durum']},
(scene details): {props},
{STIL}
""".strip()
            
            sahneler.append({
                "sahne_no": sahne["sahne_no"],
                "prompt": prompt,
                "negative_prompt": NEGATIVE_PROMPT,
                "detay": sahne,
                "created_at": self.creation_time,
                "created_by": self.user
            })
        
        return sahneler

    def hikaye_uret(self, ana_metin):
        """İngilizce hikaye üretimi"""
        prompt = f"""
Create a detailed 8-scene story about an anthropomorphic cat character.
Main plot: {ana_metin}

Return ONLY a JSON array with 8 scenes. Each scene object must have these exact fields:
- sahne_no: scene number (1-8)
- mekan: detailed scene location in English
- eylem: what the cat is doing in English
- kiyafet: what the cat is wearing in English
- durum: cat's mood and expression in English
- props: important objects in scene (as string, not array)

Requirements:
1. Each scene must be extremely detailed and visually rich
2. The cat character must be an anthropomorphic muscular orange tabby cat
3. Use modern, impressive locations
4. Create a logical story flow from scene to scene
5. Each scene should follow naturally from the previous one
6. Focus on creating Pixar/Disney/Zootopia style scenes
7. Keep consistent character appearance throughout

Return ONLY the JSON array. Do not include any other text.
"""
        try:
            response = self.ollama_request(prompt)
            if not response:
                return self.yedek_hikaye_uret(ana_metin)
                
            json_str = response.strip()
            json_str = json_str.replace("```json", "").replace("```", "").strip()
            
            if "[" not in json_str:
                print("⚠️ Geçersiz JSON formatı, yedek hikaye kullanılıyor...")
                return self.yedek_hikaye_uret(ana_metin)
                
            json_str = json_str[json_str.find("["):json_str.rfind("]")+1]
            hikaye = json.loads(json_str)
            
            if len(hikaye) != 8:
                print("⚠️ Eksik sahne sayısı, yedek hikaye kullanılıyor...")
                return self.yedek_hikaye_uret(ana_metin)
            
            return self.sahnelere_cevir(hikaye)
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON ayrıştırma hatası: {e}")
            return self.yedek_hikaye_uret(ana_metin)
        except Exception as e:
            print(f"⚠️ Hikaye üretim hatası: {e}")
            return self.yedek_hikaye_uret(ana_metin)

    def yedek_hikaye_uret(self, ana_metin):
        """Basit yedek hikaye şablonu"""
        temel_sahneler = []
        eylemler = ana_metin.lower().split()
        
        if "school" in eylemler or "okul" in eylemler:
            temel_sahneler = [
                {
                    "sahne_no": 1,
                    "mekan": "modern school entrance with impressive glass architecture",
                    "eylem": "walking confidently towards the school entrance",
                    "kiyafet": "smart casual outfit with designer backpack",
                    "durum": "confident and excited expression, whiskers twitching with anticipation",
                    "props": "modern school building, other anthropomorphic students in background"
                },
                {
                    "sahne_no": 2,
                    "mekan": "bright modern classroom with large windows",
                    "eylem": "sitting attentively at the front desk",
                    "kiyafet": "neat school uniform with stylish tie",
                    "durum": "focused and engaged expression, ears perked forward with interest",
                    "props": "interactive whiteboard, modern desk setup, textbooks"
                }
            ]
        else:
            temel_sahneler = [
                {
                    "sahne_no": 1,
                    "mekan": "modern city street with impressive skyscrapers",
                    "eylem": "walking confidently down the sidewalk",
                    "kiyafet": "stylish casual wear with designer accessories",
                    "durum": "confident and charismatic expression, tail held high",
                    "props": "luxury cars, modern buildings, city life atmosphere"
                },
                {
                    "sahne_no": 2,
                    "mekan": "upscale coffee shop with modern interior",
                    "eylem": "enjoying a gourmet coffee",
                    "kiyafet": "business casual attire",
                    "durum": "relaxed and sophisticated expression, whiskers twitching with pleasure",
                    "props": "designer coffee cup, laptop, ambient lighting"
                }
            ]
            
        # 8 sahneye tamamla
        while len(temel_sahneler) < 8:
            sahne_no = len(temel_sahneler) + 1
            if "school" in eylemler or "okul" in eylemler:
                temel_sahneler.append({
                    "sahne_no": sahne_no,
                    "mekan": "various school locations",
                    "eylem": "engaged in school activities",
                    "kiyafet": "appropriate school attire",
                    "durum": "focused and interactive expression, ears showing attention",
                    "props": "school supplies, educational materials, modern classroom equipment"
                })
            else:
                temel_sahneler.append({
                    "sahne_no": sahne_no,
                    "mekan": "continuing urban locations",
                    "eylem": "various city activities",
                    "kiyafet": "fashionable urban wear",
                    "durum": "confident and engaged expression, tail showing mood",
                    "props": "modern city elements, urban lifestyle accessories"
                })
            
        return self.sahnelere_cevir(temel_sahneler)

    def ollama_request(self, prompt):
        """Ollama API'ye istek gönderir"""
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": self.model,
                "prompt": prompt,
                "system": SYSTEM_PROMPT,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "top_k": 50,
                    "num_predict": 2000,
                    "stop": ["```"]
                }
            })
            if response.status_code == 200:
                return response.json()["response"]
            else:
                print(f"⚠️ Ollama API Hatası: {response.status_code}")
                return None
        except Exception as e:
            print(f"⚠️ Ollama Bağlantı Hatası: {e}")
            return None

def main():
    try:
        hikaye_gen = HikayeGenerator()
        hikaye = hikaye_gen.hikaye_uret("kedi okula gidiyor")
        
        print(f"\n✨ Hikaye başarıyla oluşturuldu!")
        print(f"📅 Oluşturma Tarihi: {hikaye_gen.creation_time}")
        print(f"👤 Oluşturan: {hikaye_gen.user}")
        print("\n🎬 Sahneler:")
        
        for sahne in hikaye:
            print(f"\n📺 Sahne {sahne['sahne_no']}:")
            print(f"Mekan: {sahne['detay']['mekan']}")
            print(f"Eylem: {sahne['detay']['eylem']}")
            print(f"Kiyafet: {sahne['detay']['kiyafet']}")
            print(f"Durum: {sahne['detay']['durum']}")
            print(f"Props: {sahne['detay']['props']}")
            
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    main()