# Phylax
### Legal Document & Terms & Conditions Red Flag Scanner Grounded in Indian Law

[Problem](#problem-statement) • [How It Works](#how-it-works) • [Key Features](#key-features) • [Supported Documents](#supported-document-types) • [Why Grounding Matters](#why-grounding-matters) • [Tech Stack](#tech-stack) • [Getting Started](#getting-started) • [Disclaimer](#disclaimer)

---

## Problem Statement

Every day, millions of people in India enter into binding contracts they cannot fully understand:
* **Rent Agreements** containing unlawful security deposit deductions, unreasonable lock-in periods, or arbitrary eviction terms.
* **Employment Offer Letters** imposing illegal post-employment non-compete clauses or unfair IP ownership grabs.
* **Website Terms & Conditions** forfeiting data privacy rights under dense, confusing legalese.
* **Freelance Contracts** with unbalanced indemnity obligations and delayed payment remedies.

Professional legal consultation is expensive, slow, and out of reach for most individuals. **Phylax** solves this by providing an automated, clause-by-clause legal risk scanner that translates complex legal language into plain English and grounds every flagged risk directly in Indian statutory law.

---

## How It Works

```
[ Upload PDF / Paste URL ]
           │
           ▼
[ Clause Extraction & Segmentation ]
           │
           ▼
[ Semantic Vector Search against Indian Acts Database ]
           │
           ▼
[ AI Legal Reasoning Grounded in Retrieved Sections ]
           │
           ▼
[ Clause-by-Clause Risk Flags + Plain English Translation + Summary Verdict ]
```

1. **Input**: The user uploads a contract PDF or provides a live website URL for Terms & Conditions.
2. **Parsing**: The document text is extracted, cleaned, and split into distinct logical clauses.
3. **Retrieval**: Each clause is vectorized and matched against a pre-indexed knowledge base of Indian statutory acts to retrieve the most relevant sections.
4. **Analysis**: The AI model analyzes the clause against the retrieved statutory text and assigns a risk classification with full citations.
5. **Insights**: The user receives a high-level summary score, a list of missing mandatory safeguards, and expandable clause cards showing the exact statutory text.

---

## Key Features

* **Dual Input Modes**:
  * **PDF Upload**: Drag-and-drop text-based contracts and lease agreements.
  * **T&C Web Stripper**: Paste any live website URL to extract, clean, and analyze its Terms & Conditions.
* **Traffic-Light Risk Scoring**:
  * 🔴 **Red Flag**: Unenforceable or illegal under Indian statutes, or heavily predatory.
  * 🟡 **Yellow Flag**: Unusual, aggressive, or worth negotiating prior to signing.
  * 🟢 **Green Flag**: Standard, fair, and legally compliant terms.
* **Statutory Grounding (Zero Hallucinations)**:
  * Red and yellow flags cite the exact Act and Section retrieved from the legal database (e.g., *Indian Contract Act 1872, Section 27*).
* **Missing Safeguards Detection**:
  * Scans for vital protective clauses absent from the agreement (e.g., notice period guidelines, dispute resolution mechanisms, deposit refund guarantees).
* **Plain-Language Translations**:
  * Rewrites confusing legal terms into straightforward explanations anyone can understand, accompanied by an expandable drawer showing the official law text.
* **Instant Summary Verdict**:
  * High-level risk score, breakdown counts, and recommendations on whether to negotiate or sign.
* **Export & Sharing**:
  * Copy summary insights to clipboard or export a full structured report as a PDF.

---

## Supported Document Types (At Launch)

| Document Type | Input Method | Key Indian Laws Referenced |
|---|---|---|
| **Rent / Lease Agreement** | PDF Upload | Transfer of Property Act 1882, Model Tenancy Act 2021, State Rent Control Acts |
| **Employment Offer Letter** | PDF Upload | Indian Contract Act 1872, Industrial Disputes Act, Shops & Establishments Acts |
| **Website Terms & Conditions** | URL Input | Information Technology Act 2000, Consumer Protection Act 2019, DPDP Act 2023 |

---

## Why Grounding Matters

Generic conversational AI models frequently hallucinate legal citations, confuse jurisdictions, or invent non-existent section numbers. 

**Phylax eliminates hallucination by enforcing strict retrieval grounding:**
* The model does not guess the law from general training memory.
* It is supplied with verbatim statutory sections retrieved from a dedicated Indian law vector database at query time.
* The system displays the retrieved legal section directly on screen, allowing users to verify the statutory text themselves.

---

## Tech Stack

* **Frontend**: Next.js (App Router), React, Tailwind CSS, TypeScript
* **Backend**: FastAPI (Python), `pdfplumber`, `httpx`, `BeautifulSoup4`
* **AI & Embeddings**: Gemini API & Supabase (PostgreSQL with `pgvector`)
* **Hosting**: Vercel (Frontend) & Google Cloud Run (Backend)

---

## Project Structure

```
Phylax/
├── backend/       # FastAPI service: text extraction, vector retrieval, and AI analysis
├── frontend/      # Next.js web dashboard: upload flow, clause cards, summary view
├── data/          # Statutory datasets and sample test documents
├── scripts/       # Offline database seeding and indexing tools
├── Dockerfile     # Backend container configuration for deployment
└── README.md
```

---

## Getting Started

### Prerequisites
* **Node.js** (v20+) & **npm**
* **Python** (v3.11+)
* **Google AI Studio API Key** (or compatible LLM key)
* **Supabase Project** with vector extension enabled

---

### 1. Clone & Configure Environment

```bash
git clone https://github.com/your-username/Phylax.git
cd Phylax
```

Create `.env` using `.env.example`:
```bash
cp .env.example .env
```

Set your configuration in `.env`:
```env
LLM_API_KEY=your_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

### 2. Backend Setup (FastAPI)

```bash
# Create and activate virtual environment
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Start backend development server
uvicorn backend.app.main:app --reload --port 8000
```

* Swagger API Docs: `http://localhost:8000/docs`
* Health Check: `http://localhost:8000/health`

---

### 3. Frontend Setup (Next.js)

```bash
cd frontend
npm install
npm run dev
```

* Open `http://localhost:3000` in your browser.

---

## Disclaimer

> [!WARNING]
> **Phylax is an AI-powered document analysis and comprehension tool.**
> It is designed to assist users in understanding agreements and identifying potentially problematic clauses by referencing public Indian statutes. It **does not constitute formal legal advice** and is not a substitute for consultation with a licensed legal practitioner.
