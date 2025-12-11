#!/usr/bin/env bash
# Run the reduction driver on all test cases in this directory and regenerate results.csv/plots.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"

# Activate local venv if it exists so matplotlib is available
if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

echo "Running driver on all test cases..."
python3 driver.py

echo "Generating plots..."
python3 plot_results.py

echo "Done. Outputs:"
echo "  ${PROJECT_ROOT}/results.csv"
echo "  ${PROJECT_ROOT}/pictures/runtime_vs_size.png"
echo "  ${PROJECT_ROOT}/pictures/approx_vs_bound.png"

