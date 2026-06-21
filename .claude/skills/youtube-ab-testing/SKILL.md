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
2. **Riset Keyword** — identifikasi keyword primer (long-tail), sekunder, dan broad
3. **Tentukan strategi CTR** — sesuai target yang diminta (realistis 6–10%, agresif 15–20%)
4. **Render widget interaktif** — thumbnail A & B divisualisasikan langsung di chat
5. **Output lengkap** — judul, deskripsi, hashtag, tags, kategori, image prompts, upload checklist

---

## Step 1 — Analisis SRT

Sebelum apapun, ekstrak dari transkrip:

- **Tema utama** — 1 kalimat inti video
- **Hook terkuat** — fakta, angka, atau klaim paling mengejutkan
- **Angle unik** — apa yang membedakan video ini dari konten serupa
- **Pain point audiens** — emosi apa yang akan dipicu (anger, curiosity, guilt, aspiration)
- **Kata kunci lokal** — nama tempat, tokoh, atau fenomena Indonesia yang relevan
- **Format thumbnail** — cocokkan dengan tipe konten video (lihat Step 3)

---

## Step 2 — Riset & Strategi Keyword

### Tiga Kategori Keyword

| Kategori | Karakteristik | Penggunaan |
|---|---|---|
| **Long-tail** (3–5 kata) | Volume rendah, kompetisi rendah, intent tinggi | Tag utama, title, deskripsi awal |
| **Medium-tail** (2–3 kata) | Volume sedang, rankable | Tag sekunder, variasi deskripsi |
| **Short-tail** (1 kata) | Volume tinggi, kompetisi besar | Hashtag broad, channel keywords |

### Proses Riset

1. Tentukan topik video dalam 1–2 kalimat
2. Brainstorm 8–10 variasi frasa yang mungkin diketik viewer
3. Gunakan YouTube Autocomplete dan Google Trends (filter: YouTube search)
4. Prioritaskan: high search volume + low-to-medium competition

### Penempatan Keyword

- **Filename sebelum upload**: `keyword-utama-topik-video.mp4`
- **Title**: keyword primer di 3–5 kata pertama (natural)
- **Deskripsi kalimat pertama**: keyword primer disebut dalam 1–2 kalimat pertama
- **Chapters**: gunakan frasa deskriptif, bukan hanya angka waktu
- **Tags**: dari long-tail spesifik ke short-tail broad
- **Channel keywords**: 5–10 kata/frasa yang mendeskripsikan niche channel secara keseluruhan

---

## Step 3 — Strategi CTR

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

**Sinyal algoritma yang paling dibobot YouTube:**
1. Click-Through Rate (CTR) — thumbnail + judul adalah penentu utama
2. Average View Duration — konten harus deliver apa yang dijanjikan thumbnail
3. Satisfaction signals — likes, shares, subscription earned dari video

---

## Step 4 — Format & Gaya Visual Thumbnail

### 12 Format Thumbnail (VidIQ Framework)

Pilih format yang paling cocok dengan hook video:

| # | Format | Terbaik untuk | Trigger utama |
|---|---|---|---|
| 1 | **Burning Question** | Edukasi, misteri, kontroversi | Curiosity gap |
| 2 | **Facts & Stats** | Riset, data, sains, olahraga | Angka spesifik |
| 3 | **Before-and-After** | Tutorial, transformasi, review | Aspiration / contrast |
| 4 | **Versus / Compare** | Debat, perbandingan produk, 2 opsi | Unfair fight |
| 5 | **Quote / Sound Bite** | Wawancara, drama, kontroversi | Identity threat |
| 6 | **Close-Up Reaction** | Commentary, reaksi, opini | Emotion mirror |
| 7 | **High-Energy Action** | Game, olahraga, petualangan | FOMO / excitement |
| 8 | **Featured Product** | Review, unboxing, rekomendasi | Aspiration |
| 9 | **Humor / Satire** | Entertainment, meme, parody | Pattern interrupt |
| 10 | **Stunning Landscape** | Travel, alam, ASMR, slow life | Aesthetics |
| 11 | **Emotional Moment** | Human interest, inspirasi, personal | Empathy |
| 12 | **Tutorial Result** | How-to, DIY, masak, crafts | Before-after implied |

