---
name: youtube-outline-generator
description: Buat outline konten YouTube yang terstruktur, engaging, dan siap produksi — dengan top moments, CTA strategis, dan spotlight Indonesia. Gunakan skill ini kapanpun pengguna meminta outline YouTube, struktur video, rundown konten, atau menyebut kata "outline", "struktur video", "konten YouTube", "top moment", atau meminta format outline untuk topik apapun yang akan dijadikan video. Juga aktif ketika user memberikan deskripsi topik video dan referensi buku/paper. Skill ini menghasilkan outline ringkas tanpa deskripsi visual atau narasi panjang — hanya struktur, waktu, dan top moment. Terintegrasi dengan SearXNG untuk riset data aktual dari web sebelum menyusun outline.
---

# YouTube Outline Generator

Skill ini menghasilkan outline YouTube yang terstruktur, ringkas, dan siap produksi berdasarkan topik yang diberikan pengguna.

---

## Output Format

Outline mengikuti struktur ini secara konsisten:

```
# [JUDUL VIDEO]

## I. HOOK (0:00–0:45)
- Poin pembuka yang langsung menyerang rasa ingin tahu
- **TOP MOMENT:** Reveal atau kontras yang mengejutkan

## II. CTA AWAL (0:45–1:00)
- Satu kalimat ajakan subscribe/tonton sampai habis — kontekstual dengan topik

## III. [SEGMEN UTAMA] (timestamp)
- Poin-poin konten
- **TOP MOMENT:** Momen paling shareable/memorable di segmen ini

## [dst...]

## CTA TENGAH (timestamp)
- Ajakan like — dikaitkan langsung dengan konten yang baru dibahas

## [SEGMEN LANJUTAN]

## MANIFESTO CHANNEL (opsional — pakai jika video adalah "video filosofi" channel)
- Pernyataan posisi channel
- **TOP MOMENT:** Kalimat definisi yang bisa di-screenshot

## CLOSING + CTA AKHIR (timestamp)
- Callback ke hook
- **TOP MOMENT:** Pertanyaan atau pernyataan penutup yang kuat
- Kalimat subscribe
- Viewer prompt untuk komentar
- Teaser video berikutnya
```

---

## Aturan Penulisan

### TOP MOMENT
- Setiap segmen utama wajib punya minimal satu **TOP MOMENT**
- TOP MOMENT adalah momen paling shareable, mengejutkan, atau emosional di segmen tersebut
- Ditulis singkat — maksimal 2 baris
- Fungsi: membuat penonton bertahan, atau membuat penonton skip ke momen itu saat rewatch

### CTA (Call to Action)
Selalu ada tiga CTA:
1. **CTA Awal** — setelah hook, ajakan subscribe + tonton sampai habis
2. **CTA Tengah** — di pertengahan video, ajakan like yang dikaitkan dengan konten
3. **CTA Akhir** — di closing, ajakan subscribe + viewer prompt untuk komentar

CTA harus kontekstual — bukan template generik, tapi disambungkan ke isi video.

### Spotlight Indonesia
- Jika topik bersifat global, selalu tambahkan satu segmen khusus **SPOTLIGHT INDONESIA**
- Isi: data lokal, kasus nyata Indonesia, regulasi/kondisi lokal, dan implikasi bagi penonton Indonesia
- Posisi: setelah studi kasus global, sebelum CTA tengah

### Timestamp
- Distribusikan waktu secara realistis
- Hook: 0:00–0:45
- CTA Awal: 0:45–1:00
- Konten utama: mulai dari 1:00
- Total durasi ideal: 18–27 menit untuk konten edukatif mendalam

### Ringkas
- Tidak ada deskripsi visual (tidak ada "tampilkan grafik", "footage drone", dll)
- Tidak ada narasi panjang dalam outline
- Setiap poin maksimal 1–2 baris
- Gunakan kata kerja aktif

---

## Riset Web dengan SearXNG

