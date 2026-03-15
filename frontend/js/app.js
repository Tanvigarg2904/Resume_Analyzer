 let interviewHistory = [];
 const AppState = {
  selectedFile: null,
  selectedRole: null,
  analysis: null,
 };

 function $(id) {
  return document.getElementById(id);
 }
 function create(tag, className){
  const el = document.createElement(tag);
  if(className) el.className = className;
  return el;
 }
 async function analyzeResume(file, role){
  const formData = new FormData();
  formData.append("file", file);
  formData.append("role", role);
  const res = await fetch("https://resume-analyzer-zji2.onrender.com/analyze", {
   method: "POST",
   body: formData
  });
  if(!res.ok) {
    console.error("Backend Error:");
    return null;
  }
  return await res.json();
  }
  function initUploadPage(){
    const fileInput = $("fileInput");
    const roleInput = $("roleInput");
    const analyzeBtn = $("analyzeBtn");
    const dropZone = $("dropZone");
    if(!fileInput) return;
    dropZone.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", (e) => {
      AppState.selectedFile = e.target.files[0];
      const fileName = document.getElementById("fileNameDisplay");
      if(fileName && AppState.selectedFile){
        fileName.innerText = "📄 " + AppState.selectedFile.name;
        
      }
      updateAnalyzeState();
    });
    roleInput.addEventListener("input", (e) => {
      AppState.selectedRole = e.target.value.trim();
      updateAnalyzeState();
    });
    analyzeBtn.addEventListener("click", runAnalysis);
  
  }
  function updateAnalyzeState(){
    const analyzeBtn = $("analyzeBtn");
    analyzeBtn.disabled = !(AppState.selectedFile && AppState.selectedRole);
  }
  async function runAnalysis(){
    const analyzeBtn = $("analyzeBtn");
    analyzeBtn.innerText = "Analyzing...";
    analyzeBtn.disabled = true;
    const result = await analyzeResume(AppState.selectedFile, AppState.selectedRole);
    if(!result) {
      alert("Analysis failed. Please try again.");
      analyzeBtn.innerText = "Analyze";
      analyzeBtn.disabled = false;
      return;
    }
    AppState.analysis = result;
    console.log("Analysis Result:", result);
    location.hash = "#/dashboard";

  }
  function render(view){
    switch(view){
      case "resume-upload":
        renderUploadPage();
        break;
      case "dashboard":
        renderDashboard();
        break;
        case "role-match":
          renderRoleMatch();
          break;
        case "skill-gap":
          renderSkillGap();
          break;
        case "jobs":
          renderJobs();
          break;

          case "projects":
            renderProjects();
            break;
            case "roadmap":
              renderRoadmap();
              break;
              case"interview-prep":
               renderInterviewPrep();
               break;
      default:
        renderUploadPage();
    }

  }
  function renderUploadPage(){

 const app = $("app");
 app.innerHTML = `
<div class="upload-page fade-in">

  <div class="hero">

    <div class="hero-left">

      <div class="logo-box">🧠</div>

      <h1 class="hero-title">
        SkillForge AI
        <span class="gradient-text">Career Intelligence</span>
      </h1>

      <p class="hero-sub">
        Analyze your resume, detect skill gaps, and generate a personalized
        career roadmap using AI.
      </p>

      <div class="feature-list">
        <div class="feature">⚡ ATS Match Score</div>
        <div class="feature">📊 Skill Gap Detection</div>
        <div class="feature">🧠 AI Career Roadmap</div>
      </div>

    </div>


    <div class="hero-right">

      <div id="dropZone" class="upload-box">

        <input
          id="fileInput"
          type="file"
          accept=".pdf"
          hidden
        />

        <div id="uploadContent">

          <div class="upload-icon">📄</div>

          <p class="upload-title">
            Upload Resume
          </p>

          <p class="upload-sub">
            Drag & drop your PDF here or click to browse
          </p>
          <p id = "fileNameDisplay" class = "file-name"></P>

        </div>

      </div>


      <div class="role-select">

        <input
          id="roleInput"
          class="input"
          placeholder="Target role (Frontend Developer, AI Engineer...)"
        />

      </div>


      <button
        id="analyzeBtn"
        class="analyze-btn"
        disabled
      >
        🚀 Start AI Analysis
      </button>

    </div>

  </div>

</div>
`;

 
     

   

 
 initUploadPage();

}
function renderSkills(containerId, skills){

const container = document.getElementById(containerId);

container.innerHTML = "";

skills.forEach(skill => {

const tag = document.createElement("span");

tag.className = "skill " + (containerId === "matchedSkills" ? "matched" : "missing");

tag.textContent = skill;

container.appendChild(tag);

});

}
function renderDashboard(){

 const data = AppState.analysis;

 if(!data){
  location.hash = "/";
  return;
 }

 const app = $("app");

 app.innerHTML = `
<div class="page dashboard-page fade-in">

 <h1 class="page-title">
  Dashboard
 </h1>

 <div class="dashboard-grid-3">

  <div class="card center ats-main-metric">
  <h3 class = "card-title">ATS Resume Score</h3>
   <div id="atsGaugeMount"></div>
  </div>

  <div class="card">
   <h3 class="card-title">Matched Skills</h3>
   <div id="matchedSkills"></div>
  </div>

  <div class="card">
   <h3 class="card-title">Missing Skills</h3>
   <div id="missingSkills"></div>
  </div>

 </div>

</div>
`;
$("atsGaugeMount").appendChild(createATSGauge(data.ats_score || 0));

renderSkills("matchedSkills", data.matched_skills || []);

renderSkills("missingSkills", data.missing_core_skills || []);

}
function renderJobs(){

 const jobs = AppState.analysis?.recommended_jobs;

 if(!jobs){
   $("app").innerHTML = "<p>No jobs found</p>";
   return;
 }

 const internships = jobs.internships || [];
 const remote = jobs.remote || [];
 const wfh = jobs.work_from_home || [];
 const fulltime = jobs.full_time || [];

 const allJobs = [
   ...internships,
   ...remote,
   ...wfh,
   ...fulltime
 ];

 const app = $("app");

 app.innerHTML = `
 <div class="page fade-in">

 <h1 class="page-title">Recommended Jobs</h1>

 <div class="job-filter-bar">

   <button class="job-filter active" data-type="all">
   All (${allJobs.length})
   </button>

   <button class="job-filter" data-type="Internship">
   Internships (${internships.length})
   </button>

   <button class="job-filter" data-type="Remote">
   Remote (${remote.length})
   </button>

   <button class="job-filter" data-type="Work From Home">
   WFH (${wfh.length})
   </button>

   <button class="job-filter" data-type="Full Time">
   Full Time (${fulltime.length})
   </button>

 </div>

 <div id="jobsMount" class="jobs-grid"></div>

 </div>
 `;

 const mount = $("jobsMount");

 function showJobs(type){

   mount.innerHTML = "";

   let filtered = allJobs;

   if(type !== "all"){
     filtered = allJobs.filter(j => j.job_type === type);
   }

   if(filtered.length === 0){
     mount.innerHTML = `<p>No jobs available</p>`;
     return;
   }

   filtered.forEach(job=>{
     mount.appendChild(createJobCard(job));
   });

 }

 showJobs("all");

 document.querySelectorAll(".job-filter")
 .forEach(btn=>{

   btn.addEventListener("click",()=>{

     document
      .querySelectorAll(".job-filter")
      .forEach(b=>b.classList.remove("active"));

     btn.classList.add("active");

     showJobs(btn.dataset.type);

   });

 });

}

