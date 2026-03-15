const routes = {
  "/": "resume-upload",
  "/dashboard": "dashboard",
  "/role-match": "role-match",
  "/skill-gap": "skill-gap",
  "/jobs": "jobs",
  "/projects": "projects",
  "/roadmap": "roadmap",
  "/interview": "interview-prep"
  
};

function router() {
  const path = location.hash.replace("#", "") || "/";
  const view = routes[path] || "resume-upload";
  render(view);
 
}



window.addEventListener("hashchange", router);
window.addEventListener("load", router);