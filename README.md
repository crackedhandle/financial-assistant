# Dialysis Dashboard

A small, testable, event-driven monitoring system for dialysis units — built with **Express + TypeScript** (backend) and **React + Vite + TypeScript** (frontend).

---

## 📁 Project Structure

```
dialysis-dashboard/
├─ backend/                  # Express + TypeScript API
│  ├─ src/
│  │  ├─ config/
│  │  │  └─ clinical.config.ts
│  │  ├─ domain/             # Mongoose models (patient, session, schedule)
│  │  ├─ routes/             # patient.routes.ts, schedule.routes.ts, session.routes.ts
│  │  ├─ services/           # anomaly.service.ts (business logic)
│  │  ├─ seed.ts
│  │  ├─ app.ts
│  │  └─ server.ts
│  ├─ package.json
│  └─ tests/                 # Jest tests (anomaly + API)
├─ frontend/                 # Vite + React + TypeScript UI
│  ├─ src/
│  │  ├─ components/
│  │  ├─ api/client.ts       # Axios client
│  │  ├─ types/types.ts
│  │  ├─ App.tsx
│  │  └─ main.tsx
│  ├─ package.json
│  └─ vitest.config.ts       # UI tests
├─ README.pdf                # Project summary (same content)
└─ README.md                 # This file
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/crackedhandle/dialysis-dashboard.git
cd dialysis-dashboard
```

### 2. Backend — install, seed & run

```bash
cd backend
npm install
# Create .env file (see Environment Variables section below)
npm run seed
npm run dev
```

### 3. Frontend — install & run

```bash
cd frontend
npm install
npm run dev
```

### 4. Open in browser

| Service | URL |
|---|---|
| Backend OpenAPI / Swagger | http://localhost:5000/docs |
| Frontend UI | http://localhost:5173 |

---

## ⚙️ Environment Variables

Create a `.env` file inside the `backend/` folder:

```env
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/dialysis?retryWrites=true&w=majority"
PORT=5000
```

---

## 🪟 Windows (PowerShell) Commands

### Backend

```powershell
cd C:\path\to\dialysis-dashboard\backend

npm install          # Install dependencies
npm run seed         # Seed example data
npm run dev          # Start dev server (hot reload) on port 5000
```

### Frontend

```powershell
cd C:\path\to\dialysis-dashboard\frontend

npm install          # Install dependencies
npm run dev          # Start Vite dev server on port 5173
```

---

## 📖 API Reference

Swagger UI is available after starting the backend:

> **http://localhost:5000/docs**

You can test endpoints directly from the Swagger page, or via PowerShell:

```powershell
Invoke-RestMethod "http://localhost:5000/schedule/today?unitId=U1" | ConvertTo-Json -Depth 6
```

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Simple health-check |
| `GET` | `/schedule/today?unitId=U1` | Returns today's schedule for unit U1 |
| `POST` | `/sessions` | Create a dialysis session |

### `POST /sessions` — Example Request Body

```json
{
  "patientId": "69a3e480493547850cfc773c",
  "unitId": "U1",
  "startTime": "2026-03-01T07:02:25.437Z",
  "endTime": "2026-03-01T11:02:25.437Z",
  "preWeightKg": 74,
  "postWeightKg": 69,
  "systolicBP": 170,
  "diastolicBP": 90,
  "machineId": "M1"
}
```

---

## 🏥 Clinical Assumptions & Configuration

All thresholds are **explicit and centralized** in:

```
backend/src/config/clinical.config.ts
```

```ts
export const ClinicalConfig = {
  // Maximum allowed interdialytic weight gain (% of dry weight)
  maxInterdialyticGainPercent: 5,       // 5%

  // High post-dialysis systolic blood pressure threshold
  maxPostDialysisSystolicBP: 160,       // 160 mmHg

  // Target session duration and tolerance
  targetDurationMinutes: 240,           // 4 hours
  durationTolerancePercent: 0.25,       // ±25% → allowed: 180–300 minutes
};
```

No magic numbers anywhere else in the codebase — changing a threshold here propagates everywhere automatically.

---

## 🌱 Seed Script

The seed script populates the database with example patients and sessions for local development.

**Location:** `backend/src/seed.ts`

```bash
# Run from inside the backend/ folder
npm run seed
```

**What it creates:**

- **Patients:** Rahul Sharma, Anita Verma
- **Schedule entries** for today with `unitId = U1`
- **One session for Rahul** that includes anomalies:
  - Excess interdialytic weight gain
  - High post-dialysis systolic BP

To re-seed later (reset + regenerate sample data), simply run `npm run seed` again.

---

## 🔖 Git & Release Workflow

Use small atomic commits while developing:

```bash
git add .
git commit -m "feat(backend): add anomaly detection logic + tests"
git commit -m "feat(seed): add example seed data for U1 unit"
git commit -m "feat(frontend): initial dashboard and session modal"
```

When ready to release:

```bash
git tag v1.0
git push origin main --tags
```