### Prinsip Desain Thumbnail (VidIQ Design Tips)

**Hierarki & Komposisi:**
- **Satu focal point** per thumbnail — wajah, angka, atau objek utama. Dua focal point = tidak ada focal point
- Layout minimalis: pesan tersampaikan dalam 1 detik pertama, hindari detail berlebihan
- Wajah manusia dengan ekspresi kuat (excitement, surprise, curiosity) meningkatkan engagement — gunakan jika relevan
- Pertahankan konsistensi branding antar thumbnail: warna, posisi teks, dan logo/watermark yang sama setiap video

**Warna & Kontras:**
- Gunakan warna yang kontras terhadap palet default YouTube (merah, hitam, putih) agar menonjol di feed
- Pasangkan warna komplementer atau shade yang bertentangan (terang vs gelap)
- Latar gelap + subjek terang, atau sebaliknya — jangan pernah warna serupa
- Test visibilitas di dark mode dan light mode YouTube

**Tipografi:**
- Font besar, bold, terbaca di smartphone (>50% traffic YouTube adalah mobile)
- Teks singkat dan provokatif — biarkan judul video yang menjelaskan detail
- Hindari teks berlebihan yang mengacaukan layout
- Pastikan terbaca di ukuran miniatur (88×50px)

**Kualitas & Teknis:**
- Selalu gunakan gambar high-resolution, hindari blur atau pixelated
- File size hingga 2MB boleh — jangan korbankan kualitas demi ukuran kecil
- Thumbnail harus akurat mencerminkan isi video (clickbait menyebabkan drop retention)

**Kriteria skor tinggi VidIQ Extension (target: 90+/100):**
- Sharp and crisp image — tidak ada blur, noise, atau kompresi berlebihan
- Good brightness level — tidak terlalu gelap atau overexposed
- Perfectly balanced intensity — tidak flat, tidak terlalu saturated
- **Blur background, desaturate secondary areas, atau gunakan solid color backdrop** — fokus hanya pada subjek utama
- **Increase color saturation, add motion effects, atau vibrant color grading** — thumbnail yang flat/pucat kehilangan poin
- **Crop tighter on subject, atau replace background dengan backdrop yang cleaner** — jangan biarkan ruang negatif yang tidak terkomposisi

**Kesalahan yang wajib dihindari:**
- Thumbnail menyesatkan yang tidak relevan dengan konten
- Terlalu banyak teks sampai layout penuh
- Gambar blur atau resolusi rendah
- Background ramai yang bersaing dengan subjek utama
- Warna flat/desaturated yang tidak menonjol di feed
- Desain hanya dioptimasi untuk desktop, bukan mobile

---

### Gaya Desain

Tanya user jika tidak disebutkan. Gaya yang tersedia:

#### A. Komik Vintage / Pulp 1950s
Terbaik untuk: sejarah, ekonomi, politik, konspirasi, sains
- Background: krem/sepia, halftone Ben-Day dots
- Font: Bangers (judul besar), Special Elite (keterangan)
- Elemen: burst/starburst, panel border tebal, stamp bundar, ribbon banner
- Warna: amber, crimson, gold, navy gelap
- Vibe: "majalah petualangan jadul" atau "propaganda vintage"

#### B. Marker / Spidol Latar Putih
Terbaik untuk: finansial, edukasi, self-improvement, psikologi
- Background: putih bersih dengan dot grid tipis
- Font: Permanent Marker, Caveat (handwritten feel)
- Elemen: sticky note, formula matematika, split compare, underline merah
- Warna: hitam tebal + aksen merah/hijau/biru marker
- Vibe: "whiteboard penjelasan" atau "catatan teman pintar"

