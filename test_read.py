from obspy import read

# Test satu file dulu
f = r"D:\BMKG\EQTransformer\sinyal gempa bandung 18 sept 2024\2024-09-18-02_41_07.mseed"
print("Membaca file...")
st = read(f)
print(st)
print("Berhasil!")