# 1. 분할정복

분할정복은 문제 풀이의 정석적인 방법중 하나다. 이름에서 알 수 있듯, 분할정복의 논지는 다음과 같다.

> 큰 문제를 풀 수 있는 작은 문제 여럿으로 분리해 각개격파한다.

```ts
function bigProblem(input) {
  smallProblem();
  smallProblem();
  // ...
  return solution;
}
```

## 분할정복을 사용할 수 없는 경우

## 분할정복 설계 방법

문제를 분할정복으로 풀고자 한다면 다음과 같은 순서로 설계할 수 있다.

1. 문제의 입력을 하나 이상의 작은 입력으로 분할한다.
2. 작은 입력을 각각 푼다.
3. 필요에 따라 분할하여 푼 내용을 합쳐 답을 만들어낸다.

## 분할정복을 이용하는 대표적인 알고리즘

1. 이분 탐색(binary search)
2. 병합정렬(merge sort)
3. 퀵정렬(quick sort)
4. 쉬트라쎈 행렬곱셈