function createJobCard(job){

const card = document.createElement("div");

card.className = "job-card";

card.innerHTML = `
<div class="job-card-header">

<div class="job-logo">
${job.company ? job.company[0] : "J"}
</div>

<div class="job-info">
<div class="job-title">${job.job_title || job.title || "Job Role"}</div>
<div class="job-company">${job.company || "Unknown Company"}</div>
</div>

</div>

<div class="job-meta">
<span class="job-tag location">${job.location || "Remote"}</span>
<span class="job-tag type">${job.job_type || "Job"}</span>
</div>

<button class="job-apply">Apply</button>
`;

return card;

}
function renderProjects(){

 const projects = AppState.analysis?.recommended_projects || [];

app.innerHTML = `
<div class="page fade-in">

 <h1 class="page-title">Projects</h1>

 <div id="projectsMount" class="projects-stack"></div>

</div>
`;

const mount = $("projectsMount");

if(projects.length === 0){
 mount.innerHTML = "<p>No projects generated yet</p>";
 return;
}

projects.forEach(project=>{
 mount.appendChild(createProjectCard(project));
});

}
function renderRoadmap(){

const roadmap = AppState.analysis?.learning_roadmap || [];

const app = $("app");

app.innerHTML = `
<div class="page fade-in">

<h1 class="page-title">🧠 AI Learning Roadmap</h1>

<div id="roadmapMount" class="roadmap-container"></div>

</div>
`;

const mount = $("roadmapMount");

if(!roadmap.length){
mount.innerHTML = "<p>No roadmap generated.</p>";
return;
}

roadmap.forEach(month=>{

const monthCard = create("div","roadmap-month");

monthCard.innerHTML = `
<div class="month-header">

<h2>📅 ${month.month}</h2>

<div class="month-line"></div>

</div>

<div class="weeks-container"></div>
`;

const weeksContainer = monthCard.querySelector(".weeks-container");

month.weeks.forEach(week=>{

const weekCard = create("div","roadmap-week");

weekCard.innerHTML = `

<div class="week-header">

<div class="timeline-dot"></div>

<h3>${week.week}</h3>

<span class="expand-icon">▼</span>

</div>

<div class="week-focus">
🎯 <strong>Focus:</strong> ${week.focus}
</div>

<div class="week-details">

<div class="detail-block">
<h4>🎯 Goals</h4>
<ul>
${week.goals.map(g=>`<li>${g}</li>`).join("")}
</ul>
</div>

<div class="detail-block">
<h4>📚 Resources</h4>
<ul>
${week.resources.map(r=>`<li>${r}</li>`).join("")}
</ul>
</div>

<div class="detail-block">
<h4>💻 Practice</h4>
<ul>
${week.practice.map(p=>`<li>${p}</li>`).join("")}
</ul>
</div>

<div class="mini-project">
🚀 Mini Project: ${week.mini_project}
</div>

</div>
`;

weekCard.addEventListener("click",()=>{
weekCard.classList.toggle("active");
});

weeksContainer.appendChild(weekCard);

});

mount.appendChild(monthCard);

});

}

