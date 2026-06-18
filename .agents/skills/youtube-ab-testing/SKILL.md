---
name: youtube-ab-testing
description: >
  Buat paket A/B testing YouTube lengkap dari file subtitle/transkrip (.srt atau teks).
  Output mencakup: 2 variasi thumbnail (divisualisasikan sebagai widget interaktif), 2 judul
  utama, 5–8 judul alternatif, deskripsi dengan maks 5 timestamps, hashtag (15), tags SEO
  (dipisah koma), kategori, dan 2–4 image generation prompts untuk Nano Banana Pro.
  Gunakan skill ini kapanpun pengguna upload file .srt atau transkrip dan meminta A/B testing,
  thumbnail YouTube, optimasi CTR, paket konten YouTube, atau variasi judul. Juga aktif
  ketika user menyebut "buatkan thumbnail", "optimasi CTR", "paket YouTube lengkap",
  "title dan deskripsi", atau "split test". Target CTR dan gaya visual ditentukan pengguna —
  tanyakan jika tidak disebutkan.
---

# YouTube A/B Testing Skill

## Alur Kerja Utama

1. **Baca & Pahami SRT** — ekstrak tema inti, hook terkuat, angle unik, fakta mengejutkan
2. **Tentukan strategi CTR** — sesuai target yang diminta (realistis 6–10%, agresif 15–20%)
3. **Render widget interaktif** — thumbnail A & B divisualisasikan langsung di chat
4. **Output lengkap** — judul, deskripsi, hashtag, tags, kategori, image prompts

---

## Step 1 — Analisis SRT

Sebelum apapun, ekstrak dari transkrip:

- **Tema utama** — 1 kalimat inti video
- **Hook terkuat** — fakta, angka, atau klaim paling mengejutkan
- **Angle unik** — apa yang membedakan video ini dari konten serupa
- **Pain point audiens** — emosi apa yang akan dipicu (anger, curiosity, guilt, aspiration)
- **Kata kunci lokal** — nama tempat, tokoh, atau fenomena Indonesia yang relevan

---

## Step 2 — Strategi CTR

Pilih pendekatan berdasarkan target:

| Target CTR | Pendekatan | Trigger Psikologis |
|---|---|---|
| 6–8% | Informatif + curiosity | Fakta mengejutkan, angka konkret |
| 9–11% | Provokasi ringan + contrast | Paradoks, "ternyata salah", klaim terbalik |
| 12–15% | Bold claim + personal attack | Identitas terancam, guilt trigger, "bukan salah lo" |
| 16–20%+ | Unfair fight + conspiracy hook | "Mereka vs kamu", rahasia tersembunyi, kemarahan kolektif |

**Trigger psikologis terkuat (gunakan minimal 2 per variasi):**
- Loss aversion — "yang hilang", "dirampas diam-diam"
- Curiosity gap — pertanyaan yang HARUS dijawab
- Identity threat — menyebut kelompok audiens secara spesifik
- Unfair fight — 1 orang vs institusi/sistem besar
- Contradiction — "X ternyata Y" (berlawanan dengan belief lama)
- Angka spesifik — Rp75.000, 10.000 tahun, 80 miliar persen (bukan angka bulat)

---

## Step 3 — Gaya Visual Thumbnail

Tanya user jika tidak disebutkan. Gaya yang tersedia:

### A. Komik Vintage / Pulp 1950s
Terbaik untuk: sejarah, ekonomi, politik, konspirasi, sains
- Background: krem/sepia, halftone Ben-Day dots
- Font: Bangers (judul besar), Special Elite (keterangan)
- Elemen: burst/starburst, panel border tebal, stamp bundar, ribbon banner
- Warna: amber, crimson, gold, navy gelap
- Vibe: "majalah petualangan jadul" atau "propaganda vintage"

### B. Marker / Spidol Latar Putih
Terbaik untuk: finansial, edukasi, self-improvement, psikologi
- Background: putih bersih dengan dot grid tipis
- Font: Permanent Marker, Caveat (handwritten feel)
- Elemen: sticky note, formula matematika, split compare, underline merah
- Warna: hitam tebal + aksen merah/hijau/biru marker
- Vibe: "whiteboard penjelasan" atau "catatan teman pintar"

### C. Split Compare / VS
Cocok untuk semua gaya — visual dua kolom kontras kiri vs kanan
- Format: LEFT (problem/bad) vs RIGHT (solution/good)
- Wajib ada: VS badge di tengah, label singkat tiap sisi
- Terbaik untuk CTR tinggi karena memaksa otak membandingkan

