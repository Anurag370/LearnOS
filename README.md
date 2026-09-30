# 🧠 LearnOS

> **Learn smarter. Learn your way.**

**LearnOS** is an intelligent learning platform designed to help students set goals, follow personalized learning paths, learn through structured course content, interact with an AI Tutor, and track their progress.

---

## ✨ Vision

LearnOS aims to turn a traditional course-based learning experience into a **personalized learning journey**.

```mermaid
flowchart LR
    A[👨‍🎓 Student] --> B[🎯 Set Learning Goal]
    B --> C[🗺️ Personalized Learning Plan]
    C --> D[📖 Learn]
    D --> E[📝 Practice & Assess]
    E --> F[📊 Track Progress]
    F --> G{🏆 Goal Completed?}
    G -->|No| C
    G -->|Yes| H[🎉 Achievement]

    classDef student fill:#2563EB,stroke:#1D4ED8,color:#FFFFFF,stroke-width:3px;
    classDef goal fill:#7C3AED,stroke:#6D28D9,color:#FFFFFF,stroke-width:3px;
    classDef plan fill:#0891B2,stroke:#0E7490,color:#FFFFFF,stroke-width:3px;
    classDef learn fill:#059669,stroke:#047857,color:#FFFFFF,stroke-width:3px;
    classDef assess fill:#D97706,stroke:#B45309,color:#FFFFFF,stroke-width:3px;
    classDef progress fill:#DB2777,stroke:#BE185D,color:#FFFFFF,stroke-width:3px;
    classDef decision fill:#EA580C,stroke:#C2410C,color:#FFFFFF,stroke-width:3px;
    classDef success fill:#16A34A,stroke:#15803D,color:#FFFFFF,stroke-width:3px;

    class A student;
    class B goal;
    class C plan;
    class D learn;
    class E assess;
    class F progress;
    class G decision;
    class H success;
```

---

## 🎯 Core Features

| Feature | Description |
|---|---|
| 🎯 **Learning Goals** | Students define what they want to achieve. |
| 📚 **Courses** | Structured courses organized into learning content. |
| 🗺️ **Learning Plan** | Generates a structured path toward the student's goal. |
| 🤖 **AI Tutor** | Provides contextual assistance while learning. |
| 📊 **Progress Tracking** | Tracks learning activity and completion. |
| 🧠 **Personalization** | Adapts the learning journey around goals and performance. |

---

## 🏗️ Platform Overview

```mermaid
flowchart TB
    U[👨‍🎓 Student]

    subgraph UI["🌐 LearnOS Web Application"]
        D[📊 Dashboard]
        C[📚 Courses]
        G[🎯 Goals]
        LP[🗺️ Learning Plan]
        P[📈 Progress]
        AI[🤖 AI Tutor]
        PR[👤 Profile]
    end

    subgraph API["⚡ Backend API"]
        AUTH[🔐 Authentication]
        COURSE[📚 Course Service]
        GOAL[🎯 Goal Service]
        PLAN[🗺️ Learning Plan Service]
        PROGRESS[📈 Progress Service]
        TUTOR[🤖 AI Tutor Service]
    end

    subgraph DATA["🗄️ Data Layer"]
        DB[(🐘 PostgreSQL)]
        VECTOR[(🔎 Vector Database)]
    end

    U --> D
    U --> C
    U --> G
    U --> LP
    U --> P
    U --> AI
    U --> PR

    D --> AUTH
    C --> COURSE
    G --> GOAL
    LP --> PLAN
    P --> PROGRESS
    AI --> TUTOR
    PR --> AUTH

    AUTH --> DB
    COURSE --> DB
    GOAL --> DB
    PLAN --> DB
    PROGRESS --> DB
    TUTOR --> DB
    TUTOR --> VECTOR

    classDef student fill:#2563EB,stroke:#1D4ED8,color:#FFFFFF,stroke-width:3px;
    classDef ui fill:#0891B2,stroke:#0E7490,color:#FFFFFF,stroke-width:2px;
    classDef service fill:#7C3AED,stroke:#6D28D9,color:#FFFFFF,stroke-width:2px;
    classDef database fill:#059669,stroke:#047857,color:#FFFFFF,stroke-width:3px;
    classDef vector fill:#D97706,stroke:#B45309,color:#FFFFFF,stroke-width:3px;

    class U student;
    class D,C,G,LP,P,AI,PR ui;
    class AUTH,COURSE,GOAL,PLAN,PROGRESS,TUTOR service;
    class DB database;
    class VECTOR vector;
```

---

## 🔄 Learning Journey

The central idea of LearnOS is a continuous learning loop.

