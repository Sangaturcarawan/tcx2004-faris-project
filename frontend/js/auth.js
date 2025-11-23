const API = "http://127.0.0.1:8000";

function saveToken(token) {
  localStorage.setItem("token", token);
}

function getToken() {
  return localStorage.getItem("token");
}

function login() {
  const email = document.getElementById("email").value;
  const pw = document.getElementById("password").value;

  fetch(API + "/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: email, password: pw }),
  })
    .then((res) => res.json())
    .then((data) => {
      saveToken(data.access_token);
      window.location.href = "dashboard.html";
    });
}

function signup() {
  const email = document.getElementById("email").value;
  const pw = document.getElementById("password").value;

  fetch(API + "/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: email, password: pw }),
  })
    .then((res) => res.json())
    .then(() => {
      window.location.href = "index.html";
    });
}
