"""
Langfuse Sessions (세션 관리)

Session은 관련된 여러 trace들을 그룹화합니다.
예: 사용자와의 전체 대화, 특정 작업의 여러 시도, 사용자 여정 추적

주요 기능:
1. 대화 세션 추적
2. 사용자 여정 분석
3. 세션별 메트릭 집계
4. 장기 상호작용 패턴 파악
"""

import os
import time
from datetime import datetime
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()


def simple_session_example():
    """
    기본 세션 추적 예제

    단일 세션 내에서 여러 trace를 그룹화합니다.
    """
    print("=" * 60)
    print("1. 기본 세션 추적")
    print("=" * 60)

    langfuse = Langfuse()

    session_id = "session_customer_support_001"
    user_id = "customer_12345"

    print(f"세션 시작")
    print(f"  - Session ID: {session_id}")
    print(f"  - User ID: {user_id}")
    print()

    # 첫 번째 상호작용: 인사
    print("[Interaction 1] 인사")
    trace1 = langfuse.trace(
        name="greeting",
        session_id=session_id,
        user_id=user_id,
        metadata={
            "interaction_number": 1,
            "type": "greeting"
        }
    )

    generation1 = trace1.generation(
        name="greeting_response",
        model="gpt-3.5-turbo",
        input="Hello, I need help with my account"
    )

    response1 = "Hello! I'd be happy to help you with your account. What seems to be the issue?"
    generation1.end(output=response1)
    trace1.end()

    print(f"  User: Hello, I need help with my account")
    print(f"  Bot: {response1}")

    time.sleep(0.5)

    # 두 번째 상호작용: 문제 설명
    print("\n[Interaction 2] 문제 설명")
    trace2 = langfuse.trace(
        name="problem_description",
        session_id=session_id,
        user_id=user_id,
        metadata={
            "interaction_number": 2,
            "type": "problem_identification"
        }
    )

    generation2 = trace2.generation(
        name="problem_analysis",
        model="gpt-3.5-turbo",
        input="I can't login to my account"
    )

    response2 = "I understand. Let me help you troubleshoot the login issue. Have you tried resetting your password?"
    generation2.end(output=response2)
    trace2.end()

    print(f"  User: I can't login to my account")
    print(f"  Bot: {response2}")

    time.sleep(0.5)

    # 세 번째 상호작용: 해결책 제공
    print("\n[Interaction 3] 해결책 제공")
    trace3 = langfuse.trace(
        name="solution_provided",
        session_id=session_id,
        user_id=user_id,
        metadata={
            "interaction_number": 3,
            "type": "resolution"
        }
    )

    generation3 = trace3.generation(
        name="solution_generation",
        model="gpt-3.5-turbo",
        input="Yes, but I didn't receive the reset email"
    )

    response3 = "Let me send another password reset email. Please check your spam folder as well. The email should arrive within 5 minutes."
    generation3.end(output=response3)
    trace3.end()

    print(f"  User: Yes, but I didn't receive the reset email")
    print(f"  Bot: {response3}")

    print(f"\n✓ 세션 완료: 3개의 상호작용 추적됨")

    langfuse.flush()
    return session_id


def multi_user_session_example():
    """
    다중 사용자 세션 예제

    여러 사용자의 세션을 동시에 추적합니다.
    """
    print("\n" + "=" * 60)
    print("2. 다중 사용자 세션 추적")
    print("=" * 60)

    langfuse = Langfuse()

    users = [
        {"user_id": "user_001", "name": "Alice", "query": "Product recommendation"},
        {"user_id": "user_002", "name": "Bob", "query": "Technical support"},
        {"user_id": "user_003", "name": "Charlie", "query": "Billing question"}
    ]

    for user in users:
        session_id = f"session_{user['user_id']}_{datetime.now().strftime('%Y%m%d')}"

        print(f"\n{user['name']} (Session: {session_id}):")

        trace = langfuse.trace(
            name=f"user_interaction_{user['name']}",
            session_id=session_id,
            user_id=user['user_id'],
            metadata={
                "user_name": user['name'],
                "query_type": user['query']
            }
        )

        generation = trace.generation(
            name="response_generation",
            model="gpt-3.5-turbo",
            input=user['query']
        )

        response = f"I'll help you with {user['query'].lower()}. Let me gather the information."
        generation.end(output=response)

        trace.end()

        print(f"  Query: {user['query']}")
        print(f"  Response: {response}")

    print(f"\n✓ {len(users)}명의 사용자 세션 추적 완료")

    langfuse.flush()


