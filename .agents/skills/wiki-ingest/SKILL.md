---
name: wiki-ingest
description: 블로그 포스트를 읽고 wiki에 통합하는 스킬. 포스트를 요약하고, 핵심 생각을 추출하고, 다른 포스트와의 접점을 파악하여 source 페이지를 생성하고 관련 topic 페이지를 갱신한다. "이 포스트 ingest해줘", "wiki에 추가해줘", "포스트 정리해줘", "wiki 업데이트", "전체 ingest", 포스트 폴더명을 언급하며 wiki 관련 작업을 요청할 때 트리거된다. 새 포스트를 작성했거나 wiki에 아직 반영되지 않은 포스트가 있을 때 적극적으로 사용한다.
---

# wiki-ingest

블로그 포스트를 읽고 wiki에 통합한다.

## 사전 준비

1. `wiki/WIKI_SCHEMA.md`를 읽어 wiki의 목적, 구조, 페이지 형식을 파악한다.
2. `wiki/index.md`를 읽어 현재 wiki에 어떤 페이지들이 있는지 파악한다. 파일이 없으면 새로 생성한다.
3. `wiki/log.md`를 읽어 최근 작업 이력을 파악한다. 파일이 없으면 새로 생성한다.

## ingest 대상 결정

사용자가 특정 포스트를 지정하면 해당 포스트만 ingest한다.

명시적 지정이 없으면 git diff를 이용하여 변경된 포스트만 자동으로 찾는다:

1. `wiki/log.md`에서 가장 최근 ingest 항목의 commit hash를 읽는다 (`@ ` 뒤의 값).
2. `git diff --name-only <hash> HEAD -- raw/`로 변경된 파일 목록을 구한다.
3. 변경된 파일에서 포스트 폴더명을 추출하여 ingest 대상으로 삼는다.
4. log.md가 없거나 ingest 이력이 없으면 최초 ingest로 간주하여 전체 포스트를 대상으로 한다.

이미 source 페이지가 존재하는 포스트가 변경된 경우, 기존 source를 갱신한다 (접점 정보는 보존).

## 단일 포스트 ingest 절차

### 1. 포스트 읽기

`raw/{folder-name}/index.mdx`를 읽는다. frontmatter에서 title, published, tags, draft, summary, prev, next를 파악하고, 본문 내용을 읽는다.

### 2. 사용자와 논의

포스트를 읽은 후, 다음을 사용자에게 공유하고 피드백을 받는다:

- 이 포스트의 kind 판단 (지식/회고/탐구/에세이/가이드 중 하나, 모호하면 제안)
- 핵심 생각 요약 (2-3문장)
- 떠오르는 topic 후보

사용자가 확인하면 다음 단계로 진행한다.

### 3. source 페이지 생성

`wiki/sources/{folder-name}.md`를 생성한다. WIKI_SCHEMA.md에 정의된 source 페이지 형식을 따른다.

접점 섹션을 채울 때:

- 기존 wiki source 페이지들의 내용을 훑어보고 관련 있는 포스트를 찾는다.
- 관련 topic이 이미 존재하면 링크한다.
- 관련 포스트의 source 페이지에도 역방향 링크를 추가한다 (양방향 링크 유지).

### 4. topic 페이지 갱신

이 포스트와 관련된 topic을 판단한다.

- **기존 topic이 있으면**: 해당 topic 페이지의 "관련 포스트" 섹션에 이 포스트를 추가하고, "변화와 흐름", "인사이트" 섹션을 필요에 따라 갱신한다.
- **새 topic이 필요하면**: 사용자에게 topic 생성을 제안한다. 확인받으면 `wiki/topics/{topic-name}.md`를 생성한다.

topic 이름은 kebab-case 영문으로 짓되, 본문은 한국어로 작성한다.

### 5. index.md 갱신

`wiki/index.md`의 Sources 섹션에 새 source를 추가한다.
새 topic을 만들었다면 Topics 섹션에도 추가한다.
각 섹션의 개수(N개)도 갱신한다.

### 6. log.md에 기록

`wiki/log.md` 끝에 항목을 추가한다:

```markdown
## [YYYY-MM-DD] ingest | {folder-name} @ {commit-hash}

source 생성. topic {topic-name} 갱신/생성. (기타 수정된 페이지 목록)
```

commit-hash는 ingest 시점의 `git rev-parse HEAD` 값(7자리 short hash)을 기록한다. 다음 ingest에서 이 값을 기준으로 git diff를 수행한다.

## 전체 ingest

모든 포스트를 한꺼번에 ingest할 때는 위 절차를 반복하되, 매 포스트마다 사용자 확인을 받으면 비효율적이므로 다음과 같이 진행한다:

1. 전체 포스트 목록을 보여주고 ingest 순서를 확인받는다.
2. 시간순(published 기준)으로 ingest한다. 이렇게 하면 접점과 성장 흐름을 자연스럽게 파악할 수 있다.
3. 각 포스트의 kind와 topic 판단은 LLM이 자율적으로 하되, 전체 완료 후 결과 요약을 사용자에게 보여준다.
4. 사용자가 수정을 원하는 부분이 있으면 반영한다.

## 주의사항

- `raw/`의 어떤 파일도 수정하지 않는다.
- wiki 페이지 작성 시 표준 markdown 상대 경로 링크를 사용한다.
- kind가 모호하면 비워두되, 판단 근거를 사용자에게 설명한다.
- 이미 존재하는 source를 덮어쓸 때는 기존 접점 정보를 보존하면서 갱신한다.
