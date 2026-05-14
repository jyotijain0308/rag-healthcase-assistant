
---

# Frontend README (`frontend/README.md`)

```md
# RAG Healthcare Assistant — Frontend

A Next.js frontend for interacting with the Healthcare RAG Assistant.

Features:

- JWT Authentication
- RBAC UI Protection
- PDF Upload
- AI Chat Interface
- Secure Route Middleware
- Radix UI + Tailwind UI

---

# Tech Stack

- Next.js 15+
- React
- TypeScript
- Tailwind CSS
- Radix UI
- JWT Auth

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository_url>
cd frontend

## 2. Install Dependencies
npm install

## 3. Configure Environment Variables
# Create .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
JWT_SECRET=your_secret_key

## 4. Run Application
npm run dev

# Frontend will run on 
http://localhost:3000

Features
Authentication
Login
Logout
JWT Token Storage
Token Expiration Handling
Role-Based Access Control

Protected routes using middleware.

Example:

/upload → Admin only
/chat → Authenticated users