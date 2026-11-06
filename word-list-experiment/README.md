# Word-list experiment

Part of [Dragoman](../README.md).

Do language models translate Ancient Greek into Persian **via English**? This is an ongoing
pilot study. It started with single words and four open-weight models, and I keep adding models
and tests, so some of the results here are unfinished.

Done so far: the direct run, the forced pivot, the temperature test and the kinship test
(section 4) on eight open-weight models: GPT-OSS 120B, GPT-OSS 20B, Qwen 3.8 27B, ALLaM 2 7B, Llama 3.3 70B, Llama 3.1 8B,
Mistral Small 3.1 24B and Gemma 4 26B. The cells that were left unfinished at first were filled
with one sample each on 4 November 2026 (marked ¹ below). ALLaM is in the word-list tests only.

Still open:
- a hand check of the four newer models' answers. Their counts below come from the automatic check
  plus a targeted search for the traces already known, so some hits may still be missing.

## Design

A **trap** is a Greek word whose usual English equivalent is ambiguous in a way neither Greek
nor Persian is. For example, κρόταφος is the temple of the head. English *temple* also means
a shrine, but κρόταφος never does, and Persian has two separate words: شقیقه for the head,
معبد for the shrine. An answer of معبد points to the English word. A trap needs all of
the following:

1. The Greek word has sense s1 and lacks sense s2 (checked against LSJ).
2. Its usual English equivalent covers both s1 and s2.
3. Persian uses different words: P1 for s1, P2 for s2.
4. The ambiguity belongs to English, not to Persian or Modern Greek.

The 200-word list mixes 77 traps with 123 frequent fillers, shuffled so that nothing in the
list gives the design away. Each word was sent on its own, with no system prompt.

**Direct:** Greek word → Persian, 3 samples per word at temperature 0.7.

**Forced pivot:** a benchmark for what translating through English produces. It takes two
separate requests:
1. Greek word → the single most usual English word.
2. That English word alone, with the Greek removed → Persian.

In step 2 the model can't know that *bank* came from a word for a riverbank, so a trap
fires whenever the English ambiguity wins.

## Results

### 1. Do the traps fire?

| Model | Direct | Forced pivot | Forced pivot, own English word = trap word | Direct, same words |
| --- | --- | --- | --- | --- |
| GPT-OSS 120B | 2 / 231 (0.9%) | 20 / 77 (26.0%) | 20 / 33 (60.6%) | 1 / 99 (1.0%) |
| Qwen 3.8 27B | 0 / 231 (0%) | 27 / 77 (35.1%) | 25 / 36 (69.4%) | 0 / 108 (0%) |
| GPT-OSS 20B | 0 / 231 (0%) | 10 / 77 (13.0%) | 9 / 24 (37.5%) | 0 / 72 (0%) |
| ALLaM 2 7B | 0 / 231 (0%) | 3 / 77 (3.9%) | 3 / 26 (11.5%) | 0 / 78 (0%) |
| Gemma 4 26B | 0 / 230 (0%) | 33 / 72 (45.8%) | 31 / 39 (79.5%) | 0 / 120 (0%) |
| Llama 3.3 70B | 2 / 231 (0.9%) | 18 / 77 (23.4%) | 18 / 44 (40.9%) | 0 / 132 (0%) |
| Mistral Small 3.1 24B | 1 / 231 (0.4%) | 14 / 77 (18.2%) | 14 / 49 (28.6%) | 0 / 147 (0%) |
| Llama 3.1 8B | 1 / 231 (0.4%) | 4 / 77 (5.2%) | 4 / 36 (11.1%) | 1 / 108 (0.9%) |

The "own English word = trap word" columns keep only the traps where the model's step-1 English
word was the ambiguous one (*bank*, *seal*, *temple*…). When the route really runs through that
word, the English-only sense comes out in 29–80% of cases for the stronger models (11–12% for
the weakest two, ALLaM and Llama 3.1 8B). The direct answers on the same words almost never
show it, in any of the eight models.

Gemma gives the sharpest contrast. Given the English word alone, it lists its English senses
side by side (*ring* → انگشتر، حلقه، زنگ; *bark* → پوست درخت، پارس کردن; *seal* → فک، مهر),
so the trap fires in 4 of 5 cases. Translating straight from the Greek, it never does (0 of
120). Gemma's pivot has 72 of the 77 traps: on a few short English words (*island*, *tomb*,
*crowd*, *letter*) and on one Greek word (ἔριφος) it ran past its token limit every time.