---

## Step 4 — Struktur Widget Interaktif

Render menggunakan `visualize:show_widget` dengan HTML+CSS. Komponen wajib:

```
┌─────────────────────────────────────────┐
│ Badge: VARIANT A — [nama konsep]        │
│ [THUMBNAIL RENDERED AS SVG/HTML]        │
│ Judul: ...                              │
│ Prediksi CTR: ░░░░░░░░░░░ ~X%          │
│ Chips: [trigger1] [trigger2] [trigger3] │
└─────────────────────────────────────────┘
```

**Aturan desain thumbnail:**
- Aspect ratio wajib 16:9
- Teks harus terbaca di ukuran 88×50px (mobile thumbnail)
- Maksimum 7 kata untuk headline utama
- Kontras tinggi — minimal satu elemen warna mencolok
- Selalu ada: eyebrow text (kecil atas), headline (besar tengah), sub-label (kecil bawah)

**Untuk Komik Vintage wajib ada:**
- Halftone dot texture (background-image: radial-gradient)
- Thick ink border (border: 3–4px solid #1C1C1C/gelap)
- Minimal satu: burst shape, stamp bundar, atau ribbon banner
- SVG action lines jika ada drama/konflik

**Untuk Marker Whiteboard wajib ada:**
- Dot grid background (opacity rendah)
- Font: Permanent Marker + Caveat dari Google Fonts
- Minimal satu: sticky note, formula, atau split panel
- Warna marker flat (no gradient, no shadow)

---

## Step 5 — Copywriting

### Judul Utama (2 variasi)
- Variasi A: Format KLAIM PROVOKATIF — lebih informatif, untuk audiens niche
- Variasi B: Format PERTANYAAN/PARADOKS — lebih broad, untuk CTR maksimal
- Panjang ideal: 60–70 karakter
- Wajib ada: angka spesifik ATAU kata emosi kuat (bangkrut, hancur, tersembunyi, raib, dll)
- Hindari: clickbait kosong tanpa substansi, judul terlalu panjang

### 5–8 Judul Alternatif
Variasikan format:
1. Format angka/data ("Rp X, Y persen, Z tahun...")
2. Format pertanyaan retoris
3. Format storytelling personal ("Aku ngabisin...", "Gue kira...")
4. Format klaim terbalik ("Bukan X, tapi Y")
5. Format lokal pride (nama daerah, tokoh Indonesia)
6. Format sains/riset ("Riset 2024 buktikan...", "Data menunjukkan...")

### Deskripsi YouTube
Struktur wajib:
```
[Hook 2-3 kalimat — pertanyaan atau fakta mengejutkan]

[Penjelasan konten — apa yang akan dibongkar/dipelajari, 2–3 paragraf]

⏱ Timestamps: (MAKSIMAL 5 poin)
00:00 — [hook/pembuka]
XX:XX — [topik utama 1]
XX:XX — [topik utama 2]
XX:XX — [twist/klimaks]
XX:XX — [kesimpulan/CTA]

📚 Referensi: [sumber-sumber yang disebut di video]

👇 [Pertanyaan untuk komentar — spesifik, memancing jawaban personal]
```

### Hashtag (15)
- 3 hashtag ultra-spesifik topik video
- 4 hashtag niche kategori (#LiterasiFInansial, #SejarahDunia, dll)
- 4 hashtag broad Indonesia (#EdukasiIndonesia, #BeritaIndonesia, dll)
- 2 hashtag trending potensial (#Viral2025, dll)
- 2 hashtag channel branding

### Tags SEO (dipisah koma, 15–20 tags)
- Mulai dari long-tail spesifik (3–5 kata) ke broad (1–2 kata)
- Sertakan: variasi nama topik, nama tokoh/tempat yang disebut, pertanyaan yang mungkin diketik user
- Format: semua huruf kecil, dipisah koma

### Kategori
- **Education** — edukasi, sejarah, finansial, sains, psikologi
- **News & Politics** — berita, politik, ekonomi makro, investigasi
- **Gaming** — konten game, review, analisis industri game
- Boleh rekomendasikan 2 kategori (primer + sekunder)

---

## Step 6 — Image Generation Prompts (Nano Banana Pro)

Buat 2 prompt utama (A & B) + 1–2 bonus. Format setiap prompt:

```
[Gaya/era] illustration, [medium spesifik], [komposisi utama],
[elemen visual kiri], [elemen visual kanan/tambahan],
[tipografi yang terlihat], [tekstur/efek],
[palet warna], [hal yang TIDAK boleh ada],
[aspect ratio instruction]
```

**Untuk Komik Vintage:**
```
1950s pulp [adventure/horror/noir] comic [cover/panel] illustration,
[scene utama dengan subjek jelas],
[elemen dekoratif: burst/ribbon/stamp],
bold Bangers-style typography "[TEKS YANG TERLIHAT DI THUMBNAIL]",
Ben-Day halftone dot texture throughout, thick black ink outlines,
aged yellowed paper texture, [palet warna: amber+crimson / sepia+gold / navy+red],
no photorealism, no 3d, no gradients, 16:9 landscape
```

**Untuk Marker Whiteboard:**
```
hand-drawn marker illustration on pure white background,
whiteboard sketch style, thick Copic marker outlines,
[elemen utama digambar dengan marker],
[teks yang terlihat] in Permanent Marker handwritten style,
[warna marker spesifik: red/blue/green/black ink],
imperfect wobbly hand-drawn lines, flat Copic ink colors,
zero gradients zero shadows zero 3d, pure white background,
16:9 landscape
```

**Suffix wajib di Nano Banana Pro:**
```
--ar 16:9 --style raw --no photorealism, 3d, shadow, gradient
```

---

## Step 7 — Kuis YouTube (Opsional)

Jika diminta, buat 2 pertanyaan kuis untuk disisipkan di video:

- **Kuis 1** — di 1/3 awal video, setelah fakta/konsep pertama diperkenalkan
- **Kuis 2** — di 2/3 video, setelah twist atau klimaks konten
- Format: 1 pertanyaan + 4 pilihan jawaban (tandai jawaban benar)
- Tingkat kesulitan: mudah-sedang — audiens yang menonton sampai sini harus bisa menjawab
- Tujuan: meningkatkan retention dan engagement sinyal ke algoritma YouTube

---

## Catatan Teknis

**Fonts Google yang diimpor di widget:**
```css
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Special+Elite&family=Permanent+Marker&family=Caveat:wght@600;700&family=Oswald:wght@700&display=swap');
```

**CSS Variables yang selalu dipakai:**
- `var(--color-text-primary)` — teks utama
- `var(--color-text-secondary)` — teks sekunder
- `var(--color-background-primary)` — background kartu
- `var(--color-background-secondary)` — background section
- `var(--color-border-tertiary)` — border tipis
- `var(--border-radius-lg)` — border radius kartu
- `var(--font-mono)` — font monospace untuk prompts

**Palet warna komik vintage yang terbukti bekerja:**
- Krem/parchment: `#F5E6C8`
- Dark ink: `#1C1C1C` atau `#2C1800`
- Crimson: `#C0392B` atau `#A32D2D`
- Gold: `#F4D03F` atau `#C8860A`
- Navy: `#1A1A2E` atau `#2C3E50`
- Green vintage: `#27AE60`

**Halftone pattern (wajib di komik vintage):**
```css
background-image: radial-gradient(circle, rgba(X,X,X,.15) 1px, transparent 1px);
background-size: 9px 9px;
```

**CTR bar:**
```css
.ctr-track { flex: 1; height: 7px; background: var(--color-background-tertiary); border-radius: 4px; overflow: hidden; }
.ctr-fill { height: 100%; width: [persentase]%; background: [warna]; border-radius: 4px; }
```

---

## Checklist Output Final

Sebelum menampilkan widget, pastikan semua ada:

- [ ] Widget interaktif dengan Thumbnail A & B (aspect ratio 16:9)
- [ ] 2 judul utama (A & B)
- [ ] Prediksi CTR dengan progress bar untuk masing-masing variasi
- [ ] 3 chips trigger psikologis per variasi
- [ ] 5–8 judul alternatif
- [ ] Deskripsi (hook + penjelasan + maks 5 timestamps + referensi + CTA komentar)
- [ ] 15 hashtag
- [ ] 15–20 tags SEO dipisah koma
- [ ] Kategori YouTube (+ rekomendasi playlist)
- [ ] Optimasi tambahan (upload timing, pin komentar, end screen)
- [ ] 2 prompt utama + 1–2 bonus Nano Banana Pro
- [ ] Tips suffix Nano Banana Pro
