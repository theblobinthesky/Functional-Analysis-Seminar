#!/bin/bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$script_dir"

output_dir="../output-presentation"
slides="slides"

mkdir -p "$output_dir"
pdflatex -halt-on-error -output-directory="$output_dir" "$slides"
pdflatex -halt-on-error -output-directory="$output_dir" "$slides"
