# Шаблон мастер-промпта для видео (Seedance) — по разбору HubContent

Источник: практика на вебинаре Hugency (24.09.2026, 3:52–3:54 эфира). HubContent строит «scene-by-scene Seedance prompt» автоматически. Структура восстановлена покадрово с экрана (кадры: `practice/mp_*.jpg`, `practice/z_scenes.jpg`, `practice/z_style.jpg`).
Разделы E–H на экране пролистаны быстро и не читаются. Ниже они восстановлены по логике структуры и помечены «(реконструкция)».

---

## 1. Как HubContent собирает промпт (порядок)

1. **Elements** (brand elements) — каждый референс получает имя, `@tag` и роль: Character / Product / Location / Style. Это «то, что не должно меняться».
2. **Scenario / Story Architect** — концепт из одной фразы. AI уточняет «spark» (какое чувство оставить), формат и длительность, потом пишет абзац-концепт.
3. **Style description** — один абзац про палитру, свет, фактуру и настроение. Он «drives the master prompt» и каждую сцену.
4. **Scene structure** — 5 сцен на 10 с (Hook → Movement → Focus → Transformation → Final Moment). В каждой: план/движение камеры, персонаж с @тегом, действие, свет, атмосфера.
5. **Master prompt** — сводный документ из разделов A…I (ниже). Именно он уходит в модель.

---

## 2. Оригинал с экрана (дословно, что читается)

```
# A. PRODUCTION INTENT
A visually captivating short film showcasing the allure of a vintage sports car through the journey
of a stylish young man. The action arc follows his transition from a modern car to the vintage b[eauty,
evoking feelings of] admiration in the viewer.

# B. REFERENCE CONTROL MAP
## @1111111_2
ROLE: Character reference
FIDELITY: LOCKED
ALLOWED EXTRACTION:
- [Age range …]
- Male features
- Mediterranean or Middle Eastern descent
- Lean build
- Warm olive skin tone
- Oval-shaped face
- Thick, slightly arched eyebrows
- Deep-set, dark brown almond-shaped eyes
PROTECTED ELEMENTS:
- Relaxed yet confident posture
- Average height
PROHIBITED CROSSOVER: No properties related to other characters or products.

## @asset
ROLE: Hero product reference
FIDELITY: LOCKED
ALLOWED EXTRACTION:
- Sleek, vintage sports car
- Low, aerodynamic profile
- Deep, glossy black exterior
- Chrome five-spoke wheels
- Open-top design with rich tan leather interior
PROTECTED ELEMENTS:
- Smooth, flowing lines
- Sharply tapered rear
PROHIBITED CROSSOVER: No properties related to modern cars or other products.

## @hubcontent_ebaf6840
ROLE: Identity reference
FIDELITY: LOCKED
ALLOWED EXTRACTION:
- Age range: 30 to 35
- Male features
- …

# C. OUTPUT SPECIFICATION
Aspect Ratio: 9:16
Capture Style: Cinematic
Audio: No audio

# D. SUBJECT & PRODUCT CONTINUITY
- The young man @1111111_2 maintains a relaxed yet confident posture throughout.
- The vintage sports car @asset remains the focal point in each scene.
- The warm olive skin tone of the young man @1111111_2 is consistent.
- …

[E–H — не читаются на записи]

FINAL FRAME: Fade out on the vintage sports car.

# I. ACTIVE STABILITY REQUIREMENTS
- Product Preservation
- Identity Preservation
- Lighting Continuity
- Motion Continuity
- Global Style
- Continuity Matrix
```

Style description, сгенерированный платформой:
> The style direction embraces a muted, earthy color palette with warm, desaturated tones that evoke a vintage, nostalgic feel. Soft, natural lighting enhances the texture of the scene, creating a gentle contrast that highlights the subject without overpowering the background. The image has a filmic quality with subtle grain, adding depth and authenticity. The overall mood is relaxed and introspective, perfect for conveying a sense of timeless elegance and understated sophistication.

