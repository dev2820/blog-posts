# 자료조사: Web Audio API 공부하기 1 — 가청 범위부터 디지털 표현까지

## 조사 범위

- 조사일·출처 열람일: 2026-10-02.
- 대상: `raw/web-audio-1/index.mdx`의 「인간이 들을 수 있는 소리의 범위」부터 「모노와 스테레오, 채널 이해하기」까지.
- 핵심 질문: 사람이 어떤 소리를 감지하고 구별하는지 이해한 뒤, 그 소리를 컴퓨터가 다룰 수 있는 샘플과 채널로 어떻게 표현하는가?
- 포함: 가청주파수 범위, 주파수별 가청역치, 물리적 음압과 주관적 큰소리, 음색의 스펙트럼·시간 구조, PCM 샘플링·최소한의 양자화 개념, 샘플레이트·나이퀴스트 조건·앨리어싱·재구성, 모노·스테레오·프레임.
- 제외: 앞 절의 소리 발생·귀의 구조·데시벨 공식 유도, 질병·청력 치료·소음 규제, 악기 구조·음계·포먼트 상세, FFT 구현, 압축·코덱·디더링·양자화 잡음 상세, 다채널 규약, Web Audio 노드 구현, 다음 편의 주제.
- 성격: 본문 초안이 아니라 학습 노트다. 제목·frontmatter·본문은 수정하지 않는다.

### 먼저 학습할 주제와 순서

| 순서 | 현재 목차 | 학습할 질문 | 이해했는지 확인할 기준 |
|---|---|---|---|
| 1 | 인간이 들을 수 있는 소리의 범위 | 가청주파수 범위와 가청역치는 무엇이 다른가? | Hz로 나타내는 범위와 주파수별 최소 감지 수준을 구별한다. |
| 2 | 같은 절의 보충 개념 | 같은 음압 수준인데 다르게 크게 들릴 수 있는가? | 물리적 음압 수준과 주관적 큰소리, 등청감 곡선을 구별한다. |
| 3 | 파형에 따라 달라지는 음색 | 같은 음높이의 악기 소리는 왜 다른가? | 배음의 상대 크기와 음의 시작·감쇠 같은 시간 변화를 함께 설명한다. |
| 4 | 연속적인 소리를 샘플로 기록하기 | 한 개의 샘플에는 무엇이 들어가는가? | 측정 시점의 간격과 진폭값의 표현 정밀도를 구별한다. |
| 5 | 샘플레이트와 표현할 수 있는 주파수 | 초당 샘플 수가 표현 가능한 주파수와 어떻게 연결되는가? | 대역제한·나이퀴스트 경계·앨리어싱·필터·복원 조건을 설명한다. |
| 6 | 모노와 스테레오, 채널 이해하기 | 두 채널이면 샘플레이트도 두 배인가? | 샘플·프레임·채널 수를 구별하고 같은 시간축의 병렬 신호로 이해한다. |

위 학습 순서는 아래 확인한 개념을 연결하기 위한 구성 제안이다. 참고 자료의 목차를 그대로 옮긴 것이 아니다.

## 핵심 조사 내용

### 1. 인간이 들을 수 있는 소리의 범위: 주파수와 역치를 분리하기

**학습할 용어:** 가청주파수 범위, 순음, 가청역치, 주파수별 청각 민감도, 연령·개인차.

