"""
Langfuse Scoring (평가 및 점수 매기기)

Scoring은 LLM 출력의 품질을 평가하고 측정하는 기능입니다.
자동화된 메트릭이나 사람의 피드백을 통해 모델 성능을 모니터링할 수 있습니다.

주요 기능:
1. 자동 점수 매기기 (정확도, 관련성, 독성 등)
2. 사용자 피드백 수집 (좋아요/싫어요, 별점 등)
3. 커스텀 메트릭 정의
4. A/B 테스트 결과 분석
"""

import os
import time
from datetime import datetime
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()


def basic_scoring_example():
    """
    기본 점수 매기기 예제

    Generation에 점수를 부여합니다.
    """
    print("=" * 60)
    print("1. 기본 점수 매기기")
    print("=" * 60)

    langfuse = Langfuse()

    # Trace와 Generation 생성
    trace = langfuse.trace(
        name="scored_response",
        user_id="user_scoring_001"
    )

    generation = trace.generation(
        name="answer_generation",
        model="claude-3-5-haiku-20241022",
        input="What is the capital of France?"
    )

    output = "The capital of France is Paris."
    generation.end(output=output)

    print(f"질문: What is the capital of France?")
    print(f"응답: {output}")
    print()

    # 점수 매기기 - 정확도
    score_accuracy = trace.score(
        name="accuracy",
        value=1.0,  # 0.0 ~ 1.0
        comment="Correct answer"
    )

    print(f"✓ 정확도 점수: {score_accuracy.value}")
    print(f"  Comment: {score_accuracy.comment}")

    # 점수 매기기 - 간결성
    score_conciseness = trace.score(
        name="conciseness",
        value=0.9,
        comment="Very concise and to the point"
    )

    print(f"\n✓ 간결성 점수: {score_conciseness.value}")
    print(f"  Comment: {score_conciseness.comment}")

    # 점수 매기기 - 유용성
    score_helpfulness = trace.score(
        name="helpfulness",
        value=0.85,
        comment="Helpful but could provide more context"
    )

    print(f"\n✓ 유용성 점수: {score_helpfulness.value}")
    print(f"  Comment: {score_helpfulness.comment}")

    trace.end()
    langfuse.flush()


def user_feedback_scoring_example():
    """
    사용자 피드백 점수 예제

    실제 사용자의 피드백을 점수로 기록합니다.
    """
    print("\n" + "=" * 60)
    print("2. 사용자 피드백 점수")
    print("=" * 60)

    langfuse = Langfuse()

    # 여러 사용자의 피드백 시뮬레이션
    user_feedbacks = [
        {
            "user_id": "user_001",
            "query": "How do I reset my password?",
            "response": "You can reset your password by clicking 'Forgot Password' on the login page.",
            "feedback": "positive",
            "rating": 5,
            "comment": "Very helpful!"
        },
        {
            "user_id": "user_002",
            "query": "What are your business hours?",
            "response": "We are open Monday through Friday, 9 AM to 5 PM EST.",
            "feedback": "positive",
            "rating": 4,
            "comment": "Good, but would like weekend hours too"
        },
        {
            "user_id": "user_003",
            "query": "How do I cancel my subscription?",
            "response": "Please contact customer support to cancel.",
            "feedback": "negative",
            "rating": 2,
            "comment": "Too vague, needs more specific instructions"
        }
    ]

    for i, feedback_data in enumerate(user_feedbacks, 1):
        trace = langfuse.trace(
            name=f"user_interaction_{i}",
            user_id=feedback_data['user_id'],
            metadata={"interaction_type": "customer_support"}
        )

        generation = trace.generation(
            name="support_response",
            model="claude-3-5-haiku-20241022",
            input=feedback_data['query']
        )

        generation.end(output=feedback_data['response'])

        # 사용자 피드백을 점수로 변환
        feedback_value = 1.0 if feedback_data['feedback'] == 'positive' else 0.0

        # 이진 피드백 (좋아요/싫어요)
        trace.score(
            name="user_feedback",
            value=feedback_value,
            data_type="BOOLEAN",
            comment=feedback_data['comment']
        )

        # 별점 (1-5)
        trace.score(
            name="user_rating",
            value=feedback_data['rating'] / 5.0,  # 0-1로 정규화
            data_type="NUMERIC",
            comment=f"{feedback_data['rating']}/5 stars"
        )

        trace.end()

        print(f"\n[User {i}]")
        print(f"  Query: {feedback_data['query']}")
        print(f"  Response: {feedback_data['response']}")
        print(f"  Feedback: {feedback_data['feedback']} ({feedback_data['rating']}/5)")
        print(f"  Comment: {feedback_data['comment']}")

    print(f"\n✓ {len(user_feedbacks)}개의 사용자 피드백 수집 완료")

    langfuse.flush()


