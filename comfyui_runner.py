"""
ComfyUI Runner
Geliştirici: @burakkocin
Oluşturma Tarihi: 2025-06-05 21:07:15
Versiyon: 5.5
"""

import json
import requests
import time
import os

# Sabit değişkenler
COMFYUI_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = "outputs"
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp")
MAX_BEKLEME = 60
KONTROL_ARASI = 1

# Yedek workflow
YEDEK_WORKFLOW = {
    "3": {
        "inputs": {
            "width": 768,
            "height": 768,
            "batch_size": 1
        },
        "class_type": "EmptyLatentImage"
    },
    "4": {
        "inputs": {
            "ckpt_name": "Deliberate_v2.safetensors",
            "vae_name": "vae-ft-mse-840000-ema-pruned.ckpt"
        },
        "class_type": "CheckpointLoaderSimple"
    },
    "7": {
        "inputs": {
            "text": "",
            "clip": ["4", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "8": {
        "inputs": {
            "text": "",
            "clip": ["4", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "9": {
        "inputs": {
            "seed": 123456,
            "steps": 30,
            "cfg": 8.5,
            "sampler_name": "euler_ancestral",
            "scheduler": "normal",
            "denoise": 1.0,
            "model": ["4", 0],
            "positive": ["7", 0],
            "negative": ["8", 0],
            "latent_image": ["3", 0]
        },
        "class_type": "KSampler"
    },
    "10": {
        "inputs": {
            "samples": ["9", 0],
            "vae": ["4", 2]
        },
        "class_type": "VAEDecode"
    },
    "11": {
        "inputs": {
            "images": ["10", 0],
            "filename_prefix": "gorsel_",
            "output_path": "outputs"
        },
        "class_type": "SaveImage"
    }
}

def create_directories():
    """Gerekli klasörleri oluşturur"""
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(TEMP_DIR, exist_ok=True)
        print("✅ Output klasörleri oluşturuldu")
        return True
    except Exception as e:
        print(f"❌ Klasör oluşturma hatası: {e}")
        return False

def save_workflow(workflow, is_backup=False):
    """Workflow'u kaydeder"""
    try:
        filename = "workflow_backup.json" if is_backup else "workflow_api.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(workflow, f, indent=2)
        return True
    except Exception as e:
        print(f"⚠️ Workflow kayıt hatası: {e}")
        return False

def load_workflow():
    """Workflow'u yükler"""
    try:
        with open("workflow_api.json", "r", encoding="utf-8") as f:
            workflow = json.load(f)
        save_workflow(workflow, is_backup=True)
        return workflow
    except Exception as e:
        print(f"⚠️ Ana workflow yüklenemedi: {e}")
        print("ℹ️ Yedek workflow kullanılıyor...")
        try:
            with open("workflow_backup.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            print("ℹ️ Sabit workflow kullanılıyor...")
            save_workflow(YEDEK_WORKFLOW)
            return YEDEK_WORKFLOW

def gorsel_uret(prompt, index, negative_prompt=""):
    """ComfyUI ile görsel üretir"""
    try:
        if not create_directories():
            return False
        
        prompt = prompt.strip()
        negative_prompt = negative_prompt.strip()

        if not prompt:
            raise ValueError("Prompt boş olamaz!")

        # Workflow'u yükle
        workflow = load_workflow()
        
        # Seed ve diğer ayarları güncelle
        current_time = int(time.time() * 1000)
        
        try:
            # KSampler ayarları
            for node_id, node in workflow.items():
                if node["class_type"] == "KSampler":
                    node["inputs"].update({
                        "seed": current_time % 2147483647,
                        "steps": 30,
                        "cfg": 8.5,
                        "sampler_name": "euler_ancestral",
                        "scheduler": "normal",
                        "denoise": 1.0
                    })
                    
            # SaveImage ayarları
            for node_id, node in workflow.items():
                if node["class_type"] == "SaveImage":
                    node["inputs"].update({
                        "filename_prefix": f"sahne_{index:02d}_",
                        "output_path": OUTPUT_DIR
                    })

            # Prompt ayarları
            for node_id, node in workflow.items():
                if node["class_type"] == "CLIPTextEncode":
                    if "positive" in str(node.get("output", "")):
                        node["inputs"]["text"] = prompt
                    else:
                        node["inputs"]["text"] = negative_prompt

            # API isteği gönder
            response = requests.post(
                f"{COMFYUI_URL}/prompt",
                json={"prompt": workflow},
                timeout=30
            )

            if response.status_code != 200:
                raise Exception(f"ComfyUI API hatası: {response.text}")

            result = response.json()
            prompt_id = result.get("prompt_id")

            if not prompt_id:
                raise Exception("Prompt ID alınamadı")

            print(f"🎨 [{index}] Görsel üretiliyor...")
            
            # Bekleme süresi ve kontroller
            baslangic = time.time()
            ilk_kontrol = True
            
            while True:
                gecen_sure = time.time() - baslangic
                
                # İlk kontrolü hemen yap, sonra bekleme süresini kullan
                if not ilk_kontrol and gecen_sure < KONTROL_ARASI:
                    time.sleep(0.2)
                    continue
                    
                ilk_kontrol = False
                
                if gecen_sure > MAX_BEKLEME:
                    raise Exception("Zaman aşımı")
                    
                try:
                    history_response = requests.get(
                        f"{COMFYUI_URL}/history/{prompt_id}",
                        timeout=10
                    )
                    if history_response.status_code == 200:
                        history = history_response.json()
                        if prompt_id in history and history[prompt_id].get("completed", False):
                            print(f"✅ [{index}] Görsel üretildi ({int(gecen_sure)} saniye)")
                            time.sleep(0.5)  # Dosya sisteminin senkronize olması için küçük bir bekleme
                            return True
                except requests.exceptions.Timeout:
                    print(f"⏳ Görsel üretimi devam ediyor... ({int(gecen_sure)} saniye)")
                    
                time.sleep(KONTROL_ARASI)

        except Exception as e:
            print(f"⚠️ Görsel üretim hatası: {e}")
            # Workflow'u yedeklemeyi dene
            print("ℹ️ Workflow'u yedeklemeyi deniyorum...")
            save_workflow(workflow, is_backup=True)
            return False

    except Exception as e:
        print(f"⚠️ Genel hata: {e}")
        return False

def test_comfyui_connection():
    """ComfyUI bağlantısını test eder"""
    try:
        if not create_directories():
            return False
        
        # Workflow kontrolü
        workflow = load_workflow()
        if not workflow:
            print("❌ Workflow yüklenemedi!")
            return False
        
        # API bağlantısını test et
        response = requests.get(f"{COMFYUI_URL}/history")
        if response.status_code != 200:
            print("❌ ComfyUI API bağlantısı başarısız!")
            return False
            
        print("✅ ComfyUI bağlantısı ve klasörler hazır")
        return True
        
    except Exception as e:
        print(f"❌ ComfyUI bağlantı hatası: {e}")
        return False

if __name__ == "__main__":
    if test_comfyui_connection():
        print("✅ ComfyUI bağlantısı başarılı")
        print(f"✅ Output klasörü: {os.path.abspath(OUTPUT_DIR)}")
        
        # Test için basit bir görsel üretimi
        test_prompt = """
        (masterpiece:1.4), (best quality:1.4), (ultra detailed:1.3),
        muscular orange tabby cat, anthropomorphic cat character, strong feline features,
        sitting in a modern office, wearing business attire,
        confident expression, detailed fur, high end character design
        """
        
        test_negative = """
        (human:1.6), (human face:1.6), (anime:1.6), (manga:1.6),
        text, watermark, signature, blurry, low quality, bad art
        """
        
        gorsel_uret(test_prompt, 0, test_negative)
    else:
        print("❌ ComfyUI bağlantısı başarısız")
        