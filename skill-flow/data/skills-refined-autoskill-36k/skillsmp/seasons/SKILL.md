---
name: seasons
description: This skill should be used when the user asks about "what season", "current kō", "micro-season", "72 seasons", "Japanese calendar", "seasonal awareness", or at the start of a session to ground in the present moment.
---

# /seasons

Display the current Japanese micro-season (kō 候) to foster seasonal awareness and connection to nature.

## Instructions

1. **Check if today's log exists**: Look for `./logs/YYYY-MM-DD.md`
   - **If exists**: Read and display the log file contents, then stop (no regeneration)
   - **If not**: Continue with steps below
2. **Determine today's date** and find the matching kō from the reference below
3. **Display the current micro-season** in a clean, compact format
4. **Include a brief ELI5 insight** (2-3 sentences max) explaining the natural phenomenon
5. **Add a positive contemplation** that:
   - Connects nature's wisdom to human growth and work
   - Frames challenges as opportunities
   - Suggests an actionable mindset or practice
6. **Include the pre-selected quote** from the kō reference table below
7. **Include relevant resources** (1-2 links) for deeper exploration
8. **Save output to log file**: `./logs/YYYY-MM-DD.md`

See `sekki-explanations.md` for detailed ELI5 explanations of each solar term.

## Output Format

```
## 第{number}候 · {romaji}
### "{english translation}"

> {date range} · {sekki name} ({sekki english})

<img src="../images/{number}-{slug}.jpg" alt="{description}" width="480">

**Why now?** {1-2 sentence ELI5 of the natural phenomenon}

**Insight:** {Positive philosophical musing connecting nature to
work/life—focus on growth, opportunity, patience, timing, etc.}

**Today's practice:** {One small actionable suggestion to embody
this seasonal wisdom in your work}

> **💬** "{Quote from the kō reference table}"
> — {Author from the kō reference table}

**Learn more:**
- {Relevant article, video, or resource URL}
- {Optional second resource}
```

## Images & Resources

This skill is self-contained with local images and curated URLs.

### Image Strategy

All 72 images are available locally. Always include the image in log files.

**Log file path**: Use `../images/` (logs are in `./logs/` subdirectory)

```html
<img src="../images/{number}-{slug}.jpg" alt="{description}" width="480" />
```

### Local Images

- All 72 images stored in: `./images/{number}-{romaji-slug}.jpg`
- Example: `./images/70-fuki-no-hana-saku.jpg`
- Git-tracked for portability

### Curated URLs

- See `./resources.md` for specific "Learn more" URLs for each kō
- Each micro-season has a validated Wikipedia/Japan Guide link

## Logging

Each /seasons output is saved as a markdown log file for tracking over time.

### Log Location

`./logs/YYYY-MM-DD.md`

Example: `./logs/2026-01-22.md`

### Log Format

Save the complete output to the log file. One file per day.

**Important:** Use `../images/` for image paths in logs (not `./images/`).

### Purpose

- Build a personal seasonal journal
- Track contemplations and practices over time
- Review patterns across seasons
- Git-tracked for history

## The 72 Kō Reference

Each micro-season has a pre-selected quote that resonates with its natural phenomenon and philosophical theme.

### 立春 Risshun (Beginning of Spring)

| #   | Dates     | Japanese | Romaji                | English                     | Quote                                                                                      | Author       |
| --- | --------- | -------- | --------------------- | --------------------------- | ------------------------------------------------------------------------------------------ | ------------ |
| 1   | Feb 4-8   | 東風解凍 | Harukaze kōri wo toku | East wind melts the ice     | "In the depth of winter, I finally learned that within me there lay an invincible summer." | Albert Camus |
| 2   | Feb 9-13  | 黄鶯睍睆 | Kōō kenkan su         | Bush warblers start singing | "Instructions for living a life: Pay attention. Be astonished. Tell about it."             | Mary Oliver  |
| 3   | Feb 14-18 | 魚上氷   | Uo kōri wo izuru      | Fish emerge from the ice    | "No winter lasts forever; no spring skips its turn."                                       | Hal Borland  |

### 雨水 Usui (Rainwater)

