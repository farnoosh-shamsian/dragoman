# Crito translation

Part of [Dragoman](../README.md).

*Ongoing: the machine translations are done, and I am now preparing their evaluation.*

Plato's *Crito* has been translated into Persian five times in print. Four of these translations
were made from English, French or German, and only the most recent one, Shafi'-Beyk's (2023), was
made directly from the Greek. Beside them there are the translations made from the Greek in my
course. This makes the dialogue a good test case. In this experiment I had language
models translate the whole *Crito* into Persian, and I am comparing their translations with both
kinds of human translation: does the models' Persian read more like a direct translation, or like
an indirect one?

## The files

`crito_translations.csv` has one row for each Greek sentence, 276 in all. It gives the treebank id,
the Stephanus section and the Greek, followed by one column for each model, mode and temperature.
An empty cell means that the run has not been done yet, or that it gave no usable answer for that
sentence. `crito_translations.xlsx` is the same table as a spreadsheet.

## The Greek text

I use Burnet's text from Perseus (`tlg0059.tlg003.perseus-grc2`), cut into sentences where the
Gorman treebank (Gorman 2020) ends them. Every sentence therefore has a treebank id and a Stephanus
reference, and all the translations of a sentence, machine or human, can be found by the same
number.

## The machine translations

The models are the six open-weight models of the [pro-drop test](../pro-drop-test/): Gemma 4 26B,
Mistral Small 3.1 24B, Llama 3.3 70B, GPT-OSS 120B, GPT-OSS 20B and Qwen 3.8 27B. I gave them a
plain prompt (*Translate this Ancient Greek text into Persian*) and no other help: no system
prompt, no dictionary and no treebank.

Each model translated the dialogue twice. The first time it got one sentence per request, with no
context at all. The second time it got chunks of about 250 Greek words, cut at the end of a
sentence, with every sentence numbered so that the answer could be split back into sentences.
Comparing the two shows what the lack of context costs. I ran both at temperature 0 and 1, and
some models also at 1.5 and 2; not all of the runs at the higher temperatures are complete.

I also ran three web chats by hand, ChatGPT, Gemini and DeepSeek, with a new chat for every prompt.
They translated the whole dialogue in chunks, and the first 20 sentences one at a time. Claude Opus
5.5 translated the same 20 sentences one at a time.

## The human translations

The human translations come from an earlier project of mine, a word-aligned parallel corpus of the
*Crito* in Persian (Shamsian et al. 2025):

| Translation | Kind |
|---|---|
| Foroughi (1938) | published, indirect |
| Lotfi (1979) | published, indirect |
| Jahanshahi (1989) | published, indirect |
| Golestan (2013) | published, indirect |
| Shafi'-Beyk (2023) | published, direct (the first direct Persian translation) |
| Three finalized course translations, five learner translations | unpublished, direct |

The course translations are on Zenodo, aligned with the Greek sentence by sentence and word by
word, together with the English (Jowett, Fowler) and German (Schleiermacher) translations aligned
to the same sentences:

- Dataset: Shamsian, F., Assimi, S., Mahmoudzadeh Sarabi, A., Mohammadi, N., Nikpour, K., &
  Rahimi, F. (2023–2024). *Word-aligned Parallel Corpus of Plato's Crito in Persian* [Data set].
  Zenodo. https://doi.org/10.5281/zenodo.17607620 (CC BY 4.0)
- Paper: Shamsian, F., Rahimi, F., Mahmoudzadeh Sarabi, A., Mohammadi, N., Nikpoor, K., & Assimi, S.
  (2025). Word-aligned Parallel Corpus of Plato's *Crito* in Persian: A Pedagogical Approach to
  Digital Annotations. *Journal of Open Humanities Data*, 11(1), 78.
  https://doi.org/10.5334/johd.398

The published translations are under copyright, so I do not share them here in full. Only short
passages, annotations and scores will appear.

## How I am evaluating them

I judge every translation against the Greek, and I use several methods so that each can check the
others.

The main one is MQM error annotation. I chose a sample of passages from across the dialogue: the
opening, Crito's appeal, the argument and the speech of the Laws. In every translation of these
passages I mark each error with its kind (accuracy, terminology, fluency, style or
non-translation) and its severity. All the translations are judged on the same passages and under
random codes, so that the annotation is as blind as I can make it.

The argument of the *Crito* rests on a handful of words: justice and wrongdoing, persuading and
obeying, the laws, agreement. So I also look at how each translation renders them, and whether it
renders them consistently.

The indirect translations can inherit errors from the English, French or German text they were made
from, so I check their errors against that text. I run the same check on the machine translations,
against the English translations the models will have read. This is where the experiment meets the
question behind the rest of this repository: whether the models translate through English.

Finally, I compare automatic metrics (such as chrF, COMET and MetricX) and a language model used as
a judge with my own annotation, to see whether they can be trusted for Ancient Greek into Persian.

## Where it stands

The machine translations are done, apart from some of the runs at higher temperatures. I have cut
all the human translations at the treebank sentences and drawn the sample of passages. Next I will
fix the hypotheses, write a glossary of the key terms and a list of the passages where the Greek is
disputed, and then annotate.

## Limits

This is a case study of one short dialogue, which the models have very likely seen in training, so
the results may not hold for other texts. Only one published Persian translation is direct, so
directness cannot be fully separated from translator, date and source language. I do the annotation
alone and on a sample of passages, so agreement between annotators cannot be measured, and the
error counts will be small. Since the models' training data is unknown, an error they share with an
English translation need not come from it.

The models are mid-sized, the prompt is plain, each sentence has one sample, and the web chats
cannot be reproduced exactly. The translators do not always keep the treebank's sentence
boundaries, the automatic metrics have not been validated for Ancient Greek into Persian, and the
published translations cannot be shared. Firmer conclusions would need more texts, more direct
translations, more annotators and repeated runs.

## References

- Gorman, V. B. (2020). Dependency Treebanks of Ancient Greek Prose. *Journal of Open Humanities
  Data*, 6, 1. https://doi.org/10.5334/johd.13
- Freitag, M., Foster, G., Grangier, D., Ratnakar, V., Tan, Q., & Macherey, W. (2021). Experts,
  Errors, and Context: A Large-Scale Study of Human Evaluation for Machine Translation.
  *Transactions of the ACL*, 9, 1460–1474.
- Lommel, A., Uszkoreit, H., & Burchardt, A. (2014). Multidimensional Quality Metrics (MQM): A
  Framework for Declaring and Describing Translation Quality Metrics. *Tradumàtica*, 12, 455–463.
- The Persian translations are listed with full references in Shamsian et al. (2025).
