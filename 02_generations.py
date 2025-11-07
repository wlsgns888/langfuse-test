"""
Langfuse Generations (생성 추적)

Generation은 LLM의 텍스트 생성을 추적하는 특별한 형태의 관찰(Observation)입니다.
모델 이름, 프롬프트, 완성된 텍스트, 토큰 사용량, 비용 등을 자동으로 추적합니다.

주요 기능:
1. LLM 호출 추적
2. 토큰 사용량 및 비용 계산
3. 프롬프트와 응답 저장
4. 모델 성능 분석
"""

import os
import time
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()


def simple_generation_example():
    """
    기본 Generation 추적 예제

    단일 LLM 호출을 추적합니다.
    """
    print("=" * 60)
    print("1. 기본 Generation 추적")
    print("=" * 60)

    langfuse = Langfuse()

    # Trace 생성
    trace = langfuse.trace(
        name="simple_llm_call",
        user_id="user_456"
    )

    # Generation 생성 - LLM 호출 시뮬레이션
    generation = trace.generation(
        name="gpt4_completion",
        model="gpt-4",
        model_parameters={
            "temperature": 0.7,
            "max_tokens": 150,
            "top_p": 1.0
        },
        input=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain quantum computing in simple terms."}
        ]
    )

    # LLM 응답 시뮬레이션
    time.sleep(0.5)  # API 호출 시뮬레이션

    output_text = """Quantum computing is a type of computing that uses quantum mechanics
principles. Unlike classical computers that use bits (0 or 1), quantum computers use
quantum bits or 'qubits' that can exist in multiple states simultaneously."""

    # Generation 완료
    generation.end(
        output=output_text,
        usage={
            "prompt_tokens": 25,
            "completion_tokens": 45,
            "total_tokens": 70
        },
        metadata={
            "response_time_ms": 500
        }
    )

    print(f"✓ Generation 완료")
    print(f"  - Model: gpt-4")
    print(f"  - Temperature: 0.7")
    print(f"  - Prompt Tokens: 25")
    print(f"  - Completion Tokens: 45")
    print(f"  - Total Tokens: 70")
    print(f"\n응답:")
    print(f"  {output_text[:100]}...")

    trace.end()
    langfuse.flush()

    return langfuse


def chat_generation_example():
    """
    대화형 Generation 예제

    여러 턴의 대화를 추적합니다.
    """
    print("\n" + "=" * 60)
    print("2. 대화형 Generation 추적")
    print("=" * 60)

    langfuse = Langfuse()

    trace = langfuse.trace(
        name="multi_turn_conversation",
        user_id="user_789",
        session_id="session_001"
    )

    conversation_history = []

    # Turn 1
    print("\n[Turn 1]")
    user_msg_1 = "What is Python?"
    conversation_history.append({"role": "user", "content": user_msg_1})

    generation_1 = trace.generation(
        name="chat_turn_1",
        model="gpt-3.5-turbo",
        input=conversation_history.copy()
    )

    assistant_msg_1 = "Python is a high-level, interpreted programming language known for its simplicity and readability."
    conversation_history.append({"role": "assistant", "content": assistant_msg_1})

    generation_1.end(
        output=assistant_msg_1,
        usage={
            "prompt_tokens": 15,
            "completion_tokens": 20,
            "total_tokens": 35
        }
    )

    print(f"User: {user_msg_1}")
    print(f"Assistant: {assistant_msg_1}")

    # Turn 2
    print("\n[Turn 2]")
    user_msg_2 = "What are its main use cases?"
    conversation_history.append({"role": "user", "content": user_msg_2})

    generation_2 = trace.generation(
        name="chat_turn_2",
        model="gpt-3.5-turbo",
        input=conversation_history.copy()
    )

    assistant_msg_2 = "Python is widely used for web development, data science, machine learning, automation, and scientific computing."
    conversation_history.append({"role": "assistant", "content": assistant_msg_2})

    generation_2.end(
        output=assistant_msg_2,
        usage={
            "prompt_tokens": 45,
            "completion_tokens": 22,
            "total_tokens": 67
        }
    )

    print(f"User: {user_msg_2}")
    print(f"Assistant: {assistant_msg_2}")

    # Turn 3
    print("\n[Turn 3]")
    user_msg_3 = "Which one is most popular?"
    conversation_history.append({"role": "user", "content": user_msg_3})

    generation_3 = trace.generation(
        name="chat_turn_3",
        model="gpt-3.5-turbo",
        input=conversation_history.copy()
    )

    assistant_msg_3 = "Data science and machine learning are currently the most popular use cases for Python."
    conversation_history.append({"role": "assistant", "content": assistant_msg_3})

    generation_3.end(
        output=assistant_msg_3,
        usage={
            "prompt_tokens": 75,
            "completion_tokens": 18,
            "total_tokens": 93
        }
    )

    print(f"User: {user_msg_3}")
    print(f"Assistant: {assistant_msg_3}")

    print(f"\n✓ 총 3턴의 대화 추적 완료")
    print(f"  - Session ID: session_001")
    print(f"  - 총 토큰 사용량: 195 tokens")

    trace.end()
    langfuse.flush()


