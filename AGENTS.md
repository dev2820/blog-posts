# AGENTS.md

This file provides guidance to LLM agents (Claude Code, Codex, etc.) when working with this repository.

## Repository Purpose

This is a **content-only CMS repository** for blog posts. It contains no build system, framework, or application code. The blog application lives in a separate repository and consumes this repo as a **git submodule** (mounted as `articles/`).

## Structure

```
raw/
  {post-slug}/
    index.mdx          # Post content (MDX format)
    images/             # Post-specific images (optional)
```

## Post Frontmatter Schema

Every post has this frontmatter in `index.mdx`:

```yaml
---
title: string           # Post title (Korean)
published: datetime     # ISO 8601 (e.g., 2025-07-20T10:48:00)
modified: datetime      # ISO 8601
slug: string            # URL slug (must be unique across all posts)
image: string           # Hero image path (e.g., ./images/hero.jpg) or empty
draft: boolean          # true = unpublished, false = published
tags: string[]          # Tag list
summary: string         # Short description (optional)
prev: string            # Previous post slug for series navigation (optional)
next: string            # Next post slug for series navigation (optional)
---
```

## Conventions

- Posts are written in **Korean**
- Folder names use **English kebab-case** and typically match the slug
- Series posts use `-N` suffix (e.g., `react-query-1`, `react-query-2`)
- Images are co-located in an `images/` subdirectory within each post folder

## Workflows

### Creating a new post

1. Create folder under `raw/` with kebab-case name
2. Create `index.mdx` with all required frontmatter fields
3. Set `draft: true` by default
4. Verify slug uniqueness: `grep -r "^slug:" raw/` before committing

### Publishing a post

1. Set `draft: false`
2. Ensure `title`, `slug`, `published`, `summary` are all filled
3. Update `modified` to current datetime

### Managing a series

1. Use `-N` suffix for folder names (e.g., `react-query-1`, `react-query-2`)
2. Set `prev`/`next` in frontmatter to link adjacent posts by slug
3. When inserting a post mid-series, update `prev`/`next` of neighboring posts

## Validation Rules

- **slug must be unique** across all posts — always check before creating
- **published/modified** must be ISO 8601 format (`YYYY-MM-DDTHH:MM:SS`)
- **images** must be stored in `./images/` within the same post folder, not shared across posts
- **frontmatter fields** must follow the schema above — do not add custom fields

## Critical Rule

- `raw/` folder is the **single source of truth** for all blog content. **Always ask for human approval before modifying any file under `raw/`.**

## Do NOT

- Modify other posts unless explicitly asked
- Add frontmatter fields not defined in the schema
- Reference images from other post folders
- Remove or rename existing post folders without explicit instruction