function createATSGauge(score)
{
  console.log("ATS score:",score);

const radius = 100;
const circumference = 2 * Math.PI * radius;
const offset = circumference - (score / 100) * circumference;

/* SCORE COLOR SYSTEM */

let color;
let glow;

if(score < 40){
  color = "#ef4444";
glow = "rgba(239,68,68,0.8)";
  

}
else if(score < 70){
  color = "#f59e0b";
glow = "rgba(245,158,11,0.8)";
  

}
else{
color = "#22c55e";
glow = "rgba(34,197,94,0.8)";
}

const wrapper = document.createElement("div");
wrapper.className = "ats-circle";

wrapper.innerHTML = `
<svg width="300" height="300">

<circle
cx="150"
cy="150"
r="${radius}"
stroke="#1e293b"
stroke-width="16"
fill="none"
/>

<circle
cx="150"
cy="150"
r="${radius}"
stroke="${color}"
stroke-width="16"
fill="none"
stroke-linecap="round"
stroke-dasharray="${circumference}"
stroke-dashoffset="${circumference}"
style="filter: drop-shadow(0 0 14px ${glow});"
/>

</svg>

<div class="ats-score">${score}%</div>
`;

setTimeout(()=>{
wrapper.querySelectorAll("circle")[1].style.strokeDashoffset = offset;
},100);

return wrapper;

}