How well the models know the words. This is the automatic check: the expected Persian word
appears anywhere in the answer, or as its first word.

| Model | Fillers: anywhere | Fillers: first | Traps: anywhere | Traps: first |
| --- | --- | --- | --- | --- |
| Gemma 4 26B | 95% | 83% | 75% | 60% |
| Qwen 3.8 27B | 90% | 80% | 63% | 50% |
| Llama 3.3 70B | 87% | 72% | 72% | 55% |
| GPT-OSS 120B | 86% | 74% | 64% | 52% |
| GPT-OSS 20B | 82% | 70% | 41% | 28% |
| Mistral Small 3.1 24B | 63% | 37% | 53% | 20% |
| Llama 3.1 8B | 54% | 34% | 31% | 14% |
| ALLaM 2 7B | 21% | 15% | 10% | 6% |

Gemma knows the most words and shows the fewest traces of English (below). How much English
leaks in does not simply follow how weak a model is: GPT-OSS 120B is among the strongest and
leaks the most.

### 2. Traces of English

English still shows up in the direct answers now and then. The counts below
come from the direct run (of 3 samples, temperature 0.7) and the temperature runs (of 5 samples
at each temperature). ALLaM was not in the temperature runs and shows none of these traces.
"–" means not run: only nine words are in the temperature test. ¹ means one sample instead of
five (a gap filled later).

#### A. English homonyms

| Greek | Answer | English | Model | Direct | T 0 | T 0.7 | T 1.0 | T 1.5 | T 2.0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| φώκη (seal, the animal) | مهر، نشان | *seal* → stamp | GPT-OSS 120B | 2 | 0 | 3 | 0 | 2 | 0 |
| παλάμη (palm of the hand) | نخل, «پالم» | *palm* → tree | GPT-OSS 120B | 2 | 0 | 3 | 0 | 1 | 0 |
| | | | Mistral | 0 | 0 | 1 | 0 | 0 | 0 |
| | | | Gemma | 0 | 0 | 0 | 0 | 0 | 1 |
| ἐλαφρός (light in weight) | روشن | *light* → bright | Qwen | 2 | 0 | 3 | 1 | 0 | 0 |
| | | | Llama 3.1 8B | 0 | 0 | 1 | 0 | 0 | 0¹ |
| ὅπλα (weapons) | زیربغل | *arms* → armpit | Qwen | 1 | 0 | 0 | 0 | 0 | 0 |
| σῖτος (grain) | ذرت ("maize") | *corn* → maize | Llama 3.3 70B | 2 | – | – | – | – | – |
| | | | Mistral | 1 | – | – | – | – | – |
| δακτύλιος (finger ring) | زنگ انگشت ("finger bell") | *ring* → bell | Llama 3.1 8B | 1 | – | – | – | – | – |

The English-only sense of a trap word. In the first four models, 7 of 924 direct trap answers
(0.8%), on 4 of the 77 traps; the automatic check finds 2 of the 7, and the other 5 use Persian
words missing from the key and were found by reading. In the four newer models, 4 of 923 (0.4%),
on 2 traps, none of them from Gemma.

#### B. English sound-alikes

The Greek word sounds like an English word.

| Greek | Answer | Sounds like | Model | Direct | T 0 | T 0.7 | T 1.0 | T 1.5 | T 2.0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| πίσσα (pitch) | ادرار، پیشاب | *piss* | Qwen | 3 | 5 | 4 | 4 | 3 | 1 |
| | | | GPT-OSS 20B | 1 | 0 | 0 | 0 | 0 | 0¹ |
| φοῖνιξ (date palm) | روباه، فاکس | *fox* | GPT-OSS 120B | 3 | 5 | 5 | 5 | 4 | 3 |
| | | | GPT-OSS 20B | 0 | 0 | 0 | 1 | 1 | 0¹ |
| ῥιπίς (fan) | تف، اسپیت | *spit* | GPT-OSS 120B | 2 | 5 | 3 | 3 | 3 | 1 |
| ῥόπαλον (club) | طناب، ریسمان | *rope* | GPT-OSS 20B | 3 | 5 | 2 | 3 | 0 | 1¹ |
| | | | GPT-OSS 120B | 1 | 0 | 0 | 0 | 0 | 0 |
| μίνθη (mint) | ذهن، فکر، یاد | *mind* (?) | GPT-OSS 120B | 3 | 5 | 5 | 5 | 4 | 5 |
| | | | GPT-OSS 20B | 0 | 0 | 0 | 1 | 0 | 0¹ |

