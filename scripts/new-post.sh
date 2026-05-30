#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root from script location so this works no matter where it's invoked from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RAW_DIR="$REPO_ROOT/raw"

usage() {
  cat <<EOF
Usage: $(basename "$0") [title] [slug]

Creates raw/<slug>/index.mdx and raw/<slug>/images/.
If title or slug is omitted, you'll be prompted.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

title="${1:-}"
slug="${2:-}"

if [[ -z "$title" ]]; then
  read -r -p "title: " title
fi
if [[ -z "$slug" ]]; then
  read -r -p "slug: " slug
fi

title="${title#"${title%%[![:space:]]*}"}"
title="${title%"${title##*[![:space:]]}"}"
slug="${slug#"${slug%%[![:space:]]*}"}"
slug="${slug%"${slug##*[![:space:]]}"}"

if [[ -z "$title" ]]; then
  echo "error: title is required" >&2
  exit 1
fi
if [[ -z "$slug" ]]; then
  echo "error: slug is required" >&2
  exit 1
fi

if [[ ! "$slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "error: slug must be lowercase kebab-case (e.g. 'my-new-post'): '$slug'" >&2
  exit 1
fi

target_dir="$RAW_DIR/$slug"
if [[ -e "$target_dir" ]]; then
  echo "error: folder already exists: raw/$slug" >&2
  exit 1
fi

if existing_match="$(grep -rl --include='index.mdx' --include='index.md' -E "^slug:[[:space:]]*${slug}[[:space:]]*$" "$RAW_DIR" 2>/dev/null)"; then
  if [[ -n "$existing_match" ]]; then
    echo "error: slug '$slug' is already used in:" >&2
    echo "$existing_match" >&2
    exit 1
  fi
fi

now="$(date "+%Y-%m-%dT%H:%M:%S")"

mkdir -p "$target_dir/images"

cat > "$target_dir/index.mdx" <<EOF
---
title: $title
published: $now
modified: $now
slug: $slug
image:
draft: true
tags:
summary:
---

## 제목
EOF

echo "created: raw/$slug/index.mdx"
