# CONVENTION

이 레포는 **문서(블로그 포스트) 프로젝트**다. 코드가 거의 없으므로 `feat:` / `fix:` 같은 일반적인 Conventional Commits 어휘는 이 레포의 변경 성격을 잘 설명하지 못한다. 대신 문서 작업의 라이프사이클에 맞춘 자체 prefix를 사용한다.

## 커밋 메시지 Prefix

| Prefix | 언제 | 예시 |
|---|---|---|
| `draft: <slug>` | 새 포스트의 빈 초안 폴더를 부트스트랩하는 첫 커밋. `raw/<slug>/` 가 처음 생성될 때. 본문은 이 커밋에 담지 않는다. | `draft: python-concurrency-notes` |

## 관련 자동화

- `scripts/new-post.sh` : `raw/<slug>/` 부트스트랩.
- `.agents/skills/raw-bootstrap/` : 위 스크립트 실행 + `draft: <slug>` 커밋까지 자동화하는 LLM 스킬.
