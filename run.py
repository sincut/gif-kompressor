import imageio
from PIL import Image
import os
import subprocess

def manual_compress_gif(input_path, output_path):
    if not os.path.isfile(input_path):
        print(f"❌ FILE {input_path} GA ADA, BANGSAT!")
        return
    
    print(f"📥 NGELOAD {input_path}...")
    gif = Image.open(input_path)
    frames = []
    durasi = []
    
    while True:
        frames.append(gif.copy().convert('RGB'))
        durasi.append(gif.info.get('duration', 100))
        try:
            gif.seek(gif.tell() + 1)
        except EOFError:
            break
    
    print(f"🖼️ TOTAL FRAME: {len(frames)}")
    
    # SETTINGAN EKSTREM BUAT NGEJAR <500 KB, BANGSAT!
    ukuran = 150          # KECILIN RESIZE
    skip_frame = 4        # AMBIL TIAP 4 FRAME (JADI 69 FRAME AJA, KONTOL!)
    palette_warna = 16    # PALETTE MINIMALIS
    
    print(f"⚡ KOMPRES PAKAI: resize={ukuran}, skip={skip_frame}, palette={palette_warna}")
    
    frames_final = []
    for idx, f in enumerate(frames):
        if idx % skip_frame != 0:
            continue
        temp = f.copy()
        temp.thumbnail((ukuran, ukuran), Image.Resampling.LANCZOS)
        frames_final.append(temp)
    
    durasi_final = [durasi[i] * skip_frame for i in range(0, len(durasi), skip_frame)]
    
    temp_path = "temp_manual.gif"
    imageio.mimsave(temp_path, frames_final, duration=durasi_final, 
                    loop=0, palettesize=palette_warna, optimize=True)
    
    print("⚡ PAKAI GIFSICLE BUAT KOMPRES EXTREME...")
    subprocess.run([
        "gifsicle", "-O3", "--lossy=90", "-o", output_path, temp_path
    ])
    
    os.remove(temp_path)
    
    size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ JADI {size_kb:.2f} KB, KONTOL!")
    if size_kb < 500:
        print(f"🎉 BERHASIL < 500 KB, MANTAP JIWA!")
    else:
        print(f"⚠️ MASIH {size_kb:.2f} KB, LU COBA RESIZE 100 + SKIP 5 + PALETTE 8, BANGSAT!")

if __name__ == "__main__":
    print("🔥 MANUAL COMPRESS GIF <500 KB, KONTOL!")
    print("📁 MASUKIN NAMA FILE INPUT (contoh: DOWNLOAD-APK-HIJAU.gif):")
    input_file = input("INPUT: ").strip()
    print("📁 MASUKIN NAMA FILE OUTPUT (contoh: hasil_compress.gif):")
    output_file = input("OUTPUT: ").strip()
    manual_compress_gif(input_file, output_file)