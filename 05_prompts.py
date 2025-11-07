"""
Langfuse Prompts (프롬프트 관리)

Prompt Management는 프롬프트를 중앙에서 관리하고 버전 관리하는 기능입니다.
코드와 프롬프트를 분리하여 더 쉽게 반복 개선할 수 있습니다.

주요 기능:
1. 프롬프트 중앙 관리
2. 버전 관리 및 롤백
3. A/B 테스트를 위한 다중 버전
4. 프로덕션과 개발 환경 분리
"""

import os
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()


def create_and_manage_prompts():
    """
    프롬프트 생성 및 관리 예제

    Langfuse에서 프롬프트를 생성하고 관리하는 방법을 보여줍니다.
    """
    print("=" * 60)
    print("1. 프롬프트 생성 및 관리")
    print("=" * 60)

    langfuse = Langfuse()

    # 프롬프트 생성 (API를 통해)
    # 실제로는 Langfuse UI나 API를 통해 프롬프트를 먼저 생성해야 합니다

    print("\n프롬프트 관리 기능:")
    print("  1. Langfuse 대시보드에서 프롬프트 생성")
    print("  2. 프롬프트에 이름과 버전 지정")
    print("  3. 변수(variables)를 사용한 동적 프롬프트")
    print("  4. 프로덕션 버전 태깅")

    # 프롬프트 예제 구조
    example_prompts = [
        {
            "name": "qa_assistant",
            "version": 1,
            "template": "You are a helpful assistant. Answer the following question: {{question}}",
            "variables": ["question"]
        },
        {
            "name": "code_reviewer",
            "version": 1,
            "template": "Review the following {{language}} code and provide feedback:\n\n{{code}}",
            "variables": ["language", "code"]
        },
        {
            "name": "summarizer",
            "version": 1,
            "template": "Summarize the following text in {{max_words}} words or less:\n\n{{text}}",
            "variables": ["max_words", "text"]
        }
    ]

    print("\n프롬프트 예제:")
    for prompt in example_prompts:
        print(f"\n  [{prompt['name']} v{prompt['version']}]")
        print(f"  Template: {prompt['template'][:60]}...")
        print(f"  Variables: {', '.join(prompt['variables'])}")


def fetch_and_use_prompt():
    """
    프롬프트 가져오기 및 사용 예제

    저장된 프롬프트를 가져와서 사용합니다.
    """
    print("\n" + "=" * 60)
    print("2. 프롬프트 가져오기 및 사용")
    print("=" * 60)

    langfuse = Langfuse()

    # 실제 사용 예제 (프롬프트가 이미 Langfuse에 생성되어 있다고 가정)
    print("\n프롬프트 사용 흐름:")
    print("  1. 프롬프트 이름으로 조회")
    print("  2. 특정 버전 또는 'production' 버전 가져오기")
    print("  3. 변수에 값 할당")
    print("  4. 최종 프롬프트 생성")

    # 시뮬레이션된 프롬프트 사용
    prompt_name = "qa_assistant"
    prompt_version = "production"  # 또는 특정 버전 번호

    print(f"\n[예제: {prompt_name} 사용]")

    # 프롬프트 템플릿 (실제로는 langfuse.get_prompt()로 가져옴)
    prompt_template = "You are a helpful assistant. Answer the following question: {{question}}"

    # 변수 할당
    variables = {
        "question": "What is the difference between Python and JavaScript?"
    }

    # 템플릿에 변수 적용
    final_prompt = prompt_template
    for var_name, var_value in variables.items():
        final_prompt = final_prompt.replace(f"{{{{{var_name}}}}}", var_value)

    print(f"  Template: {prompt_template}")
    print(f"  Variables: {variables}")
    print(f"  Final Prompt: {final_prompt}")

    # Trace에 프롬프트 정보 기록
    trace = langfuse.trace(
        name="prompt_usage_example",
        metadata={
            "prompt_name": prompt_name,
            "prompt_version": prompt_version
        }
    )

    generation = trace.generation(
        name="qa_response",
        model="claude-3-5-haiku-20241022",
        input=final_prompt,
        prompt={
            "name": prompt_name,
            "version": prompt_version
        }
    )

    output = "Python is a general-purpose language often used for backend development, data science, and scripting. JavaScript is primarily used for web development, running in browsers and Node.js environments."

    generation.end(output=output)
    trace.end()

    print(f"\n  Response: {output}")

    langfuse.flush()


