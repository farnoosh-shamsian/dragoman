# Crito translation

Part of [Dragoman](../README.md).

*Ongoing: the machine translations are done; the evaluation is being planned.*

How do language models translate a whole dialogue of Plato into Persian, compared with the people
who have translated it? The *Crito* has been translated into Persian several times: mostly
**indirectly**, through English, French or German, and only recently **directly** from the Greek.
This makes it a good test case. The aim is to compare the machine translations with both kinds of
human translation, and to see whether the models' Persian reads more like a direct translation or
like an indirect one.

## What is here

- `crito_translations.csv`: one row per Greek sentence (276 in all): the treebank id, the
  Stephanus section, the Greek, and one column per model, mode and temperature. An empty cell means
  that run has not been done or gave no usable answer for that sentence.
- `crito_translations.xlsx`: the same table as a spreadsheet.

**The Greek text** is Burnet's, from Perseus (`tlg0059.tlg003.perseus-grc2`), cut into sentences as
in the Gorman treebank (Gorman 2020), so that every sentence has a treebank id and a Stephanus
reference.

**The models** are the six open-weight models of the [pro-drop test](../pro-drop-test/): Gemma 4 26B,
Mistral Small 3.1 24B, Llama 3.3 70B, GPT-OSS 120B, GPT-OSS 20B and Qwen 3.8 27B. They got a plain
prompt (*Translate this Ancient Greek text into Persian*) and no other help: no system prompt, no
dictionary, no treebank. Each model translated the dialogue in two ways:

- **sentence by sentence**, one sentence per request, with no context;
- **in chunks** of about 250 Greek words, cut at sentence ends, with each sentence numbered so the
  answer can be split back into sentences.

Both ways were run at temperature 0 and 1, and some models also at 1.5 and 2 (not all of these are
complete). ChatGPT, Gemini and DeepSeek translated the whole dialogue in chunks through their web
chats, and the first 20 sentences one by one, as did Claude Opus 5.5.

## The human translations

The human translations come from an earlier project, a word-aligned parallel corpus of the
*Crito* in Persian (Shamsian et al. 2025):

| Translation | Kind |
|---|---|
| Foroughi (1938) | published, indirect |
| Lotfi (1979) | published, indirect |
| Jahanshahi (1989) | published, indirect |
| Golestan (2013) | published, indirect |
| Shafi'-Beyk (2023) | published, direct (the first direct Persian translation) |
| Three finalized course translations, five learner translations | unpublished, direct |

The course translations, aligned sentence by sentence and word by word with the Greek, are on
Zenodo, together with the English (Jowett, Fowler) and German (Schleiermacher) translations aligned
to the same sentences:

- Dataset: Shamsian, F., Assimi, S., Mahmoudzadeh Sarabi, A., Mohammadi, N., Nikpour, K., &
  Rahimi, F. (2023–2024). *Word-aligned Parallel Corpus of Plato's Crito in Persian* [Data set].
  Zenodo. https://doi.org/10.5281/zenodo.17607620 (CC BY 4.0)
- Paper: Shamsian, F., Rahimi, F., Mahmoudzadeh Sarabi, A., Mohammadi, N., Nikpoor, K., & Assimi, S.
  (2025). Word-aligned Parallel Corpus of Plato's *Crito* in Persian: A Pedagogical Approach to
  Digital Annotations. *Journal of Open Humanities Data*, 11(1), 78.
  https://doi.org/10.5334/johd.398

The published translations are under copyright, so they will not be shared here in full; only
short passages, annotations and scores will be.

## The plan

The question is how the machine translations compare with the direct and the indirect human
translations, judged against the Greek. Several methods will be used, so that each can check the
others:

- **MQM error annotation.** A sample of passages, chosen across the dialogue (the opening, Crito's
  appeal, the argument, the speech of the Laws), is annotated by hand for every translation: each
  error is marked with its kind (accuracy, terminology, fluency, style, non-translation) and how
  serious it is. All translations are judged on the same passages, under random codes, so the
  annotation is as blind as possible.
- **Key terms.** How each translation renders the dialogue's key words (justice and wrongdoing,
  persuading and obeying, the laws, agreement) and whether it keeps them consistent, since the
  argument depends on them.
- **Inherited errors.** Errors in the indirect translations are checked against the English, French
  or German text they came from. The same check is run on the machine translations against the
  English translations the models will have read, which links this project to the question of the
  rest of the repo.
- **Automatic metrics** (such as chrF, COMET and MetricX), and a language model used as a judge,
  compared with the hand annotation to see whether they can be trusted for Ancient Greek.
- **Context.** The sentence-by-sentence and chunk translations of the same model are compared, to
  see what the lack of context costs.

## Next steps

1. Fix the hypotheses and the sample of passages.
2. Prepare a glossary of the key terms and a list of the passages where the Greek is disputed.
3. Align the human translations with the treebank sentences for the sampled passages.
4. Annotate, then run the checks and the metrics.

## Limits

This is one dialogue, annotated by one person, so the results are a case study of the *Crito*,
not a verdict on Ancient Greek or on language models in general.

## References

- Gorman, V. B. (2020). Dependency Treebanks of Ancient Greek Prose. *Journal of Open Humanities
  Data*, 6, 1. https://doi.org/10.5334/johd.13
- Freitag, M., Foster, G., Grangier, D., Ratnakar, V., Tan, Q., & Macherey, W. (2021). Experts,
  Errors, and Context: A Large-Scale Study of Human Evaluation for Machine Translation.
  *Transactions of the ACL*, 9, 1460–1474.
- Lommel, A., Uszkoreit, H., & Burchardt, A. (2014). Multidimensional Quality Metrics (MQM): A
  Framework for Declaring and Describing Translation Quality Metrics. *Tradumàtica*, 12, 455–463.
- The Persian translations are listed with full references in Shamsian et al. (2025).
