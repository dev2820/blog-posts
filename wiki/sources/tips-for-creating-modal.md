---
type: source
origin: "tips-for-creating-modal"
kind: "가이드"
---

## 요약

모달(다이얼로그) 구현 시 유의할 점을 정리한 실용 가이드. ESC로 닫기, 포커스 관리(중요 버튼 우선, row-reverse 트릭), aria-modal/aria-labelledby 설정, dialog vs alertdialog의 차이, 파트별 패딩(스크롤바 위치 문제 해결) 등을 다룬다.

## 핵심 생각

접근성과 UX를 함께 고려하는 실용적 관점. 단순히 "이렇게 하라"가 아니라 "왜 이렇게 해야 하는지"를 설명한다. shadcn의 dialog/alert dialog 분리 이유, Chakra v3의 파트별 패딩 이유 등 오픈소스에서 배운 것을 정리.

## 접점

- [프론트엔드 딥다이브](../topics/frontend-deep-dive.md) — 접근성과 UX 세부 지식
- [2024-developer-retrospect-2](./2024-developer-retrospect-2.md) — Form 작업에서 접근성을 공부한 것과 연결
- [소프트웨어 장인정신](../topics/software-craftsmanship.md) — 접근성에 대한 꼼꼼한 태도

## 성장 기록

접근성(a11y)에 대한 지식이 축적되어 가이드를 쓸 수 있는 수준에 도달. "마우스 없이 페이지를 이용할 수 있는지 체크하는 습관"(회고에서 언급)의 결과물.
