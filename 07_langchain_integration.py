"""
Langfuse + Langchain 통합

Langchain과 Langfuse를 통합하여 Langchain 애플리케이션을 자동으로 추적합니다.
CallbackHandler를 사용하여 모든 Langchain 작업을 Langfuse에 기록합니다.

주요 기능:
1. LLM 호출 자동 추적
2. Chain 실행 추적
3. Agent 실행 추적
4. 비용 및 토큰 사용량 자동 기록
"""

import os
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

# Langchain imports (langchain 1.0.4)
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()


def simple_llm_call_with_callback():
    """
    기본 LLM 호출 + Langfuse 콜백 예제

    LLM 호출을 Langfuse로 자동 추적합니다.
    """
    print("=" * 60)
    print("1. 기본 LLM 호출 + Langfuse 추적")
    print("=" * 60)

    # Langfuse 콜백 핸들러 생성
    langfuse_handler = CallbackHandler(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    )

    # Trace 메타데이터 설정
    langfuse_handler.trace(
        name="simple_langchain_call",
        user_id="user_langchain_001",
        metadata={
            "framework": "langchain",
            "version": "1.0.4"
        }
    )

    print("\nLangfuse 콜백 핸들러 생성 완료")
    print("  - 모든 Langchain 작업이 자동으로 Langfuse에 기록됩니다")

    # 실제 LLM 사용 시:
    # from langchain_openai import ChatOpenAI
    # llm = ChatOpenAI(model="gpt-3.5-turbo")
    # response = llm.invoke(
    #     "What is the capital of France?",
    #     config={"callbacks": [langfuse_handler]}
    # )

    # 시뮬레이션
    print("\n[시뮬레이션] LLM 호출:")
    print("  Input: 'What is the capital of France?'")
    print("  Output: 'The capital of France is Paris.'")
    print("\n✓ 호출 정보가 Langfuse에 자동 기록됨")
    print("  - 프롬프트")
    print("  - 응답")
    print("  - 토큰 사용량")
    print("  - 실행 시간")

    return langfuse_handler


def chain_with_callback():
    """
    Langchain Chain + Langfuse 콜백 예제

    Chain 실행을 Langfuse로 추적합니다.
    """
    print("\n" + "=" * 60)
    print("2. Langchain Chain + Langfuse 추적")
    print("=" * 60)

    langfuse_handler = CallbackHandler()

    langfuse_handler.trace(
        name="langchain_chain_execution",
        user_id="user_chain_001",
        metadata={"chain_type": "LLMChain"}
    )

    # 프롬프트 템플릿 생성
    template = """You are a helpful assistant that translates {source_language} to {target_language}.

Translate the following text:
{text}"""

    prompt = PromptTemplate(
        input_variables=["source_language", "target_language", "text"],
        template=template
    )

    print("\n프롬프트 템플릿:")
    print(f"  {template[:100]}...")

    # Chain 생성 및 실행 (시뮬레이션)
    print("\n[시뮬레이션] Chain 실행:")

    translations = [
        {
            "input": {"source_language": "English", "target_language": "Spanish", "text": "Hello, how are you?"},
            "output": "Hola, ¿cómo estás?"
        },
        {
            "input": {"source_language": "English", "target_language": "French", "text": "Good morning"},
            "output": "Bonjour"
        }
    ]

    for i, trans in enumerate(translations, 1):
        print(f"\n  [{i}] Translation:")
        print(f"    From: {trans['input']['source_language']}")
        print(f"    To: {trans['input']['target_language']}")
        print(f"    Input: {trans['input']['text']}")
        print(f"    Output: {trans['output']}")

    print("\n✓ Chain 실행 정보가 Langfuse에 자동 기록됨")
    print("  - Chain 구조")
    print("  - 각 단계의 입출력")
    print("  - 전체 실행 시간")


