# LaMMA-P (Language Model-Driven Multi-Agent PDDL Planner) 완벽 학습 가이드

이 문서는 LaMMA-P 프로젝트를 심도 있게 이해하고 공부하기 위해 작성되었습니다. 코드의 구조, 작동 원리, 그리고 이 시스템이 어떻게 LLM(거대 언어 모델)과 고전적 계획법(PDDL)을 결합하여 로봇을 제어하는지 상세히 설명합니다.

---

## 1. 프로젝트 개요 (Overview)

### 1.1 LaMMA-P란?
**LaMMA-P**는 "자연어 명령"을 "로봇의 행동"으로 변환하는 하이브리드 AI 시스템입니다.
*   **Neuro (신경망)**: LLM(GPT-4 등)을 사용하여 사람의 말을 이해하고, 복잡한 작업을 작은 단위로 쪼개고(Decomposition), 어떤 로봇이 무엇을 할지 배정(Allocation)합니다.
*   **Symbolic (심볼릭)**: PDDL(Planning Domain Definition Language)과 Fast Downward 플래너를 사용하여, 논리적으로 완벽한 행동 순서를 계산합니다.

### 1.2 왜 이 방식이 강력한가?
LLM은 창의적이지만 종종 논리적 오류(환각)를 범합니다. 반면 PDDL 플래너는 논리적으로 완벽하지만 유연성이 없습니다. LaMMA-P는 **LLM의 유연성**으로 문제를 정의하고, **PDDL의 엄밀함**으로 문제를 해결하는 상호보완적 구조를 가집니다.

---

## 2. 시스템 아키텍처 및 워크플로우 (Core Workflow)

전체 시스템은 다음과 같은 5단계 파이프라인으로 작동합니다. 모든 과정은 `scripts/pddlrun_llmseparate.py`가 오케스트레이션합니다.

### Step 1: 태스크 분해 (Task Decomposition)
사용자가 "사과를 씻어서 냉장고에 넣어줘"라고 말하면, LLM은 이를 다음과 같이 분해합니다.
1. 사과 집기 (Pick up Apple)
2. 싱크대로 이동 (Go to Sink)
3. 사과 씻기 (Wash Apple)
4. 냉장고로 이동 (Go to Fridge)
5. 사과 넣기 (Put Apple in Fridge)

### Step 2: 로봇 할당 (Task Allocation)
여러 로봇(`robot1`, `robot2` 등)이 있을 때, 각 로봇의 능력(Skill)과 현재 위치를 고려하여 누가 어떤 서브 태스크를 맡을지 정합니다.
*   예: `robot1`은 '집기(Grasp)' 기능이 있으므로 사과를 옮기고, `robot2`는 청소 기능만 있다면 다른 일을 맡깁니다.

### Step 3: PDDL 생성 (PDDL Generation)
대략적으로 정해진 계획을 **PDDL Problem 파일**(`*.pddl`)로 변환합니다.
*   **Input**: "robot1이 사과를 집어야 해" (자연어/Pythonic)
*   **Output**: 
    ```lisp
    (define (problem wash_apple)
      (:objects apple1 robot1 sink1 ...)
      (:init (at robot1 kitchen) (at apple1 table))
      (:goal (holding robot1 apple1))
    )
    ```

### Step 4: 계획 수립 (Planning)
생성된 PDDL Problem 파일과 미리 정의된 **Domain 파일**(`resources/robot1.pddl`)을 **Fast Downward** 플래너에 입력합니다. 플래너는 목표 상태(Goal)에 도달하기 위한 최단 경로(Action Sequence)를 찾아냅니다.
*   결과: `GoToObject(robot1, table) -> PickupObject(robot1, apple1) ...`

### Step 5: 코드 변환 및 실행 (Execution)
플래너가 만든 추상적인 계획을 실제 파이썬 코드로 변환(`scripts/plantocode.py`)하여 AI2-THOR 시뮬레이터(`scripts/ai2_thor_controller.py`)에서 실행합니다.

---

## 3. 코드베이스 심층 분석 (Codebase Deep Dive)

이 프로젝트를 이해하기 위해 꼭 봐야 할 핵심 파일들입니다.

