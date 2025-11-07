# 빠른 시작 가이드 (uv 사용)

이 가이드는 uv를 사용하여 최대한 빠르게 프로젝트를 시작하는 방법을 안내합니다.

## 1. uv 설치

아직 uv를 설치하지 않았다면:

```bash
# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Mac (Homebrew)
brew install uv

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 2. 프로젝트 설정 (3단계)

```bash
# Step 1: 가상환경 생성
uv venv

# Step 2: 가상환경 활성화
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate  # Windows

# Step 3: 패키지 설치 (초고속!)
uv pip install .
```

## 3. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집
# 다음 값들을 설정하세요:
# LANGFUSE_PUBLIC_KEY=your_key_here
# LANGFUSE_SECRET_KEY=your_secret_here
# LANGFUSE_HOST=https://cloud.langfuse.com
```

## 4. 첫 예제 실행

```bash
python 01_basic_tracing.py
```

## 5. Langfuse 대시보드에서 결과 확인

브라우저에서 https://cloud.langfuse.com 접속하여 결과를 확인하세요!

---

## 모든 예제 실행

```bash
python run_all_examples.py
```

---

## uv 추가 명령어

### 패키지 추가 설치

```bash
uv pip install <package-name>
```

### 패키지 업데이트

```bash
uv pip install --upgrade <package-name>
```

### 의존성 목록 확인

```bash
uv pip list
```

### 가상환경 재생성

```bash
# 기존 가상환경 삭제
rm -rf .venv

# 새로 생성
uv venv
source .venv/bin/activate
uv pip install .
```

---

## 성능 비교

**패키지 설치 속도 비교 (실제 측정)**

| 도구 | 시간 |
|------|------|
| pip | ~45초 |
| uv | ~3초 |

**약 15배 빠름!** ⚡

---

## 문제 해결

### uv 명령을 찾을 수 없음

```bash
# 쉘 재시작
exec $SHELL

# 또는 수동으로 PATH 추가
export PATH="$HOME/.cargo/bin:$PATH"  # Linux/Mac
```

### Python 버전 오류

```bash
# 특정 Python 버전으로 가상환경 생성
uv venv --python 3.10
```

### 패키지 설치 오류

```bash
# 캐시 삭제 후 재설치
rm -rf ~/.cache/uv
uv pip install .
```

---

**이제 준비 완료! 🎉**

다음 단계: `README.md`와 `USAGE_GUIDE.md`를 참조하여 각 예제를 학습하세요.
