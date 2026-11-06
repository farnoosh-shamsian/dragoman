# Plato's dialogues

Part of [Dragoman](../README.md).

*Ongoing: the machine translations are done; the error annotation is under way, and the results
below are preliminary.*

Two dialogues of Plato, the *Crito* and the *Euthyphro*, translated into Persian by language models
and compared with Persian translations made by people. Four of the five printed Persian translations of the
*Crito* were made from English, French or German; only the most recent one, Shafi'-Beyk's (2023),
was made directly from the Greek. So the question is whether the models' Persian reads more like a direct
translation or like an indirect one. The *Euthyphro* was added because I took part in one of the
*Crito* translations (the course translations below), and it has none of my own.

## The texts

- ***Crito*:** the whole dialogue, 276 sentences, sent in 17 chunks of about 250 Greek words.
- ***Euthyphro*:** 2a–4b, sentences 1–65, the stretch for which I have Shafi'-Beyk's
  translation, sent in 3 chunks of about 225 Greek words. Where a translator joins or splits
  sentences, the Greek sentences are merged into one unit (44 units), the same for every
  translation.

The Greek is Burnet's text from Perseus (`tlg0059.tlg003.perseus-grc2`, `tlg0059.tlg001.perseus-grc1`),
cut into sentences where the treebanks end them (Gorman 2020 for the *Crito*; AGDT 2.1 for the
*Euthyphro*). Every sentence keeps its treebank id and its Stephanus section.

## The translations

- **Open-weight models:** Gemma 4 26B, Mistral Small 3.1 24B, Llama 3.3 70B, GPT-OSS 120B, GPT-OSS
  20B and Qwen 3.8 27B, the models of the [pro-drop test](../pro-drop-test/), at temperature 0 and 1.
- **Web chats:** Claude Opus, Claude Sonnet, ChatGPT, Gemini and DeepSeek, run by hand with a new
  chat for every chunk, with the chats' default settings. The *Crito*'s Claude Sonnet run was
  Sonnet 5 at medium effort; the other model versions were not recorded.
- **Course translations** (*Crito* only): three finalized course translations and five learner
  translations, made directly from the Greek in my course and published with an earlier corpus
  (Shamsian et al. 2025).
- **Printed translations:** Foroughi (1938), Lotfi (1979), Jahanshahi (1989) and Golestan (2013),
  all indirect, and Shafi'-Beyk (2023), direct. For the *Euthyphro*: Foroughi, Lotfi and
  Shafi'-Beyk. They are under copyright, so they are not shared as whole texts; only the short
  passages annotated with MQM appear, side by side with the other translations of the same passage
  (`mqm_units.csv`).

Every model and chat got the same plain prompt ([`prompts.toml`](prompts.toml)) and nothing else:
no system prompt, no dictionary, no treebank. The open models also translated the *Crito* one
sentence at a time and at higher temperatures; those runs are kept for later and are not in this
release.

## Preliminary results

I annotate every translation of a sample against the Greek with MQM: each error gets a type
(accuracy, addition, terminology, fluency, style, non-translation) and a severity (minor 1 point,
major 5, critical 10; a sentence left untranslated 25). The score is the penalty per 100 Greek
words, so lower is better. Units so far: *Crito* 7 (192 Greek words, 18 translations each),
*Euthyphro* 7 (164 Greek words, 13 translations each; there are no course translations of it).
Llama 3.3 70B is not scored in either, as it failed a screen for noisy output on the *Crito*.

| | *Crito* | *Euthyphro* |
|---|---|---|
| Course translations (3), mean | 1.6 | |
| Shafi'-Beyk (direct) | 7.8 | 5.5 |
| Claude Opus | 11.5 | 11.6 |
| ChatGPT | 15.1 | 24.4 |
| Gemini | 18.8 | 34.1 |
| Claude Sonnet | 20.8 | 34.1 |
| DeepSeek | 26.6 | 59.1 |
| Jahanshahi (indirect) | 26.0 | |
| Golestan (indirect) | 34.9 | |
| Lotfi (indirect) | 37.0 | 54.3 |
| Foroughi (indirect) | 44.8 | 49.4 |
| Gemma 4 26B | 54.2 | 78.0 |
| Qwen 3.8 27B | 56.8 | 70.1 |
| GPT-OSS 120B | 103.6 | 123.8 |
| Mistral Small 3.1 24B | 104.7 | 125.6 |
| GPT-OSS 20B | 142.2 | 165.2 |
| **Group means:** direct, published | **7.8** | **5.5** |
| web chats | **18.6** | **32.7** |
| indirect, published | **35.7** | **51.8** |
| open models | **92.3** | **112.6** |

The open models are scored on their temperature 0 runs.