- 교재에서 인간의 가청주파수 범위를 대략 **20 Hz~20 kHz**로 소개한다. 이를 모든 사람이 이 구간의 모든 소리를 들을 수 있다는 보장이나 정확한 절단 주파수로 쓰면 안 된다. 실제 순음 역치는 주파수·연령·개인·측정 조건에 따라 달라진다. [S01](https://openstax.org/books/university-physics-volume-1/pages/17-introduction) [S02](https://pubmed.ncbi.nlm.nih.gov/24749665/) [S03](https://pubmed.ncbi.nlm.nih.gov/2212307/)
- **가청역치는 특정 주파수와 청취 조건에서 겨우 감지할 수 있는 최소 수준**이다. 들을 수 있는 크기 전체나 최대 음량을 뜻하지 않는다. 연구에서 주파수를 바꿔 가며 순음 역치를 측정하는 이유도 이 최소 수준이 하나의 고정값이 아니기 때문이다. [S02](https://pubmed.ncbi.nlm.nih.gov/24749665/) [S03](https://pubmed.ncbi.nlm.nih.gov/2212307/)
- 645명의 건강한 피험자, 5~90세, 0.125~20 kHz를 대상으로 한 연구의 초록은 주파수와 나이에 따른 역치 증가를 보고한다. 별도의 남성 813명, 20~95세, 0.125~8 kHz 종단 연구에서도 연령에 따른 변화를 관찰했다. **서로 다른 표본의 결과를 특정 나이의 보편적 최고 가청주파수로 바꾸지는 않는다.** 두 논문은 초록만 확인했다. [S02](https://pubmed.ncbi.nlm.nih.gov/24749665/) [S03](https://pubmed.ncbi.nlm.nih.gov/2212307/)

**현재 문장에서 주의할 점**

> 들을 수 있는 소리의 높낮이는 가청주파수, 들을 수 있는 소리의 크기는 가청역치이다.

이 표현은 주파수 범위와 최소 감지 수준을 높낮이·크기 전체와 혼동하게 한다. 학습 후에는 다음 구별을 유지해야 한다.

- 가청주파수 **범위**: 감지 가능한 주파수의 대략적인 범위.
- 가청역치: 각 주파수에서 감지에 필요한 **최소** 수준.
- 소리의 주관적 큰소리: 물리적 음압만으로 동일하게 정해지는 감각이 아니다. [S02](https://pubmed.ncbi.nlm.nih.gov/24749665/) [S06](https://www.animations.physics.unsw.edu.au/jw/dB.htm)

**읽기 순서:** S01의 짧은 개괄 → S02의 연구 목적·표본·결과 → S03의 다른 표본과 측정 범위. 논문 전체의 의학적 논의를 확장해서 읽을 필요는 없다.

### 2. 음압 수준과 주관적 큰소리: 등청감 곡선 이해하기

**학습할 용어:** Hz, dB SPL, 기준 음압, loudness, 등청감 곡선. phon은 곡선의 기준을 이해하는 정도만 학습한다.

- **Hz는 주파수**, **dB SPL은 기준 음압에 대한 물리적 음압 수준**을 나타낸다. 공기 중 기준 음압은 20 μPa다. dB라는 표기만으로 주파수, 가청역치, 주관적 큰소리를 모두 나타내는 것은 아니다. [S01](https://openstax.org/books/university-physics-volume-1/pages/17-introduction) [S05](https://www.phys.unsw.edu.au/jw/musical-sounds-musical-instruments.html) [S06](https://www.animations.physics.unsw.edu.au/jw/dB.htm)
- 같은 음압 수준이라도 주파수가 다르면 똑같이 크게 느껴지지 않을 수 있다. **등청감 곡선은 서로 다른 주파수의 순음을 같은 크기로 느끼는 데 필요한 음압 수준들을 연결한다.** 최소 감지 수준을 나타내는 역치와, 이미 들리는 두 음의 큰소리를 맞추는 등청감 곡선은 구별한다. [S04](https://www.iso.org/standard/83117.html) [S06](https://www.animations.physics.unsw.edu.au/jw/dB.htm)
- ISO 226:2023의 공식 소개는 연속 순음, 정면 음원·자유 진행 평면파, 양쪽 귀 청취, 청각학적으로 정상인 18~25세 등 적용 조건을 명시한다. 표준의 곡선을 모든 연령·헤드폰·복합음의 감각과 그대로 동일시하지 않는다. 유료 부속서의 실제 수치는 확인하지 않았다. [S04](https://www.iso.org/standard/83117.html)
- **0 dB SPL은 무음이 아니라 기준 음압과 같은 수준**이다. 따라서 이를 모든 주파수에서 모든 사람에게 정확히 겨우 들리는 수준으로 단정하지 않는다. [S05](https://www.phys.unsw.edu.au/jw/musical-sounds-musical-instruments.html) [S06](https://www.animations.physics.unsw.edu.au/jw/dB.htm)

**읽기 순서:** S06의 `Standard reference levels`와 `Loudness, phons and sones, hearing response curves` → S04의 공개 적용 조건. S06의 그림은 **ISO 226:2003** 설명이므로 2023판의 수치 그림이라고 재인용하지 않는다.

### 3. 파형에 따라 달라지는 음색: 스펙트럼과 시간 변화 함께 보기

**학습할 용어:** 순음, 기본주파수, 배음, 스펙트럼, 진폭 엔벌로프, attack·decay·sustain·release.

- 음색은 같은 음높이·큰소리·길이로 맞춘 소리들을 서로 다르게 느끼게 하는 지각적 성질이다. '주파수가 높아서', '진폭이 커서'만으로 악기 소리의 차이를 설명하는 것과 구별한다. [S07](https://pmcharrison.github.io/intro-to-music-and-science/timbre.html) [S08](https://www.mcgill.ca/mpcl/files/mpcl/caclin_2005_jasa_0.pdf)
- 순음은 사인파로 설명할 수 있다. 조화적인 주기음은 기본주파수 `f₀`와 정수배 성분 `2f₀`, `3f₀`, …의 조합으로 생각할 수 있고, 각 성분의 상대 크기가 스펙트럼을 이룬다. **같은 기본주파수라도 다른 배음 분포를 가질 수 있다.** 모든 소리가 정수배 배음으로만 이루어진다는 뜻은 아니다. [S05](https://www.phys.unsw.edu.au/jw/musical-sounds-musical-instruments.html) [S07](https://pmcharrison.github.io/intro-to-music-and-science/timbre.html)
- 음색에는 이 스펙트럼뿐 아니라 **소리가 시작되고 유지되고 사라지는 시간적 변화**도 기여한다. 한 주기의 파형 모양만으로 음색을 모두 설명하면 attack와 감쇠를 놓친다. 전체 시간 파형에는 이런 변화도 들어가므로, 여기서 파형과 엔벌로프가 서로 완전히 별개의 신호라고 이해하지 않는다. [S05](https://www.phys.unsw.edu.au/jw/musical-sounds-musical-instruments.html) [S07](https://pmcharrison.github.io/intro-to-music-and-science/timbre.html) [S08](https://www.mcgill.ca/mpcl/files/mpcl/caclin_2005_jasa_0.pdf)
- ADSR는 엔벌로프를 attack, decay, sustain, release로 단순화한 학습 모델이다. 실제 악기 소리를 완전히 표현하는 보편 법칙이 아니다. [S07](https://pmcharrison.github.io/intro-to-music-and-science/timbre.html)
- Caclin 등의 통제된 합성음 실험에서는 attack time, spectral centroid, 스펙트럼의 세부 구조가 음색 차이 판단에 기여했다. spectral flux의 중요도는 함께 변하는 요소에 따라 달랐고 개인별 가중치 차이도 관찰됐다. 따라서 '음색은 배음으로만 결정된다'나 'attack가 언제나 가장 중요하다'라는 결론은 채택하지 않는다. [S08](https://www.mcgill.ca/mpcl/files/mpcl/caclin_2005_jasa_0.pdf)

**읽기 순서:** S05의 `Pure tones, harmonics ... Timbre, spectrum, envelope and transients` → S07의 8.2.1·8.2.2 → S08의 Abstract와 General Discussion. 논문의 MDS 통계 모델·신경생리까지 학습 범위를 넓히지 않는다. 교육 자료의 음원 예시는 학습자가 들어볼 수 있지만 이번 조사에서 직접 청취하지는 않았다.

### 4. 연속적인 소리를 샘플로 기록하기: 시간과 값의 이산화를 분리하기

**학습할 용어:** 아날로그 신호, 샘플, 샘플레이트, PCM, 양자화, 비트 깊이.

- 녹음에서는 마이크가 소리를 전기적 아날로그 신호로 바꾸고, 일정한 시간 간격의 신호값을 취한다. 연속 신호를 `x(t)`, 초당 샘플 수를 `fₛ`라고 하면 샘플 열은 `x[n] = x(n / fₛ)`로 나타낼 수 있다. 이는 먼저 **언제 값을 측정하는가**에 대한 모델이다. [S09](https://ccrma.stanford.edu/~jay/subpages/Lectures/Lecture8-Digital_audio.pdf) [S10](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Basic_concepts_behind_Web_Audio_API) [S12](https://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html)
- **정수 PCM**으로 기록할 때는 진폭값도 유한한 코드값으로 양자화한다. `b`비트의 고정폭 값에는 `2ᵇ`개의 코드값이 있으므로 16비트는 65,536개다. 샘플레이트는 시간 간격, 비트 깊이는 값의 표현 정밀도와 관련된다. 양자화와 샘플링을 같은 과정이라고 부르지 않는다. [S09](https://ccrma.stanford.edu/~jay/subpages/Lectures/Lecture8-Digital_audio.pdf) [S13](https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex)
- MDN이 설명하는 Web Audio 버퍼의 샘플은 **32비트 부동소수점 값**이다. 이를 '16비트 PCM 녹음의 65,536개 고정폭 진폭 단계'와 동일한 형식으로 읽지 않는다. API 구현을 배우려는 것이 아니라 샘플의 값 표현과 저장 형식이 다를 수 있음을 구별하려는 참고다. [S10](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Basic_concepts_behind_Web_Audio_API)

**학습 예:** 44,100 Hz는 채널당 1초에 44,100번의 측정 시점, 즉 약 22.676 μs 간격을 뜻한다. 44,100 Hz라는 샘플레이트가 원래 소리의 음높이 44,100 Hz라는 뜻은 아니다. [S10](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Basic_concepts_behind_Web_Audio_API) [S12](https://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html)

**읽기 순서:** S09의 `A/D conversion`·`Quantization` → S10의 `Audio data: what's in a sample`·`Audio buffers`. 양자화 잡음 계산·디더링은 이번 절의 필수 학습이 아니다.

### 5. 샘플레이트와 표현할 수 있는 주파수: 대역제한·앨리어싱·복원

**학습할 용어:** 샘플링 주파수, 나이퀴스트 주파수, 대역제한, 앨리어싱, 안티앨리어싱 필터, 재구성.

- 등간격의 이상적인 샘플링에서 원 신호가 `fₛ / 2` **미만**으로 대역제한되어 있다면 샘플로부터 연속 신호를 이론적으로 복원할 수 있다. 여기에는 대역제한과 이상적인 복원이라는 조건이 붙는다. 임의 위상의 경계 주파수까지 항상 복원이 보장된다고 쓰지 않는다. [S11](https://webusers.imj-prg.fr/~antoine.chambert-loir/enseignement/2020-21/shannon/shannon1949.pdf) [S12](https://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html)

| 샘플레이트 `fₛ` | 나이퀴스트 경계 `fₛ / 2` | 해석 |
|---|---|---|
| 44.1 kHz | 22.05 kHz | 일반적인 복원 보장은 경계 미만의 대역제한 신호에 적용한다. |
| 48 kHz | 24 kHz | 실제 기기의 유효 대역·필터 성능을 이 숫자 하나로 보장하지 않는다. |

위 값은 정리의 식에 대한 산술 계산이다. MDN의 44.1 kHz 설명과 독립된 수학 교재의 조건을 대조했다. [S10](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Basic_concepts_behind_Web_Audio_API) [S12](https://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html)

- 상한 이상의 성분이 입력에 남은 상태로 샘플링하면 서로 다른 연속 신호가 같은 샘플 열로 나타날 수 있다. 이것이 앨리어싱을 이해하는 출발점이다. 이를 막으려면 **샘플링 전에** 안티앨리어싱 필터로 입력 대역을 제한해야 한다. 이미 섞여 기록된 신호를 사후 필터 하나로 항상 원래대로 되돌릴 수 있다고 설명하지 않는다. [S09](https://ccrma.stanford.edu/~jay/subpages/Lectures/Lecture8-Digital_audio.pdf) [S10](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Basic_concepts_behind_Web_Audio_API) [S12](https://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html)
- 실제 필터는 원하는 대역을 통과시키면서 그 바로 바깥을 완벽히 끊는 이상적인 필터가 아니다. 전이대역을 위한 여유가 필요하다. 20 kHz를 대상으로 보면 44.1 kHz의 경계까지는 2.05 kHz의 여유가 있다. 이것은 설명용 대역 차이이며 실제 필터의 차수·감쇠량·음질 보장이 아니다. [S10](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Basic_concepts_behind_Web_Audio_API)
- **샘플을 계단으로 그린 그림은 디지털 소리의 최종 파형 자체가 아니다.** 이상적인 대역제한 보간은 샘플에서 연속 파형을 재구성한다. 실제 PCM의 양자화 오차와 실제 변환기·필터의 한계까지 사라진다는 뜻은 아니다. [S09](https://ccrma.stanford.edu/~jay/subpages/Lectures/Lecture8-Digital_audio.pdf) [S11](https://webusers.imj-prg.fr/~antoine.chambert-loir/enseignement/2020-21/shannon/shannon1949.pdf) [S12](https://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html)

**수치로 확인한 학습 예**

- 8 kHz로 샘플링한 6 kHz 사인파는 위상이 반전된 2 kHz 사인파와 같은 샘플 열을 만든다. 서로 다른 원 신호를 그 샘플만으로 구별할 수 없다.
- 8 kHz로 샘플링하는 경계인 4 kHz에서 위상이 0인 사인파는 모든 측정 시점에서 0이 된다. '한 주기당 두 점이면 어떤 신호든 충분하다'는 설명의 반례다.
- 위 예를 128개 측정 시점에서 직접 계산했다. 부동소수점 오차를 제외한 최대 차이는 각각 약 `1.28 × 10⁻¹³`, `8.23 × 10⁻¹⁴`였다. 수학적 예시이지 실제 녹음·청취 실험은 아니다. 정리와 경계에 대한 근거는 S12다. [S12](https://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html)

**읽기 순서:** S09의 `Aliasing`·`Anti-Aliasing Filters` → S10의 44.1 kHz 설명 → S12의 정리 첫 문장·마지막 경계 설명 → 관심이 생기면 S11 Section II. sinc 보간의 유도는 심화 자료이며 본문에 증명을 넣을 필요는 없다.

### 6. 모노와 스테레오: 채널을 병렬 신호로 이해하기

**학습할 용어:** 채널, 모노, 스테레오, 샘플 프레임.

- 모노는 한 채널, 스테레오는 두 채널이다. 두 채널을 좌·우의 시간에 따른 샘플 열로 생각하면 된다. 채널 수를 스피커 장치 개수나 샘플레이트와 동일시하지 않는다. MDN의 오디오 버퍼 설명과 Microsoft의 별도 PCM 형식 계약이 1/2채널 정의를 명시한다. [S10](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Basic_concepts_behind_Web_Audio_API) [S13](https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex)
- **샘플은 한 채널의 한 시점 값**, **프레임은 같은 시점에 재생되는 모든 채널의 값 묶음**이다. 44.1 kHz의 1초 오디오는 모노·스테레오 모두 44,100프레임이고, 개별 샘플값은 모노 44,100개, 스테레오 88,200개다. 두 채널이라고 시간축의 샘플레이트가 88.2 kHz가 되는 것은 아니다. [S10](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Basic_concepts_behind_Web_Audio_API) [S13](https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex)
- 시간축의 샘플레이트, 값의 비트 깊이, 병렬 신호 열의 채널 수는 구별할 축이다. 예를 들어 헤더·패딩을 제외한 1초의 44.1 kHz·16비트·2채널 고정폭 PCM 데이터는 `44,100 × 2 × 16 / 8 = 176,400`바이트다. 이는 비압축 PCM의 산술 예시이며 압축 파일 용량 계산이 아니다. [S09](https://ccrma.stanford.edu/~jay/subpages/Lectures/Lecture8-Digital_audio.pdf) [S13](https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex)

**읽기 순서:** S10의 `Audio buffers: frames, samples, and channels` → S13의 `nChannels`·`nSamplesPerSec`·`nBlockAlign`·`wBitsPerSample`. Win32 구조체나 Web Audio 코드를 구현하는 것은 이번 학습 범위가 아니다.

## 팩트 체크

`교차 확인`은 독립적으로 작성된 직접 설명·다른 연구 또는 수학적 논증을 대조했다는 뜻이다. 교육 문서 둘이 같은 원연구를 인용하는 경우를 독립 실험 두 개로 세지 않았다. `조건부` 행은 대조를 마쳤지만 적용 조건이 필요한 내용이다.

| 주장 | 판정 | 근거 | 조건·한계·주의할 표현 |
|---|---|---|---|
| 인간의 통상 가청주파수 범위를 20 Hz~20 kHz로 소개할 수 있다. | 조건부 | S01·S02·S03 | 교재의 대략적 범위. 모든 개인의 끝점을 입증한 값은 아니다. 두 연구는 초록만 확인했다. |
| 가청역치는 주파수·조건별 최소 감지 수준이다. | 교차 확인 | S02·S03·S06 | 들을 수 있는 크기 전체나 최대 수준이 아니다. |
| 연령에 따라 역치가 달라진다. | 조건부 | S02·S03 | 서로 다른 표본·측정 범위에서 대조. 특정 나이의 최고 가청주파수로 환산하지 않는다. |
| 같은 음압 수준이 모든 주파수에서 같은 큰소리를 보장하지 않는다. | 조건부 | S04·S06 | 순음·청취 조건을 고려한다. ISO 부속서 수치는 미확인이다. |
| 음색에는 스펙트럼과 시간적 구조가 함께 기여한다. | 조건부 | S05·S08 | 독립 교육 설명과 통제된 합성음 실험 대조. 요소의 중요도는 과제·음·개인에 따라 달라진다. |
| 샘플링 시점의 이산화와 정수 PCM 진폭 양자화는 다르다. | 교차 확인 | S09·S10·S13 | 부동소수점 내부 데이터까지 동일한 고정 진폭 단계로 설명하지 않는다. |
| 이상적인 대역제한 신호는 충분한 등간격 샘플에서 복원할 수 있다. | 조건부 | S11·S12 | 일반적 보장은 fₛ/2 미만. 유한 비트 양자화·실제 기기의 완전 복원 보장이 아니다. |
| 44.1/48 kHz의 나이퀴스트 경계는 22.05/24 kHz다. | 교차 확인 | S10·S12 | 식의 산술 계산. 경계 주파수의 임의 위상 복원과 실제 유효 대역은 구별한다. |
| 앨리어싱 방지에는 샘플링 전 대역제한이 필요하다. | 교차 확인 | S09·S10·S12 | 이미 겹친 성분을 사후 필터로 언제나 분리할 수 있다고 쓰지 않는다. |
| 계단 그림이 유일한 재구성은 아니다. | 교차 확인 | S09·S11·S12 | 이상적 보간과 실제 D/A 회로·필터를 구별한다. |
| 모노/스테레오는 1/2채널이며 시간축 샘플레이트와 다른 축이다. | 교차 확인 | S10·S13 | 각 채널의 프레임과 개별 샘플값 수를 혼동하지 않는다. |
| 두 채널의 값이 같을 수 있다. | 단일 출처 | S10 Up-mixing | MDN은 모노를 좌·우에 복제하는 규칙을 명시한다. 보조 반례로만 남긴다. 실제 공간감의 크기·품질을 검증한 연구는 아니다. |

표의 출처 ID는 아래 원문 URL·확인 위치와 연결된다. 각 핵심 설명 옆에도 직접 링크를 남겼다.

## 주의·추가 확인

- **가청역치와 등청감 곡선의 수치:** ISO 226:2023의 유료 본문·부속서를 확보하지 못했다. 조사 중 공식 소개는 확인했으나 통합 단계 재접속은 HTTP 403 및 브라우저 접근 확인 화면으로 제한됐다. 특정 주파수의 정확한 역치·phon 값을 채워 넣지 않는다.
- **청각 연구의 읽은 범위:** S02·S03은 PubMed 초록만 확인했다. 장비, 모집·제외 기준, 오차·세부 통계·개별 최고 주파수는 본문에서 검증하지 못했다. 연구 간 표본 차이는 지우지 않았다.
- **채널의 단일 출처 사례:** S10의 모노→스테레오 업믹스에서는 같은 입력을 좌·우에 복제한다. 형식상 두 채널이라는 사실만으로 서로 다른 내용이 담겼다고 판단할 수 없다는 반례다. 두 채널 형식이 어느 정도의 공간감을 만드는지는 조사하지 않았다.
- **샘플 숫자와 음압은 같은 단위가 아니다 — 해석:** 전기 신호·디지털 값이 청취 위치의 Pa나 dB SPL로 자동 환산되지는 않는다. 마이크의 변환·보정, 재생 계통과 측정 조건이 필요하다. S09의 전기 신호 설명과 S10의 부동소수점 샘플 정의를 근거로 한 구별이며 보정 방법 자체는 조사하지 않았다.
- **문서의 일반화 경고:** S10의 '샘플레이트가 높을수록 음질이 좋다'라는 단순 문장은 조건·평가 방법이 없으므로 채택하지 않았다. 샘플레이트를 올리면 어떤 청취 환경에서나 무조건 더 좋게 들린다는 주장은 이번 근거로 검증되지 않았다.
- **PDF와 판본:** S11은 1949 원논문의 1998 재인쇄본을 읽었다. 원본과 재인쇄본을 독립 연구 두 개로 세지 않았다. S09·S11은 조사에서는 원문을 확인했지만 통합 단계 재조회에서 binary fetch aborted가 발생했다. PDF 수식의 일부 추출 손실은 S12의 HTML 수식과 대조했으며 읽지 않은 원본 판본을 읽었다고 표기하지 않았다.
- **정정·철회:** 아래 논문들의 정정·철회 상태를 별도 서비스까지 조회해 확정하지는 못했다. `확인 불가`를 `정정·철회 없음`으로 바꾸지 않는다.
- **본문의 메모 위치:** 현재 가청 범위 절 아래에 파형 관련 메모, 음색 절 아래에 가청 범위 메모가 있다. 이는 원문에서 관찰한 배치다. 위 학습 주제는 절 제목을 기준으로 정리했으며 메모나 본문을 수정하지 않았다.

## 출처

등급은 이번에 인용하는 주장에 대한 평가다. 공식 문서·논문·대학 사이트라는 이름만으로 정하지 않았다. 별도 표시가 없는 웹 자료의 이해관계 선언·정정 상태는 확인 불가이며, 교육 자료는 동료심사 논문으로 취급하지 않는다. 모든 열람일은 조사일과 같다.

### S01. University Physics Volume 1 — Chapter 17 Introduction
- URL: https://openstax.org/books/university-physics-volume-1/pages/17-introduction
- 작성자·기관·날짜: William Moebs, Samuel J. Ling, Jeff Sanny / OpenStax / 2016-09-19, 페이지 서지정보.
- 확인 위치: Figure 17.1 설명과 Introduction의 20 Hz~20 kHz 문단.
- 신뢰도: **보통**. 책임 주체가 명확한 공개 교재지만 범위는 개괄적이며 개인별 역치 측정 조건을 제시하지 않는다.
- 인용 범위·한계: 통상 가청 범위의 출발점. 모든 사람의 절대 경계 근거로 사용하지 않는다.

### S02. Extended high-frequency (9–20 kHz) audiometry reference thresholds in 645 healthy subjects
- URL: https://pubmed.ncbi.nlm.nih.gov/24749665/
- DOI: https://doi.org/10.3109/14992027.2014.893375
- 저자·서지: A. Rodríguez Valiente, A. Trinidad, J. R. García Berrocal, C. Górriz, R. Ramírez Camacho / International Journal of Audiology 53(8), 531–545 / 2014-08, 온라인 2014-04-22.
- 확인 위치·읽은 범위: PubMed의 Objective·Design·Study sample·Results·Conclusions, **초록만 확인**.
- 신뢰도: **보통**, 초록에 명시된 표본과 결과에 한정. 645명·연령·측정 주파수 범위는 확인했지만 본문 방법·오차를 확인하지 못했다.
- 인용 범위·검증 상태: 주파수·연령별 역치 변화. 개별 20 kHz 청취 비율과 보편적 끝점은 미확인. 학술지 출판을 확인했으나 심사 상세·정정·철회·이해관계는 확인 불가.

### S03. Age changes in pure-tone hearing thresholds in a longitudinal study of normal human aging
- URL: https://pubmed.ncbi.nlm.nih.gov/2212307/
- DOI: https://doi.org/10.1121/1.399731
- 저자·서지: L. J. Brant, J. L. Fozard / Journal of the Acoustical Society of America 88(2), 813–820 / 1990-08.
- 확인 위치·읽은 범위: PubMed **초록만 확인**. 813명 남성, 20~95세, 0.125~8 kHz, 반복 측정의 표본·조건·결과.
- 신뢰도: **보통**. S02와 다른 표본의 종단 연구로 대조할 수 있지만 여성·8 kHz 초과에 일반화할 수 없고 본문 방법은 미확인이다.
- 인용 범위·검증 상태: 연령에 따른 역치 변화. 오래됐다는 이유만으로 제외하지 않지만 현대 인구의 정확한 평균값을 추정하는 데 사용하지 않는다. 심사 상세·정정·철회·이해관계는 확인 불가.

### S04. ISO 226:2023 — Acoustics — Normal equal-loudness-level contours
- URL: https://www.iso.org/standard/83117.html
- 작성 기관·판본: ISO / 제3판 / 2023-03.
- 확인 위치·읽은 범위: 공식 소개의 Abstract와 적용 조건. 표준 본문·Annex A/B는 미확인. 통합 단계 재접속 제한은 주의 사항에 기록했다.
- 신뢰도: **높음**, 발행 기관이 직접 명시한 정의·범위·적용 조건에 한정.
- 인용 범위·한계: 등청감 곡선의 목적과 정상 청각의 젊은 성인·자유음장 조건. 유료 표의 수치를 재현하거나 모든 환경에 일반화하지 않는다. 학술논문 심사 상태는 해당 없음, 별도 정정 상태는 확인 불가.

### S05. Musical sounds, musical instruments and musical signals
- URL: https://www.phys.unsw.edu.au/jw/musical-sounds-musical-instruments.html
- 작성자·기관·날짜: Joe Wolfe / UNSW Music Acoustics / Wolfe의 2012년 책 장 `Musical sounds and musical signals`의 multimedia appendix. 웹 갱신일 미상.
- 확인 위치: `Intensity, pressure and loudness`, `Pure tones, harmonics ... Timbre, spectrum, envelope and transients`, 보조적으로 `Music as a signal`.
- 신뢰도: **보통**. 작성자·교재 연결·직접 설명과 예시가 분명하지만 모든 진술에 대한 원실험을 제시하지는 않는다.
- 인용 범위·한계: 배음·스펙트럼·시간 변화의 기초, 음압 기준. '시간 변화가 매우 중요하다'를 모든 소리의 중요도 순위로 확대하지 않는다. 음원 링크는 확인했으나 직접 청취하지 않았다.

### S06. dB: What is a decibel?
- URL: https://www.animations.physics.unsw.edu.au/jw/dB.htm
- 작성 기관·날짜: UNSW Physics/Physclips의 교육 페이지 / 게시·갱신일 미상, 개별 본문 저자 표기 확인 불가.
- 확인 위치: `Standard reference levels`, `What does 0 dB mean?`, `Not all sound pressures are equally loud`, `Loudness, phons and sones, hearing response curves`.
- 신뢰도: **보통**. 정의·조건·청각 곡선을 구체적으로 설명하지만 등청감 그림은 ISO 226:2003을 설명한다.
- 인용 범위·한계: 기준 음압, 주파수에 따른 민감도, 등청감 곡선의 읽는 법. 소음 위험·제품·전자회로 관련 부분은 제외한다. S05와 같은 교육 계열이므로 서로를 독립 연구 두 개로 세지 않는다.

### S07. Introduction to Music and Science — Chapter 8 Timbre
- URL: https://pmcharrison.github.io/intro-to-music-and-science/timbre.html
- 작성자·날짜: Peter M. C. Harrison, 페이지 metadata / 게시·갱신일 미상.
- 확인 위치: 도입의 정의, 8.2.1 `Temporal aspects`, 8.2.2 `Spectral aspects`.
- 신뢰도: **보통**. 설명·도식·참고문헌·ADSR 단순화의 한계가 제공된다. 인용된 ASA 정의·McAdams & Giordano의 책 원문은 직접 확인하지 않았다.
- 인용 범위·한계: 스펙트럼과 엔벌로프, ADSR 입문. 표준 정의를 직접 읽은 것처럼 쓰거나 독립 원실험으로 세지 않는다. 음원·영상·앱은 재생하지 않았다.

### S08. Acoustic correlates of timbre space dimensions: A confirmatory study using synthetic tones
- 원문 URL: https://www.mcgill.ca/mpcl/files/mpcl/caclin_2005_jasa_0.pdf
- DOI: https://doi.org/10.1121/1.1929229
- 저자·서지: Anne Caclin, Stephen McAdams, Bennett K. Smith, Suzanne Winsberg / Journal of the Acoustical Society of America 118(1), 471–482 / 2005-07. 원문에 2005-04-18 revised·accepted를 명시한다.
- 확인 위치·읽은 범위: PDF 1~4쪽(원문 471~474)의 Abstract·Introduction·Experiment 1 Method, PDF 11~12쪽(481~482)의 General Discussion·개인차·한계.
- 신뢰도: **높음**, 명시된 통제 합성음 실험의 설계·관찰 결과에 한정. 참가자·자극·절차·분석·한계를 확인했다. 모든 악기·청취 과제에 일반화할 근거로는 제한적이다.
- 인용 범위·검증 상태: attack·스펙트럼 정보의 기여와 문맥·개인차. 실험 1은 청력 손실을 자기보고하지 않은 19~51세 30명이다. 심사 의견·정정·철회·상업적 이해관계 선언은 확인 불가.

### S09. Introduction to Digital Audio
- URL: https://ccrma.stanford.edu/~jay/subpages/Lectures/Lecture8-Digital_audio.pdf
- 작성 기관·날짜: Stanford CCRMA의 `~jay` 강의 자료 / 본문에서 전체 저자 이름·게시일 확인 불가.
- 확인 위치·읽은 범위: PDF 1~5쪽, `A/D conversion`, `Quantization`, `Aliasing`, `Anti-Aliasing Filters`, `D/A conversion`. 통합 단계의 재조회 실패는 주의 사항에 기록했다.
- 신뢰도: **보통**. 변환 단계·조건을 구체적으로 설명하는 대학 강의 자료지만 발행 시점·심사 상태는 미확인이다.
- 인용 범위·한계: 시간 샘플링·정수 양자화·필터·계단 유지 후 복원. 특정 변환기 성능·고비트 음질 우열에는 사용하지 않는다.

### S10. Basic concepts behind Web Audio API
- URL: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Basic_concepts_behind_Web_Audio_API
- 작성 기관·날짜: MDN Web Docs 공동 저술 / 이번 열람에서 문서 최종 변경일 확인 불가.
- 확인 위치: `Audio data: what's in a sample`, `Audio buffers: frames, samples, and channels`, 44.1 kHz와 필터 설명, `Up-mixing and down-mixing`의 모노→스테레오 사례.
- 신뢰도: **높음**(버퍼·프레임·채널의 명확한 정의와 구체적 규칙), **보통**(샘플링 입문 설명). 조건 없는 '높은 샘플레이트가 더 좋은 음질' 주장은 근거가 부족하므로 채택하지 않았다.
- 인용 범위·한계: 샘플·프레임·채널, 정수 PCM과 부동소수점 값 구별, 필터 전이대역의 입문 예. API 노드·그래프 구현과 다채널 규약은 제외한다. 학술논문이 아니며 제품 우수성 비교의 근거로 쓰지 않는다.

### S11. Communication in the Presence of Noise
- 원문으로 읽은 재인쇄 URL: https://webusers.imj-prg.fr/~antoine.chambert-loir/enseignement/2020-21/shannon/shannon1949.pdf
- 원논문 DOI: https://doi.org/10.1109/JRPROC.1949.232969
- 서지 검증 URL: https://api.crossref.org/works/10.1109/JRPROC.1949.232969
- 저자·서지: Claude E. Shannon / Proceedings of the IRE 37(1), 10–21 / 1949-01. 읽은 자료는 Proceedings of the IEEE의 1998년 재인쇄다. 원논문의 제목·저자·권호·쪽·DOI는 Crossref의 IEEE 등록 정보와 대조했다.
- 확인 위치·읽은 범위: 재인쇄 447~449쪽의 Section I·Section II Theorem 1과 복원식. PDF 일부 수식 추출 손실을 S12와 대조했다. 1949 호의 원본 PDF를 직접 읽었다고 주장하지 않는다.
- 신뢰도: **높음**, 명시된 대역제한 가정과 수학적 재구성 정리에 한정. 실제 오디오 장치의 완벽한 성능 근거가 아니다.
- 검증 상태·한계: 재인쇄와 원연구는 한 출처로 묶었다. 원 심사 절차·정정·철회 상태는 확인 불가. 재조회 제한은 주의 사항에 기록했다.

### S12. Sampling Theorem
- URL: https://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html
- 저자·서지: Julius O. Smith III / Mathematics of the Discrete Fourier Transform (DFT), with Audio Applications, 2nd ed. / W3K Publishing, 2007 / ISBN 978-0-9745607-4-8. 온라인 페이지의 표기는 Copyright 2026-08-21이다.
- 확인 위치: 정리·대역제한 가정·주파수 영역 증명·sinc 보간·마지막 경계 위상 설명과 페이지 서지정보.
- 신뢰도: **높음**, 조건과 논증을 직접 제공하는 수학적 설명. S11의 재게시가 아니라 별도 교재의 논증이다.
- 인용 범위·한계: 이상적 샘플링·경계·복원. 실제 회로 성능·주관적 음질 우열에는 사용하지 않는다. S09와 같은 대학 자료라는 이유로 독립 기관 수를 늘려 보고하지 않는다.

### S13. WAVEFORMATEX (mmeapi.h)
- URL: https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex
- 작성 기관·날짜: Microsoft Learn / 문서 `ms.date` 2018-12-05, metadata `updated_at` 2024-02-22.
- 확인 위치: `nChannels`, `nSamplesPerSec`, `nAvgBytesPerSec`, `nBlockAlign`, `wBitsPerSample`의 정의.
- 신뢰도: **높음**, Microsoft가 직접 문서화한 PCM 형식 계약에 한정. MDN과 다른 플랫폼의 독립된 형식 정의를 대조하는 데 사용했다.
- 인용 범위·한계: 모노 1/스테레오 2채널, 시간·채널·비트 수의 구별과 고정폭 PCM 데이터 양. 구조체 구현·Windows 지원 범위·제품 음질 우위는 조사하지 않는다. 컨테이너 비트 수와 실제 유효 비트 수의 구별도 본문에 명시된다.

## 검색 기록

### 웹 검색
- `site:openstax.org physics sound 20 Hz 20000 Hz hearing threshold frequency decibel sound pressure`
- `ISO 226:2023 normal equal loudness level contours 18 25 years threshold 20 Hz 12500 Hz`
- `timbre harmonics attack envelope spectral temporal acoustics university`
- `site:phys.unsw.edu.au music acoustics harmonics sine square sawtooth waves timbre`
- `site:ccrma.stanford.edu sampling theorem bandlimited reconstruction aliasing audio 44100 48000 sample rate quantization channels`
- `site:developer.mozilla.org Web Audio API AudioBuffer sampleRate numberOfChannels PCM samples channel data`
- `WAVEFORMATEX nChannels monaural one channel stereo two channels Microsoft`

### 논문 검색
- PubMed 색인 대상: `site:pubmed.ncbi.nlm.nih.gov age hearing threshold frequency pure tone audiometry population study 20 kHz equal loudness` → S02·S03의 서지·초록 확인.
- 음색 논문: `site:pmc.ncbi.nlm.nih.gov timbre perception spectral temporal attack review McAdams` → Town & Bizley(2013) 종설에서 원연구 추적.
- 원실험: `Caclin McAdams Smith Winsberg 2005 acoustic correlates timbre space dimensions attack time spectral centroid` → S08의 원문·방법·논의 확인.
- 샘플링 고전 논문: `Claude Shannon Communication in the Presence of Noise 1949 Proceedings IRE sampling theorem pdf DOI` → S11의 재인쇄 본문 확인, Crossref 등록 정보로 원논문 DOI·서지 대조.

### 중복·범위 제외
- 논문의 DOI 링크·PubMed 초록·대학 호스팅 PDF·재인쇄를 서로 다른 독립 연구로 세지 않았다.
- Town & Bizley(2013) 종설은 Caclin(2005)의 원연구를 추적하는 경로로 사용했다. 해당 실험의 독립 재현 근거로 추가하지 않았다.
- S12의 목차와 정리 페이지는 같은 교재 하나로 묶었다. S05·S06은 역할이 다른 교육 페이지지만 같은 계열 자료이므로 독립 실험 두 개로 세지 않았다.
- 소음의 건강 영향·치료·안전 수치, 신경영상·동물 실험, 음계·악기 구조, FFT·압축·디더링·고샘플레이트 음질 우열은 이번 목차에 직접 필요하지 않아 제외했다.
- `site:` 검색 결과에 제한 밖 사이트가 섞이는 경우가 있어 실제 도메인과 원문을 다시 확인했다. 검색 순위·요약문은 신뢰도 판정 근거로 사용하지 않았다.
