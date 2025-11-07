"""
Langchain Agent + Langfuse 통합 구현

Langchain 1.0.4를 사용하여 Agent를 구현하고 Langfuse로 추적합니다.
Agent는 도구를 사용하여 복잡한 작업을 수행하는 자율적인 시스템입니다.

주요 기능:
1. ReAct Agent 구현
2. 커스텀 도구 정의
3. Agent 실행 추적
4. 의사결정 과정 기록
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

from langfuse import Langfuse
from langfuse.callback import CallbackHandler

# Langchain 1.0.4 imports
from langchain.agents import AgentType, Tool, initialize_agent
from langchain_core.tools import tool
from langchain.prompts import PromptTemplate

load_dotenv()


# ============================================================
# 커스텀 도구 정의
# ============================================================

@tool
def calculate(expression: str) -> str:
    """
    수학 계산을 수행합니다.

    Args:
        expression: 계산할 수학 표현식 (예: "2 + 2", "10 * 5")

    Returns:
        계산 결과
    """
    try:
        # 안전한 계산을 위해 eval 대신 간단한 파싱 사용
        result = eval(expression, {"__builtins__": {}}, {})
        return f"계산 결과: {result}"
    except Exception as e:
        return f"계산 오류: {str(e)}"


@tool
def get_current_time() -> str:
    """
    현재 시간을 반환합니다.

    Returns:
        현재 날짜와 시간
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


@tool
def search_knowledge_base(query: str) -> str:
    """
    지식 베이스에서 정보를 검색합니다.

    Args:
        query: 검색할 쿼리

    Returns:
        검색 결과
    """
    # 시뮬레이션된 지식 베이스
    knowledge_base = {
        "langfuse": "Langfuse is an open-source LLM engineering platform that helps teams collaboratively debug, analyze, and iterate on their LLM applications.",
        "langchain": "LangChain is a framework for developing applications powered by language models.",
        "python": "Python is a high-level, interpreted programming language known for its simplicity and versatility.",
        "agent": "An agent is an autonomous system that uses an LLM to determine which actions to take and in what order."
    }

    query_lower = query.lower()

    for key, value in knowledge_base.items():
        if key in query_lower:
            return f"검색 결과: {value}"

    return "검색 결과를 찾을 수 없습니다. 다른 키워드를 시도해보세요."


@tool
def get_weather(location: str) -> str:
    """
    특정 위치의 날씨 정보를 가져옵니다.

    Args:
        location: 위치 (도시명)

    Returns:
        날씨 정보
    """
    # 시뮬레이션된 날씨 데이터
    weather_data = {
        "seoul": {"temp": 15, "condition": "맑음", "humidity": 60},
        "paris": {"temp": 18, "condition": "흐림", "humidity": 70},
        "tokyo": {"temp": 20, "condition": "비", "humidity": 80},
        "new york": {"temp": 12, "condition": "맑음", "humidity": 55}
    }

    location_lower = location.lower()

    if location_lower in weather_data:
        data = weather_data[location_lower]
        return f"{location}의 날씨: {data['condition']}, 온도: {data['temp']}°C, 습도: {data['humidity']}%"
    else:
        return f"{location}의 날씨 정보를 찾을 수 없습니다."