```mermaid
flowchart LR
    A["🎯 Set Goal"] --> B["🗺️ Plan"]
    B --> C["📖 Learn"]
    C --> D["📝 Practice"]
    D --> E["📊 Assess"]
    E --> F["📈 Analyze Progress"]
    F --> B

    classDef blue fill:#2563EB,stroke:#1D4ED8,color:#FFFFFF,stroke-width:3px;
    classDef purple fill:#7C3AED,stroke:#6D28D9,color:#FFFFFF,stroke-width:3px;
    classDef cyan fill:#0891B2,stroke:#0E7490,color:#FFFFFF,stroke-width:3px;
    classDef green fill:#059669,stroke:#047857,color:#FFFFFF,stroke-width:3px;
    classDef orange fill:#D97706,stroke:#B45309,color:#FFFFFF,stroke-width:3px;
    classDef pink fill:#DB2777,stroke:#BE185D,color:#FFFFFF,stroke-width:3px;

    class A blue;
    class B purple;
    class C cyan;
    class D green;
    class E orange;
    class F pink;
```

---

## 🤖 AI Tutor

The AI Tutor is designed to provide learning assistance based on the available course material rather than acting as a generic chatbot.

```mermaid
flowchart TD
    Q["❓ Student Question"] --> R["📚 Retrieve Relevant Course Content"]
    R --> V["🔎 Vector Search"]
    V --> C["🧩 Relevant Context"]
    C --> P["📝 Prompt Construction"]
    P --> L["🤖 LLM"]
    L --> A["💡 AI Tutor Response"]
    A --> U["👨‍🎓 Student"]

    classDef question fill:#2563EB,stroke:#1D4ED8,color:#FFFFFF,stroke-width:3px;
    classDef retrieval fill:#0891B2,stroke:#0E7490,color:#FFFFFF,stroke-width:3px;
    classDef context fill:#7C3AED,stroke:#6D28D9,color:#FFFFFF,stroke-width:3px;
    classDef prompt fill:#D97706,stroke:#B45309,color:#FFFFFF,stroke-width:3px;
    classDef llm fill:#DB2777,stroke:#BE185D,color:#FFFFFF,stroke-width:3px;
    classDef answer fill:#059669,stroke:#047857,color:#FFFFFF,stroke-width:3px;

    class Q question;
    class R,V retrieval;
    class C context;
    class P prompt;
    class L llm;
    class A,U answer;
```

### AI Learning Flow

```mermaid
flowchart LR
    A["👨‍🎓 Student"] --> B["🌐 LearnOS"]
    B --> C["⚡ FastAPI"]
    C --> D["🧠 RAG Pipeline"]
    D --> E["🔎 Semantic Search"]
    E --> F[("📚 Vector Database")]
    F --> D
    D --> G["🧩 Context + Question"]
    G --> H["🤖 Language Model"]
    H --> I["💡 Generated Answer"]
    I --> B
    B --> A

    classDef student fill:#2563EB,stroke:#1D4ED8,color:#FFFFFF,stroke-width:3px;
    classDef app fill:#0891B2,stroke:#0E7490,color:#FFFFFF,stroke-width:3px;
    classDef backend fill:#7C3AED,stroke:#6D28D9,color:#FFFFFF,stroke-width:3px;
    classDef rag fill:#D97706,stroke:#B45309,color:#FFFFFF,stroke-width:3px;
    classDef db fill:#059669,stroke:#047857,color:#FFFFFF,stroke-width:3px;
    classDef context fill:#EA580C,stroke:#C2410C,color:#FFFFFF,stroke-width:3px;
    classDef llm fill:#DB2777,stroke:#BE185D,color:#FFFFFF,stroke-width:3px;
    classDef answer fill:#16A34A,stroke:#15803D,color:#FFFFFF,stroke-width:3px;

    class A student;
    class B app;
    class C backend;
    class D,E rag;
    class F db;
    class G context;
    class H llm;
    class I answer;
```

---

## 📄 Knowledge / RAG Pipeline

Course documents can be transformed into searchable knowledge for the AI Tutor.

```mermaid
flowchart LR
    A["📄 Course Documents"] --> B["📑 Text Extraction"]
    B --> C["✂️ Chunking"]
    C --> D["🧠 Embeddings"]
    D --> E[("🔎 Vector Database")]

    Q["❓ Student Query"] --> F["🧠 Query Embedding"]
    F --> E
    E --> G["📚 Relevant Chunks"]
    G --> H["🤖 LLM"]
    H --> I["💡 Contextual Answer"]

    classDef docs fill:#2563EB,stroke:#1D4ED8,color:#FFFFFF,stroke-width:3px;
    classDef process fill:#0891B2,stroke:#0E7490,color:#FFFFFF,stroke-width:3px;
    classDef embedding fill:#7C3AED,stroke:#6D28D9,color:#FFFFFF,stroke-width:3px;
    classDef database fill:#059669,stroke:#047857,color:#FFFFFF,stroke-width:3px;
    classDef query fill:#D97706,stroke:#B45309,color:#FFFFFF,stroke-width:3px;
    classDef relevant fill:#EA580C,stroke:#C2410C,color:#FFFFFF,stroke-width:3px;
    classDef llm fill:#DB2777,stroke:#BE185D,color:#FFFFFF,stroke-width:3px;
    classDef answer fill:#16A34A,stroke:#15803D,color:#FFFFFF,stroke-width:3px;

    class A docs;
    class B,C process;
    class D,F embedding;
    class E database;
    class Q query;
    class G relevant;
    class H llm;
    class I answer;
```

