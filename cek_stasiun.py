from obspy import read

f = r"D:\BMKG\EQTransformer\sinyal gempa bandung 18 sept 2024\2024-09-18-02_41_07.mseed"
st = read(f)

# Lihat daftar stasiun unik
stations = sorted(set(f"{tr.stats.network}.{tr.stats.station}.{tr.stats.location}.{tr.stats.channel}" for tr in st))
for s in stations:
    print(s)

print(f"\nTotal channel unik: {len(stations)}")