#### C. Split Compare / VS
Cocok untuk semua gaya — visual dua kolom kontras kiri vs kanan
- Format: LEFT (problem/bad) vs RIGHT (solution/good)
- Wajib ada: VS badge di tengah, label singkat tiap sisi
- Terbaik untuk CTR tinggi karena memaksa otak membandingkan

#### D. Reaction / Close-Up
Terbaik untuk: berita, opini, commentary, kontroversi
- Wajah besar mengisi 40–60% frame, ekspresi dilebihkan
- Background kontras dengan subjek (gelap vs wajah terang)
- Tambahkan teks callout atau panah penunjuk

---

## Step 5 — Struktur Widget Interaktif

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
- Spesifikasi teknis: **1280×720px**, aspect ratio 16:9, max file size 2MB
- Format file: JPG, PNG, GIF, BMP, atau WebP
- Teks maksimum **3–4 kata** per baris (terbaca di ukuran 88×50px / mobile thumbnail)
- **Satu focal point** — satu elemen visual dominan, bukan banyak
- Font bold, besar, kontras tinggi — mobile-first (>50% traffic adalah mobile)
- Thumbnail + judul harus saling melengkapi: thumbnail picu curiosity, judul beri konteks
- Test di dark mode dan light mode YouTube — pastikan tetap menonjol di keduanya
- Warna kontras dengan palet default YouTube (merah/hitam/putih)
- Konsistensi branding: warna, posisi teks, logo di posisi sama tiap thumbnail
- Selalu ada: eyebrow text (kecil atas), headline (besar tengah), sub-label (kecil bawah)
- Jika ada wajah manusia: ekspresi kuat (surprise, excitement, anger) — lebih baik dari wajah netral

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

## Step 6 — Copywriting

### Judul Utama (2 variasi)
- Variasi A: Format KLAIM PROVOKATIF — lebih informatif, untuk audiens niche
- Variasi B: Format PERTANYAAN/PARADOKS — lebih broad, untuk CTR maksimal
- Panjang ideal: 60–70 karakter
- **Keyword primer ditempatkan di 3–5 kata pertama** (bukan di tengah/akhir)
- Wajib ada: angka spesifik ATAU kata emosi kuat (bangkrut, hancur, tersembunyi, raib, dll)
- Hindari: clickbait kosong tanpa substansi, judul terlalu panjang

**Kriteria skor tinggi VidIQ Extension (target: 90+/100):**
- Membangkitkan intrigue, surprise, dan sedikit urgency
- Jelas menyampaikan apa isi video dan mengapa viewer harus menonton
- Mudah dipahami dalam sekali baca
- Tidak terlalu panjang (muat di satu baris di feed mobile)

### 5–8 Judul Alternatif
Variasikan format:
1. Format angka/data ("Rp X, Y persen, Z tahun...")
2. Format pertanyaan retoris
3. Format storytelling personal ("Aku ngabisin...", "Gue kira...")
4. Format klaim terbalik ("Bukan X, tapi Y")
5. Format lokal pride (nama daerah, tokoh Indonesia)
6. Format sains/riset ("Riset 2024 buktikan...", "Data menunjukkan...")

### Deskripsi YouTube

**Panduan Panjang & Karakter:**
- Target: **di bawah 1.000 karakter** (max YouTube 5.000, tapi lebih panjang tidak lebih baik)
- **200 karakter pertama**: wajib mengandung keyword primer — ini yang diperiksa VidIQ extension sebagai sinyal SEO utama
- **160 karakter pertama**: terlihat di bawah video player sebelum "Lihat selengkapnya"
- **2–3 baris pertama**: harus menjawab "apa isi video ini dan mengapa harus ditonton?"

**Struktur 5-Bagian (VidIQ Framework):**

