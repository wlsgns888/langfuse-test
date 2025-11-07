# Langfuse 상세 사용 가이드

이 문서는 각 기능별로 상세한 사용 방법과 실전 활용 팁을 제공합니다.

## 목차

1. [기본 트레이싱 (Tracing)](#1-기본-트레이싱-tracing)
2. [Generations](#2-generations)
3. [Sessions](#3-sessions)
4. [Scoring](#4-scoring)
5. [Prompts](#5-prompts)
6. [Datasets](#6-datasets)
7. [Langchain 통합](#7-langchain-통합)
8. [Agent 구현](#8-agent-구현)

---

## 1. 기본 트레이싱 (Tracing)

### 개념 이해

**Trace**는 애플리케이션의 전체 실행 흐름을 나타냅니다.
**Span**은 Trace 내의 개별 작업 단위입니다.

```
Trace (전체 요청)
├── Span 1 (전처리)
├── Span 2 (LLM 호출)
│   ├── Span 2.1 (프롬프트 구성)
│   └── Span 2.2 (API 호출)
└── Span 3 (후처리)
```

### 기본 사용법

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Trace 생성
trace = langfuse.trace(
    name="user_request",
    user_id="user_123",
    metadata={"version": "1.0"},
    tags=["production", "api"]
)

# Span 추가
span = trace.span(
    name="data_processing",
    input={"data": "..."},
    metadata={"step": 1}
)

# 작업 수행
result = process_data()

# Span 종료
span.end(output=result)

# Trace 종료
trace.end()

# 데이터 전송
langfuse.flush()
```

### 실전 활용 팁

1. **계층적 구조 활용**: 복잡한 작업은 중첩 Span으로 표현
2. **메타데이터 활용**: 디버깅에 필요한 정보를 메타데이터에 저장
3. **태그 활용**: 환경(dev/prod), 기능, 팀별로 태그 지정
4. **에러 추적**: level="ERROR"로 에러 상태 기록

### 실행 명령

```bash
python 01_basic_tracing.py
```

---

## 2. Generations

### 개념 이해

**Generation**은 LLM의 텍스트 생성을 추적하는 특별한 Observation입니다.
자동으로 토큰 수, 비용, 레이턴시를 계산합니다.

### 기본 사용법

```python
trace = langfuse.trace(name="llm_call")

generation = trace.generation(
    name="gpt4_response",
    model="gpt-4",
    model_parameters={
        "temperature": 0.7,
        "max_tokens": 500
    },
    input=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

# LLM 호출 후
generation.end(
    output="Hi! How can I help you?",
    usage={
        "prompt_tokens": 20,
        "completion_tokens": 8,
        "total_tokens": 28
    }
)
```

### 활용 시나리오

1. **대화형 애플리케이션**: 각 턴을 별도 Generation으로 추적
2. **스트리밍 응답**: 청크 단위 추적
3. **모델 비교**: 동일 입력으로 여러 모델 테스트
4. **비용 분석**: 토큰 사용량 기반 비용 계산

### 비용 계산 예제

```python
MODEL_COSTS = {
    "gpt-4": {
        "prompt": 0.03 / 1000,
        "completion": 0.06 / 1000
    }
}

cost = (
    prompt_tokens * MODEL_COSTS["gpt-4"]["prompt"] +
    completion_tokens * MODEL_COSTS["gpt-4"]["completion"]
)
```

### 실행 명령

```bash
python 02_generations.py
```

---

## 3. Sessions

### 개념 이해

**Session**은 관련된 여러 Trace를 그룹화합니다.
- 사용자와의 전체 대화
- 특정 작업의 여러 시도
- 사용자 여정

### 기본 사용법

```python
session_id = "session_001"

# 첫 번째 상호작용
trace1 = langfuse.trace(
    name="interaction_1",
    session_id=session_id,
    user_id="user_123"
)
# ... 작업 수행

# 두 번째 상호작용
trace2 = langfuse.trace(
    name="interaction_2",
    session_id=session_id,
    user_id="user_123"
)
# ... 작업 수행
```

### 활용 시나리오

1. **고객 지원**: 전체 지원 세션 추적
2. **챗봇**: 대화 세션별 그룹화
3. **사용자 여정**: 웹사이트에서 사용자 행동 추적
4. **디버깅**: 문제가 발생한 세션 전체 분석

### 세션 메타데이터 예제

```python
session_metadata = {
    "user_tier": "premium",
    "device": "mobile",
    "platform": "iOS",
    "app_version": "2.5.1",
    "session_start": datetime.now().isoformat()
}

trace = langfuse.trace(
    session_id=session_id,
    metadata=session_metadata
)
```

### 실행 명령

```bash
python 03_sessions.py
```

---

## 4. Scoring

### 개념 이해

**Scoring**은 LLM 출력의 품질을 평가하는 시스템입니다.
- 자동 메트릭 (정확도, 관련성)
- 사용자 피드백 (좋아요/싫어요, 별점)
- 커스텀 메트릭

### 기본 사용법

```python
trace = langfuse.trace(name="evaluated_response")

# Generation 실행
generation = trace.generation(...)
generation.end(output=response)

# 점수 추가
trace.score(
    name="accuracy",
    value=0.95,
    comment="Very accurate response"
)

trace.score(
    name="user_feedback",
    value=1.0,  # 1.0 = 좋아요, 0.0 = 싫어요
    data_type="BOOLEAN"
)
```

### 점수 유형

1. **NUMERIC**: 0-1 사이의 연속 값
2. **BOOLEAN**: True/False (1.0/0.0)
3. **CATEGORICAL**: 카테고리 레이블

### 활용 시나리오

1. **품질 모니터링**: 실시간 출력 품질 추적
2. **사용자 피드백**: 좋아요/싫어요, 별점 수집
3. **A/B 테스트**: 모델 또는 프롬프트 버전 비교
4. **알림 시스템**: 점수가 임계값 미만일 때 알림

### A/B 테스트 예제

```python
# Version A
trace_a = langfuse.trace(
    name="test_version_a",
    metadata={"variant": "A"}
)
# ... 실행
trace_a.score(name="quality", value=0.85)

# Version B
trace_b = langfuse.trace(
    name="test_version_b",
    metadata={"variant": "B"}
)
# ... 실행
trace_b.score(name="quality", value=0.92)
```

### 실행 명령

```bash
python 04_scoring.py
```

---

## 5. Prompts

### 개념 이해

**Prompt Management**는 프롬프트를 코드에서 분리하여 중앙에서 관리하는 시스템입니다.
- 버전 관리
- A/B 테스트
- 프로덕션/개발 분리

### Langfuse UI에서 프롬프트 생성

1. Langfuse 대시보드 접속
2. "Prompts" 메뉴 클릭
3. "Create New Prompt" 클릭
4. 이름, 템플릿, 변수 설정
5. 저장 후 버전 태깅

### 코드에서 프롬프트 사용

```python
from langfuse import Langfuse

langfuse = Langfuse()

# 프롬프트 가져오기
prompt = langfuse.get_prompt(
    name="qa_assistant",
    version="production"  # 또는 특정 버전 번호
)

# 변수 적용
final_prompt = prompt.compile(
    question="What is Langfuse?"
)

# Generation에 프롬프트 정보 포함
generation = trace.generation(
    name="response",
    model="gpt-3.5-turbo",
    input=final_prompt,
    prompt={
        "name": "qa_assistant",
        "version": "production"
    }
)
```

### 프롬프트 템플릿 예제

```
You are a {{assistant_type}}.
{{additional_instructions}}

User question: {{question}}
```

### 활용 시나리오

1. **버전 관리**: 프롬프트 변경 이력 추적
2. **A/B 테스트**: 여러 프롬프트 버전 동시 테스트
3. **롤백**: 문제 발생 시 이전 버전으로 즉시 복구
4. **협업**: 팀원 간 프롬프트 공유 및 개선

### 실행 명령

```bash
python 05_prompts.py
```

---

## 6. Datasets

### 개념 이해

**Datasets**는 모델 평가를 위한 테스트 케이스 모음입니다.
- 일관된 평가
- 회귀 테스트
- 벤치마킹

### 데이터셋 생성

```python
# Langfuse UI 또는 API를 통해 생성
dataset = langfuse.create_dataset(
    name="qa_eval_dataset",
    description="QA system evaluation dataset"
)

# 아이템 추가
dataset.create_item(
    input={"question": "What is the capital of France?"},
    expected_output="Paris",
    metadata={"category": "geography"}
)
```

### 데이터셋 평가 실행

```python
# 데이터셋 가져오기
dataset = langfuse.get_dataset("qa_eval_dataset")

# 각 아이템 평가
for item in dataset.items:
    trace = langfuse.trace(
        name=f"eval_{item.id}",
        metadata={"dataset_run": "run_001"}
    )

    # 모델 실행
    output = model.generate(item.input)

    # 정확도 계산
    is_correct = output == item.expected_output

    # 점수 기록
    trace.score(
        name="correctness",
        value=1.0 if is_correct else 0.0
    )
```

### 활용 시나리오

1. **모델 평가**: 새 모델 또는 버전 평가
2. **회귀 테스트**: 업데이트 후 성능 확인
3. **벤치마킹**: 여러 모델 성능 비교
4. **품질 게이트**: 배포 전 최소 기준 확인

### 실행 명령

```bash
python 06_datasets.py
```

---

## 7. Langchain 통합

### 개념 이해

**CallbackHandler**를 사용하여 Langchain의 모든 작업을 자동으로 Langfuse에 추적합니다.

### 기본 설정

```python
from langfuse.callback import CallbackHandler

# 콜백 핸들러 생성
handler = CallbackHandler()

# Trace 메타데이터 설정
handler.trace(
    name="my_chain",
    user_id="user_123",
    metadata={"framework": "langchain"}
)
```

### Langchain과 함께 사용

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 콜백 핸들러 전달
response = llm.invoke(
    "Hello!",
    config={"callbacks": [handler]}
)
```

### Chain 추적

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="Translate {text} to {language}",
    input_variables=["text", "language"]
)

chain = LLMChain(llm=llm, prompt=prompt)

result = chain.invoke(
    {"text": "Hello", "language": "French"},
    config={"callbacks": [handler]}
)
```

### RAG 파이프라인 추적

```python
# 1. 문서 검색
retriever = vectorstore.as_retriever()
docs = retriever.get_relevant_documents(
    query,
    callbacks=[handler]
)

# 2. 컨텍스트 생성
context = "\n".join([doc.page_content for doc in docs])

# 3. LLM으로 답변 생성
response = llm.invoke(
    f"Answer based on context: {context}\nQuestion: {query}",
    config={"callbacks": [handler]}
)
```

### 자동 추적되는 정보

- LLM 호출 (입력, 출력, 토큰)
- Chain 실행 (각 단계)
- Tool 사용
- 문서 검색
- 실행 시간
- 에러

### 실행 명령

```bash
python 07_langchain_integration.py
```

---

## 8. Agent 구현

### 개념 이해

**Agent**는 도구를 사용하여 복잡한 작업을 자율적으로 수행하는 시스템입니다.

**ReAct 패턴**:
1. **Thought**: 무엇을 해야 하는지 생각
2. **Action**: 도구 선택 및 실행
3. **Observation**: 결과 확인
4. **Repeat**: 필요시 반복
5. **Answer**: 최종 답변

### 커스텀 도구 정의

```python
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """수학 계산을 수행합니다."""
    try:
        result = eval(expression)
        return f"계산 결과: {result}"
    except Exception as e:
        return f"계산 오류: {str(e)}"

@tool
def search(query: str) -> str:
    """정보를 검색합니다."""
    # 검색 로직
    return search_results
```

### Agent 실행 예제

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Trace 생성
trace = langfuse.trace(
    name="agent_execution",
    metadata={"agent_type": "react"}
)

# Step 1: Thought
thought = "사용자가 계산을 요청했습니다."
thought_span = trace.span(name="thought_1")
thought_span.end(output=thought)

# Step 2: Action
action_span = trace.span(name="action_1")
result = calculator.func("10 + 5")
action_span.end(
    input="10 + 5",
    output=result
)

# Step 3: Final Answer
answer_span = trace.span(name="final_answer")
answer = f"The result is {result}"
answer_span.end(output=answer)

trace.end()
```

### 다단계 Agent

```python
# 복잡한 쿼리: "날씨를 확인하고 메모로 저장"

# Iteration 1: 날씨 확인
trace.span(name="step_1_weather")
weather = get_weather("Seoul")

# Iteration 2: 메모 저장
trace.span(name="step_2_save")
save_note(f"Weather: {weather}")

# Final Answer
answer = "I checked the weather and saved it to your notes."
```

### 에러 처리

```python
try:
    result = tool.func(input)
    span.end(output=result)
except Exception as e:
    span.end(
        level="ERROR",
        status_message=str(e)
    )
    # 복구 로직
    recovery_span = trace.span(name="error_recovery")
    # ...
```

### Agent 성능 최적화

1. **도구 선택 최적화**: 필요한 도구만 제공
2. **컨텍스트 관리**: 대화 히스토리 적절히 관리
3. **조기 종료**: 답변을 찾으면 즉시 종료
4. **병렬 실행**: 독립적인 도구는 병렬로 실행

### 실행 명령

```bash
python 08_agent_with_langfuse.py
```

---

## 대시보드 활용

### Traces 페이지

- 모든 실행 기록 조회
- 필터링 및 검색
- 상세 정보 드릴다운

### Sessions 페이지

- 세션별 그룹화
- 사용자별 분석
- 시간별 패턴

### Scores 페이지

- 점수 분포
- 시간에 따른 추이
- 모델별 비교

### Analytics 페이지

- 비용 분석
- 레이턴시 모니터링
- 토큰 사용량

---

## 실전 활용 팁

### 1. 개발 vs 프로덕션

```python
import os

environment = os.getenv("ENVIRONMENT", "development")

trace = langfuse.trace(
    name="my_app",
    tags=[environment],
    metadata={"env": environment}
)
```

### 2. 비용 모니터링

```python
# 일일 비용 추적
daily_cost = sum([
    generation.usage.total_cost
    for generation in langfuse.get_generations(
        from_timestamp=today_start
    )
])

if daily_cost > DAILY_BUDGET:
    send_alert("Daily budget exceeded")
```

### 3. 품질 알림

```python
# 품질 점수가 낮을 때 알림
if score < QUALITY_THRESHOLD:
    trace.score(
        name="quality_alert",
        value=score,
        comment="Quality below threshold"
    )
    notify_team()
```

### 4. A/B 테스트 자동화

```python
import random

variant = "A" if random.random() < 0.5 else "B"

trace = langfuse.trace(
    metadata={"variant": variant}
)

if variant == "A":
    prompt = prompt_version_a
else:
    prompt = prompt_version_b
```

---

## 문제 해결

### 데이터가 대시보드에 나타나지 않음

```python
# flush() 호출 확인
langfuse.flush()

# 또는 컨텍스트 매니저 사용
with langfuse:
    # 작업 수행
    pass  # 자동으로 flush됨
```

### 성능 최적화

```python
# 배치 처리 사용
langfuse.batch_size = 50  # 기본값: 15

# 비동기 전송
langfuse.enabled = True
langfuse.background_flush = True
```

---

## 다음 단계

1. 예제 파일을 순서대로 실행해보세요
2. 자신의 use case에 맞게 코드를 수정해보세요
3. 대시보드에서 데이터를 탐색하세요
4. 실제 프로젝트에 통합해보세요

**Happy Learning! 🎓**
