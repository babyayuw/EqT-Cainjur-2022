from obspy import read, Stream
import glob
import os

def preprocess_station(folder_path, station_code):
    pattern = os.path.join(folder_path, "*.mseed")
    files = sorted(glob.glob(pattern))
    print(f"Ditemukan {len(files)} file .mseed")
    print(f"Mengekstrak stasiun: {station_code}\n")

    st = Stream()  # stream benar-benar kosong, bukan read()

    for f in files:
        try:
            tmp = read(f).select(station=station_code)
            if len(tmp) > 0:
                st += tmp
                print(f"  OK: {os.path.basename(f)} ({len(tmp)} trace)")
            else:
                print(f"  Skip: {os.path.basename(f)}")
        except Exception as e:
            print(f"  Error: {os.path.basename(f)}: {e}")

    if len(st) == 0:
        print("Tidak ada data untuk stasiun ini!")
        return None

    print(f"\nTotal trace sebelum merge: {len(st)}")

    # Cek sampling rate asli untuk tentukan frekuensi filter
    sr_asli = st[0].stats.sampling_rate
    nyquist = sr_asli / 2
    freqmax = min(45.0, nyquist * 0.9)  # maksimal 90% dari Nyquist
    print(f"Sampling rate asli: {sr_asli} Hz, Nyquist: {nyquist} Hz")
    print(f"Filter bandpass: 1.0 - {freqmax} Hz")

    print("\nMerge trace...")
    st.merge(method=1, fill_value='interpolate', interpolation_samples=-1)

    print("Detrend...")
    st.detrend('demean')
    st.detrend('linear')

    print("Taper...")
    st.taper(max_percentage=0.05, type='cosine')

    print("Bandpass filter...")
    st.filter('bandpass', freqmin=1.0, freqmax=freqmax, corners=4, zerophase=True)

    print("Resampling ke 100 Hz...")
    for tr in st:
        if tr.stats.sampling_rate != 100.0:
            tr.resample(100.0)
            print(f"  Resampled: {tr.id}")

    print("\nHasil akhir:")
    print(st)
    return st

folder = r"D:\BMKG\EQTransformer\sinyal gempa bandung 18 sept 2024"
st_clean = preprocess_station(folder, "CBJI")

# Simpan hasil ke file .mseed bersih
output_path = r"D:\BMKG\EQTransformer\CBJI_preprocessed.mseed"
st_clean.write(output_path, format="MSEED")
print(f"\nDisimpan ke: {output_path}")