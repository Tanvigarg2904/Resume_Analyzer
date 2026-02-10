

async function analyze() {

  const file = document.getElementById("resume").files[0];
  const role = document.getElementById("role").value;
  const status = document.getElementById("status");

  if (!file || !role) {
    alert("Upload resume and enter role");
    return;
  }

  status.innerText = "Analyzing with AI agents...";

  const fd = new FormData();
  fd.append("file", file);
  fd.append("role", role);

  try {
    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: fd
    });

    const d = await res.json();
    
    setJobs(d.jobs || []);


    window.lastResponse = d;
console.log("FULL RESPONSE", d);

    

    status.innerText = "";

    animate(d.ats_score || 0);

    document.getElementById("snapshot").innerHTML =
      `<p>${d.snapshot?.role_fit}</p>
       <p>${d.snapshot?.seniority}</p>
       <p>${d.snapshot?.readiness}</p>`;

    renderPills("skills", d.skills?.matched || []);
    renderPills("core-skills", d.core_role_skills || []);
    renderList("gaps", d.gaps || []);

    
    renderRoadmap(d);
    renderProjects(d.projects || []);

  } catch (e) {
    console.error(e);
    status.innerText = "Backend error. Check server.";
  }
}

/* HELPERS */

function renderPills(id, list) {
  document.getElementById(id).innerHTML =
    list.map(s => `<span>${s}</span>`).join("");
}

function renderList(id, list) {
  document.getElementById(id).innerHTML =
    list.map(i => `<li>${i}</li>`).join("");
}


 // ================= JOB SYSTEM =================

let jobsData = [];

function setJobs(jobs){
 jobsData = jobs || [];
 renderJobs(jobsData);
}

// MAIN RENDER
function renderJobs(list){

 const el = document.getElementById("jobs-list");

 if(!el) return;

 if(!list.length){
  el.innerHTML = "<p>No jobs found.</p>";
  return;
 }

 el.classList.remove("skeleton");

 el.innerHTML = list.map((j,i)=>`
  <div class="job-card">
   <b>#${i+1} ${j.title}</b><br>
   ${j.company || ""} — ${j.location || ""}<br><br>
   <a href="${j.link}" target="_blank">Apply</a>
  </div>
 `).join("");
}

// FILTER
function filterJobs(type){

 document.querySelectorAll(".filter")
  .forEach(f=>f.classList.remove("active"));

 event.target.classList.add("active");

 if(type==="all"){
  renderJobs(jobsData);
  return;
 }

 const out = jobsData.filter(j=>{
  const t = (j.title||"").toLowerCase();
  if(type==="intern") return t.includes("intern");
  if(type==="remote") return t.includes("remote");
  if(type==="full") return t.includes("full");
 });

 renderJobs(out);
}


// defensive helper to avoid accidental HTML injection
function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderRoadmap(d) {
  try {
    // visible debug - remove or comment in production
    console.log("renderRoadmap input:", d?.roadmap);

    const m1 = Array.isArray(d?.roadmap?.month1) ? d.roadmap.month1 : (d?.roadmap?.month1 ? [d.roadmap.month1] : []);
    const m2 = Array.isArray(d?.roadmap?.month2) ? d.roadmap.month2 : (d?.roadmap?.month2 ? [d.roadmap.month2] : []);
    const m3 = Array.isArray(d?.roadmap?.month3) ? d.roadmap.month3 : (d?.roadmap?.month3 ? [d.roadmap.month3] : []);

    const asList = (arr) => arr.length ? `<ul>${arr.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>` : `<p class="muted">No roadmap items</p>`;

    const el1 = document.getElementById("month1");
    const el2 = document.getElementById("month2");
    const el3 = document.getElementById("month3");

    if (!el1 || !el2 || !el3) {
      console.warn("renderRoadmap: missing month elements", { el1, el2, el3 });
      return;
    }

    el1.innerHTML = `<h4>Month 1</h4>${asList(m1)}`;
    el2.innerHTML = `<h4>Month 2</h4>${asList(m2)}`;
    el3.innerHTML = `<h4>Month 3</h4>${asList(m3)}`;

    // If you want small animation (fade in)
    [el1, el2, el3].forEach((el, i) => {
      el.style.opacity = 0;
      el.style.transition = "opacity 320ms ease " + (i * 80) + "ms";
      requestAnimationFrame(() => { el.style.opacity = 1; });
    });

  } catch (err) {
    console.error("renderRoadmap error:", err);
  }
}

function renderProjects(p) {
  const el = document.getElementById("projects-list");
  el.classList.remove("skeleton");

  el.innerHTML = p.map(pr => `
    <div class="job">
      <b>${pr.title}</b>
      <p>${pr.description}</p>
    </div>
  `).join("");
}


  function animate(score){

 let c = document.getElementById("ats");
 let bar = document.getElementById("ats-fill");
 let confidence = document.getElementById("confidence");

 let cur = 0;

 bar.style.width = score + "%";

 if(score < 40) confidence.innerText = "Low Match";
 else if(score < 65) confidence.innerText = "Medium Match";
 else confidence.innerText = "Strong Match";

 let t = setInterval(()=>{
  if(cur>=score){
   clearInterval(t);
   return;
  }
  cur++;
  c.innerText = cur+"%";
  c.style.background =
   `conic-gradient(#2563eb ${cur*3.6}deg,#111 0deg)`;
 },10);
}
