import os
import requests

# URL langsung ke model pre-trained resmi
url = "https://github.com/smousavi05/EQTransformer/raw/master/ModelsAndData/EqT_model.h5"
output_file = "EqT_model.h5"

print(f"Memulai download model ke: {os.getcwd()}")
print("Mohon tunggu, ukuran file sekitar 300MB...")

try:
    # Mengunduh file dengan streaming agar hemat RAM
    response = requests.get(url, stream=True)
    response.raise_for_status() # Cek jika ada error koneksi
    
    with open(output_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                
    print(f"\nBerhasil! File '{output_file}' sudah siap di folder:")
    print(os.path.abspath(output_file))

except Exception as e:
    print(f"\nGagal mengunduh: {e}")
    print("Saran: Pastikan koneksi internet stabil atau download manual file tersebut lewat browser di link berikut:")
    print(url)