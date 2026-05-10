from obspy import read, Stream
import os, glob

src = r"D:\BMKG\EQTransformer\preprocessed_crop"
dst = r"D:\BMKG\EQTransformer\preprocessed_crop_eqt"

files = sorted(glob.glob(os.path.join(src, "*.mseed")))
print(f"Ditemukan {len(files)} file\n")

for f in files:
    sta = os.path.basename(f).split(".")[1]
    st  = read(f)

    if len(st) != 3:
        print(f"Skip {sta}: hanya {len(st)} trace")
        continue

    sta_dir = os.path.join(dst, sta)
    os.makedirs(sta_dir, exist_ok=True)

    for tr in st:
        start = tr.stats.starttime.strftime("%Y-%m-%dT%H-%M-%S")
        end   = tr.stats.endtime.strftime("%Y-%m-%dT%H-%M-%S")
        sr    = tr.stats.sampling_rate
        npts  = tr.stats.npts
        fname = f"{tr.id}__{start}__{end}__{sr}__{npts}.mseed"
        tr.write(os.path.join(sta_dir, fname), format="MSEED")

    print(f"OK: {sta}")

print("\nSelesai!")