| #   | Dates     | Japanese | Romaji                    | English                  | Quote                                                                                                        | Author              |
| --- | --------- | -------- | ------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------ | ------------------- |
| 4   | Feb 19-23 | 土脉潤起 | Tsuchi no shō uruoi okoru | Rain moistens the soil   | "Adopt the pace of nature: her secret is patience."                                                          | Ralph Waldo Emerson |
| 5   | Feb 24-28 | 霞始靆   | Kasumi hajimete tanabiku  | Mist starts to linger    | "The world is full of magic things, patiently waiting for our senses to grow sharper."                       | W.B. Yeats          |
| 6   | Mar 1-5   | 草木萌動 | Sōmoku mebae izuru        | Grass sprouts, trees bud | "And the day came when the risk to remain tight in a bud was more painful than the risk it took to blossom." | Anaïs Nin           |

### 啓蟄 Keichitsu (Awakening of Insects)

| #   | Dates     | Japanese | Romaji                     | English                         | Quote                                                                                   | Author              |
| --- | --------- | -------- | -------------------------- | ------------------------------- | --------------------------------------------------------------------------------------- | ------------------- |
| 7   | Mar 6-10  | 蟄虫啓戸 | Sugomori mushito wo hiraku | Hibernating insects surface     | "Between stimulus and response there is a space. In that space is our power to choose." | Viktor Frankl       |
| 8   | Mar 11-15 | 桃始笑   | Momo hajimete saku         | First peach blossoms            | "The earth laughs in flowers."                                                          | Ralph Waldo Emerson |
| 9   | Mar 16-20 | 菜虫化蝶 | Namushi chō to naru        | Caterpillars become butterflies | "The expert in anything was once a beginner."                                           | Helen Hayes         |

### 春分 Shunbun (Spring Equinox)

| #   | Dates        | Japanese | Romaji                          | English                | Quote                                                                 | Author          |
| --- | ------------ | -------- | ------------------------------- | ---------------------- | --------------------------------------------------------------------- | --------------- |
| 10  | Mar 21-25    | 雀始巣   | Suzume hajimete sukū            | Sparrows start to nest | "The present moment is the only time over which we have dominion."    | Thích Nhất Hạnh |
| 11  | Mar 26-30    | 櫻始開   | Sakura hajimete saku            | First cherry blossoms  | "Spring passes and one remembers one's innocence."                    | Yoko Ono        |
| 12  | Mar 31-Apr 4 | 雷乃発声 | Kaminari sunawachi koe wo hassu | Distant thunder        | "You can cut all the flowers but you cannot keep spring from coming." | Pablo Neruda    |

### 清明 Seimei (Clear and Bright)

| #   | Dates     | Japanese | Romaji                | English              | Quote                                                                                     | Author              |
| --- | --------- | -------- | --------------------- | -------------------- | ----------------------------------------------------------------------------------------- | ------------------- |
| 13  | Apr 5-9   | 玄鳥至   | Tsubame kitaru        | Swallows return      | "Do not go where the path may lead, go instead where there is no path and leave a trail." | Ralph Waldo Emerson |
| 14  | Apr 10-14 | 鴻雁北   | Kōgan kaeru           | Wild geese fly north | "Not all those who wander are lost."                                                      | J.R.R. Tolkien      |
| 15  | Apr 15-19 | 虹始見   | Niji hajimete arawaru | First rainbows       | "After the rain, comes the rainbow."                                                      | Traditional saying  |

### 穀雨 Kokuu (Grain Rain)

| #   | Dates        | Japanese | Romaji                 | English                         | Quote                                                          | Author               |
| --- | ------------ | -------- | ---------------------- | ------------------------------- | -------------------------------------------------------------- | -------------------- |
| 16  | Apr 20-24    | 葭始生   | Ashi hajimete shōzu    | First reeds sprout              | "The bamboo that bends is stronger than the oak that resists." | Japanese Proverb     |
| 17  | Apr 25-29    | 霜止出苗 | Shimo yamite nae izuru | Last frost, rice seedlings grow | "The day you plant the seed is not the day you eat the fruit." | Fabienne Fredrickson |
| 18  | Apr 30-May 4 | 牡丹華   | Botan hana saku        | Peonies bloom                   | "Spring is the time of plans and projects."                    | Leo Tolstoy          |