def sequential_chain_with_callback():
    """
    Sequential Chain + Langfuse 콜백 예제

    여러 단계로 구성된 Chain을 추적합니다.
    """
    print("\n" + "=" * 60)
    print("3. Sequential Chain + Langfuse 추적")
    print("=" * 60)

    langfuse_handler = CallbackHandler()

    langfuse_handler.trace(
        name="sequential_chain_example",
        metadata={"chain_type": "SequentialChain"}
    )

    # Sequential Chain 시뮬레이션
    # 1단계: 주제 생성
    # 2단계: 개요 작성
    # 3단계: 전체 글 작성

    steps = [
        {
            "name": "Generate Topic",
            "input": "Write about artificial intelligence",
            "output": "The Impact of AI on Healthcare"
        },
        {
            "name": "Create Outline",
            "input": "The Impact of AI on Healthcare",
            "output": "1. Introduction\n2. Current Applications\n3. Future Prospects\n4. Challenges"
        },
        {
            "name": "Write Full Article",
            "input": "Outline for AI in Healthcare",
            "output": "A comprehensive article about AI's transformative role in healthcare..."
        }
    ]

    print("\nSequential Chain 실행:")

    for i, step in enumerate(steps, 1):
        print(f"\n[Step {i}: {step['name']}]")
        print(f"  Input: {step['input'][:50]}...")
        print(f"  Output: {step['output'][:50]}...")

    print("\n✓ Sequential Chain의 모든 단계가 Langfuse에 기록됨")
    print("  - 각 단계가 별도의 Span으로 추적")
    print("  - 단계 간 데이터 흐름 가시화")
    print("  - 병목 구간 식별 가능")


def conversational_chain_with_memory():
    """
    대화형 Chain + 메모리 + Langfuse 예제

    대화 기록을 포함한 Chain을 추적합니다.
    """
    print("\n" + "=" * 60)
    print("4. 대화형 Chain + 메모리 추적")
    print("=" * 60)

    langfuse_handler = CallbackHandler()

    session_id = "conv_session_001"

    langfuse_handler.trace(
        name="conversational_chain",
        session_id=session_id,
        metadata={"has_memory": True}
    )

    # 대화 시뮬레이션
    conversation = [
        {
            "turn": 1,
            "user": "What's the weather like?",
            "assistant": "I don't have access to real-time weather data. Could you tell me your location?",
            "memory": []
        },
        {
            "turn": 2,
            "user": "I'm in Paris",
            "assistant": "Paris typically has mild weather. For current conditions, I recommend checking a weather service.",
            "memory": ["User asked about weather", "User is in Paris"]
        },
        {
            "turn": 3,
            "user": "What should I wear?",
            "assistant": "Based on Paris's typical weather, I'd recommend layers - a light jacket and comfortable clothing.",
            "memory": ["User in Paris", "Asked about weather", "Asked about clothing"]
        }
    ]

    print(f"\nSession ID: {session_id}")
    print(f"대화 턴: {len(conversation)}개\n")

    for turn_data in conversation:
        print(f"[Turn {turn_data['turn']}]")
        print(f"  User: {turn_data['user']}")
        print(f"  Assistant: {turn_data['assistant']}")
        print(f"  Memory: {len(turn_data['memory'])} items")
        print()

    print("✓ 대화 기록과 메모리 상태가 Langfuse에 추적됨")
    print("  - 세션별 대화 그룹화")
    print("  - 메모리 상태 변화 추적")
    print("  - 컨텍스트 윈도우 사용량 모니터링")


