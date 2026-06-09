---
name: raw-bootstrap
description: >-
  새 블로그 포스트를 쓰기 시작할 때 raw/ 아래에 빈 draft 폴더와
  index.mdx frontmatter만 생성하는 스킬. 유저로부터 어떤 글을 쓸지 러프한
  설명(주제, 참고 URL, 책, 컨퍼런스 등)을 받아 적절한 영어 kebab-case slug와
  한국어 title을 짓고, scripts/new-post.sh를 실행해 raw/<slug>/ 폴더를 만든 뒤
  draft 커밋을 만든다. "새 포스트 폴더 만들어줘", "draft 폴더 만들어줘",
  "새 글 시작할게", "초안 폴더 만들어줘", "raw bootstrap"처럼 raw/<slug>/
  생성이 명확한 요청에 사용한다. 본문 작성, 포스트 요약, wiki 반영 요청에는
  사용하지 않는다.
---

# raw-bootstrap

새 블로그 포스트의 빈 초안 폴더를 만들고 커밋한다. 실제 글의 본문을 작성하는 스킬이 아니다 — 오직 폴더/파일 부트스트랩과 첫 커밋까지만 책임진다.

## 전체 흐름

1. 유저의 러프한 설명을 듣고 무엇에 관한 글인지 이해한다.
2. slug와 title 후보를 만들고 유저에게 확인받는다.
3. `scripts/new-post.sh "<title>" "<slug>"` 실행.
4. `raw/<slug>/` 를 git add 하고 `draft: <slug>` 메시지로 커밋한다.

## 1. 유저 입력 이해

유저는 보통 다음 중 하나를 던진다:

- 참고 자료 URL ("https://wikidocs.net/book/19868 읽고 정리할거야")
- 책/컨퍼런스/사람 이름 ("켄트 백 책 정리해서 쓸거야")
- 주제 한 줄 ("리액트 19 use 훅 정리하는 글")
- 회고/시리즈 ("2026 상반기 회고 쓸거야")

유저가 URL을 줬는데 어떤 내용인지 불명확하다면, **추측하지 말고 한 줄로 물어본다.** 예: "이 책이 어떤 책이에요? slug에 반영할 핵심 키워드 한두 단어만 알려주세요." 무리하게 WebFetch까지 동원할 필요는 없다 — 부트스트랩에는 사람의 한 줄 답이 더 정확하고 빠르다.

## 2. slug와 title 짓기

### slug 규칙 (scripts/new-post.sh가 강제하는 규칙)

- 정규식: `^[a-z0-9]+(-[a-z0-9]+)*$`
- 영어 소문자 kebab-case만 허용. 한글/공백/대문자/언더스코어 전부 거부됨.
- 짧고 의미 있게. 3~5 단어가 적당.
- `raw/` 아래 이미 존재하는 폴더명/slug와 충돌하면 스크립트가 에러를 뱉으므로, 후보를 정한 뒤 한 번 확인한다:
  ```bash
  ls raw/ | grep -i <후보>
  grep -r "^slug:" raw/ | grep <후보>
  ```

### slug 짓는 감각

- 주제의 **핵심 개념**을 영어로 옮긴다. 출처(저자, 사이트)는 식별에 꼭 필요할 때만.
- 시리즈는 `-1`, `-2` 접미사. (기존 패턴: `react-query-1`, `2024-developer-retrospect`)
- 회고는 연도 접두사. (`2025-retrospect`, `2025-developer-first-half-retrospect`)

**예시**

| 유저 입력 | 좋은 slug | 나쁜 slug |
|---|---|---|
| "https://wikidocs.net/book/19868 (파이썬 동시성 책) 정리" | `python-concurrency-notes` | `wikidocs-19868`, `python-book` (모호) |
| "켄트 백 augmented coding 정리" | `augmented-coding-by-kent-beck` | `kent-beck`, `augmented` (너무 짧음/넓음) |
| "리액트 19 use 훅" | `react-19-use-hook` | `use-hook` (충돌 위험), `react19usehook` (kebab 아님) |
| "2026 상반기 회고" | `2026-developer-first-half-retrospect` | `retrospect-2026` (기존 컨벤션과 어긋남) |

### title 짓는 감각

- 한국어 OK. 자연스러운 글 제목처럼.
- frontmatter에 그대로 들어가므로 따옴표/콜론 같은 YAML 특수문자는 피하거나 이스케이프.
- title은 나중에 글 쓰면서 얼마든지 다듬을 수 있으니 너무 고민하지 말고 합리적인 첫 안을 제시한다.

### 유저 확인

후보를 만들면 한 번에 보여주고 OK인지 묻는다. 예:

> 다음으로 부트스트랩할게요:
> - title: 파이썬 동시성 정리 노트
> - slug: `python-concurrency-notes`
>
> 이대로 진행할까요?

유저가 수정을 요청하면 반영하고 다시 확인. 유저가 "그냥 해" 류로 답하면 그대로 진행.

## 3. 스크립트 실행

프로젝트 루트에서:

```bash
./scripts/new-post.sh "<title>" "<slug>"
```

성공 시 `created: raw/<slug>/index.mdx` 가 출력된다.

실패 케이스:
- `error: folder already exists` → slug 충돌. 다른 slug 제안하고 유저 확인 받아 재시도.
- `error: slug must be lowercase kebab-case` → slug 다시 짓기. 보통 대문자/한글/공백이 섞인 경우.
- `error: slug '...' is already used in:` → 다른 포스트 frontmatter에 동일 slug. 다른 slug로.

## 4. 커밋

생성된 폴더만 add 하고 정확히 `draft: <slug>` 메시지로 커밋한다. 다른 파일은 건드리지 않는다.

```bash
git add raw/<slug>
git commit -m "draft: <slug>"
```

커밋 메시지 형식은 **정확히** `draft: <slug>` — 다른 prefix(`feat:`, `chore:` 등) 붙이지 말 것. 이 레포에서 draft 포스트의 첫 커밋을 식별하는 컨벤션이다.

커밋 후 한 줄로 결과 보고:
> `raw/<slug>/` 생성 및 커밋 완료. 이제 `raw/<slug>/index.mdx` 에 글 쓰면 됩니다.

## 하지 말 것

- 본문(`## 제목` 아래) 채우지 말 것. 이 스킬은 부트스트랩까지만.
- frontmatter의 `tags`, `summary`, `image` 미리 채우지 말 것. 글 쓰면서 채울 영역.
- `raw/` 아래 다른 포스트는 건드리지 말 것.
- 커밋 메시지에 Co-Authored-By 같은 trailer 붙이지 말 것. 이 레포 컨벤션은 단순 한 줄.
- `git push` 하지 말 것. 푸시는 유저가 직접.