### 立夏 Rikka (Beginning of Summer)

| #   | Dates     | Japanese | Romaji               | English              | Quote                                                                                              | Author                  |
| --- | --------- | -------- | -------------------- | -------------------- | -------------------------------------------------------------------------------------------------- | ----------------------- |
| 19  | May 5-9   | 蛙始鳴   | Kawazu hajimete naku | Frogs start singing  | "In summer, the song sings itself."                                                                | William Carlos Williams |
| 20  | May 10-14 | 蚯蚓出   | Mimizu izuru         | Worms surface        | "We are not apart from nature, we are a part of nature."                                           | Unknown                 |
| 21  | May 15-20 | 竹笋生   | Takenoko shōzu       | Bamboo shoots sprout | "A society grows great when old people plant trees whose shade they know they shall never sit in." | Greek Proverb           |

### 小満 Shōman (Grain Buds)

| #   | Dates        | Japanese | Romaji                   | English                              | Quote                                                                               | Author        |
| --- | ------------ | -------- | ------------------------ | ------------------------------------ | ----------------------------------------------------------------------------------- | ------------- |
| 22  | May 21-25    | 蚕起食桑 | Kaiko okite kuwa wo hamu | Silkworms start feasting on mulberry | "Amateurs sit and wait for inspiration, the rest of us just get up and go to work." | Stephen King  |
| 23  | May 26-30    | 紅花栄   | Benibana sakau           | Safflowers bloom                     | "In every walk with nature one receives far more than he seeks."                    | John Muir     |
| 24  | May 31-Jun 5 | 麦秋至   | Mugi no toki itaru       | Wheat ripens and is harvested        | "How we spend our days is, of course, how we spend our lives."                      | Annie Dillard |

### 芒種 Bōshu (Grain in Ear)

| #   | Dates     | Japanese | Romaji                         | English                        | Quote                                                                                                               | Author          |
| --- | --------- | -------- | ------------------------------ | ------------------------------ | ------------------------------------------------------------------------------------------------------------------- | --------------- |
| 25  | Jun 6-10  | 螳螂生   | Kamakiri shōzu                 | Praying mantises hatch         | "When you do something, you should burn yourself up completely, like a good bonfire, leaving no trace of yourself." | Shunryu Suzuki  |
| 26  | Jun 11-15 | 腐草為蛍 | Kusaretaru kusa hotaru to naru | Rotten grass becomes fireflies | "Even a small star shines in the darkness."                                                                         | Finnish Proverb |
| 27  | Jun 16-20 | 梅子黄   | Ume no mi kibamu               | Plums turn yellow              | "First, solve the problem. Then, write the code."                                                                   | John Johnson    |

### 夏至 Geshi (Summer Solstice)

| #   | Dates        | Japanese | Romaji               | English             | Quote                                                                                                                   | Author              |
| --- | ------------ | -------- | -------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------- |
| 28  | Jun 21-26    | 乃東枯   | Natsukarekusa karuru | Self-heal withers   | "One must maintain a little bit of summer, even in the middle of winter."                                               | Henry David Thoreau |
| 29  | Jun 27-Jul 1 | 菖蒲華   | Ayame hana saku      | Irises bloom        | "Summer afternoon—summer afternoon; to me those have always been the two most beautiful words in the English language." | Henry James         |
| 30  | Jul 2-6      | 半夏生   | Hange shōzu          | Crow-dipper sprouts | "Live in the sunshine, swim the sea, drink the wild air."                                                               | Ralph Waldo Emerson |

### 小暑 Shōsho (Minor Heat)

