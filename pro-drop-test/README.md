# Pro-drop test

Part of [Dragoman](../README.md).

*Closed (November 2026): a first, minimal answer. Larger tests may follow.*

## Question

Does the Persian of open-weight models translating Ancient Greek show a trace of an English pivot
in its subject pronouns?

Greek and Persian are both pro-drop languages: a verb can stand without a subject pronoun, and an
overt pronoun (ἐγώ, `من`) usually adds emphasis or contrast. English has to state the pronoun every
time, so the difference is lost. A translation that goes through English should lose it too: it
should drop the pronouns that the Greek stresses, or add pronouns the Greek leaves out.

## Measure

Only 1st- and 2nd-person subjects are counted, at the verb slots tagged in the Greek treebank.

- **Retention:** how often the Persian has an overt subject pronoun where the Greek has one.
- **Positive transfer:** how often the Persian adds one where the Greek has none.
- **Δ** = retention − positive transfer: how much of the Greek contrast survives in the Persian.

A translation that follows the Greek has a high Δ. A translation through English should have a Δ
near zero.

## Design

- **Text:** Plato's *Crito* (276 sentences), sent as continuous text in 17 chunks of about 250
  Greek words. It is the text with published Persian translations to compare with.
- **Models:** GPT-OSS 120B, Qwen 3.8 27B and Gemma 4 26B (Qwen and Gemma without thinking), all at
  temperature 0.
- **Conditions:**
  - *direct*: Greek → Persian;
  - *English chain*: Greek → English, then the model's own English → Persian. This is what a
    translation through English looks like, made on purpose.