function createProjectCard(project){

 const card = create("div","project-card-modern");

 const tech = project.tech_stack || [];
 const features = project.major_features || [];
 const learn = project.learning_outcomes || [];

 card.innerHTML = `
 
 <div class="project-top">

   <div class="project-icon">💻</div>

   <h3 class="project-name">
   ${project.project_name}
   </h3>

 </div>


 <p class="project-desc">
 ${project.problem_statement}
 </p>


 <div class="project-section">

   <span class="section-title">Tech Stack</span>

   <div class="tag-row">
     ${tech.map(t=>`<span class="tech-tag">${t}</span>`).join("")}
   </div>

 </div>


 <div class="project-section">

   <span class="section-title">Key Features</span>

   <ul class="feature-list">
     ${features.map(f=>`<li>${f}</li>`).join("")}
   </ul>

 </div>


 <div class="project-section">

   <span class="section-title">Skills You Gain</span>

   <div class="tag-row">
     ${learn.map(l=>`<span class="skill-tag">${l}</span>`).join("")}
   </div>

 </div>


 <div class="project-footer">

   <button class="project-btn">
   Build This Project
   </button>

 </div>

 `;

 return card;

}
function renderSkillGap(){

const matched = AppState.analysis?.matched_skills || [];
const missing = AppState.analysis?.missing_core_skills || [];

const total = matched.length + missing.length;
const percent = total ? Math.round((matched.length / total) * 100) : 0;

const app = $("app");
console.log("Matched Skills:", matched);
console.log("Missing Skills:", missing);

 app.innerHTML = `
<div class="page fade-in">

<h1 class="page-title">Skill Gap Intelligence</h1>

<div class="skill-layout">

<div class="score-card">
<h3>Skill Match</h3>

<div class="score-circle">
${percent}%
</div>

<p class="score-text">
Based on your resume analysis
</p>
</div>


<div class="radar-card">
<h3>Skill Radar</h3>
<canvas id="skillRadar"></canvas>
</div>
</div>

<div class="matched-card">
<h3>Matched Skills</h3>
<div class="skills">

${matched.map(s=>`
<span class="skill matched">${s}</span>
`).join("")}

</div>
</div>

<div class="missing-card">
<h3>Missing Skills</h3>

<div class="skills">

${missing.map(s=>`
<span class="skill missing">${s}</span>
`).join("")}

</div>

</div>

<div class="ai-card">
<h3>AI Suggestions</h3>

<ul>
${missing.map(s=>`
<li>Improve <b>${s}</b> to increase role match.</li>
`).join("")}
</ul>

</div>


`;

   

 drawRadar(matched, missing);
}
function drawRadar(matched, missing){

 const canvas = document.getElementById("skillRadar");
 if(!canvas) return;

 const ctx = canvas.getContext("2d");

 const skills = [...matched.slice(0,3), ...missing.slice(0,3)];
 if(skills.length === 0) return;

 const values = skills.map(s => matched.includes(s) ? 0.8 : 0.35);

 canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

 const centerX = canvas.width / 2;
 const centerY = canvas.height / 2;
 const radius = Math.min(centerX, centerY) - 40;
 const angleStep = (Math.PI*2)/skills.length;

 let progress = 0;

 function animate(){

  progress += 0.02;
  if(progress > 1) progress = 1;

  ctx.clearRect(0,0,canvas.width,canvas.height);

  ctx.strokeStyle="#00d4ff";
  ctx.lineWidth=1;
  ctx.font="12px Inter";

  skills.forEach((skill,i)=>{
    const angle=i*angleStep;
    const x=centerX+radius*Math.cos(angle);
    const y=centerY+radius*Math.sin(angle);

    ctx.beginPath();
    ctx.moveTo(centerX,centerY);
    ctx.lineTo(x,y);
    ctx.stroke();

    ctx.fillStyle="#aaa";
    const shortSkill = skill.split(" ").slice(0,2).join(" ");
    ctx.fillText(shortSkill,x+5,y+5);
  });

  ctx.beginPath();

  skills.forEach((skill,i)=>{
    const angle=i*angleStep;
    const r=radius*(values[i]*progress);

    const x=centerX+r*Math.cos(angle);
    const y=centerY+r*Math.sin(angle);

    if(i===0) ctx.moveTo(x,y);
    else ctx.lineTo(x,y);
  });

  ctx.closePath();

  ctx.fillStyle="rgba(0,212,255,0.25)";
  ctx.fill();

  ctx.strokeStyle="#00e5ff";
  ctx.lineWidth=2;
  ctx.stroke();

  if(progress<1) requestAnimationFrame(animate);

 }

 animate();
}
function renderRoleMatch(){

const role = AppState.analysis?.target_role || "Target Role";
const score = AppState.analysis?.ats_score || 0;

const matched = AppState.analysis?.matched_skills || [];
const missing = AppState.analysis?.missing_core_skills || [];

const marketDemand = AppState.analysis?.market_demand ?? 50;

const alignment = matched.length + missing.length
 ? Math.round((matched.length/(matched.length+missing.length))*100)
 : 0;

const stackReadiness = Math.min(100, matched.length*15);

const insight = `
Your resume shows strong ${matched.slice(0,2).join(", ") || "technical"} skills.
However ${missing.slice(0,2).join(", ") || "some important skills"} are missing
which lowers ATS compatibility for ${role}.
`;

const app = document.getElementById("app");

app.innerHTML = `
<div class="page fade-in">

<h1 class="page-title">Role Fit Compass</h1>

<div class="ai-insight">
<h3>AI Career Insight</h3>
<p>${insight}</p>
</div>

<div class="ats-section">

<h3>ATS Compatibility</h3>

<div class="ats-circle">

<svg width="260" height="260">

<defs>
<linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#22d3ee"/>
<stop offset="100%" stop-color="#6366f1"/>
</linearGradient>
</defs>

<circle cx="130" cy="130" r="110"
stroke="#333"
stroke-width="14"
fill="none"
/>

<circle
id="atsProgress"
cx="130"
cy="130"
r="110"
stroke="url(#grad)"
stroke-width="14"
fill="none"
stroke-dasharray="691"
stroke-dashoffset="691"
/>

</svg>

<div class="ats-score">${score}%</div>

</div>

</div>

<div class="metrics-row">

${metricGauge("Skill Alignment",alignment)}

${metricGauge("Stack Readiness",stackReadiness)}

${metricGauge("Market Demand",marketDemand)}

</div>

<div class="role-summary">
<h2>${role}</h2>
<p>This role matches your resume based on your current skills and experience.</p>
</div>

</div>
`;

animateATS(score);

}
function metricGauge(label,value){

return `
<div class="metric-card">

<div class="metric-circle">

<svg width="140" height="140">

<circle cx="70" cy="70" r="55"
stroke="#333"
stroke-width="10"
fill="none"
/>

<circle
cx="70"
cy="70"
r="55"
stroke="#22d3ee"
stroke-width="10"
fill="none"
stroke-dasharray="345"
stroke-dashoffset="${345 - (345*value/100)}"
/>

</svg>

<span>${value}%</span>

</div>

<p>${label}</p>

</div>
`;

}