def long_conversation_session_example():
    """
    긴 대화 세션 예제

    여러 턴으로 구성된 긴 대화를 추적합니다.
    """
    print("\n" + "=" * 60)
    print("3. 긴 대화 세션 추적")
    print("=" * 60)

    langfuse = Langfuse()

    session_id = "session_long_conversation_001"
    user_id = "user_researcher"

    conversation = [
        {
            "turn": 1,
            "user": "What is quantum entanglement?",
            "assistant": "Quantum entanglement is a phenomenon where particles become correlated in such a way that the state of one particle instantly influences the state of another, regardless of distance."
        },
        {
            "turn": 2,
            "user": "How is this different from classical correlation?",
            "assistant": "In classical correlation, particles have predetermined states. In quantum entanglement, particles exist in superposition until measured, and measurement of one immediately affects the other."
        },
        {
            "turn": 3,
            "user": "Can this be used for communication?",
            "assistant": "No, entanglement cannot be used for faster-than-light communication because the measurement results are random. However, it's useful for quantum cryptography and quantum computing."
        },
        {
            "turn": 4,
            "user": "What are some practical applications?",
            "assistant": "Practical applications include quantum key distribution for secure communication, quantum teleportation, and improving quantum computer performance."
        },
        {
            "turn": 5,
            "user": "Thank you for the explanation!",
            "assistant": "You're welcome! Feel free to ask if you have more questions about quantum physics."
        }
    ]

    print(f"세션: {session_id}")
    print(f"사용자: {user_id}\n")

    total_tokens = 0

    for turn_data in conversation:
        trace = langfuse.trace(
            name=f"conversation_turn_{turn_data['turn']}",
            session_id=session_id,
            user_id=user_id,
            metadata={
                "turn_number": turn_data['turn'],
                "total_turns": len(conversation)
            }
        )

        generation = trace.generation(
            name=f"turn_{turn_data['turn']}_generation",
            model="gpt-3.5-turbo",
            input=turn_data['user']
        )

        # 토큰 수 시뮬레이션
        prompt_tokens = len(turn_data['user'].split()) * 1.3
        completion_tokens = len(turn_data['assistant'].split()) * 1.3
        tokens = int(prompt_tokens + completion_tokens)
        total_tokens += tokens

        generation.end(
            output=turn_data['assistant'],
            usage={
                "prompt_tokens": int(prompt_tokens),
                "completion_tokens": int(completion_tokens),
                "total_tokens": tokens
            }
        )

        trace.end()

        print(f"[Turn {turn_data['turn']}]")
        print(f"  User: {turn_data['user']}")
        print(f"  Assistant: {turn_data['assistant'][:80]}...")
        print(f"  Tokens: {tokens}")
        print()

    print(f"✓ 세션 완료")
    print(f"  - 총 턴 수: {len(conversation)}")
    print(f"  - 총 토큰: {total_tokens}")

    langfuse.flush()


