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

The traps rarely fire (under 1% of answers in every model), but English does leak in. Some
Greek words get read as English words they sound like (πίσσα "pitch" becomes ادرار, via
*piss*), some answers are English words written in Persian letters (فاکس, *fox*, for φοῖνιξ),
some start in Persian and finish in English (کilling for ἀποκτείνω), and now and then, mostly
with more randomness in the sampling, an English-only meaning slips through.

Each model leaks in its own way: the sound-alikes come from GPT-OSS and Qwen, the half-English
words from Llama, and Gemma, which knows the most words, shows almost no trace of English.

Everything is in [`word-list-experiment`](word-list-experiment/): the design, the prompts,
every model answer, the code and the results.

## Note

The code and README files in this repository were generated with the assistance of Claude
Opus 5.5 (Anthropic).