function animateATS(score){

 const circle = document.getElementById("atsProgress");
 if(!circle) return;

 const circumference = 691;
 const offset = circumference - (score/100)*circumference;

 setTimeout(()=>{
   circle.style.strokeDashoffset = offset;
 },100);
}
function renderInterviewPrep(){

 const app = $("app");

 app.innerHTML = `

 <div class="page fade-in">

   <h1 class="page-title_chat">AI Interview Coach</h1>

   <div class="chat-container">

      <div id="chatMessages" class="chat-messages">
         <div class="bot-msg">
           Hello! I'm your AI Interview Coach.  
           Ask me anything about your upcoming interview.
         </div>
      </div>

      <div class="chat-input-box">

         <input 
            id="chatInput"
            placeholder="Ask interview question..." onkeydown ="if(event.key === 'Enter') sendInterviewMwssage()"
         />

         <button onclick="sendInterviewMessage()">
            Send
         </button>

      </div>

   </div>

 </div>
 `;
}

async function sendInterviewMessage(initialMessage = null){

const input = document.getElementById("chatInput");
const message =  initialMessage || input.value.trim();

if(!message) return;

const chat = document.getElementById("chatMessages");

/* Show user message */

chat.innerHTML += `<div class="user-msg">${message}</div>`;
chat.scrollTop = chat.scrollHeight;

input.value="";

/* Add to history */

interviewHistory.push({
role:"user",
content:message
});

const response = await fetch("https://resume-analyzer-zji2.onrender.com/interview-chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

message:message,
role: AppState.selectedRole || "Software Engineer",
resume_text:"",
chat_history: interviewHistory

})

});

const data = await response.json();

/* Show bot message */

chat.innerHTML += `<div class="bot-msg">${data.response}</div>`;

/* Save bot response */

interviewHistory.push({
role:"assistant",
content:data.response
});

chat.scrollTop = chat.scrollHeight;

}