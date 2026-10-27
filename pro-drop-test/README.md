# Pro-drop test

Part of [Dragoman](../README.md).

*Ongoing: first runs under way, no results yet. The details below are the current plan and may
change as the work goes on.*

## The idea

Greek and Persian are both pro-drop languages: a verb can stand without a subject pronoun, and
an overt pronoun (ἐγώ, `من`) often adds emphasis or contrast. English has to state the
pronoun every time, so this contrast has to be carried some other way (*I myself*, *as for me*),
or it is lost.

So English is a possible bottleneck for one piece of syntax that Greek and Persian share. If a
model's Persian loses the contrast in the way a translation through English does, that is a trace
of English in the syntax. The [word-list experiment](../word-list-experiment/) looked for a
surface relay at the level of words. This test looks for traces in sentence structure, even when
the meaning comes out right. It looks at the output only, so a relay that leaves no mark there
stays out of its reach.

## What I look for

Adapting terms from the study of interference in (indirect) translation:

- **added pronouns** where the Greek has a bare verb, more often than Persian needs;
- **lost emphasis**, where an emphatic Greek pronoun disappears, as it usually does in English;
- **calques** of English forms Persian doesn't use, such as a dummy subject for Greek impersonals
  (δεῖ, χρή: *"it* is necessary").

Translations in general tend to spell out more than their source, so pronoun counts alone prove
nothing. What matters is whether the Persian still follows the Greek's contrast.

## Current design

Attic prose with existing treebanks (Plato's *Crito* and *Euthyphro*, Lysias 1), sent to several
open-weight models as continuous text. The direct Greek → Persian translation is compared with two
relays made on purpose: one through English, and one through Spanish, which keeps the contrast as
Greek and Persian do. The Spanish relay is the control. It shows how much any two-step translation
loses, so that a loss can be blamed on English only when it goes beyond that.

The Greek side is annotated from the treebanks, the Persian automatically, with a hand check.

## Pilot

A pilot (October 2026, 90 single sentences, six models) showed that raw pronoun counts don't
separate direct from English-routed Persian, and that sentences without context are too hard to
use. The design above builds on that.
