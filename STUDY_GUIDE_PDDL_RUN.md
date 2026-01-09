# LaMMA-P 심층 분석: `pddlrun_llmseparate.py`

이 문서는 LaMMA-P 시스템의 핵심 두뇌인 `scripts/pddlrun_llmseparate.py` 파일의 구조와 작동 원리를 단계별로 분석한 학습 자료입니다.

---

## 1. 파일의 역할
*   **오케스트레이션(Orchestration)**: 사용자의 자연어 명령을 받아 최종 PDDL 계획이 나올 때까지의 모든 과정(분해, 할당, 생성, 검증, 계획)을 총괄합니다.
*   **LLM 파이프라인 관리**: OpenAI API(`LLMHandler`)를 통해 LLM에게 적절한 프롬프트를 보내고 응답을 처리합니다.
*   **플래너 연동**: 생성된 PDDL 파일을 Fast Downward 플래너(`PDDLPlanner`)에 입력하여 해(Solution)를 구합니다.

---

## 2. 주요 클래스 설명 (Key Classes)

이 파일은 역할별로 클래스가 잘 나누어져 있습니다.

### 2.1 인프라 클래스
*   **`PDDLUtils`**: AI2-THOR 시뮬레이터에서 현재 물체들의 정보(이름, 질량 등)를 가져오는 유틸리티입니다.
*   **`FileProcessor`**: 파일을 읽고 쓰는 역할뿐만 아니라, LLM이 생성한 긴 텍스트에서 PDDL 부분만 발췌하거나 괄호 개수를 맞추는 등 **텍스트 전처리**를 담당합니다.
*   **`LLMHandler`**: OpenAI API를 호출하는 래퍼(Wrapper) 클래스입니다. 재시도(Retry) 로직이 포함되어 있습니다.

### 2.2 핵심 로직 클래스
*   **`PDDLValidator`**: 생성된 PDDL 파일이 문법적으로 맞는지 LLM을 통해 1차 검증(Validate)합니다.
*   **`PDDLPlanner`**: 외부 프로그램인 Fast Downward를 실행(`subprocess`)시키는 역할을 합니다.

### 2.3 지휘자 클래스
*   **`TaskManager`**: 위 클래스들을 모두 멤버 변수로 가지고 있으며, 실제 작업 흐름(`process_tasks`)을 제어합니다.

---

## 3. 핵심 실행 흐름: `process_tasks()`

`TaskManager` 클래스의 `process_tasks` 메서드가 이 프로그램의 심장입니다. (코드 라인 1030 근처)
이 메서드는 다음과 같은 순서로 실행됩니다.

### Step 1: 준비 (Setup)
*   사용자 입력(Task)과 로봇 리스트, 물체 정보(`objects_ai`)를 받습니다.
*   모든 가능한 행동(`allactionrobot.pddl`)을 로드하여 LLM에게 "이런 행동들이 가능하다"고 알려줄 준비를 합니다.

### Step 2: 태스크 분해 (Decomposition)
*   **메서드**: `_generate_decomposed_plan`
*   **역할**: 복잡한 명령(예: "사과 씻고 불 꺼")을 단순한 서브 태스크들로 쪼갭니다.
*   **LLM 프롬프트**: `data/pythonic_plans/pddl_train_task_decomposesep.py`를 사용합니다.

### Step 3: 로봇 할당 (Allocation)
*   **메서드**: `_generate_allocation_plan`
*   **역할**: 쪼개진 태스크를 수행할 가장 적합한 로봇을 지정합니다. (예: 무거운 물건은 힘센 로봇에게)
*   **LLM 프롬프트**: `data/pythonic_plans/pddl_train_task_allocationsep_solution.py`를 사용합니다.

### Step 4: 문제 요약 생성 (Problem Summary)
*   **메서드**: `_generate_problem_summary`
*   **역할**: 분해된 내용과 할당된 내용을 합쳐서, 각 서브 태스크별로 구체적인 상황(Context)을 텍스트로 정리합니다. 이는 다음 단계인 PDDL 생성을 위한 중간 단계입니다.

### Step 5: PDDL 문제 파일 생성 (PDDL Generation) ⭐️ 중요
*   **메서드**: `_generate_problem_files` -> `problemextracting`
*   **역할**: 앞서 만든 요약본을 바탕으로 실제 PDDL 코드(`define (problem ...)`)를 생성합니다.
*   **특징**: 여기서 `split_and_store_tasks`를 호출하여 텍스트 덩어리를 개별 PDDL 파일로 쪼갭니다. 정규식(Regex)을 사용하여 `**Assigned Robot**` 같은 패턴을 찾아내고, 해당 로봇의 도메인 파일(규칙)을 참조하여 정확한 PDDL을 만들도록 유도합니다.

### Step 6: 검증 및 계획 수립 (Validation & Planning)
*   **메서드**: `_validate_and_plan`
*   **과정**:
    1.  `run_llmvalidator`: LLM에게 PDDL 코드를 보여주고 문법 오류나 빠진 조건이 없는지 확인시킵니다.
    2.  `run_planners`: 검증된 파일을 Fast Downward 플래너에 넣어 해법(`_plan.txt`)을 찾습니다.

### Step 7: 계획 통합 (Merge)
*   **메서드**: `_combine_all_plans`
*   **역할**: 여러 로봇의 개별 계획(`_plan.txt`)들을 하나의 거대한 실행 계획으로 합칩니다. 이때 병렬 실행이 가능한지(Parallelism)도 LLM이 판단하여 배치합니다.

---

## 4. 학습 팁 (Study Tips)

1.  **프롬프트 확인**: `data/pythonic_plans/` 폴더에 있는 파이썬 파일들이 사실은 파이썬 코드가 아니라 **LLM에게 주는 예제(Few-shot Prompt)**입니다. 이것들을 읽어보면 LLM을 어떻게 가르치는지 알 수 있습니다.
2.  **로그 확인**: 프로그램을 실행하면 `logs/` 폴더에 단계별 파일들이 생성됩니다.
    *   `decomposed_plan.py`: 분해 결과
    *   `allocated_plan.py`: 할당 결과
    *   `code_planpddl.py`: 생성된 PDDL
    *   이 파일들을 순서대로 열어보면 데이터가 어떻게 변환되는지 눈으로 확인할 수 있습니다.
