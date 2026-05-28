# Hyperscript Multilingual Reference

Hyperscript supports 22 languages with native word order transformation:

- **SVO** (Subject-Verb-Object): English, Spanish, Portuguese, French, German, Italian, Vietnamese, Chinese, Indonesian, Swahili, Tagalog
- **SOV** (Subject-Object-Verb): Japanese, Korean, Turkish, Quechua, Hindi, Bengali, Thai
- **VSO** (Verb-Subject-Object): Arabic
- **Other**: Polish, Russian, Ukrainian (flexible word order)

## Language Examples

### English (SVO)
```html
<button _="on click toggle .active">Toggle</button>
<button _="on click add .highlight to me">Add</button>
<button _="on click if me matches .open hide #menu">Conditional</button>
```

### Japanese (SOV) - 日本語
```html
<button _="クリック で .active を トグル">トグル</button>
<button _="クリック で 私 に .highlight を 追加">追加</button>
<button _="クリック で 私 が .open に 一致 なら #menu を 隠す">条件</button>
```

Keywords:
- Commands: トグル, 追加, 削除, 表示, 隠す, 設定, 増加, 減少
- Events: クリック, 入力, 変更, フォーカス
- Control: もし, 繰り返し, 待つ
- References: 私, それ, 結果
- Positional: 最初, 最後, 次, 前

### Korean (SOV) - 한국어
```html
<button _="클릭 시 .active 를 토글">토글</button>
<button _="클릭 시 나 에게 .highlight 를 추가">추가</button>
<button _="클릭 시 내가 .open 과 일치하면 #menu 를 숨기다">조건</button>
```

Keywords:
- Commands: 토글, 추가, 제거, 표시, 숨기다, 설정, 증가, 감소
- Events: 클릭, 입력, 변경, 포커스
- Control: 만약, 반복, 대기
- References: 나, 그것, 결과
- Positional: 첫번째, 마지막, 다음, 이전

### Chinese (SVO) - 中文
```html
<button _="点击 时 切换 .active">切换</button>
<button _="点击 时 添加 .highlight 到 我">添加</button>
<button _="点击 时 如果 我 匹配 .open 隐藏 #menu">条件</button>
```

Keywords:
- Commands: 切换, 添加, 移除, 显示, 隐藏, 设置, 增加, 减少
- Events: 点击, 输入, 改变, 聚焦
- Control: 如果, 重复, 等待
- References: 我, 它, 结果
- Positional: 第一, 最后, 下一个, 上一个

### Arabic (VSO) - العربية
```html
<button _="بدّل .active عند نقر">تبديل</button>
<button _="أضف .highlight إلى أنا عند نقر">إضافة</button>
<button _="إذا أنا يطابق .open أخفِ #menu عند نقر">شرط</button>
```

Keywords:
- Commands: بدّل, أضف, أزل, أظهر, أخفِ, ضع, زِد, أنقص
- Events: نقر, إدخال, تغيير
- Control: إذا, كرر, انتظر
- References: أنا, هو, النتيجة

### Spanish (SVO) - Español
```html
<button _="en clic alternar .active">Alternar</button>
<button _="en clic añadir .highlight a yo">Añadir</button>
<button _="en clic si yo coincide con .open ocultar #menu">Condicional</button>
```

Keywords:
- Commands: alternar, añadir, quitar, mostrar, ocultar, establecer, incrementar, decrementar
- Events: clic, entrada, cambio
- Control: si, sino, repetir, esperar
- References: yo, ello, resultado
- Positional: primero, último, siguiente, anterior

### Portuguese (SVO) - Português
```html
<button _="em clique alternar .active">Alternar</button>
<button _="em clique adicionar .highlight a eu">Adicionar</button>
<button _="em clique se eu corresponde a .open esconder #menu">Condicional</button>
```

Keywords:
- Commands: alternar, adicionar, remover, mostrar, esconder, definir, incrementar, decrementar
- Events: clique, entrada, mudança
- Control: se, senão, repetir, aguardar
- References: eu, isso, resultado
- Positional: primeiro, último, próximo, anterior

### French (SVO) - Français
```html
<button _="sur clic basculer .active">Basculer</button>
<button _="sur clic ajouter .highlight à moi">Ajouter</button>
<button _="sur clic si moi correspond à .open cacher #menu">Conditionnel</button>
```

Keywords:
- Commands: basculer, ajouter, supprimer, afficher, cacher, définir, incrémenter, décrémenter
- Events: cliquer, saisie, changement
- Control: si, sinon, répéter, attendre
- References: moi, cela, résultat
- Positional: premier, dernier, suivant, précédent

### German (SVO/V2) - Deutsch
```html
<button _="bei Klick umschalten .active">Umschalten</button>
<button _="bei Klick hinzufügen .highlight zu ich">Hinzufügen</button>
<button _="bei Klick wenn ich passt zu .open verbergen #menu">Bedingt</button>
```

