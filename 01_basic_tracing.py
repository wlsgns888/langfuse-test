"""
Langfuse 기본 트레이싱 (Basic Tracing)

트레이싱은 LLM 애플리케이션의 실행 흐름을 추적하고 분석하는 핵심 기능입니다.
Trace는 여러 Span들로 구성되며, 각 Span은 특정 작업(LLM 호출, 데이터 처리 등)을 나타냅니다.

주요 기능:
1. Trace 생성 - 전체 실행 흐름 추적
2. Span 추가 - 세부 작업 단위 추적
3. 메타데이터 및 태그 추가
4. 실행 시간 및 비용 추적
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from langfuse import Langfuse

# 환경 변수 로드
load_dotenv()

def basic_tracing_example():
    """
    기본 트레이싱 예제

    사용 시나리오: 사용자 질문에 대한 응답 생성 과정을 추적
    """
    print("=" * 60)
    print("1. 기본 Trace 생성")
    print("=" * 60)

    # Langfuse 클라이언트 초기화
    langfuse = Langfuse()

    # Trace 생성 - 전체 실행 흐름의 시작점
    trace = langfuse.trace(
        name="question_answering",
        user_id="user_123",
        metadata={
            "environment": "development",
            "version": "1.0.0"
        },
        tags=["qa", "test"]
    )

    print(f"✓ Trace 생성됨: {trace.id}")
    print(f"  - Name: question_answering")
    print(f"  - User ID: user_123")
    print(f"  - Tags: qa, test")

    return trace, langfuse


def add_spans_example(trace):
    """
    Span 추가 예제

    Span은 Trace 내의 세부 작업을 나타냅니다.
    예: 데이터 전처리, LLM 호출, 후처리 등
    """
    print("\n" + "=" * 60)
    print("2. Span 추가 - 작업 단위 추적")
    print("=" * 60)

    # Span 1: 데이터 전처리
    preprocessing_span = trace.span(
        name="preprocessing",
        metadata={"step": "1"}
    )

    # 실제 작업 시뮬레이션
    user_question = "What is the capital of France?"
    processed_question = user_question.strip().lower()

    preprocessing_span.end(
        output={"processed_question": processed_question}
    )

    print(f"✓ Preprocessing Span 완료")
    print(f"  - Input: {user_question}")
    print(f"  - Output: {processed_question}")

    # Span 2: LLM 호출 시뮬레이션
    llm_span = trace.span(
        name="llm_call",
        metadata={
            "step": "2",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7
        }
    )

    # LLM 응답 시뮬레이션
    llm_response = "The capital of France is Paris."

    llm_span.end(
        input={"question": processed_question},
        output={"answer": llm_response},
        metadata={
            "tokens_used": 25,
            "cost": 0.001
        }
    )

    print(f"\n✓ LLM Call Span 완료")
    print(f"  - Model: gpt-3.5-turbo")
    print(f"  - Tokens: 25")
    print(f"  - Cost: $0.001")
    print(f"  - Response: {llm_response}")

    # Span 3: 후처리
    postprocessing_span = trace.span(
        name="postprocessing",
        metadata={"step": "3"}
    )

    final_response = {
        "answer": llm_response,
        "confidence": 0.95,
        "timestamp": datetime.now().isoformat()
    }

    postprocessing_span.end(
        output=final_response
    )

    print(f"\n✓ Postprocessing Span 완료")
    print(f"  - Confidence: 0.95")
    print(f"  - Final Response: {final_response['answer']}")

    return final_response


def nested_spans_example(trace):
    """
    중첩 Span 예제

    복잡한 작업은 여러 레벨의 Span으로 구성할 수 있습니다.
    """
    print("\n" + "=" * 60)
    print("3. 중첩 Span - 계층적 작업 추적")
    print("=" * 60)

    # 부모 Span
    parent_span = trace.span(
        name="complex_operation",
        metadata={"type": "parent"}
    )

    print(f"✓ 부모 Span 시작: complex_operation")

    # 자식 Span 1
    child_span_1 = parent_span.span(
        name="sub_operation_1",
        metadata={"type": "child", "order": 1}
    )

    result_1 = "Result from sub-operation 1"
    child_span_1.end(output={"result": result_1})

    print(f"  ├─ 자식 Span 1 완료: {result_1}")

    # 자식 Span 2
    child_span_2 = parent_span.span(
        name="sub_operation_2",
        metadata={"type": "child", "order": 2}
    )

    result_2 = "Result from sub-operation 2"
    child_span_2.end(output={"result": result_2})

    print(f"  └─ 자식 Span 2 완료: {result_2}")

    # 부모 Span 종료
    parent_span.end(
        output={
            "combined_results": [result_1, result_2]
        }
    )

    print(f"✓ 부모 Span 완료: 모든 하위 작업 완료")


def trace_with_error_example(langfuse):
    """
    에러 처리가 포함된 Trace 예제

    실패한 작업도 추적하여 디버깅과 모니터링에 활용
    """
    print("\n" + "=" * 60)
    print("4. 에러 추적")
    print("=" * 60)

    trace = langfuse.trace(
        name="operation_with_error",
        metadata={"test": "error_handling"}
    )

    try:
        span = trace.span(name="risky_operation")

        # 에러 시뮬레이션
        raise ValueError("Simulated error for testing")

    except Exception as e:
        # 에러 정보를 Span에 기록
        span.end(
            level="ERROR",
            status_message=str(e),
            metadata={
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        )

        print(f"✓ 에러가 추적됨")
        print(f"  - Error Type: {type(e).__name__}")
        print(f"  - Error Message: {str(e)}")
        print(f"  - Status: ERROR")

    trace.end()


def main():
    """메인 실행 함수"""
    print("\n" + "=" * 60)
    print("LANGFUSE 기본 트레이싱 예제")
    print("=" * 60)

    try:
        # 1. 기본 Trace 생성
        trace, langfuse = basic_tracing_example()

        # 2. Span 추가
        add_spans_example(trace)

        # 3. 중첩 Span
        nested_spans_example(trace)

        # Trace 종료
        trace.end()

        # 4. 에러 처리 예제
        trace_with_error_example(langfuse)

        # 데이터 전송 완료 대기
        langfuse.flush()

        print("\n" + "=" * 60)
        print("✓ 모든 트레이싱 데이터가 Langfuse로 전송되었습니다!")
        print("=" * 60)
        print(f"\nLangfuse 대시보드에서 확인하세요:")
        print(f"{os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        print("환경 변수(.env)를 확인하세요:")
        print("  - LANGFUSE_PUBLIC_KEY")
        print("  - LANGFUSE_SECRET_KEY")
        print("  - LANGFUSE_HOST")


if __name__ == "__main__":
    main()
