# Intent Classification Reference

4 intent types untuk SEO keyword tagging.

## Informational

User mencari informasi atau jawaban.

**Sinyal bahasa (ID):** apa, cara, bagaimana, pengertian, contoh, jenis, fungsi, arti, definisi, tips, panduan, tutorial
**Sinyal bahasa (EN):** what, how, why, when, guide, tutorial, tips, definition, example, meaning
**Intent Value:** 1

## Navigational

User mencari website/brand spesifik.

**Sinyal bahasa (ID):** login, log in, download, official, website, situs
**Sinyal bahasa (EN):** login, sign in, download, official, website, site
**Intent Value:** 1

## Commercial

User meneliti sebelum membeli — comparing, reviewing.

**Sinyal bahasa (ID):** terbaik, review, rekomendasi, vs, perbandingan, atau, harga, murah, bagus
**Sinyal bahasa (EN):** best, review, vs, comparison, top, recommended, alternative, affordable
**Intent Value:** 2

## Transactional

User siap melakukan transaksi.

**Sinyal bahasa (ID):** beli, harga, diskon, order, daftar, langganan, sewa, jual, kupon, promo
**Sinyal bahasa (EN):** buy, price, discount, order, subscribe, rent, sell, coupon, promo, cheap
**Intent Value:** 3

---

## Fallback Rules

1. Jika 2+ intent terdeteksi, gunakan yang memiliki Intent Value tertinggi
2. Jika tidak ada sinyal, default ke Informational
3. Jika keyword mengandung nama brand + kata transaksional, prioritaskan Transactional