def streaming_generation_example():
    """
    스트리밍 Generation 예제

    실시간 스트리밍 응답을 추적합니다.
    """
    print("\n" + "=" * 60)
    print("3. 스트리밍 Generation 추적")
    print("=" * 60)

    langfuse = Langfuse()

    trace = langfuse.trace(
        name="streaming_response",
        user_id="user_streaming"
    )

    generation = trace.generation(
        name="streaming_gpt4",
        model="gpt-4",
        input="Write a haiku about coding"
    )

    # 스트리밍 시뮬레이션
    print("\n스트리밍 응답:")
    stream_chunks = [
        "Code flows like water,\n",
        "Bugs dance in moonlit debug,\n",
        "Peace in merged PR."
    ]

    full_response = ""
    for i, chunk in enumerate(stream_chunks):
        print(chunk, end="", flush=True)
        full_response += chunk
        time.sleep(0.3)  # 스트리밍 딜레이 시뮬레이션

    print("\n")

    # 스트리밍 완료 후 Generation 종료
    generation.end(
        output=full_response,
        usage={
            "prompt_tokens": 8,
            "completion_tokens": 18,
            "total_tokens": 26
        },
        metadata={
            "streaming": True,
            "chunks_count": len(stream_chunks)
        }
    )

    print(f"✓ 스트리밍 Generation 완료")
    print(f"  - Chunks: {len(stream_chunks)}")
    print(f"  - Total Tokens: 26")

    trace.end()
    langfuse.flush()


def generation_with_cost_tracking():
    """
    비용 추적이 포함된 Generation 예제

    토큰 사용량을 기반으로 비용을 계산하고 추적합니다.
    """
    print("\n" + "=" * 60)
    print("4. 비용 추적 Generation")
    print("=" * 60)

    langfuse = Langfuse()

    # 모델별 비용 (예시)
    MODEL_COSTS = {
        "gpt-4": {
            "prompt": 0.03 / 1000,  # $0.03 per 1K tokens
            "completion": 0.06 / 1000  # $0.06 per 1K tokens
        },
        "gpt-3.5-turbo": {
            "prompt": 0.0005 / 1000,
            "completion": 0.0015 / 1000
        }
    }

    models_to_test = [
        {
            "name": "gpt-4",
            "prompt_tokens": 500,
            "completion_tokens": 300
        },
        {
            "name": "gpt-3.5-turbo",
            "prompt_tokens": 500,
            "completion_tokens": 300
        }
    ]

    total_cost = 0

    for model_config in models_to_test:
        model = model_config["name"]
        prompt_tokens = model_config["prompt_tokens"]
        completion_tokens = model_config["completion_tokens"]

        # 비용 계산
        prompt_cost = prompt_tokens * MODEL_COSTS[model]["prompt"]
        completion_cost = completion_tokens * MODEL_COSTS[model]["completion"]
        total_model_cost = prompt_cost + completion_cost

        trace = langfuse.trace(
            name=f"cost_tracking_{model}",
            metadata={"cost_tracking": True}
        )

        generation = trace.generation(
            name=f"generation_{model}",
            model=model,
            input="Analyze the impact of AI on healthcare"
        )

        generation.end(
            output="AI is transforming healthcare through improved diagnostics, personalized treatment plans, and efficient patient care management.",
            usage={
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens
            },
            usage_details={
                "input_cost": prompt_cost,
                "output_cost": completion_cost,
                "total_cost": total_model_cost
            },
            metadata={
                "cost_usd": total_model_cost
            }
        )

        trace.end()

        print(f"\n{model}:")
        print(f"  - Prompt Tokens: {prompt_tokens} (${prompt_cost:.6f})")
        print(f"  - Completion Tokens: {completion_tokens} (${completion_cost:.6f})")
        print(f"  - Total Cost: ${total_model_cost:.6f}")

        total_cost += total_model_cost

    print(f"\n✓ 총 비용: ${total_cost:.6f}")

    langfuse.flush()


def generation_comparison_example():
    """
    여러 모델 비교 예제

    동일한 프롬프트로 여러 모델의 응답을 비교합니다.
    """
    print("\n" + "=" * 60)
    print("5. 모델 비교 Generation")
    print("=" * 60)

    langfuse = Langfuse()

    prompt = "Explain machine learning in one sentence."

    models = [
        {
            "name": "gpt-4",
            "response": "Machine learning is a subset of AI that enables computers to learn from data and improve their performance without explicit programming.",
            "tokens": {"prompt": 12, "completion": 23, "total": 35}
        },
        {
            "name": "gpt-3.5-turbo",
            "response": "Machine learning is when computers learn patterns from data to make predictions or decisions.",
            "tokens": {"prompt": 12, "completion": 16, "total": 28}
        },
        {
            "name": "claude-3-sonnet",
            "response": "Machine learning is a method where algorithms learn from data patterns to make predictions without being explicitly programmed.",
            "tokens": {"prompt": 12, "completion": 20, "total": 32}
        }
    ]

    trace = langfuse.trace(
        name="model_comparison",
        metadata={"comparison": True}
    )

    print(f"\nPrompt: {prompt}\n")

    for model_config in models:
        generation = trace.generation(
            name=f"compare_{model_config['name']}",
            model=model_config['name'],
            input=prompt
        )

        generation.end(
            output=model_config['response'],
            usage=model_config['tokens']
        )

        print(f"{model_config['name']}:")
        print(f"  Response: {model_config['response']}")
        print(f"  Tokens: {model_config['tokens']['total']}")
        print()

    print(f"✓ 3개 모델 비교 완료")

    trace.end()
    langfuse.flush()


def main():
    """메인 실행 함수"""
    print("\n" + "=" * 60)
    print("LANGFUSE GENERATIONS 예제")
    print("=" * 60)

    try:
        # 1. 기본 Generation
        simple_generation_example()

        # 2. 대화형 Generation
        chat_generation_example()

        # 3. 스트리밍 Generation
        streaming_generation_example()

        # 4. 비용 추적
        generation_with_cost_tracking()

        # 5. 모델 비교
        generation_comparison_example()

        print("\n" + "=" * 60)
        print("✓ 모든 Generation 예제 완료!")
        print("=" * 60)
        print(f"\nLangfuse 대시보드에서 확인하세요:")
        print(f"{os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