Sebelum menyusun outline, riset informasi terkini menggunakan SearXNG untuk memastikan data dan fakta aktual.

**REQUIRED SUB-SKILL:** Gunakan [searxng](../searxng/SKILL.md) untuk web search.

### Wajib Riset untuk Segmen Ini

| Segmen | Riset SearXNG |
|--------|---------------|
| **Angka / data** (di segmane pun) | Search statistik terkini: `--query "statistik [topik] 2026" --category news --limit 5` |
| **Studi kasus global** | Search kasus nyata: `--query "studi kasus [topik]" --limit 5` |
| **Spotlight Indonesia** | Search konteks lokal: `--query "[topik] Indonesia 2026" --category news --limit 5` |
| **Berita terbaru** | Search update: `--query "[topik] terbaru" --category news --limit 5` |
| **Argumen pro/kontra** | Search perspektif: `--query "pro kontra [topik]" --limit 5` |

### Alur Riset

1. **Hook & Framing** — search angles atau fakta mengejutkan tentang topik
2. **Data & Angka** — search statistik kuantitatif untuk memperkuat argumen
3. **Studi Kasus** — search contoh nyata, sejarah, atau kejadian aktual
4. **Spotlight Indonesia** — search data lokal Indonesia TOP MOMENT
5. **Integrasikan temuan** ke poin outline dan TOP MOMENT

> Data hasil SearXNG digunakan sebagai referensi konten outline. Setiap statistik/fakta dalam outline harus bisa diverifikasi dari hasil pencarian.

---

## Cara Menentukan Segmen

Berdasarkan jenis topik:

| Jenis Topik | Segmen Wajib |
|---|---|
| Sejarah / investigasi | Hook → Framing → Kasus per kasus → Human cost → Akuntabilitas → Angka → Jalan keluar → Closing |
| Finansial / ekonomi | Hook → Framing → Anatomi masalah → Studi kasus + angka nyata → Spotlight Indonesia → Framework keputusan → Manifesto → Closing |
| Psikologi / sosial | Hook → Framing → Anatomi manipulasi → Studi kasus → Spotlight Indonesia → Siapa yang bertanggung jawab → Jalan keluar → Manifesto → Closing |
| Sains / sejarah budaya | Hook → Framing → Poin utama 1–5 → Spotlight Indonesia → Relevansi modern → Manifesto → Closing |

---

## Input yang Diproses

Skill ini membaca input berupa:
- **Judul atau deskripsi topik** — langsung dijadikan outline
- **Referensi buku/paper** — diintegrasikan sebagai poin konten atau TOP MOMENT
- **Instruksi gaya** — "ringkas", "tanpa narasi", "fokus Indonesia", dll → langsung diterapkan
- **Topik dengan sub-poin** — sub-poin dijadikan segmen atau sub-segmen

---

## Contoh Pola Top Moment yang Kuat

- Data yang mengejutkan: *"Jerman 1923: harga berlipat dua setiap 3,7 hari"*
- Paradoks: *"Negara dengan cadangan minyak terbesar di dunia — warganya kelaparan"*
- Perbandingan: *"Side-by-side: dua orang modal sama, hasil berbeda karena sistemnya berbeda"*
- Reveal: *"Siapa yang memegang pelatuknya — dan apakah kamu ada di pihak yang tepat?"*
- Angka konkret: *"Simulasi: pinjam Rp2 juta, bunga 0,4%/hari — total yang harus dibayar dalam 30 hari"*

---

## Variasi Format

Pengguna bisa meminta:
- **Versi panjang** — dengan deskripsi tiap segmen (default untuk draft awal)
- **Versi ringkas** — hanya judul segmen, timestamp, dan top moment (untuk review cepat)
- **Tanpa narasi/ilustrasi** — hapus semua kalimat narrator dan deskripsi visual

Jika tidak disebutkan, gunakan **versi ringkas** sebagai default.