def prompt_versioning_example():
    """
    프롬프트 버전 관리 예제

    프롬프트의 여러 버전을 관리하고 비교합니다.
    """
    print("\n" + "=" * 60)
    print("3. 프롬프트 버전 관리")
    print("=" * 60)

    langfuse = Langfuse()

    # 프롬프트의 여러 버전 시뮬레이션
    prompt_versions = [
        {
            "version": 1,
            "template": "Translate to French: {{text}}",
            "description": "Initial simple version"
        },
        {
            "version": 2,
            "template": "Translate the following English text to French. Maintain the tone and style:\n\n{{text}}",
            "description": "Added context about tone and style"
        },
        {
            "version": 3,
            "template": "You are a professional translator. Translate the following English text to French, maintaining the original tone, style, and any cultural nuances:\n\n{{text}}\n\nProvide only the translation without explanations.",
            "description": "Added role and explicit instructions"
        }
    ]

    test_text = "Hello, how are you doing today?"

    print(f"\n테스트 텍스트: {test_text}\n")
    print("프롬프트 버전 비교:")

    for version_data in prompt_versions:
        print(f"\n  [Version {version_data['version']}]")
        print(f"  Description: {version_data['description']}")
        print(f"  Template: {version_data['template'][:80]}...")

        # 템플릿에 변수 적용
        final_prompt = version_data['template'].replace("{{text}}", test_text)

        trace = langfuse.trace(
            name=f"translation_v{version_data['version']}",
            metadata={
                "prompt_version": version_data['version'],
                "experiment": "version_comparison"
            }
        )

        generation = trace.generation(
            name="translation",
            model="claude-3-5-haiku-20241022",
            input=final_prompt
        )

        # 시뮬레이션된 응답 (실제로는 LLM 호출)
        responses = {
            1: "Bonjour, comment allez-vous aujourd'hui?",
            2: "Bonjour, comment allez-vous aujourd'hui? (maintaining friendly tone)",
            3: "Bonjour, comment allez-vous aujourd'hui ?"
        }

        generation.end(output=responses[version_data['version']])
        trace.end()

        print(f"  Output: {responses[version_data['version']]}")

    print("\n✓ 버전별 성능을 대시보드에서 비교할 수 있습니다")

    langfuse.flush()


def prompt_with_chat_template():
    """
    채팅 템플릿 프롬프트 예제

    채팅 형식의 프롬프트를 관리합니다.
    """
    print("\n" + "=" * 60)
    print("4. 채팅 템플릿 프롬프트")
    print("=" * 60)

    langfuse = Langfuse()

    # 채팅 템플릿 예제
    chat_prompt_template = [
        {
            "role": "system",
            "content": "You are {{assistant_type}}. {{additional_instructions}}"
        },
        {
            "role": "user",
            "content": "{{user_message}}"
        }
    ]

    # 다양한 assistant 타입 테스트
    test_cases = [
        {
            "name": "technical_support",
            "variables": {
                "assistant_type": "a technical support specialist",
                "additional_instructions": "Provide clear, step-by-step solutions.",
                "user_message": "My printer is not working"
            }
        },
        {
            "name": "creative_writer",
            "variables": {
                "assistant_type": "a creative writing assistant",
                "additional_instructions": "Use vivid imagery and engaging language.",
                "user_message": "Write a short story about a robot"
            }
        },
        {
            "name": "data_analyst",
            "variables": {
                "assistant_type": "a data analyst",
                "additional_instructions": "Provide insights backed by logical reasoning.",
                "user_message": "Analyze this sales trend"
            }
        }
    ]

    for test_case in test_cases:
        print(f"\n[{test_case['name']}]")

        # 템플릿에 변수 적용
        messages = []
        for template_msg in chat_prompt_template:
            content = template_msg['content']
            for var_name, var_value in test_case['variables'].items():
                content = content.replace(f"{{{{{var_name}}}}}", var_value)

            messages.append({
                "role": template_msg['role'],
                "content": content
            })

        print(f"  System: {messages[0]['content']}")
        print(f"  User: {messages[1]['content']}")

        trace = langfuse.trace(
            name=f"chat_prompt_{test_case['name']}",
            metadata={
                "prompt_type": "chat_template",
                "use_case": test_case['name']
            }
        )

        generation = trace.generation(
            name="chat_response",
            model="claude-3-5-haiku-20241022",
            input=messages
        )

        # 시뮬레이션된 응답
        generation.end(
            output=f"Response for {test_case['name']} use case"
        )

        trace.end()

    print(f"\n✓ 채팅 템플릿 프롬프트 테스트 완료")

    langfuse.flush()