Сцены (10 с, 9:16):
1. **Hook** — Wide shot of a modern car parked on the street — stylish young man @1111111_2 stands confidently next to the car, looking around with a relaxed posture — natural daylight highlights the sleek lines of the car — grounded cinematic realism, luxury atmosphere.
2. **Movement Begins** — Medium shot, camera positioned in front of the same young man @1111111_2 — he takes a slow step away from the modern car and begins walking towards a vintage sports car parked a bit further down the street — a subtle light effect appears around him as he moves, creating a special atmospheric feel — cinematic elegance with a hint of magic.
3. **Focus on Retro Car** — Smooth tracking shot following the same young man @1111111_2 as he approaches the vintage sports car @asset — the camera gradually increases focus on the retro vehicle, showcasing its glossy black exterior and chrome wheels — a warm, nostalgic ambiance envelops the scene, enhancing the connection to the car, while the background subtly reflects the stylish vibe of the young man @hubcontent_ebaf6840.
4. **Transformation** — Close-up shot of the vintage sports car @asset as the same young man @1111111_2 stands right in front of it — the background becomes more saturated with vintage colors, creating a nostalgic effect that highlights the beauty of the car — a soft, dreamy glow surrounds the scene, emphasizing the luxury feel.
5. **Final Moment** — Medium close-up of the same young man @1111111_2 as he gazes in admiration at the vintage sports car @asset — the light falls perfectly to accentuate his features and the details of the car, the camera performs a slight zoom on his face capturing the expression of awe — elegant lighting and a cinematic feel, the scene sets up for the final fade out.

---

## 3. Чистый шаблон (копировать и заполнять)

```
# A. PRODUCTION INTENT
[Одно-два предложения: что за ролик, чей путь, какая эмоция у зрителя в финале.]

# B. REFERENCE CONTROL MAP
## @[hero]
ROLE: Character reference
FIDELITY: LOCKED
ALLOWED EXTRACTION:
- [возраст, этничность, телосложение, тон кожи]
- [форма лица, брови, глаза, причёска — ОБЯЗАТЕЛЬНО длина и тип волос]
- [гардероб дословно, одинаковый во всех промптах]
PROTECTED ELEMENTS:
- [осанка, походка, рост, то, что нельзя «улучшать»]
PROHIBITED CROSSOVER: No properties related to other characters or products.

## @[product / object]
ROLE: Hero product reference
FIDELITY: LOCKED
ALLOWED EXTRACTION:
- [форма, материал, цвет, ключевые детали]
PROTECTED ELEMENTS:
- [силуэт, пропорции, то, что делает объект узнаваемым]
PROHIBITED CROSSOVER: No properties related to [похожие объекты, которые модель любит подмешивать].

## @[location]
ROLE: Location / architecture reference
FIDELITY: LOCKED
ALLOWED EXTRACTION:
- [планировка, материалы, свет, время суток]
PROTECTED ELEMENTS:
- [геометрия, которую нельзя менять: число проёмов, где дорожки, где стены]
PROHIBITED CROSSOVER: [чего здесь быть не должно]

## @[style]
ROLE: Style reference (palette, lighting, mood only — no content)
FIDELITY: GUIDED

# C. OUTPUT SPECIFICATION
Aspect Ratio: [16:9 | 9:16 | 1:1]
Duration: [5/10/15 s]
Capture Style: Cinematic, [lens, e.g. 35mm / 50mm anamorphic], [frame rate 24 fps]
Audio: [No audio | diegetic only: footsteps, room tone]

# D. SUBJECT & PRODUCT CONTINUITY
- @hero keeps [причёска, гардероб, осанка] in every scene.
- @product remains [фокусная точка / в одной и той же позиции].
- [тон кожи, освещение лица, направление взгляда]

# E. CAMERA & MOTION RULES (реконструкция)
- Allowed moves: [Static | Dolly in | Follow from behind | Slider | Tilt up …]
- Forbidden: orbit, drone, handheld, crane rise, zoom, whip pan.
- Speed: slow, constant; no sudden acceleration.

# F. LIGHTING & COLOR (реконструкция)
[Коротко повторить style description: палитра, источник света, контраст, зерно.]

# G. SCENE BREAKDOWN (реконструкция)
Scene 1 — [название] — [0.0–2.0 s]: [shot size + camera move] — [the same @hero ...] — [action] — [light/atmosphere] — [mood].
Scene 2 — …
Scene 5 — …

# H. NEGATIVE / DO NOT (реконструкция)
- No morphing of architecture, no new doors/columns/paths, no text, no logos, no extra people.
- No change of hair, wardrobe or face between scenes.

FINAL FRAME: [чем заканчивается кадр — важно для склейки со следующим]

# I. ACTIVE STABILITY REQUIREMENTS
- Product Preservation
- Identity Preservation
- Lighting Continuity
- Motion Continuity
- Global Style
- Continuity Matrix
```