```
[BAGIAN 1 — HOOK: 2–3 kalimat dengan keyword primer alami]
[Keyword primer ada di kalimat pertama. Jawab: apa isinya + kenapa menarik]

[BAGIAN 2 — WATCH NEXT: Link ke video lain di channel]
▶ Tonton juga: [judul video terkait] → [URL]

[BAGIAN 3 — SUBSCRIBE CTA]
🔔 Subscribe untuk [manfaat spesifik]: [URL channel]

[BAGIAN 4 — RESOURCES: website, social media, afiliasi]
📎 [Penjelasan singkat nilai/manfaat link] → [URL]
📱 Follow: [sosmed] → [URL]

⏱ CHAPTERS (untuk video 10+ menit):
0:00 - [hook/pembuka]
XX:XX - [topik utama 1]
XX:XX - [topik utama 2]
XX:XX - [twist/klimaks]
XX:XX - [kesimpulan]

[Keyword sekunder & variasi frasa disebar natural di bagian 1 dan 4]

📚 Referensi: [sumber yang disebut di video]

👇 [Pertanyaan untuk komentar — spesifik, memancing jawaban personal]

#hashtag1 #hashtag2 #hashtag3
```

**Aturan penting deskripsi:**
- Tulis untuk manusia dulu, baru SEO — jangan keyword stuffing
- Setiap link harus disertai penjelasan nilai/manfaat klik-nya ("Hindari X dengan ini", "Subscribe untuk Y")
- Deskripsi harus akurat dengan isi video — tidak boleh mislead (berdampak ke monetisasi)
- Jangan pakai deskripsi yang sama/copy-paste antar video (negatif untuk monetisasi eligibility)
- Hindari profanity, hate speech, atau spam links

### Hashtag (15)
**Penempatan:** YouTube menampilkan 3 hashtag pertama yang ditemukan di atas judul video. Letakkan 2–3 hashtag paling relevan di **akhir deskripsi** (setelah semua konten). YouTube akan otomatis mengambil yang pertama untuk ditampilkan di atas judul.

