import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/discrepancies/";

function App() {
  const [data, setData] = useState([]);
  const [reason, setReason] = useState("");
  const [orgId, setOrgId] = useState("");
  const [sort, setSort] = useState("");
  
  const missingCount = data.filter(
  (item) => item.reason === "MISSING_IN_SYSTEM_B"
).length;

const mismatchCount = data.filter(
  (item) => item.reason === "VALUE_MISMATCH"
).length;

const orphanCount = data.filter(
  (item) => item.reason === "ORPHAN_IN_SYSTEM_B"
).length;

const duplicateCount = data.filter(
  (item) => item.reason === "DUPLICATE_IN_SYSTEM_B"
).length;

useEffect(() => {
  let url = API_URL;
  const params = new URLSearchParams();

  if (reason) params.append("reason", reason);
  if (sort) params.append("sort", sort);

  if (params.toString()) {
    url += `?${params.toString()}`;
  }

  fetch(url, {
    headers: {
      "X-Org-ID": orgId || "ORG-A",
    },
  })
    .then((response) => response.json())
    .then((result) => setData(result))
    .catch((error) => console.error("API error:", error));
}, [reason, orgId, sort]);

  return (
    <div className="app">
      <header>
        <h1>Cross-System Reconciliation</h1>
        <p>System A vs System B discrepancy audit</p>
      </header>

      <section className="filters">
        <div>
          <label>Reason</label>
          <select
            value={reason}
            onChange={(e) => setReason(e.target.value)}
          >
            <option value="">All Reasons</option>
            <option value="MISSING_IN_SYSTEM_B">
              Missing in System B
            </option>
            <option value="ORPHAN_IN_SYSTEM_B">
              Orphan in System B
            </option>
            <option value="DUPLICATE_IN_SYSTEM_B">
              Duplicate in System B
            </option>
            <option value="VALUE_MISMATCH">
              Value Mismatch
            </option>
          </select>
        </div>

        <div>
          <label>Organization</label>
          <select
            value={orgId}
            onChange={(e) => setOrgId(e.target.value)}
          >
            <option value="">All Organizations</option>
            <option value="ORG-A">ORG-A</option>
            <option value="ORG-B">ORG-B</option>
          </select>
        </div>

        <div>
          <label>Sort by Value</label>
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
          >
            <option value="">Default</option>
            <option value="value_a">System A: Low → High</option>
            <option value="-value_a">System A: High → Low</option>
            <option value="value_b">System B: Low → High</option>
            <option value="-value_b">System B: High → Low</option>
          </select>
        </div>
      </section>

 <section className="summary">
  <div className="summary-title">
    <strong>{data.length}</strong>
    <span> discrepancies found</span>
  </div>

  <div className="cards">
    <div className="card missing">
      <span className="card-number">{missingCount}</span>
      <span className="card-label">Missing in System B</span>
    </div>

    <div className="card mismatch">
      <span className="card-number">{mismatchCount}</span>
      <span className="card-label">Value Mismatch</span>
    </div>

    <div className="card orphan">
      <span className="card-number">{orphanCount}</span>
      <span className="card-label">Orphan in System B</span>
    </div>

    <div className="card duplicate">
      <span className="card-number">{duplicateCount}</span>
      <span className="card-label">Duplicate in System B</span>
    </div>
  </div>
</section>

      <section className="table-container">
        <table>
          <thead>
            <tr>
              <th>Record ID</th>
              <th>Reason</th>
              <th>Location</th>
              <th>Organization</th>
              <th>System A Value</th>
              <th>System B Value</th>
            </tr>
          </thead>

          <tbody>
            {data.map((item) => (
              <tr key={item.id}>
                <td>{item.record_id}</td>

                <td>
                  <span className={`badge ${item.reason}`}>
                    {item.reason.replaceAll("_", " ")}
                  </span>
                </td>

                <td>{item.location_id}</td>
                <td>{item.org_id}</td>
                <td>{item.val_a || "—"}</td>
                <td>{item.val_b || "—"}</td>
              </tr>
            ))}

            {data.length === 0 && (
              <tr>
                <td colSpan="6" className="empty">
                  No discrepancies found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </section>
    </div>
  );
}

export default App;