### 3.1 `scripts/pddlrun_llmseparate.py` (The Brain)
이 파일은 전체 프로세스의 지휘자입니다.
*   **`TaskManager` 클래스**: 전체 흐름을 관리합니다. `process_tasks()` 메서드에서 분해 -> 할당 -> PDDL 생성 -> 검증 -> 계획 -> 실행 순서로 로직이 진행됩니다.
*   **`LLMHandler` 클래스**: OpenAI API와 통신하며 프롬프트를 전송하고 응답을 받습니다.
*   **`_generate_problem_files()`**: 여기가 핵심입니다. LLM이 만든 텍스트 계획을 파싱하고 정규식(Regex)을 사용하여 PDDL 포맷으로 다듬습니다. **Prompt Engineering** 기술이 집약된 곳이기도 합니다.

### 3.2 `resources/` (The Rules)
로봇이 할 수 있는 일과 규칙이 정의된 폴더입니다.
*   **`robot1.pddl` (Domain Definition)**:
    *   **:types**: `robot`, `object` 등 존재할 수 있는 타입 정의.
    *   **:predicates**: `(at ?robot ?loc)`, `(holding ?robot ?obj)` 등 현재 상태를 묘사하는 변수들.
    *   **:actions**: `GoToObject`, `PickupObject` 등 로봇이 취할 수 있는 구체적인 행동과 그 조건(Precondition), 결과(Effect)가 정의되어 있습니다.
    *   *공부 팁*: 이 파일을 보며 "어떤 조건일 때 물건을 집을 수 있는가?"를 파악해보세요. (예: 로봇 손이 비어있어야 하고, 물건 위치에 있어야 함)

### 3.3 `scripts/plantocode.py` (The Translator)
PDDL 플래너가 뱉어낸 결과물(텍스트)을 실행 가능한 Python 코드로 바꿉니다.
*   **Mimic Format**: LLM을 다시 사용하여, PDDL 계획을 `ai2_thor_controller.py`가 이해할 수 있는 함수 호출(`GoToObject(...)`) 형태로 번역합니다.

### 3.4 `scripts/ai2_thor_controller.py` (The Body)
실제 시뮬레이터와 상호작용하는 부분입니다.
*   **`GoToObject` 함수**: 실제로 AI2-THOR 환경에서 로봇을 해당 좌표로 이동시키는 명령을 보냅니다.
*   **`Action Queue`**: 멀티 에이전트 환경이므로, 여러 로봇의 행동 요청을 큐(Queue)에 쌓아두고 처리하는 방식을 사용합니다.

---

## 4. 학습 로드맵 및 발전 방향 (RAG & Future)

이 코드를 완벽히 내 것으로 만들기 위한 단계별 학습법입니다.

### 4.1 기초 다지기
1.  **PDDL 문법 공부**: `resources/robot1.pddl`을 한 줄씩 읽으며 `:precondition`과 `:effect`의 관계를 이해하세요.
2.  **프롬프트 분석**: `data/pythonic_plans/` 폴더에 있는 프롬프트 템플릿들을 열어보세요. LLM에게 어떻게 "PDDL처럼 생각하라"고 가스라이팅(?)하는지 볼 수 있습니다.

### 4.2 고급 응용 (RAG 도입 아이디어)
현재 이 프로젝트는 정적 프롬프트(`data/` 폴더)를 사용합니다. 여기에 **RAG (Retrieval-Augmented Generation)** 를 붙인다면 시스템을 비약적으로 발전시킬 수 있습니다.

*   **배경**: 새로운 환경이나 낯선 물건이 등장하면 LLM이 PDDL을 잘못 짤 수 있습니다.
*   **RAG 적용**:
    1.  성공했던 수천 개의 PDDL 계획(Plan)과 태스크 설명을 **벡터 데이터베이스**에 저장합니다.
    2.  새로운 요청("책을 책장에 꽂아줘")이 들어오면, 벡터 DB에서 "책과 유사한 물건을 옮겼던 성공 사례"를 검색(Retrieve)합니다.
    3.  검색된 예시를 프롬프트에 포함시켜("Context") LLM에게 전달하면, 훨씬 정확하고 실행 가능한 PDDL을 생성할 수 있습니다.