Komposisi:
- 3 hashtag ultra-spesifik topik video (long-tail)
- 4 hashtag niche kategori (#LiterasiFInansial, #SejarahDunia, dll) (medium-tail)
- 4 hashtag broad Indonesia (#EdukasiIndonesia, #BeritaIndonesia, dll) (short-tail)
- 2 hashtag trending potensial (#Viral2025, dll)
- 2 hashtag channel branding

### Tags SEO
**Batasan teknis YouTube:** total seluruh tag **maksimal 500 karakter**, **minimal 10 tag**.

Stratifikasi berdasarkan kategori keyword:
- **Long-tail (6–8 tags):** 3–5 kata, spesifik — ini yang paling mudah diranking
- **Medium-tail (3–4 tags):** 2–3 kata, variasi topik dan nama tokoh/tempat
- **Short-tail (2–3 tags):** 1–2 kata, broad — tambahkan hanya jika relevan
- Sertakan: variasi ejaan, pertanyaan yang mungkin diketik user, sinonim
- Format: semua huruf kecil, dipisah koma, **keyword primer di paling depan**
- Selalu hitung total karakter sebelum output — jangan melebihi 500 karakter

### Kategori
- **Education** — edukasi, sejarah, finansial, sains, psikologi
- **News & Politics** — berita, politik, ekonomi makro, investigasi
- **Gaming** — konten game, review, analisis industri game
- Boleh rekomendasikan 2 kategori (primer + sekunder)

---

## Step 7 — Upload & SEO Checklist

Berikan checklist ini kepada user bersama output:

### Sebelum Upload
- [ ] Rename file video: `keyword-utama-topik.mp4` sebelum upload
- [ ] Siapkan 2–3 variasi thumbnail untuk A/B testing YouTube

### Saat Upload
- [ ] Sertakan keyword primer dalam 3–5 kata pertama judul
- [ ] Deskripsi: keyword primer di kalimat pertama
- [ ] Tambahkan 2–3 hashtag terpilih di baris PERTAMA deskripsi
- [ ] Chapters dimulai dari `0:00` (wajib agar YouTube generate chapter otomatis)
- [ ] Aktifkan auto-generated captions lalu review & koreksi nama brand/istilah teknis
- [ ] Masukkan video ke playlist yang relevan (meningkatkan watch session)
- [ ] Set end screen (5–20 detik terakhir): rekomendasikan video/playlist terkait
- [ ] Tambahkan mid-video cards pada momen puncak (saat retention tinggi)

### Setelah Upload
- [ ] Pin komentar pertama: sertakan keyword + CTA engagement
- [ ] Pantau **YouTube Studio > Reach tab** pada hari ke-7 dan ke-28
- [ ] Jika impressi tinggi tapi CTR rendah → ganti thumbnail, revisi judul
- [ ] Jika impressi rendah → rewrite deskripsi, tambahkan chapters yang lebih deskriptif

---

## Step 8 — Image Generation Prompts (Nano Banana Pro)

> **Gunakan skill `text-to-image-prompt-optimizer`** untuk menghasilkan dan mengoptimalkan prompt gambar thumbnail. Skill tersebut memiliki panduan khusus untuk Nano Banana Pro (Google Gemini), termasuk keyword library, platform-specific rules, dan prompt structure yang lebih detail. Invoke sebelum membuat prompt jika user meminta optimasi maksimal.

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

## Step 9 — Kuis YouTube (Opsional)

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

**Thumbnail:**
- [ ] Widget interaktif dengan Thumbnail A & B (16:9, spesifikasi 1280×720px)
- [ ] Teks thumbnail: maks 3–4 kata per baris, terbaca di ukuran mobile
- [ ] Satu focal point jelas per thumbnail, layout minimalis
- [ ] Warna kontras terhadap palet YouTube (merah/hitam/putih)
- [ ] Background diblur/desaturate, atau diganti solid color backdrop
- [ ] Saturation warna cukup vibrant, tidak flat/pucat
- [ ] Subjek di-crop tighter atau background diganti lebih bersih
- [ ] Jika ada wajah: ekspresi kuat (bukan netral)
- [ ] Konsisten dengan branding channel (warna, posisi teks, logo)

**Judul & Copy:**
- [ ] 2 judul utama (A & B) dengan keyword primer di 3–5 kata pertama
- [ ] Judul: evoke intrigue + surprise + urgency, jelas, mudah dipahami, tidak terlalu panjang
- [ ] Prediksi CTR dengan progress bar untuk masing-masing variasi
- [ ] 3 chips trigger psikologis per variasi
- [ ] 5–8 judul alternatif

**Deskripsi:**
- [ ] Total panjang deskripsi di bawah 1.000 karakter
- [ ] **200 karakter pertama** mengandung keyword primer (skor VidIQ Extension)
- [ ] Struktur 5-bagian: Hook → Watch Next → Subscribe CTA → Resources → Chapters
- [ ] Chapters mulai dari `0:00` (untuk video 10+ menit)
- [ ] Setiap link ada penjelasan nilai/manfaat klik
- [ ] Deskripsi unik, tidak copy-paste dari video lain

**SEO & Tags:**
- [ ] 15 hashtag — 2–3 terpenting di akhir deskripsi (YouTube auto-display di atas judul)
- [ ] Tags SEO: **minimal 10 tag**, **total ≤500 karakter**, long-tail dahulu, dipisah koma
- [ ] Kategori YouTube (+ rekomendasi playlist)

**Upload & Post-publish:**
- [ ] Upload & SEO checklist (filename, chapters, captions, end screen, monitoring)

**Image Generation:**
- [ ] Invoke `text-to-image-prompt-optimizer` jika perlu optimasi prompt maksimal
- [ ] 2 prompt utama + 1–2 bonus Nano Banana Pro
- [ ] Tips suffix Nano Banana Pro
