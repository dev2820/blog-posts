---
name: raw-publish
description: 블로그 포스트를 발행 상태로 전환하는 스킬. 지정한 포스트의 frontmatter에서 draft를 false로 바꾸고, 필수 필드를 검증한 뒤 `publish: <slug>` 커밋을 만든다. 커밋이 끝나면 바로 wiki-ingest 스킬을 실행해 wiki를 최신 상태로 유지한다.
---

# raw-publish

지정한 블로그 포스트를 공개(publish) 상태로 전환하고 wiki를 동기화한다.

## 사전 체크

1. 사용자에게 발행할 포스트의 **slug** 혹은 `raw/<slug>/` 경로를 확인받는다.
2. `raw/<slug>/index.mdx`의 frontmatter를 읽는다.
3. 아래 항목이 모두 채워져 있는지 확인한다. 비어 있으면 사용자에게 값을 요청하거나 발행을 중단한다.
   - `title`
   - `slug`
   - `published` (ISO 8601, 예: `2026-06-17T12:34:56`)
   - `summary`
4. `draft`가 이미 `false`면 사용자와 상의하여 재발행 여부를 확인한다.

## 발행 처리

1. `edit_frontmatter`를 사용하여 다음을 수행한다.
   - `draft: false`
   - `modified`를 현재 시각으로 갱신 (`autoUpdateModified: true` 활용)
   - 필요하면 `summary`, `published` 등을 함께 수정하되 사용자 확인을 받는다.
2. 변경 사항을 다시 읽어 원하는 값이 들어갔는지 검증한다.

## 커밋

1. `git status --short raw/<slug>`로 변경 파일을 확인한다.
2. `git add raw/<slug>`
3. 커밋 메시지 **정확히** `publish: <slug>`로 커밋한다.
4. 다른 파일이 stage 되지 않았는지 확인한다. 필요하면 `git restore --staged`로 정리한다.

## 위키 동기화

1. 커밋이 완료되면 곧바로 `wiki-ingest` 스킬을 실행한다.
   - 대상 포스트는 방금 발행한 `<slug>` 하나로 지정한다.
   - wiki-ingest 절차에 따라 source/topic/index/log를 갱신한다.
2. wiki-ingest 결과를 요약해 사용자에게 보고한다.

## 마무리 보고

1. 발행된 포스트의 주요 정보(title, slug, published)를 간략히 공유한다.
2. 커밋 해시와 wiki-ingest 실행 여부를 함께 보고한다.

## 주의사항

- `raw/` 외 다른 디렉터리는 수정하지 않는다.
- 발행 처리 중 내용 수정을 요청받지 않은 경우 본문을 건드리지 않는다.
- ISO 형식이 아닌 날짜를 발견하면 사용자에게 수정 요청을 먼저 한다.
- wiki-ingest가 실패하면 에러 메시지와 함께 사용자에게 즉시 알리고 지시를 기다린다.
