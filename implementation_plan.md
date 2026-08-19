# Lender Login & Loan Review Workflow

Add a complete lender portal where lenders can login, view pending loan applications, assess credit scores with graphical visualizations, and approve/reject/review applications. Customers who apply for loans now go into a "waiting" state, and are shown rejection reasons if rejected.

## Proposed Changes

### Backend – New Lender Model & DB Table

#### [NEW] [lender_account.py](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/backend/app/models/lender_account.py)
- New SQLAlchemy model `LenderAccount` with fields: `lender_id` (PK), `email` (unique), `password_hash`, `full_name`, `is_active`, `created_at`
- Separate from `UserAccount` — lenders are not applicants

#### [MODIFY] [__init__.py](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/backend/app/models/__init__.py)
- Import and register `LenderAccount` model

---

### Backend – Lender Auth & Security

#### [MODIFY] [security.py](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/backend/app/core/security.py)
- Add `create_lender_token()` that includes `"role": "lender"` in JWT payload
- Add `get_current_lender()` dependency that validates the JWT has `role=lender`

#### [NEW] [lender_repository.py](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/backend/app/repositories/lender_repository.py)
- `get_lender_by_email()`, `create_lender_account()`

#### [NEW] [lender_service.py](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/backend/app/services/lender_service.py)
- `register_lender()` – create lender with hashed password
- `login_lender()` – verify credentials, return lender JWT
- `get_pending_applications()` – fetch all applications with status = "Pending"
- `get_application_for_review()` – get full application details for any applicant (lender-facing)
- `update_application_decision()` – approve/reject/review an application, store rejection reason

---

### Backend – Lender API Routes

#### [NEW] [lender.py](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/backend/app/routers/lender.py)
- `POST /api/lender/login` – lender login
- `POST /api/lender/register` – lender registration (for seeding)
- `GET /api/lender/pending-applications` – list all pending applications
- `GET /api/lender/application/{application_id}` – full applicant details for review
- `POST /api/lender/application/{application_id}/decide` – approve/reject with reason

#### [MODIFY] [main.py](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/backend/app/main.py)
- Register the new `lender_router`

---

### Backend – Application Status Changes

#### [MODIFY] [application.py](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/backend/app/models/application.py)
- Add `rejection_reason` column (Text, nullable)
- Add `reviewed_by` column (BigInteger, FK to lender_account, nullable)

#### [MODIFY] [risk_service.py](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/backend/app/services/risk_service.py)
- Change: When a customer applies, set **all** applications to `status = "Pending"` initially regardless of the ML decision
- The ML assessment is still computed and stored, but the application waits for lender action
- For LOW risk: auto-approve immediately (lender sees it as pre-approved)
- For HIGH risk: auto-reject with risk factors as reason
- For MEDIUM risk: stays "Pending" for lender manual review

> [!IMPORTANT]
> **Design Decision**: Based on your request, LOW risk applications will be **auto-approved** (since they can be "directly approved"), HIGH risk will be **auto-rejected** with reasons shown to customer, and MEDIUM risk will be **left pending** for lender manual review. This matches your requirement flow. Is this correct, or should ALL applications wait for lender action?

---

### Backend – Schemas

#### [NEW] [lender.py](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/backend/app/schemas/lender.py)
- `LenderLoginRequest`, `LenderRegisterRequest`, `LenderTokenResponse`
- `PendingApplicationItem`, `PendingApplicationsResponse`
- `LenderDecisionRequest` (decision: approve/reject, rejection_reason: optional str)

#### [MODIFY] [loan.py](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/backend/app/schemas/loan.py)
- Add `rejection_reason` field to `ApplicationResponse` and `LoanHistoryItem`

---

### Frontend – Lender Login Page

#### [NEW] [LenderLogin.jsx](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/frontend/src/pages/LenderLogin.jsx)
- Separate login page with distinct branding ("Lender Portal")
- Email + password form, styled with the existing `auth.css` patterns but with a different color accent (e.g., deep purple/indigo theme)
- Stores `lender_token` separately from `access_token` in localStorage

