# CONVENTION

이 레포는 **문서(블로그 포스트) 프로젝트**다. 코드가 거의 없으므로 `feat:` / `fix:` 같은 일반적인 Conventional Commits 어휘는 이 레포의 변경 성격을 잘 설명하지 못한다. 대신 문서 작업의 라이프사이클에 맞춘 자체 prefix를 사용한다.

## 커밋 메시지 Prefix

| Prefix            | 언제                                                                                                              | 예시                                |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `draft: <slug>`   | 새 포스트의 빈 초안 폴더를 부트스트랩하는 첫 커밋. `raw/<slug>/` 가 처음 생성될 때. 본문은 이 커밋에 담지 않는다. | `draft: python-concurrency-notes`   |
| `publish: <slug>` | 포스트를 publish하는 커밋. wiki를 갱신해야한다.                                                                   | `publish: python-concurrency-notes` |
| `wiki:`           | wiki 디렉토리의 변경. ingest, query 결과 저장, lint 수정, 스키마 변경 등 wiki 관련 모든 커밋.                     | `wiki: 전체 ingest (16개 포스트)`   |

## 관련 자동화

- `scripts/new-post.sh` : `raw/<slug>/` 부트스트랩.
- `.agents/skills/raw-bootstrap/` : 위 스크립트 실행 + `draft: <slug>` 커밋까지 자동화하는 LLM 스킬.
- `.agents/skills/wiki-ingest/` : 포스트를 wiki에 통합하는 LLM 스킬. `wiki:` prefix 사용.
- `.agents/skills/wiki-query/` : wiki를 검색하고 질문에 답변하는 LLM 스킬.
- `.agents/skills/wiki-lint/` : wiki 건강 상태를 점검하는 LLM 스킬.