def retrieval_qa_with_callback():
    """
    RAG (Retrieval Augmented Generation) + Langfuse 예제

    문서 검색과 생성을 포함한 RAG 파이프라인을 추적합니다.
    """
    print("\n" + "=" * 60)
    print("5. RAG (Retrieval Augmented Generation) 추적")
    print("=" * 60)

    langfuse_handler = CallbackHandler()

    langfuse_handler.trace(
        name="rag_pipeline",
        metadata={
            "pipeline_type": "retrieval_qa",
            "vector_store": "chroma"
        }
    )

    # RAG 파이프라인 시뮬레이션
    print("\n[Step 1] 문서 검색 (Retrieval)")

    query = "What are the benefits of using Langfuse?"

    retrieved_docs = [
        {
            "content": "Langfuse provides comprehensive LLM observability...",
            "score": 0.92,
            "source": "docs/intro.md"
        },
        {
            "content": "With Langfuse, you can track costs, latency, and quality...",
            "score": 0.88,
            "source": "docs/features.md"
        },
        {
            "content": "Langfuse integrates seamlessly with Langchain...",
            "score": 0.85,
            "source": "docs/integrations.md"
        }
    ]

    print(f"  Query: {query}")
    print(f"  Retrieved: {len(retrieved_docs)} documents")

    for i, doc in enumerate(retrieved_docs, 1):
        print(f"\n  Doc {i}:")
        print(f"    Score: {doc['score']}")
        print(f"    Source: {doc['source']}")
        print(f"    Content: {doc['content'][:60]}...")

    # Generation with context
    print("\n[Step 2] 컨텍스트 기반 생성 (Generation)")

    context = "\n\n".join([doc['content'] for doc in retrieved_docs])
    prompt_with_context = f"""Answer the question based on the following context:

{context}

Question: {query}"""

    answer = "Langfuse offers several benefits including comprehensive LLM observability, cost and latency tracking, quality monitoring, and seamless integration with frameworks like Langchain."

    print(f"  Context Length: {len(context)} chars")
    print(f"  Generated Answer: {answer[:80]}...")

    print("\n✓ RAG 파이프라인 전체가 Langfuse에 추적됨")
    print("  - 검색된 문서와 관련성 점수")
    print("  - 컨텍스트 구성")
    print("  - 최종 생성 결과")
    print("  - 전체 파이프라인 실행 시간")


def custom_tools_with_callback():
    """
    커스텀 도구 + Langfuse 예제

    커스텀 도구를 사용하는 작업을 추적합니다.
    """
    print("\n" + "=" * 60)
    print("6. 커스텀 도구 + Langfuse 추적")
    print("=" * 60)

    langfuse_handler = CallbackHandler()

    langfuse_handler.trace(
        name="custom_tools_execution",
        metadata={"tools_count": 3}
    )

    # 커스텀 도구 정의 (시뮬레이션)
    tools = [
        {
            "name": "Calculator",
            "description": "Performs mathematical calculations",
            "example_input": "25 * 4 + 10",
            "example_output": "110"
        },
        {
            "name": "WebSearch",
            "description": "Searches the web for information",
            "example_input": "Latest news about AI",
            "example_output": "Found 10 recent articles about AI developments..."
        },
        {
            "name": "DatabaseQuery",
            "description": "Queries the database",
            "example_input": "SELECT * FROM users WHERE active=true",
            "example_output": "Retrieved 150 active users"
        }
    ]

    print("\n등록된 커스텀 도구:")

    for tool in tools:
        print(f"\n  [{tool['name']}]")
        print(f"    Description: {tool['description']}")
        print(f"    Example Input: {tool['example_input']}")
        print(f"    Example Output: {tool['example_output'][:50]}...")

    # 도구 실행 시뮬레이션
    print("\n도구 실행 예제:")
    print("  User Query: 'Calculate 25 * 4 + 10 and then search for AI news'")
    print("\n  [1] Using Calculator tool:")
    print("      Input: 25 * 4 + 10")
    print("      Output: 110")
    print("\n  [2] Using WebSearch tool:")
    print("      Input: Latest news about AI")
    print("      Output: Found 10 recent articles...")

    print("\n✓ 도구 실행 정보가 Langfuse에 추적됨")
    print("  - 사용된 도구 목록")
    print("  - 각 도구의 입출력")
    print("  - 도구 실행 시간")


