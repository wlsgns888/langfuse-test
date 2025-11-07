# Langfuse 테스트 환경

Langfuse 최신 버전의 모든 주요 기능을 실제로 사용하고 테스트할 수 있는 완전한 예제 모음입니다.

## 📋 목차

- [개요](#개요)
- [설치](#설치)
- [환경 설정](#환경-설정)
- [예제 파일 구조](#예제-파일-구조)
- [실행 방법](#실행-방법)
- [주요 기능](#주요-기능)
- [Langchain 통합](#langchain-통합)
- [Agent 구현](#agent-구현)

> 💡 **빠른 시작을 원하시나요?** [QUICK_START.md](QUICK_START.md)를 참조하세요!

## 🎯 개요

이 프로젝트는 Langfuse의 모든 주요 기능을 실제로 활용하는 예제를 제공합니다. 각 예제는 실용적인 사용 사례를 보여주며, 상세한 설명과 함께 제공됩니다.

**주요 특징:**
- ✅ Langfuse 최신 버전 (2.54.4+) 사용
- ✅ Langchain 1.0.4 통합
- ✅ 8개의 실전 예제 파일
- ✅ 각 기능별 상세한 설명 포함
- ✅ Agent 구현 예제 포함
- ✅ 실행 가능한 코드

## 🌿 브랜치 정보

- **메인 브랜치**: `claude/main-011CUt9bDg2NYeMmKh2DumZH` - 안정적인 메인 개발 브랜치
- **기능 브랜치**: `claude/langfuse-feature-testing-011CUt9bDg2NYeMmKh2DumZH` - 초기 개발 브랜치

메인 브랜치를 클론하여 사용하세요:
```bash
git clone -b claude/main-011CUt9bDg2NYeMmKh2DumZH <repository-url>
```

## 🚀 설치

### 방법 1: uv 사용 (권장 ⚡ 빠름!)

[uv](https://github.com/astral-sh/uv)는 Rust로 작성된 초고속 Python 패키지 관리자입니다.

```bash
# 1. 저장소 클론
git clone <repository-url>
cd langfuse-test

# 2. uv 설치 (아직 설치하지 않은 경우)
curl -LsSf https://astral.sh/uv/install.sh | sh
# 또는 Mac: brew install uv
# 또는 Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 3. 가상환경 생성
uv venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate  # Windows

# 4. 패키지 설치 (방법 1: pyproject.toml 사용)
uv pip install .

# 또는 (방법 2: requirements.txt 사용)
uv pip install -r requirements.txt
```

### 방법 2: pip 사용 (기존 방식)

```bash
# 1. 저장소 클론
git clone <repository-url>
cd langfuse-test

# 2. 가상 환경 생성
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 3. 패키지 설치
pip install -r requirements.txt
```

### 설치되는 패키지:
- `langfuse>=2.54.4` - Langfuse 클라이언트
- `langchain==1.0.4` - Langchain 프레임워크
- `langchain-openai>=0.2.11` - OpenAI 통합
- `langchain-community>=0.3.13` - 커뮤니티 통합
- `openai>=1.58.1` - OpenAI API
- `python-dotenv>=1.0.0` - 환경 변수 관리

### uv를 사용하는 이유

- ⚡ **10-100배 빠른 속도**: pip보다 훨씬 빠른 패키지 설치
- 🔒 **안정적인 의존성**: 자동 의존성 해결
- 🎯 **간편한 사용**: pip과 호환되는 인터페이스
- 💾 **효율적인 캐싱**: 디스크 공간 절약

## ⚙️ 환경 설정

### 1. 환경 변수 파일 생성

`.env.example` 파일을 `.env`로 복사:

```bash
cp .env.example .env
```

### 2. 환경 변수 설정

`.env` 파일을 편집하여 다음 값들을 설정:

```env
# Langfuse 설정
LANGFUSE_PUBLIC_KEY=your_public_key_here
LANGFUSE_SECRET_KEY=your_secret_key_here
LANGFUSE_HOST=https://cloud.langfuse.com

# OpenAI 설정 (선택사항 - 실제 LLM 사용 시)
OPENAI_API_KEY=your_openai_api_key_here
```

### Langfuse 키 발급 방법:

1. [Langfuse Cloud](https://cloud.langfuse.com) 또는 자체 호스팅 인스턴스에 접속
2. 프로젝트 생성 또는 선택
3. Settings → API Keys에서 새 키 생성
4. Public Key와 Secret Key를 `.env`에 복사

## 📁 예제 파일 구조

```
langfuse-test/
├── pyproject.toml               # 프로젝트 설정 (uv용)
├── requirements.txt              # 패키지 의존성 (pip용)
├── .python-version              # Python 버전 지정
├── .env.example                  # 환경 변수 예제
├── README.md                     # 이 파일
├── USAGE_GUIDE.md               # 상세 사용 가이드
├── run_all_examples.py          # 모든 예제 실행 스크립트
│
├── 01_basic_tracing.py          # 기본 트레이싱
├── 02_generations.py            # Generation 추적
├── 03_sessions.py               # 세션 관리
├── 04_scoring.py                # 점수 매기기
├── 05_prompts.py                # 프롬프트 관리
├── 06_datasets.py               # 데이터셋 관리
├── 07_langchain_integration.py  # Langchain 통합
└── 08_agent_with_langfuse.py   # Agent 구현
```

## 🏃 실행 방법

### 개별 예제 실행

각 예제를 독립적으로 실행할 수 있습니다:

```bash
# 1. 기본 트레이싱
python 01_basic_tracing.py

# 2. Generation 추적
python 02_generations.py

# 3. 세션 관리
python 03_sessions.py

# 4. 점수 매기기
python 04_scoring.py

# 5. 프롬프트 관리
python 05_prompts.py

# 6. 데이터셋 관리
python 06_datasets.py

# 7. Langchain 통합
python 07_langchain_integration.py

# 8. Agent 구현
python 08_agent_with_langfuse.py
```

### 모든 예제 순차 실행

```bash
python run_all_examples.py
```

## 🎨 주요 기능

### 1. 기본 트레이싱 (`01_basic_tracing.py`)

**무엇을 배울 수 있나요?**
- Trace와 Span의 개념
- 계층적 작업 추적
- 메타데이터 및 태그 추가
- 에러 추적 및 처리

**주요 예제:**
- 기본 Trace 생성
- Span 추가 및 중첩
- 에러 상황 추적

### 2. Generations (`02_generations.py`)

**무엇을 배울 수 있나요?**
- LLM 호출 추적
- 토큰 사용량 및 비용 계산
- 대화형 Generation
- 스트리밍 응답 추적
- 모델 간 비교

**주요 예제:**
- 단일 LLM 호출
- 다중 턴 대화
- 스트리밍 Generation
- 비용 추적
- 모델 비교

### 3. Sessions (`03_sessions.py`)

**무엇을 배울 수 있나요?**
- 세션을 통한 Trace 그룹화
- 사용자 여정 추적
- 장기 대화 관리
- 세션 메타데이터 활용

**주요 예제:**
- 고객 지원 세션
- 다중 사용자 추적
- 긴 대화 세션
- 세션 분석

### 4. Scoring (`04_scoring.py`)

**무엇을 배울 수 있나요?**
- LLM 출력 품질 평가
- 사용자 피드백 수집
- 자동화된 메트릭
- A/B 테스트
- 커스텀 점수 카테고리

**주요 예제:**
- 기본 점수 매기기
- 사용자 피드백 (좋아요/싫어요, 별점)
- 자동화된 품질 평가
- 모델 A/B 테스트
- 임계값 기반 알림

### 5. Prompts (`05_prompts.py`)

**무엇을 배울 수 있나요?**
- 프롬프트 중앙 관리
- 버전 관리 및 롤백
- 프롬프트 변수 활용
- A/B 테스트
- 폴백 전략

**주요 예제:**
- 프롬프트 템플릿 사용
- 버전별 비교
- 채팅 템플릿
- 실험 및 A/B 테스트
- 자동 폴백

### 6. Datasets (`06_datasets.py`)

**무엇을 배울 수 있나요?**
- 테스트 데이터셋 생성
- 모델 평가 자동화
- 회귀 테스트
- 벤치마킹
- 정답 데이터셋 활용

**주요 예제:**
- 데이터셋 생성
- 자동 평가 실행
- 모델 비교
- 회귀 테스트
- 벤치마크

### 7. Langchain 통합 (`07_langchain_integration.py`)

**무엇을 배울 수 있나요?**
- CallbackHandler 사용법
- Chain 추적
- RAG 파이프라인 추적
- 대화형 Chain
- 배치 처리

**주요 예제:**
- 기본 LLM 호출
- Sequential Chain
- 대화 메모리
- RAG (Retrieval Augmented Generation)
- 에러 처리

### 8. Agent 구현 (`08_agent_with_langfuse.py`)

**무엇을 배울 수 있나요?**
- ReAct 스타일 Agent 구현
- 커스텀 도구 정의
- Agent 사고 과정 추적
- 다단계 추론
- 에러 처리 및 복구

**주요 예제:**
- 기본 Agent
- 다단계 Agent
- 에러 처리 Agent
- 다중 도구 사용
- 대화 기억 Agent
- 성능 비교

## 🔗 Langchain 통합

### CallbackHandler 사용법

```python
from langfuse.callback import CallbackHandler

# 콜백 핸들러 생성
handler = CallbackHandler()

# Trace 메타데이터 설정
handler.trace(
    name="my_application",
    user_id="user_123",
    metadata={"version": "1.0"}
)

# Langchain과 함께 사용
# llm.invoke(prompt, config={"callbacks": [handler]})
```

### 자동 추적되는 정보

- 모든 LLM 호출
- Chain 실행
- Tool 사용
- 토큰 사용량
- 실행 시간
- 에러 및 예외

## 🤖 Agent 구현

### 커스텀 도구 정의

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(input: str) -> str:
    """도구 설명"""
    # 도구 로직
    return result
```

### Agent 사고 과정

Agent는 다음 단계를 반복합니다:

1. **Thought**: 무엇을 해야 하는지 생각
2. **Action**: 도구를 선택하고 실행
3. **Observation**: 도구 실행 결과 확인
4. **Answer**: 최종 답변 생성

모든 단계가 Langfuse에 자동으로 추적됩니다.

## 📊 대시보드에서 확인하기

모든 예제 실행 후 Langfuse 대시보드에서 다음을 확인할 수 있습니다:

1. **Traces**: 모든 실행 기록
2. **Sessions**: 세션별 그룹화된 trace
3. **Scores**: 점수 및 피드백 분포
4. **Prompts**: 프롬프트 버전 관리
5. **Datasets**: 평가 결과
6. **Analytics**: 비용, 레이턴시, 품질 메트릭

## 🔍 문제 해결

### 환경 변수 오류

```
오류: LANGFUSE_PUBLIC_KEY not found
해결: .env 파일을 생성하고 올바른 키를 설정하세요
```

### 패키지 설치 오류

```
오류: No module named 'langfuse'
해결: pip install -r requirements.txt 실행
```

### API 연결 오류

```
오류: Connection refused
해결: LANGFUSE_HOST 값을 확인하세요
       - Cloud: https://cloud.langfuse.com
       - Self-hosted: http://localhost:3000
```

## 📚 추가 리소스

- [Langfuse 공식 문서](https://langfuse.com/docs)
- [Langchain 공식 문서](https://python.langchain.com/)
- [Langfuse GitHub](https://github.com/langfuse/langfuse)
- [Langchain GitHub](https://github.com/langchain-ai/langchain)

## 🤝 기여

개선 사항이나 버그를 발견하셨나요? 이슈를 열거나 PR을 보내주세요!

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 💡 팁

1. **시작하기**: `01_basic_tracing.py`부터 순서대로 실행해보세요
2. **실험하기**: 각 예제의 파라미터를 변경하며 테스트해보세요
3. **대시보드 활용**: 실행 후 즉시 대시보드에서 결과를 확인하세요
4. **커스터마이징**: 자신의 use case에 맞게 코드를 수정해보세요
5. **Agent 활용**: Agent 예제를 기반으로 복잡한 작업을 자동화하세요

---

**Happy Testing! 🚀**
