import openai
from datetime import datetime

class HikayeGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
        
    def hikaye_uret(self, ana_metin):
        """Ana metinden detaylı hikaye üretir"""
        
        # GPT prompt template
        prompt = f"""
        Bir çizgi film için kısa bir hikaye yaz. Ana karakter kaslı, güçlü bir kedi.
        Ana olay: {ana_metin}
        
        Hikaye şu özelliklere sahip olmalı:
        - 8 sahnelik bir hikaye
        - Her sahne aksiyon dolu ve görsel olarak etkileyici
        - Kaslı kedi karakteri hep güçlü ve karizmatik
        - Modern, lüks ve etkileyici mekanlar
        - Mantıklı bir hikaye akışı
        - Her sahne bir öncekinin devamı niteliğinde
        - Kedi karakteri tutarlı (hep ayakta ve güçlü)
        
        Çıktı formatı:
        [
          {
            "sahne_no": 1,
            "mekan": "detaylı mekan açıklaması",
            "eylem": "kedinin ne yaptığı",
            "kiyafet": "kedinin kıyafeti",
            "durum": "kedinin ruh hali ve duruşu",
            "props": "sahnedeki önemli objeler"
          },
          ...devamı
        ]
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen bir profesyonel senaryo yazarısın."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # GPT'den gelen JSON formatındaki hikayeyi parse et
            hikaye = eval(response.choices[0].message.content)
            return self.sahnelere_cevir(hikaye)
            
        except Exception as e:
            print(f"Hikaye üretim hatası: {e}")
            return self.yedek_hikaye_uret(ana_metin)
    
    def sahnelere_cevir(self, hikaye_json):
        """JSON formatındaki hikayeyi görsel prompt'lara çevirir"""
        sahneler = []
        
        for sahne in hikaye_json:
            prompt = f"""3D render of muscular anthropomorphic orange tabby cat,
                        {sahne['durum']},
                        wearing {sahne['kiyafet']},
                        {sahne['eylem']},
                        in a {sahne['mekan']},
                        with {sahne['props']},
                        Pixar style animation,
                        modern CGI,
                        cinematic lighting,
                        photorealistic textures,
                        high end character design,
                        depth of field,
                        dramatic composition,
                        high detail facial expressions,
                        ultra realistic fur and materials"""
            
            sahneler.append({
                "sahne_no": sahne["sahne_no"],
                "prompt": prompt,
                "detay": sahne
            })
        
        return sahneler
    
    def yedek_hikaye_uret(self, ana_metin):
        """GPT çalışmazsa basit bir hikaye üretir"""
        # Basit hikaye şablonları
        return basit_hikaye_sablonu(ana_metin)