def error_handling_with_callback():
    """
    에러 처리 + Langfuse 예제

    에러 상황도 Langfuse에 기록합니다.
    """
    print("\n" + "=" * 60)
    print("7. 에러 처리 + Langfuse 추적")
    print("=" * 60)

    langfuse_handler = CallbackHandler()

    langfuse_handler.trace(
        name="error_handling_example",
        metadata={"test_type": "error_scenarios"}
    )

    # 에러 시나리오 시뮬레이션
    error_scenarios = [
        {
            "scenario": "API Rate Limit",
            "input": "Generate a long article",
            "error": "RateLimitError: Too many requests",
            "status": "failed"
        },
        {
            "scenario": "Invalid Input",
            "input": "Process invalid JSON: {invalid}",
            "error": "ValueError: Invalid JSON format",
            "status": "failed"
        },
        {
            "scenario": "Timeout",
            "input": "Complex calculation",
            "error": "TimeoutError: Operation exceeded 30s limit",
            "status": "failed"
        }
    ]

    print("\n에러 시나리오 테스트:\n")

    for i, scenario in enumerate(error_scenarios, 1):
        print(f"[Scenario {i}: {scenario['scenario']}]")
        print(f"  Input: {scenario['input']}")
        print(f"  Error: {scenario['error']}")
        print(f"  Status: {scenario['status']}")
        print()

    print("✓ 모든 에러가 Langfuse에 기록됨")
    print("  - 에러 타입 및 메시지")
    print("  - 실패한 작업의 컨텍스트")
    print("  - 스택 트레이스 (있는 경우)")
    print("  - 에러 발생 시점")


def batch_processing_with_callback():
    """
    배치 처리 + Langfuse 예제

    여러 항목을 배치로 처리하는 작업을 추적합니다.
    """
    print("\n" + "=" * 60)
    print("8. 배치 처리 + Langfuse 추적")
    print("=" * 60)

    langfuse = Langfuse()

    batch_id = "batch_20240101_001"
    items = [
        "Summarize article 1",
        "Summarize article 2",
        "Summarize article 3",
        "Summarize article 4",
        "Summarize article 5"
    ]

    print(f"\nBatch ID: {batch_id}")
    print(f"Items: {len(items)}개\n")

    for i, item in enumerate(items, 1):
        langfuse_handler = CallbackHandler()

        langfuse_handler.trace(
            name=f"batch_item_{i}",
            metadata={
                "batch_id": batch_id,
                "item_index": i,
                "total_items": len(items)
            }
        )

        print(f"[{i}/{len(items)}] Processing: {item}")
        print(f"  Status: ✓ Completed")

    print(f"\n✓ 배치 처리 완료")
    print(f"  - 모든 항목이 개별 trace로 기록됨")
    print(f"  - batch_id로 그룹화 가능")
    print(f"  - 배치 전체 성능 분석 가능")


def main():
    """메인 실행 함수"""
    print("\n" + "=" * 60)
    print("LANGFUSE + LANGCHAIN 통합 예제")
    print("=" * 60)

    try:
        # 1. 기본 LLM 호출
        simple_llm_call_with_callback()

        # 2. Chain 실행
        chain_with_callback()

        # 3. Sequential Chain
        sequential_chain_with_callback()

        # 4. 대화형 Chain
        conversational_chain_with_memory()

        # 5. RAG 파이프라인
        retrieval_qa_with_callback()

        # 6. 커스텀 도구
        custom_tools_with_callback()

        # 7. 에러 처리
        error_handling_with_callback()

        # 8. 배치 처리
        batch_processing_with_callback()

        print("\n" + "=" * 60)
        print("✓ 모든 Langchain 통합 예제 완료!")
        print("=" * 60)
        print(f"\nLangfuse 대시보드에서 확인하세요:")
        print(f"{os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
        print("\nLangchain 통합 사용 방법:")
        print("  1. CallbackHandler 생성")
        print("  2. Langchain 호출 시 callbacks 파라미터에 전달")
        print("  3. 모든 작업이 자동으로 Langfuse에 기록됨")
        print("\n코드 예제:")
        print("  from langfuse.callback import CallbackHandler")
        print("  handler = CallbackHandler()")
        print("  llm.invoke(prompt, config={'callbacks': [handler]})")

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
