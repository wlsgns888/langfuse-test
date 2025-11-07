"""
Langfuse Datasets (데이터셋 관리)

Datasets는 테스트 케이스를 관리하고 모델 성능을 평가하는 데 사용됩니다.
동일한 테스트 데이터로 여러 모델이나 프롬프트 버전을 비교할 수 있습니다.

주요 기능:
1. 테스트 데이터셋 생성 및 관리
2. 모델 평가 자동화
3. 회귀 테스트
4. 벤치마킹 및 성능 비교
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()


def create_dataset_example():
    """
    데이터셋 생성 예제

    테스트용 데이터셋을 생성합니다.
    """
    print("=" * 60)
    print("1. 데이터셋 생성")
    print("=" * 60)

    langfuse = Langfuse()

    # 데이터셋 생성
    dataset_name = "qa_evaluation_dataset"

    print(f"\n데이터셋 생성: {dataset_name}")
    print("=" * 40)

    # 데이터셋 아이템 예제
    dataset_items = [
        {
            "input": "What is the capital of France?",
            "expected_output": "Paris",
            "metadata": {
                "category": "geography",
                "difficulty": "easy"
            }
        },
        {
            "input": "Explain quantum entanglement in simple terms.",
            "expected_output": "Quantum entanglement is a phenomenon where two particles become connected and the state of one instantly affects the other, regardless of distance.",
            "metadata": {
                "category": "science",
                "difficulty": "hard"
            }
        },
        {
            "input": "What is 15 * 24?",
            "expected_output": "360",
            "metadata": {
                "category": "math",
                "difficulty": "easy"
            }
        },
        {
            "input": "Who wrote Romeo and Juliet?",
            "expected_output": "William Shakespeare",
            "metadata": {
                "category": "literature",
                "difficulty": "easy"
            }
        },
        {
            "input": "What is the time complexity of binary search?",
            "expected_output": "O(log n)",
            "metadata": {
                "category": "computer_science",
                "difficulty": "medium"
            }
        }
    ]

    # 데이터셋 아이템 생성
    # 실제로는 langfuse.create_dataset() 및 dataset.create_item() 사용
    print("\n데이터셋 아이템:")
    for i, item in enumerate(dataset_items, 1):
        print(f"\n[Item {i}]")
        print(f"  Category: {item['metadata']['category']}")
        print(f"  Difficulty: {item['metadata']['difficulty']}")
        print(f"  Input: {item['input']}")
        print(f"  Expected: {item['expected_output']}")

    print(f"\n✓ 데이터셋 생성 완료: {len(dataset_items)}개 아이템")

    # 데이터셋 정보 저장 (시뮬레이션)
    dataset_info = {
        "name": dataset_name,
        "description": "QA evaluation dataset for testing model accuracy",
        "items_count": len(dataset_items),
        "categories": list(set(item['metadata']['category'] for item in dataset_items)),
        "created_at": datetime.now().isoformat()
    }

    print(f"\n데이터셋 정보:")
    print(f"  - Name: {dataset_info['name']}")
    print(f"  - Description: {dataset_info['description']}")
    print(f"  - Items: {dataset_info['items_count']}")
    print(f"  - Categories: {', '.join(dataset_info['categories'])}")

    return dataset_name, dataset_items


def run_dataset_evaluation():
    """
    데이터셋 평가 실행 예제

    데이터셋의 모든 아이템에 대해 모델을 평가합니다.
    """
    print("\n" + "=" * 60)
    print("2. 데이터셋 평가 실행")
    print("=" * 60)

    langfuse = Langfuse()

    # 평가할 데이터셋 (이전 예제에서 생성한 것과 동일)
    dataset_items = [
        {
            "input": "What is the capital of France?",
            "expected_output": "Paris",
            "metadata": {"category": "geography"}
        },
        {
            "input": "What is 15 * 24?",
            "expected_output": "360",
            "metadata": {"category": "math"}
        },
        {
            "input": "Who wrote Romeo and Juliet?",
            "expected_output": "William Shakespeare",
            "metadata": {"category": "literature"}
        }
    ]

    model_name = "gpt-3.5-turbo"
    run_name = f"evaluation_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    print(f"\n평가 실행: {run_name}")
    print(f"모델: {model_name}")
    print(f"테스트 아이템: {len(dataset_items)}개\n")

    results = []

    for i, item in enumerate(dataset_items, 1):
        print(f"[{i}/{len(dataset_items)}] 평가 중...")

        # Trace 생성
        trace = langfuse.trace(
            name=f"dataset_evaluation_{i}",
            metadata={
                "dataset_run": run_name,
                "dataset_item_id": i,
                "category": item['metadata']['category']
            }
        )

        # Generation 실행
        generation = trace.generation(
            name="model_response",
            model=model_name,
            input=item['input']
        )

        # 모델 응답 시뮬레이션
        # 실제로는 OpenAI API 등을 호출
        if "France" in item['input']:
            model_output = "Paris"
        elif "15 * 24" in item['input']:
            model_output = "360"
        elif "Romeo and Juliet" in item['input']:
            model_output = "William Shakespeare"
        else:
            model_output = "Unknown"

        generation.end(output=model_output)

        # 정확도 계산
        is_correct = model_output.strip().lower() == item['expected_output'].strip().lower()
        accuracy_score = 1.0 if is_correct else 0.0

        # 점수 기록
        trace.score(
            name="accuracy",
            value=accuracy_score,
            comment="Exact match" if is_correct else "Mismatch"
        )

        trace.end()

        results.append({
            "item_id": i,
            "category": item['metadata']['category'],
            "correct": is_correct,
            "expected": item['expected_output'],
            "actual": model_output
        })

        status = "✓" if is_correct else "✗"
        print(f"  {status} {item['metadata']['category']}: {model_output}")

    # 결과 요약
    correct_count = sum(1 for r in results if r['correct'])
    total_count = len(results)
    accuracy = correct_count / total_count

    print(f"\n평가 결과:")
    print(f"  - 정확도: {correct_count}/{total_count} ({accuracy*100:.1f}%)")

    # 카테고리별 정확도
    categories = {}
    for result in results:
        cat = result['category']
        if cat not in categories:
            categories[cat] = {'correct': 0, 'total': 0}
        categories[cat]['total'] += 1
        if result['correct']:
            categories[cat]['correct'] += 1

    print(f"\n  카테고리별 정확도:")
    for cat, stats in categories.items():
        cat_accuracy = stats['correct'] / stats['total'] * 100
        print(f"    - {cat}: {stats['correct']}/{stats['total']} ({cat_accuracy:.1f}%)")

    langfuse.flush()

    return results


def compare_models_with_dataset():
    """
    데이터셋으로 여러 모델 비교 예제

    동일한 데이터셋으로 여러 모델을 평가하고 비교합니다.
    """
    print("\n" + "=" * 60)
    print("3. 데이터셋으로 모델 비교")
    print("=" * 60)

    langfuse = Langfuse()

    # 테스트 데이터셋
    test_dataset = [
        {"input": "Translate to Spanish: Hello", "expected": "Hola"},
        {"input": "Translate to Spanish: Goodbye", "expected": "Adiós"},
        {"input": "Translate to Spanish: Thank you", "expected": "Gracias"}
    ]

    # 비교할 모델들
    models = ["gpt-3.5-turbo", "gpt-3.5-turbo", "gpt-4"]

    print(f"\n테스트 데이터셋: {len(test_dataset)}개 아이템")
    print(f"비교 모델: {len(models)}개\n")

    comparison_results = {}

    for model in models:
        print(f"[{model}] 평가 중...")

        model_results = []

        for i, item in enumerate(test_dataset):
            trace = langfuse.trace(
                name=f"model_comparison_{model}_{i}",
                metadata={
                    "experiment": "model_comparison",
                    "model": model,
                    "dataset_item": i
                }
            )

            generation = trace.generation(
                name="translation",
                model=model,
                input=item['input']
            )

            # 모델별 응답 시뮬레이션
            if "gpt-3.5" in model:
                outputs = ["Hola", "Adiós", "Gracias"]
            elif "gpt-3.5-turbo" in model:
                outputs = ["Hola", "Adiós", "Gracias"]
            else:  # claude
                outputs = ["Hola", "Adiós", "Gracias"]

            model_output = outputs[i]
            generation.end(output=model_output)

            # 정확도 평가
            is_correct = model_output == item['expected']
            trace.score(name="accuracy", value=1.0 if is_correct else 0.0)

            trace.end()

            model_results.append(is_correct)

        accuracy = sum(model_results) / len(model_results) * 100
        comparison_results[model] = accuracy

        print(f"  정확도: {accuracy:.1f}%")

    # 비교 결과
    print(f"\n비교 결과:")
    sorted_models = sorted(comparison_results.items(), key=lambda x: x[1], reverse=True)

    for rank, (model, accuracy) in enumerate(sorted_models, 1):
        print(f"  {rank}. {model}: {accuracy:.1f}%")

    langfuse.flush()


def regression_testing_example():
    """
    회귀 테스트 예제

    모델 업데이트 후 성능 저하를 감지합니다.
    """
    print("\n" + "=" * 60)
    print("4. 회귀 테스트")
    print("=" * 60)

    langfuse = Langfuse()

    # 기준 성능 (이전 버전)
    baseline_results = {
        "version": "v1.0",
        "accuracy": 0.85,
        "avg_response_time": 1.2
    }

    # 테스트 데이터셋
    regression_dataset = [
        {"input": "What is AI?", "expected_contains": "artificial intelligence"},
        {"input": "Define machine learning", "expected_contains": "learning"},
        {"input": "Explain neural networks", "expected_contains": "network"}
    ]

    print(f"\n기준 성능 (Baseline):")
    print(f"  - Version: {baseline_results['version']}")
    print(f"  - Accuracy: {baseline_results['accuracy']*100:.1f}%")
    print(f"  - Avg Response Time: {baseline_results['avg_response_time']}s")

    # 새 버전 테스트
    new_version = "v2.0"
    print(f"\n새 버전 테스트: {new_version}")

    correct_count = 0
    total_time = 0

    for i, item in enumerate(regression_dataset):
        trace = langfuse.trace(
            name=f"regression_test_{i}",
            metadata={
                "test_type": "regression",
                "version": new_version,
                "baseline_version": baseline_results['version']
            }
        )

        generation = trace.generation(
            name="model_response",
            model="gpt-3.5-turbo",
            input=item['input']
        )

        # 응답 시뮬레이션
        response = f"Response containing {item['expected_contains']}"
        response_time = 1.1  # seconds

        generation.end(
            output=response,
            metadata={"response_time_seconds": response_time}
        )

        # 검증
        is_correct = item['expected_contains'] in response.lower()
        if is_correct:
            correct_count += 1

        total_time += response_time

        trace.score(
            name="correctness",
            value=1.0 if is_correct else 0.0
        )

        trace.end()

    # 새 버전 결과
    new_accuracy = correct_count / len(regression_dataset)
    avg_response_time = total_time / len(regression_dataset)

    print(f"\n새 버전 결과:")
    print(f"  - Accuracy: {new_accuracy*100:.1f}%")
    print(f"  - Avg Response Time: {avg_response_time:.2f}s")

    # 회귀 검사
    print(f"\n회귀 검사:")

    accuracy_change = new_accuracy - baseline_results['accuracy']
    time_change = avg_response_time - baseline_results['avg_response_time']

    if accuracy_change < -0.05:  # 5% 이상 정확도 감소
        print(f"  ⚠ 정확도 회귀 감지: {accuracy_change*100:.1f}%")
    elif accuracy_change > 0.05:
        print(f"  ✓ 정확도 개선: +{accuracy_change*100:.1f}%")
    else:
        print(f"  ✓ 정확도 유지: {accuracy_change*100:.1f}%")

    if time_change > 0.3:  # 0.3초 이상 느려짐
        print(f"  ⚠ 응답 시간 회귀 감지: +{time_change:.2f}s")
    elif time_change < -0.3:
        print(f"  ✓ 응답 시간 개선: {time_change:.2f}s")
    else:
        print(f"  ✓ 응답 시간 유지: {time_change:.2f}s")

    langfuse.flush()


def dataset_with_golden_answers():
    """
    정답 데이터셋 예제

    정확한 정답이 있는 데이터셋으로 평가합니다.
    """
    print("\n" + "=" * 60)
    print("5. 정답 데이터셋 평가")
    print("=" * 60)

    langfuse = Langfuse()

    # 정답이 명확한 데이터셋
    golden_dataset = [
        {
            "input": "Calculate: 25 + 17",
            "golden_answer": "42",
            "type": "exact_match"
        },
        {
            "input": "What is the chemical formula for water?",
            "golden_answer": "H2O",
            "type": "exact_match"
        },
        {
            "input": "Name the first president of the United States",
            "golden_answer": "George Washington",
            "type": "exact_match"
        },
        {
            "input": "What color do you get when mixing blue and yellow?",
            "golden_answer": "green",
            "type": "exact_match"
        }
    ]

    print(f"\n정답 데이터셋: {len(golden_dataset)}개 아이템\n")

    exact_matches = 0
    partial_matches = 0

    for i, item in enumerate(golden_dataset, 1):
        trace = langfuse.trace(
            name=f"golden_test_{i}",
            metadata={
                "dataset_type": "golden_answers",
                "evaluation_type": item['type']
            }
        )

        generation = trace.generation(
            name="answer_generation",
            model="gpt-3.5-turbo",
            input=item['input']
        )

        # 응답 시뮬레이션
        if "25 + 17" in item['input']:
            model_answer = "42"
        elif "water" in item['input']:
            model_answer = "H2O"
        elif "president" in item['input']:
            model_answer = "George Washington"
        elif "blue and yellow" in item['input']:
            model_answer = "Green"
        else:
            model_answer = "Unknown"

        generation.end(output=model_answer)

        # 정답 비교
        exact_match = model_answer.strip().lower() == item['golden_answer'].strip().lower()
        partial_match = item['golden_answer'].lower() in model_answer.lower()

        if exact_match:
            exact_matches += 1
            match_type = "exact_match"
            score = 1.0
        elif partial_match:
            partial_matches += 1
            match_type = "partial_match"
            score = 0.7
        else:
            match_type = "no_match"
            score = 0.0

        trace.score(
            name="answer_correctness",
            value=score,
            comment=match_type
        )

        trace.end()

        status = "✓" if exact_match else ("~" if partial_match else "✗")
        print(f"[{i}] {status} {item['input'][:40]}...")
        print(f"    Expected: {item['golden_answer']}")
        print(f"    Got: {model_answer}")
        print(f"    Match Type: {match_type}\n")

    # 결과 요약
    total = len(golden_dataset)
    print(f"평가 결과:")
    print(f"  - Exact Matches: {exact_matches}/{total} ({exact_matches/total*100:.1f}%)")
    print(f"  - Partial Matches: {partial_matches}/{total} ({partial_matches/total*100:.1f}%)")
    print(f"  - No Matches: {total-exact_matches-partial_matches}/{total}")

    langfuse.flush()


def benchmark_dataset_example():
    """
    벤치마크 데이터셋 예제

    표준 벤치마크 데이터셋을 사용하여 모델 성능을 평가합니다.
    """
    print("\n" + "=" * 60)
    print("6. 벤치마크 데이터셋")
    print("=" * 60)

    langfuse = Langfuse()

    # 벤치마크 데이터셋 (예: MMLU, HellaSwag 등과 유사한 형식)
    benchmark_dataset = [
        {
            "question": "Which programming language is known for its use in data science?",
            "options": ["A) JavaScript", "B) Python", "C) C++", "D) Ruby"],
            "correct_answer": "B",
            "category": "programming"
        },
        {
            "question": "What does CPU stand for?",
            "options": ["A) Central Processing Unit", "B) Computer Personal Unit", "C) Central Program Utility", "D) Computer Processing Unit"],
            "correct_answer": "A",
            "category": "computer_science"
        },
        {
            "question": "In which year was Python first released?",
            "options": ["A) 1989", "B) 1991", "C) 1995", "D) 2000"],
            "correct_answer": "B",
            "category": "programming_history"
        }
    ]

    benchmark_name = "Custom Tech Benchmark"
    model = "gpt-3.5-turbo"

    print(f"\nBenchmark: {benchmark_name}")
    print(f"Model: {model}")
    print(f"Questions: {len(benchmark_dataset)}\n")

    correct = 0

    for i, item in enumerate(benchmark_dataset, 1):
        trace = langfuse.trace(
            name=f"benchmark_{i}",
            metadata={
                "benchmark_name": benchmark_name,
                "category": item['category'],
                "question_id": i
            }
        )

        # 프롬프트 구성
        prompt = f"{item['question']}\n" + "\n".join(item['options'])

        generation = trace.generation(
            name="multiple_choice_answer",
            model=model,
            input=prompt
        )

        # 모델 응답 시뮬레이션
        model_answer = item['correct_answer']  # 100% 정확도로 시뮬레이션

        generation.end(output=model_answer)

        # 정답 확인
        is_correct = model_answer == item['correct_answer']
        if is_correct:
            correct += 1

        trace.score(
            name="correctness",
            value=1.0 if is_correct else 0.0
        )

        trace.end()

        status = "✓" if is_correct else "✗"
        print(f"[{i}] {status} {item['category']}")
        print(f"    Q: {item['question'][:50]}...")
        print(f"    Answer: {model_answer} (Correct: {item['correct_answer']})\n")

    # 벤치마크 결과
    accuracy = correct / len(benchmark_dataset) * 100

    print(f"벤치마크 결과:")
    print(f"  - Score: {correct}/{len(benchmark_dataset)} ({accuracy:.1f}%)")
    print(f"  - Model: {model}")
    print(f"  - Benchmark: {benchmark_name}")

    langfuse.flush()


def main():
    """메인 실행 함수"""
    print("\n" + "=" * 60)
    print("LANGFUSE DATASETS 예제")
    print("=" * 60)

    try:
        # 1. 데이터셋 생성
        create_dataset_example()

        # 2. 데이터셋 평가
        run_dataset_evaluation()

        # 3. 모델 비교
        compare_models_with_dataset()

        # 4. 회귀 테스트
        regression_testing_example()

        # 5. 정답 데이터셋
        dataset_with_golden_answers()

        # 6. 벤치마크
        benchmark_dataset_example()

        print("\n" + "=" * 60)
        print("✓ 모든 Datasets 예제 완료!")
        print("=" * 60)
        print(f"\nLangfuse 대시보드에서 확인하세요:")
        print(f"{os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
        print("\n데이터셋 활용 방법:")
        print("  - 일관된 테스트 케이스로 모델 평가")
        print("  - 버전 간 성능 비교")
        print("  - 회귀 테스트 자동화")
        print("  - 프로덕션 배포 전 검증")

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
