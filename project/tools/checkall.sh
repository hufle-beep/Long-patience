#!/bin/bash
# Full pre-push check, fast: syntax first, then sanity, the regression tests and every Playwright check (6 at a time)
# all running at once. Prints one summary; exit code 1 if anything failed. About 1.5-2 min (was ~15 min in sequence).
# Usage: bash project/tools/checkall.sh   (P=n to change how many Playwright checks run at once)
R=/home/claude/long-patience; W=/tmp/claude-0/sim; P=${P:-6}
mkdir -p $W && cp $R/project/tools/*.py $R/project/tools/*.js $W/ 2>/dev/null; cp $R/project/tools/fixtures/* $W/
cd $R
node -e "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');[...h.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].forEach(m=>new Function(m[1]))" || { echo "SYNTAX ERROR"; exit 1; }
start=$(date +%s)
(cd $W && timeout 600 python3 sanity.py > $W/c_sanity.txt 2>&1) &
(cd $R && timeout 600 node --test project/tools/tests/*.test.js > $W/c_tests.txt 2>&1) &
(cd $W && ls pw1[5-9][0-9].py | xargs -P $P -I{} sh -c 'timeout 300 python3 {} > c_{}.txt 2>&1') &
wait
fail=0
s=$(grep -E "page errors|text problems|without a handler|pop-up taps" $W/c_sanity.txt)
echo "$s"; echo "$s" | grep -qE "page errors: none" && echo "$s" | grep -qE "text problems: none" || fail=1
for f in $W/c_pw1*.txt; do e=$(grep -o "errors \[.*\]" $f | tail -1); [ "$e" = "errors []" ] || { echo "FAIL $(basename $f .txt | sed 's/^c_//'): $(tail -3 $f | cut -c1-200)"; fail=1; }; done
echo "pw: $(ls $W/c_pw1*.txt | wc -l) checks"
grep -E "^# (pass|fail)|^not ok" $W/c_tests.txt; grep -q "^# fail 0" $W/c_tests.txt || fail=1
echo "time: $(( $(date +%s) - start )) s · $([ $fail = 0 ] && echo ALL OK || echo FAILURES)"
exit $fail