---

## 🧩 Technology Stack

```mermaid
flowchart TB
    ROOT["🧠 LearnOS"]

    subgraph FRONTEND["🎨 Frontend"]
        NEXT["Next.js"]
        REACT["React"]
        TS["TypeScript"]
        TAILWIND["Tailwind CSS"]
    end

    subgraph BACKEND["⚡ Backend"]
        FASTAPI["FastAPI"]
        PYTHON["Python"]
        SQLA["SQLAlchemy"]
    end

    subgraph DATABASE["🗄️ Database"]
        POSTGRES["PostgreSQL"]
        PGVECTOR["pgvector"]
    end

    subgraph AI["🤖 AI"]
        LANGCHAIN["LangChain"]
        LANGGRAPH["LangGraph"]
        RAG["RAG"]
        EMBEDDINGS["Embeddings"]
        LLM["LLM"]
    end

    subgraph INFRA["🚢 Infrastructure"]
        DOCKER["Docker"]
        COMPOSE["Docker Compose"]
    end

    ROOT --> NEXT
    ROOT --> FASTAPI
    ROOT --> POSTGRES
    ROOT --> LANGCHAIN
    ROOT --> DOCKER

    NEXT --> REACT
    NEXT --> TS
    NEXT --> TAILWIND
    FASTAPI --> PYTHON
    FASTAPI --> SQLA
    POSTGRES --> PGVECTOR
    LANGCHAIN --> LANGGRAPH
    LANGCHAIN --> RAG
    RAG --> EMBEDDINGS
    RAG --> LLM
    DOCKER --> COMPOSE

    classDef root fill:#0F172A,stroke:#020617,color:#FFFFFF,stroke-width:4px;
    classDef frontend fill:#2563EB,stroke:#1D4ED8,color:#FFFFFF,stroke-width:2px;
    classDef backend fill:#7C3AED,stroke:#6D28D9,color:#FFFFFF,stroke-width:2px;
    classDef database fill:#059669,stroke:#047857,color:#FFFFFF,stroke-width:2px;
    classDef ai fill:#DB2777,stroke:#BE185D,color:#FFFFFF,stroke-width:2px;
    classDef infra fill:#D97706,stroke:#B45309,color:#FFFFFF,stroke-width:2px;
    class ROOT root;
    class NEXT,REACT,TS,TAILWIND frontend;
    class FASTAPI,PYTHON,SQLA backend;
    class POSTGRES,PGVECTOR database;
    class LANGCHAIN,LANGGRAPH,RAG,EMBEDDINGS,LLM ai;
    class DOCKER,COMPOSE infra;
```

---

## 🔐 High-Level Architecture

```mermaid
flowchart TB
    CLIENT["🌐 Web Client<br/>Next.js + React"]
    API["⚡ FastAPI Backend"]

    subgraph SERVICES["🧩 Application Services"]
        AUTH["🔐 Authentication"]
        COURSES["📚 Courses"]
        GOALS["🎯 Goals"]
        LEARNING["🗺️ Learning Plans"]
        TRACKING["📈 Progress"]
        AI["🤖 AI / RAG"]
    end

    DB[("🐘 PostgreSQL")]
    VECTOR[("🔎 pgvector")]
    LLM["🧠 LLM"]

    CLIENT --> API
    API --> AUTH
    API --> COURSES
    API --> GOALS
    API --> LEARNING
    API --> TRACKING
    API --> AI

    AUTH --> DB
    COURSES --> DB
    GOALS --> DB
    LEARNING --> DB
    TRACKING --> DB
    AI --> VECTOR
    AI --> LLM
    AI --> DB

    classDef client fill:#2563EB,stroke:#1D4ED8,color:#FFFFFF,stroke-width:3px;
    classDef api fill:#7C3AED,stroke:#6D28D9,color:#FFFFFF,stroke-width:3px;
    classDef service fill:#0891B2,stroke:#0E7490,color:#FFFFFF,stroke-width:2px;
    classDef database fill:#059669,stroke:#047857,color:#FFFFFF,stroke-width:3px;
    classDef vector fill:#D97706,stroke:#B45309,color:#FFFFFF,stroke-width:3px;
    classDef llm fill:#DB2777,stroke:#BE185D,color:#FFFFFF,stroke-width:3px;

    class CLIENT client;
    class API api;
    class AUTH,COURSES,GOALS,LEARNING,TRACKING,AI service;
    class DB database;
    class VECTOR vector;
    class LLM llm;
```

