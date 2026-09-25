# Как генерируем реалистично: фото → видео, мастер-промпт, чек-лист

(Согласовано с пользователем 24.09.2026 для ролика №3 «ONE NIGHT»; действует для всех роликов.)

## 1. Каждый кадр в два шага
**Шаг 1. Стоп-кадр (Nano Banana, 2 кр за вариант).** 2–3 варианта первого кадра сцены, пользователь выбирает.
- Дешевле: фото стоит 2 кредита, 5 секунд видео — 15–60. Композицию, свет и героя выбираем на фото.
- Утверждённое фото фиксирует героя, пространство, свет и крупность, Seedance только оживляет кадр.
- Следующие кадры делаются от утверждённых фото: герой и пространство одинаковые (пример из ролика №1: бассейн с фото, а не со слов).

**Шаг 2. Видео (Seedance 2.5).** Утверждённое фото — start frame; если важен финал кадра — ещё end frame. В промпте только движение: что делает герой, как идёт камера, что меняется в свете.

## 2. Зачем мастер-промпт (`research/hugency-webinar-2026-09-24/MASTER_PROMPT_TEMPLATE.md`)
- Один текстовый «паспорт» героя, пространства и стиля — дословно одинаковый во всех промптах. Меняется только строка действия.
- Жёсткие рамки: FIDELITY: LOCKED, protected elements, prohibited crossover — модель меньше «улучшает» от себя.
- Один style-блок (свет, цвет, зерно) во всех кадрах → генерации монтируются как один фильм.
- Встроены наши правила: без подъёма камеры, без морфинга, без лишних людей.

Пример (S1 трейлера):
```
# B. REFERENCE CONTROL MAP
## @one  (утверждённый стоп-кадр S1)
ROLE: Character · FIDELITY: LOCKED
ALLOWED: man ~35, short dark hair, plain black crewneck and black trousers, seen from behind 3/4
PROTECTED: posture, silhouette, clothing
## @void
ROLE: Location · FIDELITY: LOCKED
ALLOWED: endless black studio, wet glossy black floor, single soft top light, thin haze
PROTECTED: nothing appears in the darkness, no walls, no objects
# C. OUTPUT  16:9 · cinematic, 35mm, 24 fps · audio: room tone only
# E. CAMERA  Static. No zoom, no orbit, no rise.
# F. LIGHT   near-monochrome darkness, warm golden top light, deep violet shadows, fine film grain
# SCENE     the same man @one stands still, head lowered; after 3 seconds he slowly lifts his head. Nothing else moves except the haze.
# H. NEGATIVE  no text, no logo, no other people, no morphing floor
```

## 3. Реализм — правила
1. Одно простое действие на кадр, 4–6 с.
2. Камера только из белого списка: статика, медленный наезд, камера за героем. Без облётов и подъёмов.
3. Язык кино в промпте: объектив, источник света, время суток, зерно.
4. Минимум крупных лиц: силуэты, руки, свет, предметы.
5. Буквы, логотипы, цифры — только графикой в посте.
6. Черновики 480p → финалы ключевых кадров заново в 1080p.
7. Покадровая проверка каждого дубля (лицо, одежда, пространство, руки).
8. Один грейд и одно зерно на весь ролик; звук — синтез и фоли (шаги, дыхание, сердце, тишина).

## 4. Порядок согласования
Стоп-кадры (2–3 на сцену) → выбор → черновики видео 480p (сверка с аниматиком) → финалы → сборка. Без «да» пользователя ничего не генерируется.
