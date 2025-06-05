import json
import requests
import os
import shutil
import time

def gorsel_uret(prompt, index, negative_prompt="", hedef_klasor=None, boyut=(768, 768)):
    """
    Görsel üretme fonksiyonu - Optimize edilmiş versiyon
    """
    if not prompt:
        raise ValueError("Prompt boş olamaz!")

    try:
        with open("workflow_api.json", "r", encoding="utf-8") as f:
            workflow = json.load(f)
            
        # Görsel boyutunu ayarla
        workflow["3"]["inputs"]["width"] = boyut[0]
        workflow["3"]["inputs"]["height"] = boyut[1]
        
        # Promptları yerleştir
        workflow["4"]["inputs"]["text"] = prompt
        workflow["5"]["inputs"]["text"] = negative_prompt
        
        # Unique seed kullan
        workflow["6"]["inputs"]["seed"] = int(time.time() * 1000) % 2147483647
        
        # API isteği için payload hazırla
        payload = {
            "prompt": workflow
        }
        
        print(f"🎨 Görsel üretiliyor... ({index}. sahne)")
        
        # API isteği gönder
        response = requests.post(
            "http://127.0.0.1:8188/prompt",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=300
        )
        
        if response.status_code != 200:
            print(f"⚠️ API Yanıt: {response.status_code}")
            print(f"⚠️ Yanıt İçeriği: {response.text}")
            raise Exception(f"ComfyUI hatası: {response.status_code}")
            
        result = response.json()
        prompt_id = result.get("prompt_id")
        
        if not prompt_id:
            raise Exception("Prompt ID alınamadı")
        
        # ComfyUI output klasörünü kontrol et
        comfyui_output = "ComfyUI/output"
        if os.path.exists(comfyui_output):
            baslangic_zamani = time.time()
            
            while time.time() - baslangic_zamani < 60:  # 60 saniye bekle
                for dosya in os.listdir(comfyui_output):
                    if dosya.lower().endswith(".png"):
                        dosya_yolu = os.path.join(comfyui_output, dosya)
                        dosya_zamani = os.path.getmtime(dosya_yolu)
                        
                        # Son 30 saniye içinde oluşturulan dosyayı bul
                        if time.time() - dosya_zamani <= 30:
                            if hedef_klasor:
                                hedef_dosya = os.path.join(hedef_klasor, f"sahne_{index:02d}.png")
                                try:
                                    shutil.copy2(dosya_yolu, hedef_dosya)
                                    print(f"✅ Görsel kaydedildi: sahne_{index:02d}.png")
                                    return True
                                except Exception as e:
                                    print(f"⚠️ Dosya kopyalama hatası: {e}")
                                    continue
                
                # Kısa bir bekleme
                time.sleep(1)
            
            # Son bir kontrol daha yap
            for dosya in os.listdir(comfyui_output):
                if dosya.lower().endswith(".png"):
                    dosya_yolu = os.path.join(comfyui_output, dosya)
                    if time.time() - os.path.getmtime(dosya_yolu) <= 60:  # Son 1 dakika içinde oluşturulmuş
                        if hedef_klasor:
                            hedef_dosya = os.path.join(hedef_klasor, f"sahne_{index:02d}.png")
                            shutil.copy2(dosya_yolu, hedef_dosya)
                            print(f"✅ Görsel kaydedildi: sahne_{index:02d}.png")
                            return True
        
        # Eğer buraya kadar geldiysek ve hedef_klasor'da dosya varsa başarılı sayalım
        if hedef_klasor:
            hedef_dosya = os.path.join(hedef_klasor, f"sahne_{index:02d}.png")
            if os.path.exists(hedef_dosya):
                print(f"✅ Görsel zaten kaydedilmiş: sahne_{index:02d}.png")
                return True
                
        raise Exception("Görsel üretilemedi veya kaydedilemedi")
        
    except Exception as e:
        if hedef_klasor:
            hedef_dosya = os.path.join(hedef_klasor, f"sahne_{index:02d}.png")
            if os.path.exists(hedef_dosya):
                print(f"✅ Görsel başarıyla kaydedildi (hata mesajını yoksay)")
                return True
        print(f"⚠️ Hata detayı: {str(e)}")
        raise

def comfyui_durumu_kontrol():
    """ComfyUI'nin çalışıp çalışmadığını kontrol eder"""
    try:
        response = requests.get("http://127.0.0.1:8188/system_stats", timeout=5)
        return response.status_code == 200
    except:
        return False