| #   | Dates     | Japanese | Romaji                       | English              | Quote                                                                          | Author                   |
| --- | --------- | -------- | ---------------------------- | -------------------- | ------------------------------------------------------------------------------ | ------------------------ |
| 31  | Jul 7-11  | 温風至   | Atsukaze itaru               | Warm winds blow      | "You can't stop the waves, but you can learn to surf."                         | Jon Kabat-Zinn           |
| 32  | Jul 12-16 | 蓮始開   | Hasu hajimete hiraku         | First lotus blossoms | "Sitting quietly, doing nothing, spring comes, and the grass grows by itself." | Zen saying               |
| 33  | Jul 17-22 | 鷹乃学習 | Taka sunawachi waza wo narau | Hawks learn to fly   | "The best way to predict the future is to implement it."                       | David Heinemeier Hansson |

### 大暑 Taisho (Major Heat)

| #   | Dates        | Japanese | Romaji                       | English                     | Quote                                                                                                                   | Author              |
| --- | ------------ | -------- | ---------------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------- |
| 34  | Jul 23-28    | 桐始結花 | Kiri hajimete hana wo musubu | Paulownia produces seeds    | "The creation of a thousand forests is in one acorn."                                                                   | Ralph Waldo Emerson |
| 35  | Jul 29-Aug 2 | 土潤溽暑 | Tsuchi uruōte mushi atsushi  | Earth is damp, air is humid | "Rest is not idleness, and to lie sometimes on the grass under trees on a summer's day is by no means a waste of time." | John Lubbock        |
| 36  | Aug 3-7      | 大雨時行 | Taiu tokidoki furu           | Great rains sometimes fall  | "The cure for anything is salt water: sweat, tears, or the sea."                                                        | Isak Dinesen        |

### 立秋 Risshū (Beginning of Autumn)

| #   | Dates     | Japanese | Romaji           | English              | Quote                                                    | Author       |
| --- | --------- | -------- | ---------------- | -------------------- | -------------------------------------------------------- | ------------ |
| 37  | Aug 8-12  | 涼風至   | Suzukaze itaru   | Cool winds blow      | "Autumn is a second spring when every leaf is a flower." | Albert Camus |
| 38  | Aug 13-17 | 寒蝉鳴   | Higurashi naku   | Evening cicadas sing | "The quieter you become, the more you are able to hear." | Rumi         |
| 39  | Aug 18-22 | 蒙霧升降 | Fukaki kiri matō | Dense fog descends   | "Attention is the rarest and purest form of generosity." | Simone Weil  |

### 処暑 Shosho (Limit of Heat)

| #   | Dates        | Japanese | Romaji                    | English                 | Quote                                                               | Author              |
| --- | ------------ | -------- | ------------------------- | ----------------------- | ------------------------------------------------------------------- | ------------------- |
| 40  | Aug 23-27    | 綿柎開   | Wata no hana shibe hiraku | Cotton flowers bloom    | "Notice that autumn is more the season of the soul than of nature." | Friedrich Nietzsche |
| 41  | Aug 28-Sep 1 | 天地始粛 | Tenchi hajimete samushi   | Heat starts to die down | "Life starts all over again when it gets crisp in the fall."        | F. Scott Fitzgerald |
| 42  | Sep 2-7      | 禾乃登   | Kokumono sunawachi minoru | Rice ripens             | "Make it work, make it right, make it fast."                        | Kent Beck           |

### 白露 Hakuro (White Dew)

| #   | Dates     | Japanese | Romaji                 | English                     | Quote                                                                                                             | Author        |
| --- | --------- | -------- | ---------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------- |
| 43  | Sep 8-12  | 草露白   | Kusa no tsuyu shiroshi | Dew glistens white on grass | "Those who contemplate the beauty of the earth find reserves of strength that will endure as long as life lasts." | Rachel Carson |
| 44  | Sep 13-17 | 鶺鴒鳴   | Sekirei naku           | Wagtails sing               | "Every leaf speaks bliss to me, fluttering from the autumn tree."                                                 | Emily Brontë  |
| 45  | Sep 18-22 | 玄鳥去   | Tsubame saru           | Swallows leave              | "Rivers know this: there is no hurry. We shall get there some day."                                               | A.A. Milne    |

### 秋分 Shūbun (Autumn Equinox)

