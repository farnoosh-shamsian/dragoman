# Word-list experiment

Part of [Dragoman](../README.md).

Do language models translate Ancient Greek into Persian **via English**? This is an ongoing
pilot study. It started with single words and four open-weight models, and I keep adding models
and tests, so some of the results here are unfinished.

Done so far: the direct run and the temperature test on eight open-weight models. The first four
(GPT-OSS 120B, GPT-OSS 20B, Qwen 3.8 27B, ALLaM 2 7B) also have the forced pivot and the
kinship test; the four added later (Llama 3.3 70B, Llama 3.1 8B, Mistral Small 3.1 24B,
Gemma 4 26B) do not yet.

Still open:
- the forced pivot and the kinship test (section 4) for the four newer models;
- a hand check of the newer models' answers. Their counts below come from the automatic check
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
| GPT-OSS 20B | 0 / 231 (0%) | not run | – | 0 / 72 (0%) |
| ALLaM 2 7B | 0 / 231 (0%) | 3 / 77 (3.9%) | 3 / 26 (11.5%) | 0 / 78 (0%) |
| Gemma 4 26B | 0 / 230 (0%) | not run | – | – |
| Llama 3.3 70B | 2 / 231 (0.9%) | not run | – | – |
| Llama 3.1 8B | 1 / 231 (0.4%) | not run | – | – |
| Mistral Small 3.1 24B | 1 / 231 (0.4%) | not run | – | – |

The "own English word = trap word" columns keep only the traps where the model's step-1 English
word was the ambiguous one (*bank*, *seal*, *temple*…). When the route really runs through that
word, the English-only sense comes out about two times in three. The direct answers almost
never show it, in any of the eight models.

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
"–" means not run: only nine words are in the temperature test.

#### A. English homonyms

| Greek | Answer | English | Model | Direct | T 0 | T 0.7 | T 1.0 | T 1.5 | T 2.0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| φώκη (seal, the animal) | مهر، نشان | *seal* → stamp | GPT-OSS 120B | 2 | 0 | 3 | 0 | 2 | 0 |
| παλάμη (palm of the hand) | نخل, «پالم» | *palm* → tree | GPT-OSS 120B | 2 | 0 | 3 | 0 | 1 | 0 |
| | | | Mistral | 0 | 0 | 1 | 0 | 0 | 0 |
| | | | Gemma | 0 | 0 | 0 | 0 | 0 | 1 |
| ἐλαφρός (light in weight) | روشن | *light* → bright | Qwen | 2 | 0 | 3 | 1 | 0 | 0 |
| | | | Llama 3.1 8B | 0 | 0 | 1 | 0 | 0 | – |
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
| | | | GPT-OSS 20B | 1 | 0 | 0 | 0 | 0 | – |
| φοῖνιξ (date palm) | روباه، فاکس | *fox* | GPT-OSS 120B | 3 | 5 | 5 | 5 | 4 | 3 |
| | | | GPT-OSS 20B | 0 | 0 | 0 | 1 | 1 | – |
| ῥιπίς (fan) | تف، اسپیت | *spit* | GPT-OSS 120B | 2 | 5 | 3 | 3 | 3 | 1 |
| ῥόπαλον (club) | طناب | *rope* | GPT-OSS 20B | 3 | 5 | 2 | 3 | 0 | – |
| | | | GPT-OSS 120B | 1 | 0 | 0 | 0 | 0 | 0 |
| μίνθη (mint) | ذهن، فکر، یاد | *mind* (?) | GPT-OSS 120B | 3 | 5 | 5 | 5 | 4 | 5 |
| | | | GPT-OSS 20B | 0 | 0 | 0 | 1 | 0 | – |

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

Full list: `results/findings.csv`.

### 3. What temperature shows

The sound-alikes (B) are what the model answers by default: at temperature 0 the main model
gives them in 5 of 5 samples, and most are still there at 2.0. The homonym senses (A) never
appear at temperature 0, only at 0.7–1.5. So the English meaning is there as a weaker option
that the model sometimes picks.