### 4.3 실행 금지 규칙 준수
현재 서버 환경(SSH)에서는 시뮬레이터 GUI를 띄울 수 없으므로, 코드를 수정할 때는 **"논리적 흐름"**과 **"파일 생성 로직"** 위주로 디버깅하고 학습해야 합니다. 시각적 확인 대신 `logs/` 폴더에 생성되는 `code_plan.py`나 `*.pddl` 파일을 열어보며 결과물을 검증하는 습관을 들이세요.

---

## 5. 핵심 스크립트 상세 분석: `pddlrun_llmseparate.py`

이 스크립트는 LaMMA-P의 "두뇌"에 해당합니다. 각 클래스와 주요 메서드가 어떤 역할을 수행하는지 상세히 분석합니다.

### 5.1 `PDDLUtils` 클래스
AI2-THOR 시뮬레이터 환경의 정보를 PDDL이 이해할 수 있는 형태로 변환하는 도구상자입니다.
*   **`get_ai2_thor_objects(floor_plan)`**: 특정 플로어 플랜(방 구조)에 있는 모든 물체의 정보와 질량을 가져와 리스트로 반환합니다.

### 5.2 `FileProcessor` 클래스
파일 입출력과 텍스트 전처리를 담당합니다. 단순한 읽기/쓰기 외에도 중요한 파싱 로직이 포함되어 있습니다.
*   **`split_pddl_tasks`**: LLM이 여러 개의 PDDL 문제를 한 번에 생성했을 때, 이를 개별 파일로 쪼갭니다.
*   **`balance_parentheses`**: LLM이 괄호 개수를 틀리는 경우가 많아서(Lisp 기반인 PDDL의 취약점), 이를 자동으로 맞춰주는 보정 함수입니다.
*   **`split_and_store_tasks`**: "문제 요약"과 "연속 동작(Sequence)" 부분을 텍스트에서 분리해냅니다.

### 5.3 `LLMHandler` 클래스
OpenAI API와의 통신을 전담합니다.
*   **`query_model`**: GPT-3.5, GPT-4 등 버전에 맞춰 API를 호출하고 재시도(Retry) 로직을 처리합니다.

### 5.4 `PDDLValidator` 클래스
생성된 PDDL 파일이 올바른지 검사합니다.
*   **`validate_problem`**: 도메인 파일(규칙)과 생성된 문제 파일을 LLM에게 보여주며 "이게 논리적으로 말이 되니?"라고 물어보고, 수정된 버전을 받습니다.

### 5.5 `PDDLPlanner` 클래스
외부 프로그램인 Fast Downward 플래너를 실행합니다.
*   **`run_plan`**: `subprocess`를 사용하여 실제 플래너 프로그램을 실행하고, 결과(Plan)를 받아옵니다.

### 5.6 `TaskManager` 클래스 (핵심!)
전체 파이프라인을 조율하는 지휘자입니다.

#### 주요 메서드 흐름 (Pipeline)
1.  **`process_tasks`**: 전체 메인 루프입니다. 태스크 리스트를 순회하며 아래 과정들을 순차적으로 호출합니다.
2.  **`_generate_decomposed_plan`**: 복잡한 명령을 "사과 집기", "이동하기" 등 작은 단위로 쪼갭니다.
3.  **`_generate_allocation_plan`**: 쪼개진 일을 수행할 로봇을 배정합니다.
4.  **`_generate_problem_summary`**: PDDL을 짜기 전, 사람의 언어로 상황을 정리(Summary)합니다.
5.  **`_generate_problem_files`**: 정리된 내용을 바탕으로 실제 `.pddl` 파일을 생성합니다.
    *   내부적으로 **`problemextracting`**을 호출하는데, 여기가 가장 복잡합니다. 정규식(Regex)을 써서 로봇 배정과 물체 정보를 파싱하고, LLM에게 최종 PDDL 생성을 요청합니다.
6.  **`_validate_and_plan`**: 생성된 PDDL을 검증(`PDDLValidator`)하고, 계획(`PDDLPlanner`)을 세웁니다.
7.  **`_combine_all_plans`**: 여러 로봇의 개별 계획을 하나로 합칩니다.
8.  **`_match_references_for_plan`**: 마지막으로 변수명이나 참조 오류를 LLM을 통해 최종 수정합니다.
