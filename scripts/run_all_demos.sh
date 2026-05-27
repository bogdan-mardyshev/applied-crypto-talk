#!/usr/bin/env bash
# Запустить smoke-тесты всех демок и вывести pass/fail с временем выполнения.

set -e

DEMOS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/demos"
PASS=0
FAIL=0
ERRORS=()

echo "=========================================="
echo "  Smoke Tests — All Demos"
echo "=========================================="
echo ""

for demo_dir in "$DEMOS_DIR"/0*; do
    demo_name="$(basename "$demo_dir")"
    smoke_test="$demo_dir/smoke_test.py"

    if [[ ! -f "$smoke_test" ]]; then
        echo "  [SKIP] $demo_name — нет smoke_test.py"
        continue
    fi

    start_ts=$(date +%s%N)
    if pytest "$smoke_test" -v --tb=short -q 2>&1; then
        end_ts=$(date +%s%N)
        elapsed=$(( (end_ts - start_ts) / 1000000 ))
        echo "  [PASS] $demo_name  (${elapsed} ms)"
        (( PASS++ )) || true
    else
        end_ts=$(date +%s%N)
        elapsed=$(( (end_ts - start_ts) / 1000000 ))
        echo "  [FAIL] $demo_name  (${elapsed} ms)"
        (( FAIL++ )) || true
        ERRORS+=("$demo_name")
    fi
done

echo ""
echo "=========================================="
echo "  Results: $PASS passed, $FAIL failed"
echo "=========================================="

if [[ ${#ERRORS[@]} -gt 0 ]]; then
    echo ""
    echo "  Failed demos:"
    for err in "${ERRORS[@]}"; do
        echo "    - $err"
    done
    exit 1
fi

echo ""
echo "  All smoke tests passed!"
