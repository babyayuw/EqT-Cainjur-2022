from obspy import read, Stream, UTCDateTime
import glob, os

mseed_dir = r"D:\BMKG\EQTransformer\preprocessed_cianjur"
out_dir   = r"D:\BMKG\EQTransformer\preprocessed_crop"
os.makedirs(out_dir, exist_ok=True)

# Perlebar window ke 06:00–06:40 UTC (40 menit)
T1 = UTCDateTime("2022-11-21T06:00:00")
T2 = UTCDateTime("2022-11-21T06:40:00")

valid = [
    "ACJM","BBJI","BKJI","CBJI","CGJI","CIJI","CIJM","CMJI","CNJI",
    "CSJI","CSJM","CTJI","CWJM","DBJI","JBJI","JPJI","JTJM","KPJI",
    "LEM","PBJI","PKJM","PSLI","PTJI","SCJI","TNGI","TSJM","WSJM"
]

for sta in valid:
    f = os.path.join(mseed_dir, f"IA.{sta}.preprocessed.mseed")
    if not os.path.exists(f):
        print(f"  TIDAK ADA: {sta}")
        continue
    try:
        st = read(f)
        st_crop = st.slice(T1, T2)
        if len(st_crop) == 0:
            print(f"  KOSONG: {sta}")
            continue
        out = os.path.join(out_dir, f"IA.{sta}.preprocessed.mseed")
        st_crop.write(out, format="MSEED")
        print(f"  OK: {sta} — {len(st_crop)} trace")
    except Exception as e:
        print(f"  Error {sta}: {e}")

print("\nSelesai!")