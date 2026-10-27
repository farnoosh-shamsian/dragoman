# Dragoman

A dragoman was the interpreter who stood between languages. The word itself travelled from
Arabic and Persian *tarjumān* (ترجمان) into Europe. Language models seem to be the dragomans of our times, standing between some of these languages too!
Here I share some of my experiments on how they translate Ancient Greek into Persian, and especially whether they go straight from
Greek to Persian or take a detour through English.
The whole repo follows a general enquiry into this point rather than specific research questions. The specifics are declared in each experiment.


## Word-list experiment

The first experiment gives eight open-weight models (GPT-OSS, Qwen, ALLaM, Llama, Mistral and
Gemma) 200 Ancient Greek words, one at a time, and asks for Persian. Some of the words are
traps: their usual English translation has a second meaning that the Greek word never has.
φώκη is a seal, the animal, but English *seal* is also a stamp. A model that answers مهر
("stamp") has probably gone through the English word.

The traps rarely fire (under 1% of answers in every model), although the same models fall
into them 29–80% of the time when they are made to go through their own English word. Still,
English does leak in. Some
Greek words get read as English words they sound like (πίσσα "pitch" becomes ادرار, via
*piss*), some answers are English words written in Persian letters (فاکس, *fox*, for φοῖνιξ),
some start in Persian and finish in English (کilling for ἀποκτείνω), and now and then, mostly
with more randomness in the sampling, an English-only meaning slips through.

Each model leaks in its own way: the sound-alikes come from GPT-OSS and Qwen, the half-English
words from Llama, and Gemma, which knows the most words, shows almost no trace of English.

What a word list can test is a **surface relay**: Greek word → English word → Persian word,
with the English word's ambiguity carried over. Subtler relays are possible. A model could go
through English, or through English-shaped meanings, and still pick the right sense; that would
leave no trace in a word list. Those relays need other methods, which the next experiments will
try. Still, even at the surface, English is not absent. The traces are few, but the fact that
there are any at all is important.

Everything is in [`word-list-experiment`](word-list-experiment/): the design, the prompts,
every model answer, the code and the results.

## Pro-drop test

*Ongoing: most of the work is still to be done.*

Greek and Persian are both pro-drop languages: they can leave out the subject pronoun. English
cannot. If a model relays through English, its Persian may spell out pronouns that the Greek
leaves out, so this test traces what happens to subjects in the syntax. In
[`pro-drop-test`](pro-drop-test/).

## Historical-present test

*Ongoing: most of the work is still to be done.*

Greek, Persian and English use the historical present (the present tense for past events)
differently. If a model relays through English, the Persian may carry traces of how English
handles the tense, and so of how the Greek meaning passed through English. In
[`historical-present-test`](historical-present-test/).

## Limits

These experiments are small for now, and they will be expanded. The traces of English they
find could have other causes than a relay through English. The prompts are written in English,
so English is already in the context before the Greek arrives. And most of what the models have
read about Ancient Greek probably came with English: dictionaries, translations and textbooks.
A Greek word may then sit close to its English equivalent because of the training data, not
because the model goes through English while it translates. The experiments so far can't tell
these explanations apart.

The main aim of the repo stays the same: to see how well these models translate Ancient Greek
into Persian, and whether their Persian shows the kind of problems that indirect translation,
through a third language, leaves behind. Whatever their cause, such traces matter to a reader of
the Persian. The next step is to move from single words and sentences to much larger texts.

## Whole dialogues

*Ongoing: the machine translations are done; the evaluation is being planned.*

The larger aim is to have models translate a whole dialogue of Plato into Persian and to compare
their translations at length. The first is the *Crito*. Six open-weight models and three web chats
have translated the whole dialogue, sentence by sentence and in longer chunks. The *Crito* has
also been translated into Persian by people, both indirectly (through English, French or German)
and directly from the Greek, and these translations are collected in an earlier corpus
([Shamsian et al. 2025](https://doi.org/10.5334/johd.398); data on
[Zenodo](https://doi.org/10.5281/zenodo.17607620)). The goal is to compare the machine
translations with the direct and the indirect human ones, with several methods: hand annotation
of errors (MQM), key-term consistency, errors inherited from an intermediate translation,
automatic metrics and a language model as judge. In [`crito-translation`](crito-translation/).

## Note

The code and README files in this repository were generated with the assistance of Claude
Opus 5.5 (Anthropic).
