#!/usr/bin/env bash
# Every run, in order.
# Re-running fetches only what is missing.
set -eu
cd "$(dirname "$0")"
R="python run.py"
GPT120=openai/gpt-oss-120b
GPT20=openai/gpt-oss-20b
QWEN=qwen/qwen3.8-27b
NOTHINK=qwen/qwen3.8-27b-nothink
ALLAM=allam-2-7b

# 1. word list, direct
$R greek-words --prompt words-neutral --reps 3 --temperature 0.7

# 2. pivot step 1
$R greek-words --prompt words-pivot-en --reps 1 --temperature 0.2

# 3. pivot step 2 (20B dropped)
python pivot.py
for m in $ALLAM $GPT120 $QWEN; do
  src=greek-words-pivot-$(echo "$m" | tr 'A-Z' 'a-z' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g')
  $R "$src" --prompt words-pivot-fa --model "$m" --reps 1 --temperature 0.2
done

# 4. temperature side test
for t in 00:0.0 07:0.7 10:1.0 15:1.5; do
  $R greek-words-temp${t%%:*} --prompt words-neutral --reps 5 --temperature ${t#*:} --model $GPT120 --model $GPT20 --model $QWEN
done
$R greek-words-temp20 --prompt words-neutral --reps 5 --temperature 2.0 --model $GPT120 --model $QWEN

# 5. kinship, isolated and in lists
for t in 00:1:0.0 07:3:0.7 10:3:1.0; do
  IFS=: read tt reps temp <<< "$t"
  $R kinship-words-temp$tt --prompt words-neutral --reps $reps --temperature $temp --model $GPT120 --model $QWEN --model $NOTHINK
  $R kinship-lists-temp$tt --prompt words-list --reps $reps --temperature $temp --model $GPT120 --model $QWEN --model $NOTHINK
done
# 20B: stopped early
$R kinship-words-temp00 --prompt words-neutral --reps 1 --temperature 0.0 --model $GPT20
$R kinship-lists-temp00 --prompt words-list --reps 1 --temperature 0.0 --model $GPT20
$R kinship-words-temp07 --prompt words-neutral --reps 3 --temperature 0.7 --model $GPT20

# 6. free-tier models, October 2026
NEW=(llama-3.3-70b-instruct-fp8 llama-3.1-8b-instruct-fp8 mistral-small-3.1-24b-instruct gemma-4-26b-a4b-it)
ALL=$(printf -- '--model %s ' "${NEW[@]}")
$R greek-words --prompt words-neutral --reps 3 --temperature 0.7 $ALL
$R greek-words --prompt words-pivot-en --reps 1 --temperature 0.2 $ALL
python pivot.py
for m in "${NEW[@]}"; do
  src=greek-words-pivot-$(echo "$m" | tr 'A-Z' 'a-z' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g')
  $R "$src" --prompt words-pivot-fa --model "$m" --reps 1 --temperature 0.2
done
for t in 00:0.0 07:0.7 10:1.0 15:1.5 20:2.0; do
  $R greek-words-temp${t%%:*} --prompt words-neutral --reps 5 --temperature ${t#*:} $ALL
done
for t in 00:1:0.0 07:3:0.7 10:3:1.0; do
  IFS=: read tt reps temp <<< "$t"
  $R kinship-words-temp$tt --prompt words-neutral --reps $reps --temperature $temp $ALL
  $R kinship-lists-temp$tt --prompt words-list --reps $reps --temperature $temp $ALL
done

# 7. flags
python score.py