Keywords:
- Commands: umschalten, hinzufügen, entfernen, anzeigen, verbergen, setzen, erhöhen, verringern
- Events: Klick, Eingabe, Änderung
- Control: wenn, sonst, wiederholen, warten
- References: ich, es, Ergebnis
- Positional: erste, letzte, nächste, vorherige

### Turkish (SOV) - Türkçe
```html
<button _="tıklama da .active değiştir">Değiştir</button>
<button _="tıklama da ben e .highlight ekle">Ekle</button>
<button _="tıklama da ben .open ile eşleşirse #menu gizle">Koşullu</button>
```

Keywords:
- Commands: değiştir, ekle, kaldır, göster, gizle, ayarla, arttır, azalt
- Events: tıklama, giriş, değişim
- Control: eğer, yoksa, tekrarla, bekle
- References: ben, o, sonuç
- Positional: ilk, son, sonraki, önceki

### Indonesian (SVO) - Bahasa Indonesia
```html
<button _="pada klik alih .active">Alih</button>
<button _="pada klik tambah .highlight ke saya">Tambah</button>
<button _="pada klik jika saya cocok dengan .open sembunyikan #menu">Kondisional</button>
```

Keywords:
- Commands: alih, tambah, hapus, tampilkan, sembunyikan, atur, tambahkan, kurangi
- Events: klik, masukan, perubahan
- Control: jika, kalau, ulangi, tunggu
- References: saya, itu, hasil
- Positional: pertama, terakhir, berikutnya, sebelumnya

### Swahili (SVO) - Kiswahili
```html
<button _="kwa kubofya badilisha .active">Badilisha</button>
<button _="kwa kubofya ongeza .highlight kwa mimi">Ongeza</button>
<button _="kwa kubofya ikiwa mimi inaendana na .open ficha #menu">Masharti</button>
```

Keywords:
- Commands: badilisha, ongeza, ondoa, onyesha, ficha, weka, ongezea, punguza
- Events: bofya, ingizo, badiliko
- Control: ikiwa, kama, rudia, subiri
- References: mimi, hiyo, matokeo
- Positional: kwanza, mwisho, inayofuata, iliyotangulia

### Quechua (SOV) - Runasimi
```html
<button _="ñit'iy pi .active tikray">Tikray</button>
<button _="ñit'iy pi ñuqa man .highlight yapay">Yapay</button>
<button _="ñit'iy pi ñuqa .open wan tupanakun chayka #menu pakay">Sichus</button>
```

Keywords:
- Commands: tikray, yapay, qichuy, rikuchiy, pakay, churay, pisiyachiy
- Events: ñit'iy, yaykuchiy
- Control: sichus, mana, kutipay, suyay
- References: ñuqa, chay, lluqsisqa
- Positional: ñawpaq, qhipa, hamuq, ñawpaqnin

## Word Order Summary

| Language | Order | Example Pattern |
|----------|-------|-----------------|
| English | SVO | `on click toggle .active` |
| Japanese | SOV | `クリック で .active を トグル` |
| Korean | SOV | `클릭 시 .active 를 토글` |
| Turkish | SOV | `tıklama da .active değiştir` |
| Quechua | SOV | `ñit'iy pi .active tikray` |
| Arabic | VSO | `بدّل .active عند نقر` |
| Chinese | SVO | `点击 时 切换 .active` |
| Spanish | SVO | `en clic alternar .active` |
| Portuguese | SVO | `em clique alternar .active` |
| French | SVO | `sur clic basculer .active` |
| German | V2 | `bei Klick umschalten .active` |
| Indonesian | SVO | `pada klik alih .active` |
| Swahili | SVO | `kwa kubofya badilisha .active` |

## Using Multilingual Hyperscript

### Browser Bundle
```html
<script src="hyperfixi-semantic.browser.global.js"></script>
<script src="hyperfixi-multilingual.js"></script>
<script>
  // Execute in any language
  await hyperfixi.execute('トグル .active', 'ja');
  await hyperfixi.execute('alternar .active', 'es');
</script>
```

### Vite Plugin
```javascript
// vite.config.js
import { hyperfixi } from '@hyperfixi/vite-plugin';

export default {
  plugins: [hyperfixi({
    languages: ['ja', 'ko', 'es'], // Include specific languages
  })]
};
```

### Regional Bundles
Choose the smallest bundle for your target languages:

| Bundle | Size (gzip) | Languages |
|--------|-------------|-----------|
| browser-en.js | 20 KB | English only |
| browser-es-en.js | 25 KB | English + Spanish |
| browser-western.js | 30 KB | en, es, pt, fr, de |
| browser-east-asian.js | 24 KB | ja, zh, ko |
| browser-priority.js | 48 KB | Top 11 languages |
| browser.global.js | 61 KB | All 13 languages |