def session_with_metadata_example():
    """
    메타데이터가 풍부한 세션 예제

    세션에 다양한 컨텍스트 정보를 추가합니다.
    """
    print("\n" + "=" * 60)
    print("4. 메타데이터 활용 세션")
    print("=" * 60)

    langfuse = Langfuse()

    session_id = "session_premium_user_001"
    user_id = "premium_user_789"

    # 세션 시작 시간
    session_start = datetime.now()

    session_metadata = {
        "user_tier": "premium",
        "session_start": session_start.isoformat(),
        "device": "mobile",
        "platform": "iOS",
        "app_version": "2.5.1",
        "location": "US-East",
        "language": "en-US"
    }

    print(f"세션 메타데이터:")
    for key, value in session_metadata.items():
        print(f"  - {key}: {value}")
    print()

    # 세션 내 여러 작업
    tasks = [
        {"name": "document_analysis", "description": "PDF 분석 요청"},
        {"name": "data_extraction", "description": "데이터 추출"},
        {"name": "summary_generation", "description": "요약 생성"}
    ]

    for i, task in enumerate(tasks, 1):
        trace = langfuse.trace(
            name=task['name'],
            session_id=session_id,
            user_id=user_id,
            metadata={
                **session_metadata,
                "task_number": i,
                "task_type": task['name'],
                "task_description": task['description']
            }
        )

        generation = trace.generation(
            name=f"{task['name']}_generation",
            model="gpt-3.5-turbo",
            input=task['description']
        )

        generation.end(
            output=f"Completed: {task['description']}",
            metadata={
                "processing_time_ms": 1500 + (i * 200)
            }
        )

        trace.end()

        print(f"[Task {i}] {task['description']}")
        print(f"  Status: ✓ Completed")
        print(f"  Processing Time: {1500 + (i * 200)}ms")
        print()

    session_duration = (datetime.now() - session_start).total_seconds()

    print(f"✓ 세션 완료")
    print(f"  - 총 작업 수: {len(tasks)}")
    print(f"  - 세션 지속 시간: {session_duration:.2f}초")

    langfuse.flush()


def session_analytics_example():
    """
    세션 분석 예제

    세션 데이터를 분석하여 인사이트를 도출합니다.
    """
    print("\n" + "=" * 60)
    print("5. 세션 분석")
    print("=" * 60)

    langfuse = Langfuse()

    # 여러 세션 시뮬레이션
    sessions = [
        {
            "session_id": "session_analytics_001",
            "user_id": "user_analyst_1",
            "interactions": 3,
            "satisfaction": "high"
        },
        {
            "session_id": "session_analytics_002",
            "user_id": "user_analyst_2",
            "interactions": 7,
            "satisfaction": "medium"
        },
        {
            "session_id": "session_analytics_003",
            "user_id": "user_analyst_3",
            "interactions": 2,
            "satisfaction": "high"
        }
    ]

    total_interactions = 0

    for session_data in sessions:
        session_traces = []

        for i in range(session_data['interactions']):
            trace = langfuse.trace(
                name=f"interaction_{i+1}",
                session_id=session_data['session_id'],
                user_id=session_data['user_id'],
                metadata={
                    "interaction_index": i + 1,
                    "session_satisfaction": session_data['satisfaction']
                }
            )

            generation = trace.generation(
                name=f"generation_{i+1}",
                model="gpt-3.5-turbo",
                input=f"Query {i+1}"
            )

            generation.end(output=f"Response {i+1}")
            trace.end()

            session_traces.append(trace)

        total_interactions += session_data['interactions']

        print(f"Session: {session_data['session_id']}")
        print(f"  - Interactions: {session_data['interactions']}")
        print(f"  - Satisfaction: {session_data['satisfaction']}")
        print()

    print(f"✓ 분석 완료")
    print(f"  - 총 세션 수: {len(sessions)}")
    print(f"  - 총 상호작용 수: {total_interactions}")
    print(f"  - 평균 상호작용/세션: {total_interactions/len(sessions):.1f}")

    langfuse.flush()


def main():
    """메인 실행 함수"""
    print("\n" + "=" * 60)
    print("LANGFUSE SESSIONS 예제")
    print("=" * 60)

    try:
        # 1. 기본 세션
        simple_session_example()

        # 2. 다중 사용자 세션
        multi_user_session_example()

        # 3. 긴 대화 세션
        long_conversation_session_example()

        # 4. 메타데이터 활용
        session_with_metadata_example()

        # 5. 세션 분석
        session_analytics_example()

        print("\n" + "=" * 60)
        print("✓ 모든 세션 예제 완료!")
        print("=" * 60)
        print(f"\nLangfuse 대시보드에서 확인하세요:")
        print(f"{os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
        print("\n대시보드에서 다음을 확인할 수 있습니다:")
        print("  - 세션별 그룹화된 trace")
        print("  - 세션 지속 시간 및 상호작용 수")
        print("  - 사용자별 세션 패턴")

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
