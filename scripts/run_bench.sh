#!/usr/bin/env bash
# 跑一遍 RTF 基准。用法: scripts/run_bench.sh [repeat]
set -euo pipefail
REPEAT="${1:-10}"
python benchmarks/bench_rtf.py --repeat "$REPEAT"