| #   | Dates        | Japanese | Romaji                          | English                    | Quote                                                                                                              | Author             |
| --- | ------------ | -------- | ------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------ |
| 46  | Sep 23-27    | 雷乃収声 | Kaminari sunawachi koe wo osamu | Thunder ceases             | "Wherever you are, be all there."                                                                                  | Jim Elliot         |
| 47  | Sep 28-Oct 2 | 蟄虫坏戸 | Mushi kakurete to wo fusagu     | Insects hide in the ground | "In all things success depends on previous preparation, and without such preparation there is sure to be failure." | Confucius          |
| 48  | Oct 3-7      | 水始涸   | Mizu hajimete karuru            | Farmers drain fields       | "Simplicity is prerequisite for reliability."                                                                      | Edsger W. Dijkstra |

### 寒露 Kanro (Cold Dew)

| #   | Dates     | Japanese | Romaji               | English                    | Quote                                                                               | Author          |
| --- | --------- | -------- | -------------------- | -------------------------- | ----------------------------------------------------------------------------------- | --------------- |
| 49  | Oct 8-12  | 鴻雁来   | Kōgan kitaru         | Wild geese return          | "If you want to go fast, go alone. If you want to go far, go together."             | African Proverb |
| 50  | Oct 13-17 | 菊花開   | Kiku no hana hiraku  | Chrysanthemums bloom       | "How beautifully leaves grow old. How full of light and color are their last days." | John Burroughs  |
| 51  | Oct 18-22 | 蟋蟀在戸 | Kirigirisu to ni ari | Crickets chirp in doorways | "The old pond—a frog jumps in, sound of water."                                     | Matsuo Bashō    |

### 霜降 Sōkō (Frost Falls)

| #   | Dates        | Japanese | Romaji               | English                    | Quote                                                                                                | Author            |
| --- | ------------ | -------- | -------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------- | ----------------- |
| 52  | Oct 23-27    | 霜始降   | Shimo hajimete furu  | First frost                | "The flower that blooms in adversity is the most rare and beautiful of all."                         | Mulan (Disney)    |
| 53  | Oct 28-Nov 1 | 霎時施   | Kosame tokidoki furu | Light rains sometimes fall | "There is something incredibly nostalgic and significant about the annual cascade of autumn leaves." | Joe L. Wheeler    |
| 54  | Nov 2-6      | 楓蔦黄   | Momiji tsuta kibamu  | Maples and ivy turn yellow | "Simplicity is the ultimate sophistication."                                                         | Leonardo da Vinci |

### 立冬 Rittō (Beginning of Winter)

| #   | Dates     | Japanese | Romaji                  | English               | Quote                                                                                                                                    | Author          |
| --- | --------- | -------- | ----------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 55  | Nov 7-11  | 山茶始開 | Tsubaki hajimete hiraku | Camellias bloom       | "I prefer winter and fall, when you feel the bone structure of the landscape. Something waits beneath it; the whole story doesn't show." | Andrew Wyeth    |
| 56  | Nov 12-16 | 地始凍   | Chi hajimete kōru       | Land starts to freeze | "Look deep into nature, and then you will understand everything better."                                                                 | Albert Einstein |
| 57  | Nov 17-21 | 金盞香   | Kinsenka saku           | Daffodils bloom       | "The best time to plant a tree was 20 years ago. The second best time is now."                                                           | Chinese Proverb |

### 小雪 Shōsetsu (Minor Snow)

| #   | Dates        | Japanese | Romaji                    | English                 | Quote                                                                                 | Author              |
| --- | ------------ | -------- | ------------------------- | ----------------------- | ------------------------------------------------------------------------------------- | ------------------- |
| 58  | Nov 22-26    | 虹蔵不見 | Niji kakurete miezu       | Rainbows hide           | "What good is the warmth of summer, without the cold of winter to give it sweetness." | John Steinbeck      |
| 59  | Nov 27-Dec 1 | 朔風払葉 | Kitakaze konoha wo harau  | North wind blows leaves | "Be like a tree and let the dead leaves drop."                                        | Rumi                |
| 60  | Dec 2-6      | 橘始黄   | Tachibana hajimete kibamu | Tangerines turn yellow  | "I took a walk in the woods and came out taller than the trees."                      | Henry David Thoreau |

### 大雪 Taisetsu (Major Snow)

