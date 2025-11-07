"""
모든 Langfuse 예제를 순차적으로 실행하는 스크립트

이 스크립트는 다음 예제들을 순서대로 실행합니다:
1. 기본 트레이싱
2. Generations
3. Sessions
4. Scoring
5. Prompts
6. Datasets
7. Langchain 통합
8. Agent 구현
"""

import os
import sys
import time
import subprocess
from datetime import datetime


def print_banner(text, char="="):
    """배너 출력"""
    width = 70
    print("\n" + char * width)
    print(text.center(width))
    print(char * width + "\n")


def run_example(file_name, description):
    """개별 예제 실행"""
    print_banner(f"실행 중: {description}", "─")
    print(f"파일: {file_name}")
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    start_time = time.time()

    try:
        # 예제 실행
        result = subprocess.run(
            [sys.executable, file_name],
            capture_output=False,
            text=True,
            check=True
        )

        elapsed_time = time.time() - start_time

        print()
        print("─" * 70)
        print(f"✅ 완료: {description}")
        print(f"실행 시간: {elapsed_time:.2f}초")
        print("─" * 70)

        return True, elapsed_time

    except subprocess.CalledProcessError as e:
        elapsed_time = time.time() - start_time

        print()
        print("─" * 70)
        print(f"❌ 실패: {description}")
        print(f"오류: {str(e)}")
        print(f"실행 시간: {elapsed_time:.2f}초")
        print("─" * 70)

        return False, elapsed_time

    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
        sys.exit(1)


def check_environment():
    """환경 설정 확인"""
    print_banner("환경 설정 확인", "=")

    required_vars = [
        "LANGFUSE_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY",
        "LANGFUSE_HOST"
    ]

    missing_vars = []

    for var in required_vars:
        value = os.getenv(var)
        if value:
            # 키는 마스킹하여 표시
            if "KEY" in var:
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"✓ {var}: {masked_value}")
            else:
                print(f"✓ {var}: {value}")
        else:
            print(f"✗ {var}: 설정되지 않음")
            missing_vars.append(var)

    print()

    if missing_vars:
        print("⚠️  경고: 다음 환경 변수가 설정되지 않았습니다:")
        for var in missing_vars:
            print(f"   - {var}")
        print()
        print("계속하시겠습니까? (y/n): ", end="")
        response = input().strip().lower()

        if response != "y":
            print("실행이 취소되었습니다.")
            sys.exit(0)

    print()


def main():
    """메인 실행 함수"""
    print_banner("LANGFUSE 예제 전체 실행", "=")
    print("이 스크립트는 모든 Langfuse 예제를 순차적으로 실행합니다.")
    print()

    # 환경 확인
    check_environment()

    # 실행할 예제 목록
    examples = [
        {
            "file": "01_basic_tracing.py",
            "description": "기본 트레이싱 (Basic Tracing)"
        },
        {
            "file": "02_generations.py",
            "description": "Generations (생성 추적)"
        },
        {
            "file": "03_sessions.py",
            "description": "Sessions (세션 관리)"
        },
        {
            "file": "04_scoring.py",
            "description": "Scoring (점수 매기기)"
        },
        {
            "file": "05_prompts.py",
            "description": "Prompts (프롬프트 관리)"
        },
        {
            "file": "06_datasets.py",
            "description": "Datasets (데이터셋 관리)"
        },
        {
            "file": "07_langchain_integration.py",
            "description": "Langchain 통합"
        },
        {
            "file": "08_agent_with_langfuse.py",
            "description": "Agent 구현"
        }
    ]

    print(f"총 {len(examples)}개의 예제를 실행합니다.\n")
    print("시작하시겠습니까? (y/n): ", end="")
    response = input().strip().lower()

    if response != "y":
        print("실행이 취소되었습니다.")
        sys.exit(0)

    # 실행 결과 추적
    results = []
    total_start_time = time.time()

    # 각 예제 실행
    for i, example in enumerate(examples, 1):
        print()
        print("=" * 70)
        print(f"진행: {i}/{len(examples)}")
        print("=" * 70)

        # 파일 존재 확인
        if not os.path.exists(example["file"]):
            print(f"❌ 파일을 찾을 수 없습니다: {example['file']}")
            results.append({
                "file": example["file"],
                "description": example["description"],
                "success": False,
                "time": 0
            })
            continue

        # 예제 실행
        success, elapsed_time = run_example(
            example["file"],
            example["description"]
        )

        results.append({
            "file": example["file"],
            "description": example["description"],
            "success": success,
            "time": elapsed_time
        })

        # 다음 예제로 넘어가기 전 잠시 대기
        if i < len(examples):
            print("\n다음 예제로 넘어갑니다...")
            time.sleep(2)

    # 전체 실행 시간
    total_elapsed_time = time.time() - total_start_time

    # 결과 요약
    print_banner("실행 결과 요약", "=")

    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful

    print(f"총 실행: {len(results)}개")
    print(f"성공: {successful}개")
    print(f"실패: {failed}개")
    print(f"총 실행 시간: {total_elapsed_time:.2f}초")
    print()

    # 상세 결과
    print("상세 결과:")
    print("─" * 70)

    for i, result in enumerate(results, 1):
        status = "✅" if result["success"] else "❌"
        print(f"{i}. {status} {result['description']}")
        print(f"   파일: {result['file']}")
        print(f"   시간: {result['time']:.2f}초")
        print()

    # 실패한 예제가 있는 경우
    if failed > 0:
        print("\n⚠️  일부 예제가 실패했습니다.")
        print("실패한 예제:")
        for result in results:
            if not result["success"]:
                print(f"  - {result['description']} ({result['file']})")
        print()
        print("실패 원인:")
        print("  1. 환경 변수(.env)가 올바르게 설정되지 않음")
        print("  2. 필요한 패키지가 설치되지 않음")
        print("  3. Langfuse 서버에 연결할 수 없음")
        print()
        print("해결 방법:")
        print("  1. .env 파일 확인")
        print("  2. pip install -r requirements.txt 실행")
        print("  3. 인터넷 연결 확인")

    else:
        print("\n🎉 모든 예제가 성공적으로 실행되었습니다!")
        print()
        print("다음 단계:")
        print(f"  1. Langfuse 대시보드 확인: {os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
        print("  2. 각 예제의 trace, session, score 확인")
        print("  3. 자신의 use case에 맞게 코드 수정")
        print("  4. USAGE_GUIDE.md 참조")

    print()
    print_banner("실행 완료", "=")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램이 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 예상치 못한 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
