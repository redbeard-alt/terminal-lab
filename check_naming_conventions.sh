#!/usr/bin/env zsh
set -euo pipefail

echo "Checking Terminal Lab filenames against NN_Category_Short_Name_vN.md..."

bad=0
for f in *.md; do
  if [[ "$f" == "Space_Instructions_Compact.md" || "$f" == "README.md" ]]; then
    continue
  fi
  if ! [[ "$f" =~ '^[0-9]{2}_(Index|Core|Tool|Store|Troubleshooting|Meta)_[A-Za-z0-9_]+_v[0-9]+\.md$' ]]; then
    echo "NON-COMPLIANT: $f"
    bad=1
  fi
done

if (( bad == 0 )); then
  echo "All governed files comply."
else
  echo "Found non-compliant filenames."
  exit 1
fi