### Формула одной сцены
`[крупность + движение камеры] — [the same @hero] — [одно действие] — [свет/атмосфера] — [жанр/настроение]`
Главное: **в каждой сцене повторять «the same … @tag»** и **называть каждый референс**. На вебинаре одежда «уплыла», когда её не упомянули в промпте.

---

## 4. Адаптация под XFUSION (наш стек: Nano Banana → Seedance 2.5 omni_reference в Higgsfield)

В Higgsfield нет «Elements» с @тегами, как в HubContent. Их роль у нас выполняют:
1. **референс-изображения** в omni_reference (лист персонажа, мастер-стилл локации, стилл объекта);
2. **блок B в тексте промпта** с описанием каждого референса словами (Seedance читает текст, @тег для него — просто имя; главное — дословное описание);
3. **start/end frame** — жёстче всего держит геометрию.

```
# A. PRODUCTION INTENT
A cinematic 16:9 short about a man who arrives at the villa he once only dreamed of. Quiet, confident, emotional; the viewer should feel that the dream has become an address.

# B. REFERENCE CONTROL MAP
## @hero (images: character sheet 772e1659, 1998e136)
ROLE: Character reference
FIDELITY: LOCKED
ALLOWED EXTRACTION:
- man in his mid-30s, short dark wavy hair (NOT curly), trimmed beard, lean build
- black wool single-breasted suit, two buttons, notch lapels, slim tailored, plain-hem black wool trousers, white cotton shirt, no tie, black leather cap-toe oxford shoes with closed lacing and leather soles, polished but not mirror-like, black socks, no watch, no jewelry
PROTECTED ELEMENTS:
- calm, unhurried walk, ~0.6–0.77 s per step
- same face and hairline in every scene
PROHIBITED CROSSOVER: no other people, no curly hair, no accessories.

## @villa (image: master 3d4d0356)
ROLE: Location / architecture reference
FIDELITY: LOCKED
ALLOWED EXTRACTION:
- modern travertine-and-glass villa, one continuous black-water pool in front of the house
- walking paths ONLY on the left and right sides of the pool
- central glass entrance, dark bronze side panels, two planters
PROTECTED ELEMENTS:
- the pool is one uninterrupted surface; no path, bridge or fountain across its middle
- number and position of windows, doors and columns
PROHIBITED CROSSOVER: no central walkway, no extra doors.

## @stairs (image: cleaned still 8367b03e)
ROLE: Location reference
FIDELITY: LOCKED
PROTECTED ELEMENTS: floating travertine steps, glass balustrade, NO central post, NO handrail in the middle.

## @key (still 76bda9d1 / aed01a1f)
ROLE: Hero product reference
FIDELITY: LOCKED
ALLOWED EXTRACTION: classic brass key, oval bow; lies FLAT on the marble.

# C. OUTPUT SPECIFICATION
Aspect Ratio: 16:9 · Capture Style: Cinematic, 35mm, 24 fps · Audio: diegetic only (footsteps, room tone)

# D. SUBJECT & PRODUCT CONTINUITY
- @hero keeps short dark wavy hair and the exact suit in every scene.
- @villa geometry never changes; the pool stays continuous.

# E. CAMERA & MOTION RULES
- Allowed: Static (01), Follow from behind (17), Dolly in (08), Push past (13), Slider right (12), Tilt up (04, only on objects, not architecture with windows).
- Forbidden: orbit, drone, crane/rise, zoom, handheld.
  (Lesson: when the camera rises, Seedance shifts the left-wall windows toward the centre.)

# F. LIGHTING & COLOR
Warm golden-hour key from the west, deep purple shadows (#56129B / #160B27), accents of warm orange (#DC462E); soft contrast, fine film grain, no crushed blacks.

# H. NEGATIVE / DO NOT
No morphing walls, no new paths across the pool, no central stair post, no text, no logos, no other people, no hair change.

# I. ACTIVE STABILITY REQUIREMENTS
Product Preservation · Identity Preservation · Lighting Continuity · Motion Continuity · Global Style · Continuity Matrix
```

**QA после каждой генерации** (наши правила из film1): slitscan по строке со стенами (`video/xfusion-01-home-achievement/slitscan.py`), сверка причёски и лица, бассейн сплошной, двери совпадают с мастером, ключ лежит плашмя, у лестницы нет стойки посередине.
