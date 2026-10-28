# Peta Suara 2024 Kota Surabaya

Sumber: 30 PDF D.Hasil Kecamatan DPRD Kota Surabaya (Dapil 1-5), folder GDrive Dapil 1-5.
Tegalsari tidak ada berkasnya di folder itu, jadi 31 kecamatan belum utuh.

## Isi
- dhasil_tps.json: struktur berjenjang kecamatan > kelurahan > TPS. PKB tersedia sampai TPS.
- dhasil_tps_pkb.csv: 7891 baris TPS dengan suara PKB.
- dhasil_kelurahan_partai.csv: 148 kelurahan x 18 partai (lihat status_validasi).
- dhasil_validasi.json: perbandingan angka parse vs rekap KPU per kecamatan.
- dhasil_anomali.json: 176 nilai mustahil yang dibuang (melebihi total resmi partai).

## Status validasi
- penuh (18 partai persis KPU): 18 kecamatan -> Benowo, Bubutan, Dukuh Pakis, Gayungan, Gunung Anyar, Jambangan, Karang Pilang, Krembangan, Lakarsantri, Pabean Cantian, Rungkut, Sambikerep, Sawahan, Semampir, Simokerto, Tenggilis Mejoyo, Wiyung, Wonokromo
- pkb (hanya PKB yang sahih): 0 kecamatan -> -
- sebagian (PKB dan sebagian partai beda): 12 kecamatan -> Asemrowo, Bulak, Genteng, Gubeng, Kenjeran, Mulyorejo, Pakal, Sukolilo, Sukomanunggal, Tambaksari, Tandes, Wonocolo

## Catatan
- PKB per TPS berjumlah tepat sama dengan total kelurahan di seluruh 30 kecamatan.
- Total PKB parse 153622 vs KPU 153614. Selisih 8 suara (Tandes +9, Wonocolo -1), 0,005 persen.
- Partai selain PKB di kecamatan berstatus sebagian belum lengkap per TPS, pakai hanya angka kelurahan dengan sadar risiko.
- Nomor TPS mengikuti dokumen 2024, bisa bergeser pada 2029.