def automated_quality_scoring_example():
    """
    자동화된 품질 평가 예제

    여러 품질 메트릭을 자동으로 계산하고 점수를 부여합니다.
    """
    print("\n" + "=" * 60)
    print("3. 자동화된 품질 평가")
    print("=" * 60)

    langfuse = Langfuse()

    def calculate_quality_metrics(input_text, output_text):
        """품질 메트릭 계산 (간단한 시뮬레이션)"""
        # 실제로는 더 정교한 알고리즘이나 다른 모델을 사용
        metrics = {
            "relevance": min(1.0, len(set(input_text.lower().split()) &
                                       set(output_text.lower().split())) / 5),
            "completeness": min(1.0, len(output_text.split()) / 20),
            "clarity": 0.85,  # 실제로는 readability score 등을 사용
            "factual_accuracy": 0.90  # 실제로는 fact-checking API 사용
        }
        return metrics

    test_cases = [
        {
            "input": "Explain the process of photosynthesis",
            "output": "Photosynthesis is the process by which plants convert light energy into chemical energy. Plants use sunlight, water, and carbon dioxide to produce glucose and oxygen. This occurs in chloroplasts, specifically using chlorophyll."
        },
        {
            "input": "What is machine learning?",
            "output": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed."
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        trace = langfuse.trace(
            name=f"quality_assessment_{i}",
            metadata={"automated_scoring": True}
        )

        generation = trace.generation(
            name="model_response",
            model="claude-3-5-haiku-20241022",
            input=test_case['input']
        )

        generation.end(output=test_case['output'])

        # 품질 메트릭 계산
        metrics = calculate_quality_metrics(
            test_case['input'],
            test_case['output']
        )

        print(f"\n[Test Case {i}]")
        print(f"  Input: {test_case['input']}")
        print(f"  Output: {test_case['output'][:80]}...")
        print(f"\n  품질 메트릭:")

        # 각 메트릭을 점수로 기록
        for metric_name, metric_value in metrics.items():
            trace.score(
                name=metric_name,
                value=metric_value,
                data_type="NUMERIC"
            )
            print(f"    - {metric_name}: {metric_value:.2f}")

        # 종합 점수 계산
        overall_score = sum(metrics.values()) / len(metrics)
        trace.score(
            name="overall_quality",
            value=overall_score,
            data_type="NUMERIC",
            comment=f"Average of {len(metrics)} metrics"
        )

        print(f"    - Overall: {overall_score:.2f}")

        trace.end()

    print(f"\n✓ 자동화된 품질 평가 완료")

    langfuse.flush()


def ab_testing_scoring_example():
    """
    A/B 테스트 점수 비교 예제

    두 가지 다른 모델/프롬프트를 비교합니다.
    """
    print("\n" + "=" * 60)
    print("4. A/B 테스트 점수 비교")
    print("=" * 60)

    langfuse = Langfuse()

    test_prompt = "Summarize the benefits of regular exercise"

    # 버전 A: GPT-3.5
    print("\n[Version A: GPT-3.5 Turbo]")
    trace_a = langfuse.trace(
        name="ab_test_version_a",
        metadata={
            "experiment": "model_comparison",
            "variant": "A",
            "model": "claude-3-5-haiku-20241022"
        }
    )

    generation_a = trace_a.generation(
        name="model_a_response",
        model="claude-3-5-haiku-20241022",
        input=test_prompt
    )

    response_a = "Regular exercise improves cardiovascular health, boosts mood, helps maintain healthy weight, and increases energy levels."
    generation_a.end(
        output=response_a,
        usage={"total_tokens": 35}
    )

    # A 버전 점수
    scores_a = {
        "completeness": 0.75,
        "readability": 0.85,
        "engagement": 0.70
    }

    for score_name, score_value in scores_a.items():
        trace_a.score(name=score_name, value=score_value)

    trace_a.end()

    print(f"  Response: {response_a}")
    print(f"  Scores: {scores_a}")

    # 버전 B: GPT-4
    print("\n[Version B: GPT-4]")
    trace_b = langfuse.trace(
        name="ab_test_version_b",
        metadata={
            "experiment": "model_comparison",
            "variant": "B",
            "model": "claude-3-5-haiku-20241022"
        }
    )

    generation_b = trace_b.generation(
        name="model_b_response",
        model="claude-3-5-haiku-20241022",
        input=test_prompt
    )

    response_b = "Regular exercise offers numerous benefits: it strengthens your heart and improves circulation, releases endorphins that enhance mood and reduce stress, aids in weight management by burning calories, and boosts overall energy levels throughout the day. Additionally, it can improve sleep quality and reduce the risk of chronic diseases."
    generation_b.end(
        output=response_b,
        usage={"total_tokens": 68}
    )

    # B 버전 점수
    scores_b = {
        "completeness": 0.95,
        "readability": 0.90,
        "engagement": 0.88
    }

    for score_name, score_value in scores_b.items():
        trace_b.score(name=score_name, value=score_value)

    trace_b.end()

    print(f"  Response: {response_b[:100]}...")
    print(f"  Scores: {scores_b}")

    # 비교 분석
    print("\n[비교 분석]")
    print(f"  Completeness: A={scores_a['completeness']:.2f} vs B={scores_b['completeness']:.2f}")
    print(f"  Readability: A={scores_a['readability']:.2f} vs B={scores_b['readability']:.2f}")
    print(f"  Engagement: A={scores_a['engagement']:.2f} vs B={scores_b['engagement']:.2f}")

    avg_a = sum(scores_a.values()) / len(scores_a)
    avg_b = sum(scores_b.values()) / len(scores_b)

    print(f"\n  평균 점수: A={avg_a:.2f} vs B={avg_b:.2f}")
    print(f"  → 승자: {'Version B (GPT-4)' if avg_b > avg_a else 'Version A (GPT-3.5)'}")

    langfuse.flush()


def custom_scoring_categories_example():
    """
    커스텀 점수 카테고리 예제

    특정 도메인이나 use case에 맞는 커스텀 점수를 정의합니다.
    """
    print("\n" + "=" * 60)
    print("5. 커스텀 점수 카테고리")
    print("=" * 60)

    langfuse = Langfuse()

    # 고객 지원 응답 평가
    trace = langfuse.trace(
        name="customer_support_evaluation",
        metadata={"domain": "customer_support"}
    )

    generation = trace.generation(
        name="support_response",
        model="claude-3-5-haiku-20241022",
        input="My order hasn't arrived yet. What should I do?"
    )

    response = """I apologize for the delay in your order. Let me help you with this:

1. First, please provide your order number so I can check its status
2. I'll track your package and provide you with the current location
3. If there's a significant delay, I can offer you a refund or replacement

Is there anything else I can help you with?"""

    generation.end(output=response)

    # 고객 지원 특화 점수 카테고리
    custom_scores = {
        "empathy": {
            "value": 0.95,
            "comment": "Shows understanding of customer frustration"
        },
        "actionability": {
            "value": 0.90,
            "comment": "Provides clear next steps"
        },
        "professionalism": {
            "value": 0.92,
            "comment": "Polite and professional tone"
        },
        "solution_offered": {
            "value": 1.0,
            "comment": "Offers refund or replacement"
        },
        "response_structure": {
            "value": 0.88,
            "comment": "Well-organized with numbered steps"
        }
    }

    print(f"고객 지원 응답 평가:\n")
    print(f"응답:\n{response}\n")
    print(f"평가 점수:")

    for score_name, score_data in custom_scores.items():
        trace.score(
            name=score_name,
            value=score_data['value'],
            comment=score_data['comment']
        )
        print(f"  - {score_name}: {score_data['value']:.2f}")
        print(f"    → {score_data['comment']}")

    overall = sum(s['value'] for s in custom_scores.values()) / len(custom_scores)
    print(f"\n  종합 점수: {overall:.2f}/1.00")

    trace.end()
    langfuse.flush()


def scoring_with_thresholds_example():
    """
    임계값을 사용한 점수 평가 예제

    점수가 특정 임계값 이하일 때 알림을 생성합니다.
    """
    print("\n" + "=" * 60)
    print("6. 임계값 기반 점수 평가")
    print("=" * 60)

    langfuse = Langfuse()

    # 품질 임계값 정의
    QUALITY_THRESHOLDS = {
        "accuracy": 0.8,
        "relevance": 0.75,
        "safety": 0.9
    }

    test_responses = [
        {
            "name": "good_response",
            "input": "What is 2+2?",
            "output": "2+2 equals 4.",
            "scores": {"accuracy": 1.0, "relevance": 1.0, "safety": 1.0}
        },
        {
            "name": "mediocre_response",
            "input": "Explain blockchain",
            "output": "Blockchain is a technology.",
            "scores": {"accuracy": 0.7, "relevance": 0.6, "safety": 1.0}
        },
        {
            "name": "poor_response",
            "input": "What is the capital of Japan?",
            "output": "I think it might be somewhere in Asia.",
            "scores": {"accuracy": 0.3, "relevance": 0.5, "safety": 1.0}
        }
    ]

    alerts = []

    for response_data in test_responses:
        trace = langfuse.trace(
            name=response_data['name'],
            metadata={"quality_check": True}
        )

        generation = trace.generation(
            name="evaluated_response",
            model="claude-3-5-haiku-20241022",
            input=response_data['input']
        )

        generation.end(output=response_data['output'])

        print(f"\n[{response_data['name']}]")
        print(f"  Input: {response_data['input']}")
        print(f"  Output: {response_data['output']}")
        print(f"  Scores:")

        # 각 점수 확인 및 임계값 비교
        for score_name, score_value in response_data['scores'].items():
            trace.score(name=score_name, value=score_value)

            threshold = QUALITY_THRESHOLDS.get(score_name, 0.0)
            status = "✓" if score_value >= threshold else "⚠"

            print(f"    {status} {score_name}: {score_value:.2f} (threshold: {threshold:.2f})")

            # 임계값 미달 시 알림
            if score_value < threshold:
                alert = {
                    "response": response_data['name'],
                    "metric": score_name,
                    "value": score_value,
                    "threshold": threshold
                }
                alerts.append(alert)

        trace.end()

    # 알림 요약
    if alerts:
        print(f"\n⚠ 품질 알림: {len(alerts)}개")
        for alert in alerts:
            print(f"  - {alert['response']}: {alert['metric']} = {alert['value']:.2f} < {alert['threshold']:.2f}")
    else:
        print(f"\n✓ 모든 응답이 품질 기준을 충족했습니다!")

    langfuse.flush()


def main():
    """메인 실행 함수"""
    print("\n" + "=" * 60)
    print("LANGFUSE SCORING 예제")
    print("=" * 60)

    try:
        # 1. 기본 점수 매기기
        basic_scoring_example()

        # 2. 사용자 피드백
        user_feedback_scoring_example()

        # 3. 자동화된 품질 평가
        automated_quality_scoring_example()

        # 4. A/B 테스트
        ab_testing_scoring_example()

        # 5. 커스텀 점수 카테고리
        custom_scoring_categories_example()

        # 6. 임계값 기반 평가
        scoring_with_thresholds_example()

        print("\n" + "=" * 60)
        print("✓ 모든 Scoring 예제 완료!")
        print("=" * 60)
        print(f"\nLangfuse 대시보드에서 확인하세요:")
        print(f"{os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
        print("\n대시보드에서 다음을 확인할 수 있습니다:")
        print("  - 각 trace의 점수 분포")
        print("  - 시간에 따른 점수 추이")
        print("  - 모델 간 점수 비교")
        print("  - 사용자 피드백 통계")

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
