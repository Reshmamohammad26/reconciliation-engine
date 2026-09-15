# Engineering Decisions

## 1. Store source values as text

### Decision
Store imported numeric-looking values as text.

### Rejected alternative
Store all values immediately as Decimal or Float.

### Reasoning
The assignment contains dirty data, including blank and potentially unparseable numeric values. Storing the original value prevents rows from being silently lost during import.

---

## 2. Use a database reconciliation result table

### Decision
Store detected discrepancies in a `Discrepancy` model.

### Rejected alternative
Calculate discrepancies only when the frontend requests the API.

### Reasoning
A separate discrepancy table makes the reconciliation result easy to inspect, test, filter, and expose through the API.

---

## 3. Group System B records by record reference

### Decision
Group System B records using `record_ref`.

### Rejected alternative
Assume every System B record has a unique reference.

### Reasoning
System B deliberately contains duplicate references. Grouping records allows the system to identify duplicate discrepancies instead of silently choosing one record.

---

## 4. Resolve organization through location

### Decision
Determine the organization from the location mapping.

### Rejected alternative
Trust the organization supplied by the source transaction row.

### Reasoning
The assignment defines the relationship between locations and organizations. Using the location mapping provides a consistent tenant boundary.

---

## 5. Filter tenant data in the backend

### Decision
Apply organization filtering in the API queryset.

### Rejected alternative
Fetch all discrepancies and filter them only in React.

### Reasoning
Client-side filtering would expose data belonging to other organizations. Filtering must happen on the backend.

---

## 6. Keep malformed references

### Decision
Do not normalize or silently discard malformed record references during import.

### Rejected alternative
Automatically modify malformed IDs to make them match.

### Reasoning
The assignment requires dirty data to survive the import. Keeping the original value makes the discrepancy visible and auditable.

---

## 7. Use React with Vite

### Decision
Use React + Vite for the frontend.

### Rejected alternative
Build the UI entirely with Django templates.

### Reasoning
The assignment allows React/Next and the reconciliation table requires interactive filtering and sorting. React provides a simple way to implement these interactions.

---

## 8. Use REST API between frontend and backend

### Decision
Expose discrepancies through Django REST Framework.

### Rejected alternative
Have React access the database or use server-rendered HTML.

### Reasoning
A REST API separates the frontend from the backend and makes the reconciliation results reusable by other clients.

## 9. Run reconciliation explicitly

### Decision
Use a Django management command:

```text
python manage.py reconcile