| #   | Dates     | Japanese | Romaji                   | English                         | Quote                                                    | Author           |
| --- | --------- | -------- | ------------------------ | ------------------------------- | -------------------------------------------------------- | ---------------- |
| 61  | Dec 7-11  | 閉塞成冬 | Sora samuku fuyu to naru | Cold sets in, winter begins     | "Nature does not hurry, yet everything is accomplished." | Lao Tzu          |
| 62  | Dec 12-16 | 熊蟄穴   | Kuma ana ni komoru       | Bears hibernate                 | "In seed time learn, in harvest teach, in winter enjoy." | William Blake    |
| 63  | Dec 17-21 | 鱖魚群   | Sake no uo muragaru      | Salmon gather and swim upstream | "Fall seven times, stand up eight."                      | Japanese Proverb |

### 冬至 Tōji (Winter Solstice)

| #   | Dates     | Japanese | Romaji                    | English                  | Quote                                                                                                                                                       | Author             |
| --- | --------- | -------- | ------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| 64  | Dec 22-26 | 乃東生   | Natsukarekusa shōzu       | Self-heal sprouts        | "The snow itself is lonely or, if you prefer, self-sufficient. There is no other time when the whole world seems composed of one thing and one thing only." | Joseph Wood Krutch |
| 65  | Dec 27-31 | 麋角解   | Sawashika no tsuno otsuru | Deer shed antlers        | "There is a privacy about winter which no other season gives you."                                                                                          | Ruth Stout         |
| 66  | Jan 1-4   | 雪下出麦 | Yuki watarite mugi nobiru | Wheat sprouts under snow | "Vision without action is a daydream. Action without vision is a nightmare."                                                                                | Japanese Proverb   |

### 小寒 Shōkan (Minor Cold)

| #   | Dates     | Japanese | Romaji                    | English                 | Quote                                                                                                                        | Author           |
| --- | --------- | -------- | ------------------------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| 67  | Jan 5-9   | 芹乃栄   | Seri sunawachi sakau      | Parsley flourishes      | "The frog does not drink up the pond in which it lives."                                                                     | Buddhist Proverb |
| 68  | Jan 10-14 | 水泉動   | Shimizu atataka wo fukumu | Springs thaw            | "Before enlightenment; chop wood, carry water. After enlightenment; chop wood, carry water."                                 | Zen Proverb      |
| 69  | Jan 15-19 | 雉始雊   | Kiji hajimete naku        | Pheasants start to call | "Winter is the time for comfort, for good food and warmth, for the touch of a friendly hand and for a talk beside the fire." | Edith Sitwell    |

### 大寒 Daikan (Major Cold)

| #   | Dates        | Japanese | Romaji                          | English                 | Quote                                                                               | Author         |
| --- | ------------ | -------- | ------------------------------- | ----------------------- | ----------------------------------------------------------------------------------- | -------------- |
| 70  | Jan 20-24    | 款冬華   | Fuki no hana saku               | Butterburs bud          | "In the midst of winter, I found there was, within me, an invincible summer."       | Albert Camus   |
| 71  | Jan 25-29    | 水沢腹堅 | Sawamizu kōri tsumeru           | Ice thickens on streams | "To appreciate the beauty of a snowflake it is necessary to stand out in the cold." | Aristotle      |
| 72  | Jan 30-Feb 3 | 鶏始乳   | Niwatori hajimete toya ni tsuku | Hens start laying       | "The pine stays green in winter... wisdom in hardship."                             | Norman Douglas |

## Resource Library

Use these for the "Learn more" section. Select 1-2 relevant to the current season:

**General 72 Seasons:**