- **Human baseline** (*Crito* only): published Persian translations made directly from the Greek
  (Shafi'-Beyk 2023, and the course translations of the
  [Crito corpus](https://doi.org/10.5281/zenodo.17607620)) and translations made through a
  modern language (Foroughi 1938, Lotfi 1979, Jahanshahi 1989, Golestan 2013). Only the figures
  are published here, not the translations.
- **Web chats** (direct only): ChatGPT, Gemini, DeepSeek, Claude Opus and Claude Sonnet, given the same
  chunks with the same direct prompt, by hand in each web chat with its default settings. Their
  translations come from the [Plato's dialogues](../plato-dialogues/) folder; we have no English
  chain for them.
- **Annotation:** the Greek side comes from the treebank. The Persian side is marked by a
  rule-based detector, which I checked by hand on 19 blinded rows (below).

### Prompts

The three prompts, as sent, are in [`prompts.toml`](prompts.toml): `chunk-direct` (direct,
and the web chats), `chunk-pivot-en` (English chain, step 1) and `chunk-relay-fa` (English chain,
step 2, where the model gets its own English with the Greek left out and the source language not
named). Each request was a new conversation with no system prompt.

### Models

| Model | Provider and model id | Settings |
|---|---|---|
| GPT-OSS 120B | Groq, `openai/gpt-oss-120b` | temperature 0, reasoning effort low, max 3,000 tokens |
| Qwen 3.8 27B | Groq, `qwen/qwen3.8-27b` | temperature 0, reasoning off, max 1,000 tokens |
| Gemma 4 26B | Cloudflare Workers AI, `@cf/google/gemma-4-26b-a4b-it` | temperature 0, thinking off, max 2,000 tokens |

One answer per chunk. The answers were split back into sentences by their numbers.

The measures and predictions for the models were fixed before the main analysis was run. The human
baseline, the web chats and the extra-pronoun checks were added afterwards and are exploratory. The plan also ran
two of the models on Plato's *Euthyphro* and Lysias 1; with no Persian translations of those to
compare with, they are left out of this release. The *Crito* has only 12 sentences with one stressed
pronoun, so the per sentence and person count (24 stressed, 128 left out) is the steadier figure.

## Results

Δ in percentage points. Intervals (95%, bootstrap over sentences) are in
[`results.csv`](results.csv).

| | Sentences with one slot (81) | Per sentence and person (152) |
|---|---|---|
| GPT-OSS 120B, direct | **+76** | **+72** |
| GPT-OSS 120B, English chain | +6 | +22 |
| Qwen 3.8 27B, direct | **+45** | **+55** |
| Qwen 3.8 27B, English chain | +9 | +33 |
| Gemma 4 26B, direct | **+66** | **+65** |
| Gemma 4 26B, English chain | +27 | +41 |
| Web chats, direct (five, averaged) | **+58** | **+64** |
| Human, direct from Greek | **+59** | **+73** |
| Human, through another language | +15 | **+25** |

## Answer

**No trace of English, by this measure.** Going through English wipes out most of the Greek
contrast, for the models' English chains and for the human translators who worked from a modern
language alike. The models' direct Persian keeps it about as well as the direct human translations
do (models − humans: −9 points, interval −21 to +6). In its pronouns, their direct translation
looks like a direct translation, not like a pivot. The five web chats come out the same: +64 on
average, from +54 (ChatGPT) to +72 (DeepSeek), no different from the open models (0 points,
interval −13 to +12).

**One reservation.** The models add pronouns the Greek doesn't have more often than human
translators do: 19–24% of the empty Greek slots in the *Crito*, against 7% for the direct human
translations and 13% for the indirect ones. The web chats add 12% on average, half as many as
the open models (−10 points, interval −15 to −6), though still more than the direct human
translations (+5, interval +1 to +9). So most of the excess belongs to the open models. They keep
the gap as high as the web chats only because they also keep more of the Greek's own pronouns
(86% against 76%). This test can't say why they add so many. The exploratory checks (the
"added pronouns" rows of [`results.csv`](results.csv)) point both ways:

- The added pronouns are mostly 1st person (13–33% of empty 1st-person slots, against 5–13% of
  2nd-person ones, in sentences with one slot).
- About 70% of them sit where at least one human translator also adds a pronoun, as in most human
  translations. For the English chains the figure is lower, 51–58%. This points away from English.
- Qwen's and Gemma's direct translations add pronouns more often where their own English chain
  adds one than where the other models' English chains do (+23 and +20 points). This may be each
  model's own habit, or a trace of English. GPT-OSS shows no such difference (+8, not clear), but
  its direct translation adds 1st-person pronouns nearly as often as its English chain does (23%
  and 30%).

## Detector check

I checked 19 *Crito* rows blind (GPT-OSS and Qwen: 7 direct, 12 English chain), without knowing
which model or condition each came from: 18 right, 0 wrong, 1 unsure (an English-chain row whose
syntax differs from the Greek, with plural `شما` for a Greek singular). All 7 direct rows were
right. The check is small: with no errors in 18 decided rows, the error rate could still be up to
about 18% (95% upper bound).

## Limits

- The test sees only what is on the surface of the output. A relay that leaves the pronouns as the
  Greek has them is invisible to it.
- One text, one author: the *Crito*. Other texts and genres may behave differently.
- The detector check is small (19 rows; above), and covers open-model rows only, not the web chats
  or the human translations.
- Each web chat is one run with settings we can't see or set (Claude Sonnet was Sonnet 5 at
  medium effort; the other versions were not recorded).
- The English chain translates twice. Part of what it loses may come from translating twice, not
  from English.
- The human translations were transcribed from scans and have not all been proofread. The three
  course translations are versions of one class translation and count as one translator in the
  group figures. Most published Persian *Crito*s are indirect; only Shafi'-Beyk's is direct.
- The prompts are in English, as in the other Dragoman experiments.

## Files

Three tables, linked by the sentence number `n`, and [`prompts.toml`](prompts.toml) with the
three prompts as sent.

[`greek.csv`](greek.csv): the *Crito*, one row per sentence (276).

- `n`, `tb_id`, `section`: sentence number, treebank id, Stephanus section (as in the treebank).
- `chunk`: which of the 17 chunks the sentence was sent in.
- `greek`: the sentence.
- `person_1`, `person_2`: what the Greek does with 1st- and 2nd-person subjects in the sentence.
  `null` means every such verb leaves the pronoun out, `overt` means every one has it, `mixed` means
  both (left out of the counts), and an empty cell means the sentence has none.
- `single_slot`: `null` or `overt` for the 81 sentences with exactly one 1st/2nd-person slot.
- `verbs`: the slot verbs, as form, person and number, slot (`ἀφῖξαι 2s null`).

[`translations.csv`](translations.csv): one row per sentence × system × route (6,072).

- `system`, `kind` (open model, web chat, human), `route` (`direct`, `English step 1`,
  `English chain`; for humans `direct` or `indirect`).
- `translation`: the text. `English step 1` rows are the English that was sent back for step 2.
  Left empty for the human translations, which are counted but not published here.
- `subj_1`, `subj_2`: overt 1st/2nd-person subject pronouns the detector found (in the
  `English step 1` rows, English subject pronouns).
- `pronouns`: every free pronoun the detector saw, as word:person:call (`subj`, `maybe`, `obj`,
  `obl`), for checking it.
- `emphasis`: English emphatic forms (*I myself*, *for my part*) in the `English step 1` rows.
- `problem`: a missing, looping or misnumbered sentence; such rows are left out of the counts.
- `hand_check`, `hand_check_note`: my verdict on the detector (`y` right, `?` unsure) for the 19
  checked rows.

[`results.csv`](results.csv): every reported figure (214 rows).

- `analysis`: `single-slot sentences` (81), `per sentence and person` (152), or one of the three
  `added pronouns` checks.
- `system`, `route`: a system, a group (human translators, open models, web chats) or a
  difference between groups.
- `measure`, `value`, `lo`, `hi`: retention, positive transfer or Δ (as shares, 0–1) with the 95%
  interval; `n`: units counted.

The code is not published; ask me if you need it.

## Sources and licence

The Greek text (Burnet) and treebank come from the Perseus Digital Library
(`urn:cts:greekLit:tlg0059.tlg003`; treebank `tlg0059.tlg003.kahl.tb.xml`). They are under
CC BY-SA, and so is [`greek.csv`](greek.csv), which is built from them. Everything else here is
CC BY 4.0, like the rest of the repo.

An earlier pilot (October 2026: 90 single sentences, six models) showed that raw pronoun counts
don't separate direct from English-routed Persian, and that sentences without context are too
hard. This design grew out of it.
