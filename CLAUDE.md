# Claude Code Instructions


## 커맨드

```bash
# 가상환경 생성 및 활성화
uv venv && source .venv/bin/activate

# 의존성 설치
uv pip install -e ".[dev]"

# 개발 서버
uvicorn app.main:app --reload

# Docker 서비스 (PostgreSQL, Redis, Qdrant)
docker compose up -d

# 테스트
pytest

# 린트 & 포맷
ruff check .
ruff format .
```

> 존재하지 않는 커맨드는 임의로 가정하지 말 것.

---

# 코딩 스타일

## Python 공통
외부 I/O: API/DB 요청/응답은 반드시 Pydantic 모델 사용.

타입 힌트: 함수 파라미터, 반환값 필수 (mypy 호환).

비동기: I/O 바운드 작업은 async def 필수.

구조적 로직: dict 난사 금지. 명확한 스키마(Class/Model) 우선.

## LangGraph (Core Workflow)
State: TypedDict 또는 Pydantic 모델로 정의 (불변성 지향).

Node: (state: GraphState) -> dict 형태 유지.

Logic: 비즈니스 로직은 domain/이나 workflows/에 위치, 인터페이스(api, mcp)에 종속되지 않음.

## FastMCP (Agent Interface) [NEW]
역할: FastMCP는 로직을 직접 구현하지 않고, domain 서비스나 workflows를 호출하는 Wrapper 역할만 수행.

문서화: @mcp.tool() 데코레이터가 붙은 함수는 Docstring 필수 (AI가 도구를 이해하는 유일한 수단).

리소스: mcp:// URI 스키마를 명확히 정의하여 데이터 접근성 제공.

## FastAPI (Web Interface)
역할: RESTful 엔드포인트, 인증(Auth), SSE 스트리밍.

스키마: 입출력은 schemas/ 내의 Pydantic 모델 사용.

## 디렉토리 구조 (Updated)
src/mcp 디렉토리가 추가되었으며, src/api와 동일한 레벨에서 workflows와 domain을 소비합니다.

Plaintext
graph-ai/
├── src/
│   ├── api/                            # [Interface 1] HTTP/Web (Next.js 연동)
│   │   ├── routers/                    # REST 라우터
│   │   ├── schemas/                    # Web API 전용 DTO
│   │   └── dependencies.py             # FastAPI 의존성 주입
│   │
│   ├── mcp/                            # [Interface 2] Model Context Protocol (AI 에이전트 연동)
│   │   ├── server.py                   # FastMCP 서버 인스턴스 및 설정
│   │   ├── tools/                      # Tool 정의 (workflows/domain 호출 래퍼)
│   │   └── resources/                  # Resource 정의 (파일/DB 접근)
│   │
│   ├── workflows/                      # [Core] LangGraph 엔진
│   │   ├── assistants/                 # 에이전트별 그래프 정의
│   │   └── shared/                     # 공통 노드 및 유틸리티
│   │
│   ├── domain/                         # [Core] 순수 비즈니스 로직
│   │   ├── models/                     # 도메인 엔티티
│   │   └── services/                   # 도메인 서비스
│   │
│   ├── infrastructure/                 # [Infra] 외부 시스템 구현체
│   │   ├── llm_provider/               # LLM 어댑터
│   │   └── persistence/                # DB/VectorStore 리포지토리
│   │
│   └── core/                           # 앱 전반 설정 및 상수
│       ├── settings.py
│       └── constants/
│
├── tests/
├── .env.example
├── docker-compose.yml
├── pyproject.toml
└── main.py                             # 통합 엔트리포인트 (FastAPI + FastMCP 마운트)

## 아키텍처 원칙 (Architecture Decision Records)

### Shared Core (공유 코어):
api(FastAPI)와 mcp(FastMCP)는 서로를 참조하지 않습니다.
둘 다 workflows(LangGraph)와 domain 계층을 공통으로 임포트하여 사용합니다.

### Dual Entrypoint (이중 진입점):
Web User: Next.js → FastAPI (/api/v1/...) → LangGraph 실행.
AI Agent: Claude/IDE → FastMCP (Stdio/SSE) → LangGraph 실행 (Tool 호출).
State Management:
두 인터페이스 모두 동일한 infrastructure/persistence (Postgres Checkpointer)를 사용하여 대화 상태(State)를 공유합니다.