μίνθη is uncertain: یاد ("memory") may instead come from Greek μνήμη.

None of the four newer models gives any of these sound-alikes, at any temperature. Gemma, for
example, answers قیر / قطران for πίσσα, نعنا for μίνθη and ققنوس / فنیقی for φοῖνιξ. So these
traces belong to GPT-OSS and Qwen, not to the models in general.

#### C. English words in Persian script

| Written | English | For | Answers (all runs) |
| --- | --- | --- | --- |
| فاکس | *fox* | φοῖνιξ | 17 (GPT-OSS 120B 16, GPT-OSS 20B 1) |
| پالم | *palm* | παλάμη | 12 (GPT-OSS 120B 10, GPT-OSS 20B 1, Mistral 1) |
| اسپیت | *spit* | ῥιπίς | 4 (GPT-OSS 120B) |
| آرک | *ark* | κιβωτός | 1 (GPT-OSS 120B) |
| لارد | *lard* | πίσσα | 1 (GPT-OSS 120B) |
| لایت | *light* | ἐλαφρός | 1 (Llama 3.1 8B) |

#### D. English or Modern Greek?

Here the source can't be told apart.

| Greek | Answer | Possible source | Model: direct |
| --- | --- | --- | --- |
| βακτηρία (staff) | باکتری | *bacteria*; Modern Greek βακτήριο | GPT-OSS 120B 3/3, GPT-OSS 20B 3/3, Qwen 3/3, Llama 3.3 70B 3/3, Llama 3.1 8B 3/3, Gemma 2/3, Mistral 2/3 |
| κορμός (tree trunk) | بدن، جسم ("body"), بالاتنه ("torso") | *trunk* as torso; Modern Greek κορμί | GPT-OSS 120B 3/3, GPT-OSS 20B 2/3, ALLaM 3/3, Llama 3.3 70B 3/3, Gemma 2/3, Mistral 2/3 |

#### E. Switching to English inside a word

Llama, and less often Mistral and Qwen, start a word in Persian script and finish it in Latin
letters. The Persian letter is the first sound of the English word, so the English word was
already chosen when the first letter came out.

| Greek | Written | English | Model |
| --- | --- | --- | --- |
| ἀποκτείνω (kill) | کilling | *killing* | Llama 3.3 70B (3 of 3) |
| δόρυ (spear) | سpear, سPEAR | *spear* | Llama 3.3 70B (2) |
| φλοιός (bark) | بark | *bark* | Llama 3.3 70B |
| πρύμνα (stern) | سtern | *stern* | Llama 3.3 70B |
| πλέω (sail) | سailing | *sailing* | Llama 3.3 70B |
| φέρω (carry) | هaulم | *haul* | Llama 3.3 70B |
| μαθητής (pupil) | استUDENT | *student* | Llama 3.1 8B |
| δοῦλος (slave) | بondservant | *bondservant* | Llama 3.1 8B |
| θύω (sacrifice) | بLOODریختن | *blood* + Persian ریختن ("shed") | Llama 3.1 8B |
| εἰρήνη (peace) | سرenity | *serenity* | Llama 3.1 8B |
| δικαστήριον (court) | تribunals | *tribunals* | Mistral |
| ξίφος (sword) | دagger | *dagger* | Qwen |

This is the most direct surface sign of an English word under the Persian so far. It is not
only English, though: Llama 3.1 8B does the same with French and Italian or Latin (پrière,
لupo, دexter), and Llama 3.3 70B now and then drops a Chinese word into the Persian (金属
"metal" for μέταλλον, 额 "forehead" for κρόταφος). GPT-OSS and Gemma never do it.

Many other errors have nothing to do with English:
- Confusion with another Greek word: νῆσσα (duck) → island, from νῆσος (also Gemma 3/3); ἧλος
  (nail) → sun, from ἥλιος (also Llama 3.3 70B), and → marsh, from ἕλος (Gemma); βραχίων (arm)
  → short, from βραχύς; κρόταφος (temple of the head) → grave, from τάφος, and → rattle or
  cymbal, from κρόταλον (Gemma 3/3); ῥιπίς (fan) → missile or whip, from ῥίπτω (Gemma).
- Later Greek senses: δρόμος → road (all eight models), μέταλλον → metal, τράπεζα → bank
  (GPT-OSS 120B and 20B, Gemma, Llama 3.1 8B 3/3; Llama 3.3 70B 2/3).