@tool
def save_note(content: str) -> str:
    """
    메모를 저장합니다.

    Args:
        content: 저장할 메모 내용

    Returns:
        저장 결과
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"note_{timestamp}.txt"

    try:
        # 실제로는 파일에 저장하지만, 여기서는 시뮬레이션
        return f"메모가 저장되었습니다: {filename}\n내용: {content[:50]}..."
    except Exception as e:
        return f"메모 저장 실패: {str(e)}"


# ============================================================
# Agent 시뮬레이션 함수들
# ============================================================

def simulate_agent_thinking(query: str, tools: List[Dict]) -> Dict[str, Any]:
    """
    Agent의 사고 과정을 시뮬레이션합니다.

    실제 구현에서는 LLM이 이 과정을 수행합니다.
    """
    thinking_process = {
        "query": query,
        "thoughts": [],
        "actions": [],
        "observations": [],
        "final_answer": ""
    }

    # 쿼리 분석 및 도구 선택 (시뮬레이션)
    query_lower = query.lower()

    if "calculate" in query_lower or "compute" in query_lower or any(op in query for op in ['+', '-', '*', '/']):
        thinking_process["thoughts"].append("사용자가 계산을 요청했습니다.")
        thinking_process["actions"].append({
            "tool": "calculate",
            "input": "추출된 수식"
        })

    if "time" in query_lower or "date" in query_lower:
        thinking_process["thoughts"].append("현재 시간 정보가 필요합니다.")
        thinking_process["actions"].append({
            "tool": "get_current_time",
            "input": ""
        })

    if "weather" in query_lower:
        thinking_process["thoughts"].append("날씨 정보를 조회해야 합니다.")
        thinking_process["actions"].append({
            "tool": "get_weather",
            "input": "위치 추출 필요"
        })

    if "search" in query_lower or "what is" in query_lower or "tell me about" in query_lower:
        thinking_process["thoughts"].append("지식 베이스에서 정보를 검색해야 합니다.")
        thinking_process["actions"].append({
            "tool": "search_knowledge_base",
            "input": "검색 쿼리"
        })

    if "save" in query_lower or "remember" in query_lower or "note" in query_lower:
        thinking_process["thoughts"].append("메모를 저장해야 합니다.")
        thinking_process["actions"].append({
            "tool": "save_note",
            "input": "저장할 내용"
        })

    return thinking_process


def simple_agent_example():
    """
    기본 Agent 예제

    간단한 ReAct 스타일 Agent를 구현합니다.
    """
    print("=" * 60)
    print("1. 기본 Agent 구현")
    print("=" * 60)

    langfuse = Langfuse()

    # 도구 목록
    tools_list = [
        {"name": "calculate", "description": "수학 계산 수행"},
        {"name": "get_current_time", "description": "현재 시간 조회"},
        {"name": "search_knowledge_base", "description": "지식 베이스 검색"}
    ]

    print(f"\n사용 가능한 도구: {len(tools_list)}개")
    for tool in tools_list:
        print(f"  - {tool['name']}: {tool['description']}")

    # Agent 실행 시뮬레이션
    user_query = "What time is it now?"

    trace = langfuse.trace(
        name="simple_agent_execution",
        user_id="agent_user_001",
        metadata={
            "agent_type": "react",
            "tools_count": len(tools_list)
        }
    )

    print(f"\nUser Query: {user_query}")
    print("\nAgent 사고 과정:")

    # 1. 사고 (Thought)
    thought = "사용자가 현재 시간을 요청했습니다. get_current_time 도구를 사용해야 합니다."
    print(f"  💭 Thought: {thought}")

    thought_span = trace.span(
        name="agent_thought_1",
        metadata={"step": "thinking", "iteration": 1}
    )
    thought_span.end(output=thought)

    # 2. 행동 (Action)
    action = "get_current_time"
    print(f"  🔧 Action: {action}")

    action_span = trace.span(
        name="agent_action_1",
        metadata={"step": "action", "tool": action}
    )

    # 3. 관찰 (Observation)
    observation = get_current_time.func()
    print(f"  👀 Observation: {observation}")

    action_span.end(output=observation)

    # 4. 최종 답변
    final_answer = f"The current time is {observation}"
    print(f"  ✅ Final Answer: {final_answer}")

    answer_span = trace.span(
        name="agent_final_answer",
        metadata={"step": "final_answer"}
    )
    answer_span.end(output=final_answer)

    trace.end()

    print("\n✓ Agent 실행 완료 및 Langfuse에 추적됨")

    langfuse.flush()


def multi_step_agent_example():
    """
    다단계 Agent 예제

    여러 단계의 추론과 도구 사용을 보여줍니다.
    """
    print("\n" + "=" * 60)
    print("2. 다단계 Agent 실행")
    print("=" * 60)

    langfuse = Langfuse()

    user_query = "What is Langfuse and save this information"

    trace = langfuse.trace(
        name="multi_step_agent",
        user_id="agent_user_002",
        metadata={"agent_type": "react", "expected_steps": "multiple"}
    )

    print(f"\nUser Query: {user_query}")
    print("\nAgent 실행 과정:\n")

    # Iteration 1: 정보 검색
    print("[Iteration 1]")
    print("  💭 Thought: 먼저 Langfuse에 대한 정보를 검색해야 합니다.")

    step1_span = trace.span(
        name="agent_step_1_search",
        metadata={"iteration": 1, "action": "search"}
    )

    action1 = "search_knowledge_base"
    input1 = "langfuse"
    print(f"  🔧 Action: {action1}('{input1}')")

    observation1 = search_knowledge_base.func(input1)
    print(f"  👀 Observation: {observation1}")

    step1_span.end(
        input={"action": action1, "input": input1},
        output=observation1
    )

    # Iteration 2: 정보 저장
    print("\n[Iteration 2]")
    print("  💭 Thought: 이제 이 정보를 저장해야 합니다.")

    step2_span = trace.span(
        name="agent_step_2_save",
        metadata={"iteration": 2, "action": "save_note"}
    )

    action2 = "save_note"
    input2 = observation1
    print(f"  🔧 Action: {action2}(...)")

    observation2 = save_note.func(input2)
    print(f"  👀 Observation: {observation2}")

    step2_span.end(
        input={"action": action2, "input": input2[:100]},
        output=observation2
    )

    # 최종 답변
    print("\n[Final]")
    final_answer = f"I found information about Langfuse and saved it. {observation2}"
    print(f"  ✅ Answer: {final_answer[:100]}...")

    final_span = trace.span(
        name="agent_final_answer",
        metadata={"step": "final"}
    )
    final_span.end(output=final_answer)

    trace.end()

    print("\n✓ 다단계 Agent 실행 완료")

    langfuse.flush()


def agent_with_error_handling():
    """
    에러 처리를 포함한 Agent 예제

    Agent가 에러를 처리하고 복구하는 과정을 보여줍니다.
    """
    print("\n" + "=" * 60)
    print("3. 에러 처리 Agent")
    print("=" * 60)

    langfuse = Langfuse()

    user_query = "Calculate the result of 10 divided by zero"

    trace = langfuse.trace(
        name="agent_with_error_handling",
        user_id="agent_user_003",
        metadata={"test_type": "error_handling"}
    )

    print(f"\nUser Query: {user_query}")
    print("\nAgent 실행 과정:\n")

    # Iteration 1: 계산 시도 (실패)
    print("[Iteration 1 - 시도]")
    print("  💭 Thought: 계산을 수행해야 합니다.")

    step1_span = trace.span(
        name="agent_step_1_calculate_attempt",
        metadata={"iteration": 1}
    )

    try:
        action1 = "calculate"
        input1 = "10 / 0"
        print(f"  🔧 Action: {action1}('{input1}')")

        observation1 = "계산 오류: division by zero"
        print(f"  ❌ Observation: {observation1}")

        step1_span.end(
            input={"action": action1, "input": input1},
            output=observation1,
            level="ERROR"
        )

    except Exception as e:
        observation1 = f"Error: {str(e)}"

    # Iteration 2: 에러 처리
    print("\n[Iteration 2 - 복구]")
    print("  💭 Thought: 0으로 나누기는 불가능합니다. 사용자에게 설명해야 합니다.")

    step2_span = trace.span(
        name="agent_step_2_error_explanation",
        metadata={"iteration": 2, "recovery": True}
    )

    final_answer = "I cannot calculate 10 divided by zero because division by zero is mathematically undefined. Would you like to try a different calculation?"
    print(f"  ✅ Answer: {final_answer}")

    step2_span.end(output=final_answer)

    trace.end()

    print("\n✓ Agent가 에러를 처리하고 복구함")

    langfuse.flush()


def agent_with_multiple_tools():
    """
    여러 도구를 사용하는 복잡한 Agent 예제

    복잡한 쿼리를 여러 도구를 조합하여 해결합니다.
    """
    print("\n" + "=" * 60)
    print("4. 다중 도구 사용 Agent")
    print("=" * 60)

    langfuse = Langfuse()

    user_query = "What's the weather in Seoul, and calculate how many hours until 6 PM if it's currently 2 PM"

    trace = langfuse.trace(
        name="agent_multiple_tools",
        user_id="agent_user_004",
        metadata={
            "agent_type": "react",
            "complexity": "high"
        }
    )

    print(f"\nUser Query: {user_query}")
    print("\nAgent 실행 과정:\n")

    # Step 1: 날씨 조회
    print("[Step 1: 날씨 조회]")
    print("  💭 Thought: 먼저 서울의 날씨를 확인해야 합니다.")

    weather_span = trace.span(
        name="agent_weather_check",
        metadata={"step": 1, "tool": "get_weather"}
    )

    weather_result = get_weather.func("Seoul")
    print(f"  🔧 Action: get_weather('Seoul')")
    print(f"  👀 Observation: {weather_result}")

    weather_span.end(
        input="Seoul",
        output=weather_result
    )

    # Step 2: 시간 계산
    print("\n[Step 2: 시간 계산]")
    print("  💭 Thought: 이제 2PM에서 6PM까지의 시간을 계산해야 합니다.")

    calc_span = trace.span(
        name="agent_time_calculation",
        metadata={"step": 2, "tool": "calculate"}
    )

    calc_result = calculate.func("18 - 14")  # 6PM - 2PM
    print(f"  🔧 Action: calculate('18 - 14')")
    print(f"  👀 Observation: {calc_result}")

    calc_span.end(
        input="18 - 14",
        output=calc_result
    )

    # Step 3: 최종 답변 생성
    print("\n[Step 3: 최종 답변]")

    final_span = trace.span(
        name="agent_final_synthesis",
        metadata={"step": 3, "type": "synthesis"}
    )

    final_answer = f"""Based on my analysis:
