#!/bin/bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
output_dir="$script_dir/../output-writeup"
root_file="writeup"

mkdir -p "$output_dir"

cd "$script_dir"
pdflatex -halt-on-error -output-directory="$output_dir" "$root_file"

cd "$output_dir"
bibtex "$root_file"

cd "$script_dir"
pdflatex -halt-on-error -output-directory="$output_dir" "$root_file"
pdflatex -halt-on-error -output-directory="$output_dir" "$root_file"