- GPT-OSS 120B always reads πίσσα as چربی ("fat"), probably from πῖαρ / πίων.

Gemma's mistakes are almost all of this Greek-internal kind.

Full list: [`findings.csv`](findings.csv).

### 3. What temperature shows

The sound-alikes (B) are what the model answers by default: at temperature 0 the main model
gives them in 5 of 5 samples, and most are still there at 2.0. The homonym senses (A) never
appear at temperature 0, only at 0.7–1.5. So the English meaning is there as a weaker option
that the model sometimes picks.

Across the eight models GPT-OSS 120B is the outlier: the nine effects together show up in 15
of its 45 samples even at temperature 0 (φοῖνιξ, ῥιπίς and μίνθη, 5 of 5 each). Qwen and GPT-OSS 20B have a few. The four newer models
have almost none at any temperature (Gemma: 1 of 219 samples, παλάμη → برگ نخل at 2.0). Llama
and Mistral fall into gibberish from temperature 1.0 upward (Mistral: all 45 samples at 1.5),
so for them only 0 and 0.7 can be compared. Their missing 1.5 and 2.0 words, filled later with
one sample each, are gibberish too, mostly running to the token limit (Llama 3.3 70B: all 14).

### 4. Kinship

*Paused: may be continued later. Files in [`kinship/`](kinship/).*

Greek and Persian mark which side of the family a relative is on, and English does not:
πάτρως is the father's brother (عمو), μήτρως the mother's brother (دایی), and both are *uncle*
in English. A wrong-side answer would point to English. The test uses 13 such terms, sent
alone (one term per request) and inside lists of 12 words, where they are mixed with filler
words from the word list.

Counts from the automatic check, of all samples at temperatures 0, 0.7 and 1.0 (91 per
condition when all three were run). "Kept" means only the right side; "wrong" only the wrong
side; "both" gives both sides, e.g. عمو and دایی for the same word.

| Model | Alone: kept | Alone: wrong | Alone: both | In list: kept | In list: wrong | In list: both |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-OSS 120B | 16 / 91 | 1 | 3 | 9 / 91 | 3 | 1 |
| Llama 3.3 70B | 17 / 91 | 2 | 1 | 17 / 91 | 1 | 8 |
| Qwen 3.8 27B | 9 / 91 | 1 | 1 | 9 / 91 | 1 | 1 |
| Qwen 3.8 27B (no thinking) | 9 / 91 | 1 | 3 | 10 / 91 | 0 | 0 |
| Gemma 4 26B | 6 / 91 | 0 | 0 | 0 / 2 | 0 | 0 |
| Gemma 4 26B (no thinking) | 0 / 91 | 0 | 0 | 4 / 91 | 0 | 0 |
| GPT-OSS 20B | 5 / 65 | 0 | 0 | 3 / 39 | 0 | 0 |
| Llama 3.1 8B | 2 / 39¹ | 1 | 0 | 3 / 39¹ | 1 | 1 |
| Mistral Small 3.1 24B | 5 / 39¹ | 0 | 0 | 2 / 39¹ | 0 | 0 |

¹ One sample at 0.7 and 1.0 instead of three. For these two models the automatic "kept" is
generous: on a first reading (not yet hand-checked), only 4 of their 10 "kept" answers at 0.7
and 1.0 are right (ὁμοπάτριος → همپدری, θυγατριδοῦς → دخترزاده, ὁμομήτριος → خواهر مادری).
The others are wrong in ways that have nothing to do with English, e.g. Mistral's πάτρως →
پدر ("father") and θυγατριδοῦς → دختر کوچک ("little girl").

Many of these words are rare, and the models often fail on the Greek itself before English
could play any part:
- Apart from one Llama 3.1 8B answer (below), no model gets any of the inherited terms
  (πάτρως, μήτρως, δαήρ, γάλοως, εἰνάτερες, ἀέλιοι, ἑκυρός, ἑκυρά). Only the transparent compounds (πατράδελφος, μητράδελφος,
  ὁμοπάτριος, ὁμομήτριος, θυγατριδοῦς) are ever right.
- Gemma's errors are again Greek-internal. It reads the πατρ- words as πατρίς / πάτριος
  ("fatherland"): πάτρως → وطن, πατράδελφος and ὁμοπάτριος → هم‌وطن ("compatriot").
  μητράδελφος becomes a half-brother by the same mother (برادر ناتنی، برادر از یک مادر),
  θυγατριδοῦς a little girl (دخترک), and μήτρως → مادر.
