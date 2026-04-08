#!/usr/bin/env zsh
set -euo pipefail

BACKUP_DIR=".rename_backup_$(date +%Y%m%d_%H%M%S)"
MANIFEST="rename_manifest_$(date +%Y%m%d_%H%M%S).csv"

mkdir -p "$BACKUP_DIR"
echo "old_name,new_name,backup_path" > "$MANIFEST"

typeset -A MAP
MAP=(
  "00_Index_and_Router.md"               "00_Index_Router_v5.md"
  "01_Core_Shell.md"                     "01_Core_Shell_v5.md"
  "02_Core_Advanced.md"                  "02_Core_Advanced_v5.md"
  "03_Tool_Command_Builder_Templates.md" "03_Tool_Command_Builder_Templates_v5.md"
  "04_Tool_QuickRef.md"                  "04_Tool_Quick_Ref_v5.md"
  "05_Store_Database.md"                 "05_Store_Database_v5.md"
  "06_AI_Terminal.md"                    "06_Tool_AI_Terminal_v5.md"
  "07_MCP.md"                            "07_Meta_MCP_v5.md"
)

for old new in ${(kv)MAP}; do
  if [[ ! -e "$old" ]]; then
    echo "SKIP: $old not found"
    continue
  fi
  if [[ -e "$new" ]]; then
    echo "ERROR: target $new already exists; aborting to avoid overwrite."
    exit 1
  fi
  cp "$old" "$BACKUP_DIR/$old"
  mv "$old" "$new"
  echo "$old,$new,$BACKUP_DIR/$old" >> "$MANIFEST"
  echo "RENAMED: $old -> $new"
done

echo "Backup dir: $BACKUP_DIR"
echo "Manifest: $MANIFEST"
