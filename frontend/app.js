document.getElementById("connectBtn").onclick = connectDB;
document.getElementById("uploadBtn").onclick = uploadDocs;
document.getElementById("askBtn").onclick = ask;

const API_BASE = "http://127.0.0.1:8000";  // backend URL

async function connectDB() {
  const conn = document.getElementById("conn").value;
  const form = new FormData();
  form.append("connection_string", conn);
  const res = await fetch(`${API_BASE}/api/connect-database`, { 
    method: "POST", 
    body: form 
  });
  const j = await res.json();
  document.getElementById("schema").innerText = JSON.stringify(j.schema, null, 2);
}

async function uploadDocs() {
  const files = document.getElementById("docs").files;
  const fd = new FormData();
  for (let f of files) fd.append("files", f);
  const res = await fetch(`${API_BASE}/api/upload-documents`, { 
    method: "POST", 
    body: fd 
  });
  const j = await res.json();
  alert("Processed: " + j.count);
}

async function ask() {
  const q = document.getElementById("query").value;
  const res = await fetch(`${API_BASE}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: q })
  });
  const j = await res.json();
  document.getElementById("results").innerText = JSON.stringify(j, null, 2);
}

