# Dragoman

A dragoman was the interpreter who stood between languages. The word itself travelled from
Arabic and Persian _tarjumān_ (ترجمان) into Europe. Language models seem to be the dragomans of our times, standing between some of these languages too!
Here I share some of my experiments on how they translate Ancient Greek into Persian, and especially whether they go straight from
Greek to Persian or take a detour through English.
The whole repo follows a general enquiry into this point rather than specific research questions. The specifics are declared in each experiment.

## Word-list experiment

The first experiment gives eight open-weight models (GPT-OSS, Qwen, ALLaM, Llama, Mistral and
Gemma) 200 Ancient Greek words, one at a time, and asks for Persian. Some of the words are
traps: their usual English translation has a second meaning that the Greek word never has.
φώκη is a seal, the animal, but English _seal_ is also a stamp. A model that answers مهر
("stamp") has probably gone through the English word.

The traps rarely fire (under 1% of answers in every model), although the same models fall
into them 29–80% of the time when they are made to go through their own English word. Still,
English does leak in. Some
Greek words get read as English words they sound like (πίσσα "pitch" becomes ادرار, via
_piss_), some answers are English words written in Persian letters (فاکس, _fox_, for φοῖνιξ),
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
every model answer and the results. A small kinship test (paused) sits in the same folder.

## Pro-drop test

Greek and Persian are both pro-drop languages: they can leave out the subject pronoun. English
cannot. If a model relays through English, its Persian should lose the Greek difference between a
bare verb and a stressed pronoun. Three models translated Plato's _Crito_ directly and through
their own English, and were compared with published human translations of the _Crito_.

Going through English does wipe out most of the contrast, for the models and for the human
translators who worked from a modern language. The models' direct Persian keeps it about as well
as direct human translations do, so in this respect it shows no trace of English. Five web chats
(ChatGPT, Gemini, DeepSeek and two Claude chats) do the same. The open models add more pronouns
than human translators, about twice as many as the web chats, for reasons this test can't settle.
Data, results and limits are in [`pro-drop-test`](pro-drop-test/).

## Historical-present test

_Ongoing: most of the work is still to be done._

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

## Plato's dialogues

_Ongoing: the machine translations are done; the error annotation is under way._

Two dialogues, the _Crito_ and the _Euthyphro_ (2a–4b), translated into Persian by six open-weight
models and five web chats, in chunks of about 250 Greek words. Four of the five printed Persian
translations of the _Crito_ were made through English, French or German, and only one directly from
the Greek, so the models' Persian can be compared with both kinds. I annotate the errors by hand
(MQM). In the first units, the direct human translations make the fewest errors, then the web chats,
then the indirect human translations, then the open models, in the same order in both dialogues.
In [`plato-dialogues`](plato-dialogues/).

## Note

The code and README files in this repository were produced with the assistance of Claude
Opus 5.5 (Anthropic).