Across the eight models GPT-OSS 120B is the outlier: the nine effects together show up in 15
of its 45 samples even at temperature 0 (φοῖνιξ, ῥιπίς and μίνθη, 5 of 5 each). Qwen and GPT-OSS 20B have a few. The four newer models
have almost none at any temperature (Gemma: 1 of 219 samples, παλάμη → برگ نخل at 2.0). Llama
and Mistral fall into gibberish from temperature 1.0 upward (Mistral: all 45 samples at 1.5),
so for them only 0 and 0.7 can be compared, and their 1.5 and 2.0 runs were not finished.

### 4. Kinship (in progress)

Greek and Persian mark which side of the family a relative is on, and English does not:
πάτρως is the father's brother (عمو), μήτρως the mother's brother (دایی), and both are *uncle*
in English. A wrong-side answer would point to English. The test uses 13 such terms, sent
alone and inside word lists.

Many of these words are rare, and the models often fail on the Greek itself before English
could play any part. Very early results: the transparent compounds (πατράδελφος,
μητράδελφος, ὁμοπάτριος, ὁμομήτριος) are understood, the inherited terms (πάτρως, μήτρως,
δαήρ…) almost never are, and wrong-side answers are rare (at most 3 of 91 per model). More
results are coming. The four newer models are not in this test yet.

### Reading the results

English does leak in, mostly through what a word looks or sounds like, and sometimes, with
sampling, through an English double meaning. It doesn't look like a word-for-word pivot,
which would make the traps fire far more often (see the forced pivot). But a pivot that keeps
the meaning, going through English concepts rather than English words, would leave no trace
in the traps at all, so this design can't rule that out.

With eight models, the traces turn out to be specific to each model rather than shared. GPT-OSS
leaks through sound-alikes, Llama through English words that show through mid-word, and Gemma,
the model that knows the most words, hardly leaks at all. None of the sound-alikes found in
GPT-OSS and Qwen turns up in the four newer models. Whatever role English plays, it is not one
route that all models take in the same way. Next I want to look at whole passages and syntax
(word order, calques), and at what happens inside the models.

## Runs

| Test | Source files | Prompt | Models | Samples | Temperature |
| --- | --- | --- | --- | --- | --- |
| Direct: Greek → Persian | `greek-words` | `words-neutral` | all 8 | 3 | 0.7 |
| Pivot step 1: Greek → English | `greek-words` | `words-pivot-en` | first 4 | 1 | 0.2 |
| Pivot step 2: own English word → Persian | `greek-words-pivot-*` | `words-pivot-fa` | ALLaM, GPT-OSS 120B, Qwen | 1 | 0.2 |
| Temperature: 9 items from the direct run | `greek-words-temp*` | `words-neutral` | all except ALLaM | 5 | 0, 0.7, 1.0, 1.5, 2.0 |
| Kinship, one word per request | `kinship-words-temp*` | `words-neutral` | GPT-OSS 120B, Qwen (thinking on and off) | 1 / 3 / 3 | 0, 0.7, 1.0 |
| Kinship, embedded in lists of 12 | `kinship-lists-temp*` | `words-list` | as above | 1 / 3 / 3 | 0, 0.7, 1.0 |

Models: `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `qwen/qwen3.8-27b` and `allam-2-7b`,
all open-weight, served by [Groq](https://console.groq.com), 7–9 October 2026. GPT-OSS 20B was
dropped from pivot step 2, from temperature 2.0 and from most of the kinship runs after
performing poorly early on. ALLaM is in the word-list tests only, and mostly answered in Arabic
or with nonsense.

The four models added later are `@cf/meta/llama-3.3-70b-instruct-fp8-fast`,
`@cf/meta/llama-3.1-8b-instruct-fp8`, `@cf/mistralai/mistral-small-3.1-24b-instruct` and
`@cf/google/gemma-4-26b-a4b-it`, all open-weight, served by
[Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/) on the free tier,
13–16 October 2026. Gaps:
- Gemma has 598 of 600 direct samples. On ὕδωρ and ῥιπίς it sometimes keeps going past its
  3000-token limit and returns nothing; ῥιπίς does so in all 5 samples at temperature 0.
- Llama 3.3 70B and 3.1 8B have only 4 of the 9 words at temperature 1.5 and few or none at
  2.0, and Mistral has 4 of 9 at 2.0. These were left unfinished because both models already
  answer mostly gibberish at those temperatures.

## Note

The code and README files were generated with the assistance of Claude Opus 5.5.