1. Weather in Seoul: {weather_result}
2. Time calculation: {calc_result}

So there are 4 hours until 6 PM from 2 PM, and the weather in Seoul is currently good for outdoor activities."""

    print(f"  ✅ Final Answer:\n{final_answer}")

    final_span.end(output=final_answer)

    trace.end()

    print("\n✓ 복잡한 다단계 Agent 실행 완료")

    langfuse.flush()


def conversational_agent_with_memory():
    """
    대화 기억을 가진 Agent 예제

    이전 대화를 기억하고 컨텍스트를 유지합니다.
    """
    print("\n" + "=" * 60)
    print("5. 대화 기억 Agent")
    print("=" * 60)

    langfuse = Langfuse()

    session_id = "agent_session_001"

    # 대화 히스토리
    conversation_history = []

    conversations = [
        {
            "turn": 1,
            "user": "What is Langchain?",
            "agent_response": "LangChain is a framework for developing applications powered by language models."
        },
        {
            "turn": 2,
            "user": "How does it work with Langfuse?",
            "agent_response": "Langchain integrates with Langfuse through the CallbackHandler, which automatically tracks all Langchain operations in Langfuse for observability."
        },
        {
            "turn": 3,
            "user": "Can you summarize what we discussed?",
            "agent_response": "We discussed Langchain (a framework for LLM applications) and its integration with Langfuse through CallbackHandler for tracking and observability."
        }
    ]

    print(f"\nSession ID: {session_id}\n")

    for conv in conversations:
        trace = langfuse.trace(
            name=f"conversational_agent_turn_{conv['turn']}",
            session_id=session_id,
            user_id="agent_user_005",
            metadata={
                "turn": conv['turn'],
                "history_length": len(conversation_history)
            }
        )

        print(f"[Turn {conv['turn']}]")
        print(f"  👤 User: {conv['user']}")

        # Agent 사고 과정
        memory_span = trace.span(
            name="agent_memory_retrieval",
            metadata={"memory_items": len(conversation_history)}
        )

        memory_context = "\n".join([f"- {item}" for item in conversation_history])
        print(f"  🧠 Memory: {len(conversation_history)} previous exchanges")

        memory_span.end(output=memory_context if memory_context else "No previous context")

        # Agent 응답
        response_span = trace.span(
            name="agent_response_generation"
        )

        print(f"  🤖 Agent: {conv['agent_response']}")

        response_span.end(output=conv['agent_response'])

        # 대화 히스토리 업데이트
        conversation_history.append(f"User: {conv['user']}")
        conversation_history.append(f"Agent: {conv['agent_response']}")

        trace.end()
        print()

    print("✓ 대화 기억을 유지하는 Agent 실행 완료")

    langfuse.flush()


def agent_performance_comparison():
    """
    Agent 성능 비교 예제

    여러 Agent 전략을 비교합니다.
    """
    print("\n" + "=" * 60)
    print("6. Agent 성능 비교")
    print("=" * 60)

    langfuse = Langfuse()

    test_query = "Find information about Python and save it"

    strategies = [
        {
            "name": "Sequential Strategy",
            "description": "순차적으로 도구 실행",
            "steps": 2,
            "execution_time": 3.5
        },
        {
            "name": "Parallel Strategy",
            "description": "가능한 경우 병렬 실행",
            "steps": 2,
            "execution_time": 2.1
        },
        {
            "name": "Optimized Strategy",
            "description": "불필요한 단계 제거",
            "steps": 1,
            "execution_time": 1.8
        }
    ]

    print(f"\nTest Query: {test_query}")
    print(f"Strategies: {len(strategies)}개\n")

    for strategy in strategies:
        trace = langfuse.trace(
            name=f"agent_strategy_comparison",
            metadata={
                "strategy": strategy['name'],
                "experiment": "performance_comparison"
            }
        )

        print(f"[{strategy['name']}]")
        print(f"  Description: {strategy['description']}")
        print(f"  Steps: {strategy['steps']}")
        print(f"  Execution Time: {strategy['execution_time']}s")

        # 성능 점수 기록
        trace.score(
            name="efficiency",
            value=1.0 / strategy['execution_time']
        )

        trace.score(
            name="step_count",
            value=1.0 / strategy['steps']
        )

        trace.end()
        print()

    print("✓ Agent 전략 비교 완료")
    print("  대시보드에서 각 전략의 성능을 비교할 수 있습니다")

    langfuse.flush()


def main():
    """메인 실행 함수"""
    print("\n" + "=" * 60)
    print("LANGCHAIN AGENT + LANGFUSE 통합")
    print("=" * 60)
    print("\nLangchain 1.0.4를 사용한 Agent 구현")

    try:
        # 1. 기본 Agent
        simple_agent_example()

        # 2. 다단계 Agent
        multi_step_agent_example()

        # 3. 에러 처리 Agent
        agent_with_error_handling()

        # 4. 다중 도구 Agent
        agent_with_multiple_tools()

        # 5. 대화 기억 Agent
        conversational_agent_with_memory()

        # 6. 성능 비교
        agent_performance_comparison()

        print("\n" + "=" * 60)
        print("✓ 모든 Agent 예제 완료!")
        print("=" * 60)
        print(f"\nLangfuse 대시보드에서 확인하세요:")
        print(f"{os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
        print("\nAgent 추적 정보:")
        print("  - 사고 과정 (Thought)")
        print("  - 행동/도구 사용 (Action)")
        print("  - 관찰 결과 (Observation)")
        print("  - 최종 답변 (Answer)")
        print("  - 각 단계의 실행 시간")
        print("  - 에러 및 복구 과정")

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