- [72 Seasons Japan (Nippon.com)](https://www.nippon.com/en/features/h00124/)
- [Japanese Microseasons (Wikipedia)](https://en.wikipedia.org/wiki/Japanese_calendar#Seasons)
- [Kurashi no Goyomi App](https://www.kurashikata.com/en/)

**Seasonal Philosophy:**

- [In Praise of Shadows - Tanizaki](https://www.penguin.co.uk/books/57555/in-praise-of-shadows-by-tanizaki-junichiro/9780099283577)
- [Wabi-Sabi for Artists (Leonard Koren)](https://www.amazon.com/Wabi-Sabi-Artists-Designers-Poets-Philosophers/dp/0981484603)
- [The Book of Tea - Okakura](https://www.gutenberg.org/ebooks/769)

**Nature & Attention:**

- [How to Do Nothing - Jenny Odell](https://www.penguinrandomhouse.com/books/600671/how-to-do-nothing-by-jenny-odell/)
- [Braiding Sweetgrass - Robin Wall Kimmerer](https://milkweed.org/book/braiding-sweetgrass)
- [The Overstory - Richard Powers](https://www.richardpowers.net/the-overstory/)

**Productivity & Natural Rhythms:**

- [Deep Work - Cal Newport](https://www.calnewport.com/books/deep-work/)
- [Rest - Alex Soojung-Kim Pang](https://www.hachettebookgroup.com/titles/alex-soojung-kim-pang/rest/9781541604834/)
- [Four Thousand Weeks - Oliver Burkeman](https://www.oliverburkeman.com/fourthousandweeks)

**Contemplative Practice:**

- [On the Shortness of Life - Seneca](https://en.wikisource.org/wiki/On_the_shortness_of_life)
- [Meditations - Marcus Aurelius](https://www.gutenberg.org/ebooks/2680)
- [Zen Mind, Beginner's Mind - Shunryu Suzuki](https://www.penguinrandomhouse.com/books/175559/zen-mind-beginners-mind-by-shunryu-suzuki/)

## Contemplation Themes

Match insights to these positive themes based on the season:

| Season Phase | Themes                                              |
| ------------ | --------------------------------------------------- |
| Early Spring | Hidden beginnings, patience, trust in process       |
| Mid Spring   | Emergence, receptivity, opening to growth           |
| Late Spring  | Crossing thresholds, balance points, clarity        |
| Early Summer | Energy arriving, production mode, abundance         |
| Mid Summer   | Full engagement, strategic timing, momentum         |
| Late Summer  | Peak effort, endurance, knowing extremes pass       |
| Early Autumn | Sensing shifts, harvesting, completing              |
| Mid Autumn   | Releasing, revealing, elegant endings               |
| Late Autumn  | Preparing, simplifying, countercyclical opportunity |
| Early Winter | Withdrawal with purpose, essential focus            |
| Mid Winter   | Deep rest, hibernation as strategy, conservation    |
| Late Winter  | Hidden spring, reversal underway, quiet preparation |

## Design Notes

**Quote Selection Rationale:**

- Each of the 72 quotes is carefully matched to its micro-season's natural phenomenon
- Quotes balance Eastern wisdom, Western philosophy, and modern productivity insights
- Mix of timeless wisdom with practical action orientation
- Themes flow naturally through the year: emergence → growth → abundance → harvest → rest → preparation

**Why pre-mapped quotes?**

- Perfect alignment: one quote per micro-season
- Pre-mapping eliminates AI selection overhead
- Intentional curation: each kō has its perfect companion thought
- Meaningful rotation: see each quote ~5 times per year

## Example Output

For January 22 (kō #70):

## 第70候 · Fuki no hana saku

### "Butterburs bud"

> January 20-24 · 大寒 Daikan (Major Cold)

<img src="../images/70-fuki-no-hana-saku.jpg" alt="Butterbur buds emerging through cold earth" width="480">

**Why now?** While air is coldest, soil stays warmer underground. The butterbur taps this hidden warmth, blooming before competitors wake—first-mover advantage in nature's economy.

**Insight:** The coldest days come _after_ the solstice turn, not before. Light has been returning for a month—the reversal is already underway, even when conditions feel hardest. This is the "hidden spring": change begins before evidence appears.

**Today's practice:** Identify one project that's quietly building momentum beneath the surface. Give it 15 minutes of attention—water roots that others can't see yet.

> **💬** "In the midst of winter, I found there was, within me, an invincible summer."
> — Albert Camus

**Learn more:**

- [Butterbur (Petasites japonicus)](https://en.wikipedia.org/wiki/Petasites_japonicus)
- [Daikan - Coldest Period](https://www.nippon.com/en/features/h00124/)