---

## 👨‍🎓 Student Experience

```mermaid
flowchart LR
    A["🔵 Create Account"] --> B["🔵 Select Course"]
    B --> C["🟣 Define Goal"]
    C --> D["🟣 Follow Learning Plan"]
    D --> E["🩵 Study Course Material"]
    E --> F["🩷 Ask AI Tutor"]
    F --> G["🟠 Practice"]
    G --> H["🟠 Take Assessment"]
    H --> I["🟢 Review Progress"]
    I --> J["🟢 Identify Weak Areas"]
    J --> D

    classDef setup fill:#2563EB,stroke:#1D4ED8,color:#FFFFFF,stroke-width:3px;
    classDef learning fill:#7C3AED,stroke:#6D28D9,color:#FFFFFF,stroke-width:3px;
    classDef material fill:#0891B2,stroke:#0E7490,color:#FFFFFF,stroke-width:3px;
    classDef tutor fill:#DB2777,stroke:#BE185D,color:#FFFFFF,stroke-width:3px;
    classDef assess fill:#D97706,stroke:#B45309,color:#FFFFFF,stroke-width:3px;
    classDef improve fill:#059669,stroke:#047857,color:#FFFFFF,stroke-width:3px;

    class A,B,C setup;
    class D learning;
    class E material;
    class F tutor;
    class G,H assess;
    class I,J improve;
```

---

## 🚀 Development Roadmap

```mermaid
flowchart LR
    P1["🟦 Phase 1<br/>Core Platform<br/><br/>Authentication<br/>Courses<br/>User Profiles"] -->
    P2["🟪 Phase 2<br/>Learning System<br/><br/>Goals<br/>Enrollments<br/>Learning Plans<br/>Progress Tracking"] -->
    P3["🩵 Phase 3<br/>AI Foundation<br/><br/>Document Ingestion<br/>Chunking<br/>Embeddings<br/>Vector Search"] -->
    P4["🟧 Phase 4<br/>AI Tutor<br/><br/>RAG<br/>LangChain<br/>LangGraph<br/>Contextual Responses"] -->
    P5["🩷 Phase 5<br/>Intelligent Personalization<br/><br/>Performance Analysis<br/>Adaptive Learning<br/>Personalized Recommendations"]

    classDef phase1 fill:#2563EB,stroke:#1D4ED8,color:#FFFFFF,stroke-width:3px;
    classDef phase2 fill:#7C3AED,stroke:#6D28D9,color:#FFFFFF,stroke-width:3px;
    classDef phase3 fill:#0891B2,stroke:#0E7490,color:#FFFFFF,stroke-width:3px;
    classDef phase4 fill:#D97706,stroke:#B45309,color:#FFFFFF,stroke-width:3px;
    classDef phase5 fill:#DB2777,stroke:#BE185D,color:#FFFFFF,stroke-width:3px;

    class P1 phase1;
    class P2 phase2;
    class P3 phase3;
    class P4 phase4;
    class P5 phase5;
```

---

## 💡 What Makes LearnOS Different?

LearnOS is built around the idea that **learning should be a continuous feedback loop**.

Instead of:

> Course → Content → Finish

LearnOS aims for:

> **Goal → Plan → Learn → Practice → Assess → Analyze → Adapt → Learn**

This architecture creates a foundation for progressively introducing more intelligent personalization as the platform evolves.

---

## 📌 Project Summary

**LearnOS** is an AI-powered learning platform that combines:

- 🎯 Goal-oriented learning
- 🗺️ Personalized learning plans
- 📚 Structured course content
- 🤖 AI-assisted learning
- 🔎 Retrieval-Augmented Generation
- 📊 Progress tracking
- 🔄 Continuous learning feedback

The long-term vision is to build a **personal learning operating system** that helps students understand *what to learn, how to learn it, and what to do next*.

---

## 🛠️ Project Status

> 🚧 **Active Development**

LearnOS is being developed as an evolving project, with the current focus on building the core learning platform and AI-powered learning infrastructure.

---

## 👥 Team

**Team:** Code of Duty  
**Project:** LearnOS  
**Built during:** College Hackathon organized by the Hack Club

---

## 🧠 LearnOS

**Learn smarter. Learn your way. 🚀**