def prompt_experimentation_example():
    """
    프롬프트 실험 예제

    여러 프롬프트 변형을 동시에 테스트합니다.
    """
    print("\n" + "=" * 60)
    print("5. 프롬프트 실험 및 A/B 테스트")
    print("=" * 60)

    langfuse = Langfuse()

    # 같은 작업에 대한 다른 프롬프트 접근법
    prompt_variations = [
        {
            "variant": "A",
            "name": "direct_instruction",
            "template": "Classify the sentiment of this text as positive, negative, or neutral: {{text}}"
        },
        {
            "variant": "B",
            "name": "few_shot",
            "template": """Classify the sentiment as positive, negative, or neutral.

Examples:
- "I love this product!" → positive
- "This is terrible." → negative
- "It's okay." → neutral

Text: {{text}}"""
        },
        {
            "variant": "C",
            "name": "chain_of_thought",
            "template": """Analyze the sentiment of the following text step by step:
1. Identify key emotional words
2. Determine the overall tone
3. Classify as positive, negative, or neutral

Text: {{text}}"""
        }
    ]

    test_texts = [
        "This movie was absolutely amazing!",
        "I'm disappointed with the service.",
        "The product works as expected."
    ]

    experiment_id = "sentiment_analysis_prompts"

    print(f"\n실험 ID: {experiment_id}")
    print(f"테스트 텍스트: {len(test_texts)}개")
    print(f"프롬프트 변형: {len(prompt_variations)}개\n")

    for text in test_texts:
        print(f"Text: {text}")

        for variation in prompt_variations:
            # 변수 적용
            final_prompt = variation['template'].replace("{{text}}", text)

            trace = langfuse.trace(
                name=f"sentiment_experiment",
                metadata={
                    "experiment_id": experiment_id,
                    "variant": variation['variant'],
                    "prompt_name": variation['name']
                }
            )

            generation = trace.generation(
                name=f"sentiment_classification_{variation['variant']}",
                model="claude-3-5-haiku-20241022",
                input=final_prompt
            )

            # 시뮬레이션된 결과
            if "amazing" in text:
                result = "positive"
            elif "disappointed" in text:
                result = "negative"
            else:
                result = "neutral"

            generation.end(output=result)

            # 성능 점수 추가 (시뮬레이션)
            trace.score(
                name="accuracy",
                value=1.0 if result else 0.0
            )

            trace.score(
                name="response_quality",
                value=0.85 + (ord(variation['variant']) - ord('A')) * 0.05
            )

            trace.end()

            print(f"  Variant {variation['variant']}: {result}")

        print()

    print(f"✓ 프롬프트 실험 완료")
    print(f"  대시보드에서 각 변형의 성능을 비교할 수 있습니다")

    langfuse.flush()


