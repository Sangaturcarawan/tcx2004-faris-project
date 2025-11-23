const API = "http://127.0.0.1:8000";

function loadGroups() {
  fetch(API + "/groups/", {
    headers: { Authorization: "Bearer " + getToken() },
  })
    .then((res) => res.json())
    .then((groups) => {
      const div = document.getElementById("group-list");
      div.innerHTML = "";

      groups.forEach((g) => {
        const html = `
                <div class="card">
                    <h3>${g.name}</h3>
                    <button onclick="openGroup(${g.id})">Open</button>
                </div>
            `;
        div.innerHTML += html;
      });
    });
}

function createGroup() {
  const name = document.getElementById("group-name").value;

  fetch(API + "/groups/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + getToken(),
    },
    body: JSON.stringify({ name }),
  }).then(() => loadGroups());
}

function openGroup(id) {
  window.location.href = `group.html?group_id=${id}`;
}

window.onload = async () => {
  const me = await fetch(API + "/me", {
    headers: { Authorization: "Bearer " + getToken() },
  }).then((r) => r.json());

  document.getElementById(
    "welcome"
  ).innerHTML = `<h2>Welcome, ${me.email}</h2>`;
};