- Llama 3.3 70B understands the compounds best, but in lists it often gives both sides:
  πατράδελφος → عمو، دایی، عموی پدر; μητράδελφος → برادر مادر، عمو. Both Persian
  words for the one English *uncle* is the pattern an English route would produce. GPT-OSS
  120B does the same with μητράδελφος (4 wrong, 4 both).
- Llama 3.1 8B once gives ἑκυρά (husband's mother) as مادرزن ("wife's mother") next to
  مادرشوهر, the two sides of English *mother-in-law*, and at 0.7 as مادرزن alone.

Wrong-side and both-side answers stay rare (at most 9 of 91 per condition), and 28 of
the 31 fall on two compounds, πατράδελφος and μητράδελφος.

### Reading the results

This experiment tests only the simplest kind of relay, a **surface relay**: the Greek word
becomes an English word, and the Persian comes from that English word, ambiguity and all. The
forced pivot shows what such a relay produces. When the model's own English word is the
ambiguous one, the trap fires in 29–80% of cases for the stronger models. The direct answers
come nowhere near that, so as a rule the models do not relay through English words.

A relay can be much harder to see, though. A model could go through English, or through an
English-shaped space of meanings, and still know which sense of *seal* the Greek word had. Its
answers would then look exactly like a direct translation, and no trap would fire. A model that
is good at telling senses apart hides such a relay from this test, so the test can't detect
it or rule it out. Finding these relays needs other methods.

Even so, the surface relay is not absent. English shows through in a small share of the direct
answers: English double meanings, sound-alikes, English words in Persian script, and words
that switch to English halfway. These traces are few, but the fact that they exist at all
matters. A model that went straight from Greek to Persian should leave none. If English shows
at the surface, it is worth asking what it does underneath.

With eight models, the traces turn out to be specific to each model rather than shared. GPT-OSS
leaks through sound-alikes, Llama through English words that show through mid-word, and Gemma,
the model that knows the most words, hardly leaks at all. None of the sound-alikes found in
GPT-OSS and Qwen turns up in the four newer models. Whatever role English plays, it is not one
route that all models take in the same way.

Next I want to move to subtler ways of finding a relay: detailed traces of English in the
syntax and semantics of whole sentences, looking at both negative and positive transfer and
how they differ. Pronouns are one example. Greek and Persian both drop subject pronouns, but
English cannot, so a Persian translation that spells them out would point to English in
between.

## Files

| File | What it holds |
| --- | --- |
| `prompts.toml` | The three prompts, word for word. `user` is the whole message; `{{SOURCE}}` is replaced by the word or the English word. |
| `greek_words.csv` | The 200 words: trap or filler, the Greek sense, the English pivot word, the right Persian (`fa_correct`) and the Persian that only comes via English (`fa_via_english`). |
| `answers.csv` | The direct run and the forced pivot: one row per answer, with the model's English word from step 1, whether the English-only Persian appears and where. |
| `temperature.csv` | The temperature test: one row per answer, with whether the effect looked for appears. |
| `findings.csv` | The traces found by reading the answers (section 2). |
| `kinship/prompts.toml` | The two kinship prompts, word for word: `words-neutral` (alone) and `words-list` (in a list). |
| `kinship/kinship_terms.csv` | The 13 kinship terms: LSJ gloss, English word, the Persian for the right side (`fa_side_kept`) and for the wrong side (`fa_side_lost`). |
| `kinship/answers.csv` | The kinship test: one row per term per answer, alone (`isolated`) or in a list, classed as kept, wrong, both, generic, other or missing. |

Every answer is in these files as the model returned it (column `raw`), next to the Persian
equivalents split out of it. The flags (`p2_found`, `effect_seen`, `class`) come from an
automatic whole-word search against the keys and have been only partly checked by hand. The code
is not published; ask me if you need it.

## How the models were run

Each word was one request to an OpenAI-compatible chat API: a single user message built from
the prompt, no system prompt, no seed, and nothing else in the conversation. The three prompts,
as sent, are in [`prompts.toml`](prompts.toml).

| Model | API model | Served by | Token limit | Settings |
| --- | --- | --- | --- | --- |
| GPT-OSS 120B | `openai/gpt-oss-120b` | Groq | 3000 | `reasoning_effort = low` |
| GPT-OSS 20B | `openai/gpt-oss-20b` | Groq | 3000 | `reasoning_effort = low` |
| Qwen 3.8 27B | `qwen/qwen3.8-27b` | Groq | 2048 | default |
| Qwen 3.8 27B (no thinking) | `qwen/qwen3.8-27b` | Groq | 1000 | `reasoning_effort = none`; kinship only |
| ALLaM 2 7B | `allam-2-7b` | Groq | 1024 | |
| Llama 3.3 70B | `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | Cloudflare | 1024 | |
| Llama 3.1 8B | `@cf/meta/llama-3.1-8b-instruct-fp8` | Cloudflare | 1024 | |
| Mistral Small 3.1 24B | `@cf/mistralai/mistral-small-3.1-24b-instruct` | Cloudflare | 1024 | |
| Gemma 4 26B | `@cf/google/gemma-4-26b-a4b-it` | Cloudflare | 3000 (kinship and pivot step 1: 8000) | default (thinking on) |
| Gemma 4 26B (no thinking) | `@cf/google/gemma-4-26b-a4b-it` | Cloudflare | 1500 | `chat_template_kwargs = { enable_thinking = false }`; kinship only |

All ten are open-weight. Groq is [Groq](https://console.groq.com); Cloudflare is
[Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/) on the free tier.

| Test | Prompt | Models | Samples | Temperature |
| --- | --- | --- | --- | --- |
| Direct: Greek → Persian | `words-neutral` | all 8 | 3 | 0.7 |
| Pivot step 1: Greek → English | `words-pivot-en` | all 8 | 1 | 0.2 |
| Pivot step 2: own English word → Persian | `words-pivot-fa` | all 8 | 1 | 0.2 |
| Temperature: 9 items from the direct run | `words-neutral` | all except ALLaM | 5 (gaps: 1) | 0, 0.7, 1.0, 1.5, 2.0 |
| Kinship, one word per request | `words-neutral` | GPT-OSS 120B, Llama 3.3 70B, Qwen and Gemma (thinking on and off); GPT-OSS 20B (1 at 1.0); Llama 3.1 8B and Mistral (1 / 1 / 1) | 1 / 3 / 3 | 0, 0.7, 1.0 |
| Kinship, embedded in lists of 12 | `words-list` | as above (GPT-OSS 20B 1 / 1 / 1), but Gemma with thinking on only at 0 | 1 / 3 / 3 | 0, 0.7, 1.0 |

The Groq models ran on 7–9 October 2026. GPT-OSS 20B was first left out of pivot step 2,
temperature 2.0 and most of the kinship runs after performing poorly early on; these were run on 4 November 2026, with one
sample per word. ALLaM is in the word-list tests only, and mostly answered in Arabic or with nonsense.

The Cloudflare models were added later, 13–16 October 2026. Gaps:
- Gemma has 598 of 600 direct samples. On ὕδωρ and ῥιπίς it sometimes keeps going past its
  3000-token limit and returns nothing; ῥιπίς does so in all 5 samples at temperature 0.
- Llama 3.3 70B and 3.1 8B had only 4 of the 9 words at temperature 1.5 and few or none at
  2.0, and Mistral had 4 of 9 at 2.0, because both models already answer mostly gibberish
  there. The missing words were run on 4 November 2026 with one sample each, and the same
  date filled Llama 3.1 8B's and Mistral's kinship runs at 0.7 and 1.0 (one sample each).
- Kinship ran on 17 October 2026. Gemma's token limit was raised from 3000 to 8000 for it
  (the direct run used 3000). Gemma with thinking on spends more than 8000 tokens on most lists
  and returns nothing (1 of 5 lists at temperature 0 came back), so the lists were also run
  with thinking switched off, in the same way as Qwen. Llama 3.1 8B and Mistral understood none
  of the 13 terms alone at temperature 0, so at 0.7 and 1.0 they have one sample each. At 1.0
  Llama 3.1 8B's lists fall into gibberish (12 of 13 terms missing).
- The forced pivot ran 18–19 October 2026, Gemma with thinking on (as in its direct run): step
  1 with a limit of 8000 tokens, step 2 with 3000. Gemma's step 2 has 186 of its 199 English
  words; the other 13 (among them *horse*, *bread*, *mountain*, *night*) ran past the limit
  every time, while no answer that came back used more than 2445 tokens.

## Note

The code that ran and scored these tests, and the README files, were generated with the
assistance of Claude Opus 5.5.