def prompt_fallback_example():
    """
    프롬프트 폴백 전략 예제

    프롬프트 버전에 문제가 있을 때 이전 버전으로 폴백합니다.
    """
    print("\n" + "=" * 60)
    print("6. 프롬프트 폴백 전략")
    print("=" * 60)

    langfuse = Langfuse()

    # 프롬프트 버전과 상태
    prompt_config = {
        "name": "customer_support",
        "versions": [
            {"version": 1, "status": "deprecated", "quality_score": 0.70},
            {"version": 2, "status": "stable", "quality_score": 0.85},
            {"version": 3, "status": "experimental", "quality_score": 0.60}  # 문제가 있음
        ],
        "fallback_threshold": 0.75
    }

    print(f"\n프롬프트: {prompt_config['name']}")
    print(f"품질 임계값: {prompt_config['fallback_threshold']}\n")

    def select_prompt_version(versions, threshold):
        """품질 점수를 기반으로 프롬프트 버전 선택"""
        # 최신 버전부터 확인
        for version_data in reversed(versions):
            if version_data['quality_score'] >= threshold:
                return version_data
        # 모든 버전이 임계값 미달이면 가장 높은 점수의 버전 사용
        return max(versions, key=lambda x: x['quality_score'])

    selected_version = select_prompt_version(
        prompt_config['versions'],
        prompt_config['fallback_threshold']
    )

    print("버전 선택 과정:")
    for version_data in reversed(prompt_config['versions']):
        is_selected = version_data['version'] == selected_version['version']
        marker = "→ 선택됨" if is_selected else ""
        print(f"  Version {version_data['version']}: "
              f"quality={version_data['quality_score']:.2f}, "
              f"status={version_data['status']} {marker}")

    print(f"\n최종 선택: Version {selected_version['version']}")
    print(f"  이유: 임계값({prompt_config['fallback_threshold']})을 "
          f"충족하는 가장 최신 버전")

    # 선택된 버전으로 실행
    trace = langfuse.trace(
        name="customer_support_with_fallback",
        metadata={
            "prompt_name": prompt_config['name'],
            "selected_version": selected_version['version'],
            "fallback_applied": selected_version['version'] != 3
        }
    )

    generation = trace.generation(
        name="support_response",
        model="claude-3-5-haiku-20241022",
        input="How do I return a product?",
        prompt={
            "name": prompt_config['name'],
            "version": selected_version['version']
        }
    )

    generation.end(
        output="To return a product, please visit our returns page and follow the instructions."
    )

    trace.end()

    print(f"\n✓ 폴백 전략 적용 완료")

    langfuse.flush()


def main():
    """메인 실행 함수"""
    print("\n" + "=" * 60)
    print("LANGFUSE PROMPTS 예제")
    print("=" * 60)

    try:
        # 1. 프롬프트 생성 및 관리
        create_and_manage_prompts()

        # 2. 프롬프트 가져오기 및 사용
        fetch_and_use_prompt()

        # 3. 버전 관리
        prompt_versioning_example()

        # 4. 채팅 템플릿
        prompt_with_chat_template()

        # 5. 프롬프트 실험
        prompt_experimentation_example()

        # 6. 폴백 전략
        prompt_fallback_example()

        print("\n" + "=" * 60)
        print("✓ 모든 Prompts 예제 완료!")
        print("=" * 60)
        print(f"\nLangfuse 대시보드에서 확인하세요:")
        print(f"{os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
        print("\n프롬프트 관리 기능:")
        print("  - 중앙 집중식 프롬프트 저장소")
        print("  - 버전 관리 및 롤백")
        print("  - A/B 테스트 및 실험")
        print("  - 프로덕션/개발 환경 분리")
        print("\n프롬프트 생성 방법:")
        print("  1. Langfuse 대시보드에서 'Prompts' 메뉴로 이동")
        print("  2. 'Create New Prompt' 클릭")
        print("  3. 이름, 템플릿, 변수 설정")
        print("  4. 코드에서 langfuse.get_prompt()로 사용")

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