- **The same order in both dialogues:** the direct human translations make the fewest errors, then
  the web chats, then the indirect human translations, then the open models. In the *Euthyphro*, a
  resampling of the units keeps each step of this order in 98–100% of draws.
- **The best web chat, Claude Opus, comes closest to the direct translator** in both dialogues; the
  other chats sit between the direct and the indirect translations.
- **The open models make the most errors**, more than any human translation, so taken together the
  language models do not fall between the direct and the indirect translators.
- **The two dialogues rank the 13 shared translations almost alike** (Spearman ρ 0.97), and 12 of
  the 13 score worse on the *Euthyphro*.

These figures rest on 7 short units per dialogue and a single annotator, so they will move as the
annotation goes on.

## Limits

These are case studies of two short dialogues, which the models have very likely seen in training,
so the results may not hold for other texts. Only one published Persian translation is direct, so
directness cannot be fully separated from translator, date and source language. I do the
annotation alone and on a small sample, so agreement between annotators cannot be measured. The web
chats cannot be reproduced exactly, and each chunk was run once.

## Files

| File | What it holds |
| --- | --- |
| `prompts.toml` | The prompt, word for word. `user` is the whole message; `{{SOURCE}}` is replaced by a chunk. |
| `crito.csv` | The *Crito*, one row per sentence (276): treebank id, Stephanus section, chunk, Greek, then one column per translation: the 8 course translations, each open model at T 0 and T 1, and the 5 web chats. |
| `euthyphro.csv` | The *Euthyphro* 2a–4b, one row per unit (44): unit, sentence numbers, treebank ids, section, speaker, chunk, Greek, then each open model at T 0 and T 1 and the 5 web chats. |
| `mqm_results.csv` | The scores in the table above: one row per translation and per group, for each dialogue. |
| `mqm_units.csv` | Every annotated passage in every translation (233 rows): dialogue, unit, passage (Stephanus section and sentence numbers), Greek words, translation, group, the Greek and the Persian with sentence numbers in brackets, and my annotation of it: whether I took it for a human or an LLM translation before marking errors (`judged as`, `guess`), its register, the minutes spent, the number of errors, the points and the penalty per 100 Greek words. |
| `mqm_errors.csv` | Every error marked (547 rows): dialogue, unit, translation, sentence, whether it was marked in the Persian or in the Greek (an omission), the step (1: reading the Persian alone; 2: against the Greek), the words marked, category, subcategory, severity, points, an unsure flag and my note. |

In the MQM tables, `annotation` is `main` for the annotation the scores use. For 16 *Crito*
translations I annotated the same passage a second time under new codes, to check my own
consistency; these rows are marked `repeat` and do not count in the scores. Errors of the category
`Other` (a reading from another edition) are listed but score 0 points. The Persian in the MQM
tables is the text as I annotated it, with spacing and letter forms normalised.

An empty cell means that the translation has no text for that sentence: a translator merged it
with the next one, or a model left it out (Mistral at T 1 leaves out 12 *Euthyphro* units).

## References

- Gorman, V. B. (2020). Dependency Treebanks of Ancient Greek Prose. *Journal of Open Humanities
  Data*, 6, 1. https://doi.org/10.5334/johd.13
- Shamsian, F., Assimi, S., Mahmoudzadeh Sarabi, A., Mohammadi, N., Nikpour, K., & Rahimi, F.
  (2023–2024). *Word-aligned Parallel Corpus of Plato's Crito in Persian* [Data set]. Zenodo.
  https://doi.org/10.5281/zenodo.17607620 (CC BY 4.0)
- Shamsian, F., Rahimi, F., Mahmoudzadeh Sarabi, A., Mohammadi, N., Nikpoor, K., & Assimi, S.
  (2025). Word-aligned Parallel Corpus of Plato's *Crito* in Persian: A Pedagogical Approach to
  Digital Annotations. *Journal of Open Humanities Data*, 11(1), 78.
  https://doi.org/10.5334/johd.398 (full references for the printed Persian translations)
- Freitag, M., Foster, G., Grangier, D., Ratnakar, V., Tan, Q., & Macherey, W. (2021). Experts,
  Errors, and Context: A Large-Scale Study of Human Evaluation for Machine Translation.
  *Transactions of the ACL*, 9, 1460–1474.
- Lommel, A., Uszkoreit, H., & Burchardt, A. (2014). Multidimensional Quality Metrics (MQM): A
  Framework for Declaring and Describing Translation Quality Metrics. *Tradumàtica*, 12, 455–463.

The Greek texts and treebanks are under CC BY-SA, and so is the Greek in `crito.csv` and
`euthyphro.csv`. Everything else here is CC BY 4.0, like the rest of the repo.