#### [NEW] [lender-auth.css](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/frontend/src/styles/lender-auth.css)
- Lender-specific auth page styling with a distinctive dark/indigo gradient theme

---

### Frontend – Lender Dashboard

#### [NEW] [LenderDashboard.jsx](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/frontend/src/pages/LenderDashboard.jsx)
- Lists all pending loan applications in a table/card grid
- Each application shows: applicant name, loan amount, purpose, date, risk level badge
- "Assess Credit Score" button on each row → navigates to review page
- Stats at top: total pending, approved today, rejected today

#### [NEW] [LenderReview.jsx](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/frontend/src/pages/LenderReview.jsx)
- **Graphical customer information display**:
  - Credit score gauge chart (SVG arc)
  - Risk score bar chart
  - Debt-to-income ratio donut chart
  - Payment history timeline
  - Approval probability meter
  - Employment & income summary cards
- Decision buttons: "Approve" (green), "Reject" (red with reason textarea), "Send for Further Review"
- All charts built with pure SVG/CSS — no external charting library needed

#### [NEW] [lender-dashboard.css](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/frontend/src/styles/lender-dashboard.css)
- Premium dark theme dashboard for lender portal
- Glassmorphism cards, animated charts, gradient accents

#### [NEW] [lender-review.css](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/frontend/src/styles/lender-review.css)
- Styling for the graphical review page with chart containers and decision panel

---

### Frontend – Lender Services & Auth

#### [NEW] [lenderAuth.js](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/frontend/src/services/lenderAuth.js)
- `lenderLogin()`, `lenderLogout()`, `getLenderToken()`, `isLenderAuthenticated()`

#### [NEW] [lender.js](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/frontend/src/services/lender.js)
- `getPendingApplications()`, `getApplicationForReview(id)`, `submitDecision(id, decision, reason)`

---

### Frontend – Customer-Facing Changes

#### [MODIFY] [ApplyLoan.jsx](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/frontend/src/pages/ApplyLoan.jsx)
- After submission, show a **"Waiting for Approval"** status page instead of immediately redirecting to application details
- Display a pending animation with message: "Your application has been submitted and is being reviewed"

#### [MODIFY] [ApplicationDetails.jsx](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/frontend/src/pages/ApplicationDetails.jsx)
- Show rejection reason prominently if application was rejected
- Show "Under Review" badge for pending applications

---

### Frontend – Routing

#### [MODIFY] [App.jsx](file:///c:/Users/mukul/Downloads/credit_rating_for_faster_lending-main%20(1)1/credit_rating_for_faster_lending-main/frontend/src/App.jsx)
- Add routes:
  - `/lender/login` → `LenderLogin`
  - `/lender/dashboard` → `LenderDashboard` (protected with lender auth)
  - `/lender/review/:applicationId` → `LenderReview` (protected with lender auth)

---

## Open Questions

> [!IMPORTANT]
> **Auto-decision vs. all manual**: Should LOW risk loans be auto-approved and HIGH risk auto-rejected (with only MEDIUM going to lender review)? Or should ALL applications wait for the lender to take action regardless of risk level?

> [!NOTE]
> **Lender registration**: For now, I'll add a `/api/lender/register` endpoint for seeding lender accounts. In production this would be admin-only. Is that acceptable?

## Verification Plan

### Manual Verification
1. Customer applies for a loan → sees "waiting/pending" state
2. Lender logs in → sees list of pending applications
3. Lender clicks "Assess Credit Score" → sees graphical customer profile
4. LOW risk → auto-approved, customer sees approved status
5. HIGH risk → auto-rejected with reasons shown to customer
6. MEDIUM risk → lender reviews graphical data, clicks approve/reject
7. Rejected customer sees rejection reason on their application details page
