---
type: source
origin: "how-does-v8-array-sort-work"
kind: "탐구"
---

## 요약

V8 엔진의 Array.sort 구현을 깊이 파헤친 기술 포스트. 과거의 QuickSort에서 현재의 TimSort로 전환된 배경과 TimSort의 동작 원리(run 생성, 병합 최적화, galloping 모드)를 상세히 설명한다. V8의 Torque 언어를 이용한 추가 최적화도 간략히 다룬다.

## 핵심 생각

순수한 기술 탐구 포스트로, 저자 본인의 의견은 명시되지 않음. 다만 이 주제를 선택하여 깊이 파고든 것 자체가 알고리즘과 엔진 내부에 대한 관심을 보여준다. run 생성, 피보나치 스택, galloping 모드 등 복잡한 개념을 시각적 예시와 함께 단계별로 설명하는 능력이 돋보인다.

## 접점

- [프론트엔드 딥다이브](../topics/frontend-deep-dive.md) — V8 내부 동작에 대한 깊은 탐구
- [CS 기초](../topics/cs-fundamentals.md) — 정렬 알고리즘에 대한 이론적 이해
