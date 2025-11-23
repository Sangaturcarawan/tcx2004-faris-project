const API = "http://127.0.0.1:8000";

const params = new URLSearchParams(window.location.search);
const groupId = params.get("group_id");

document.getElementById("group-title").innerText = "Group #" + groupId;

function addExpense() {
  const amount = document.getElementById("amount").value;
  const desc = document.getElementById("description").value;

  fetch(`${API}/expenses/group/${groupId}`, {
    method: "POST",
    headers: {
      Authorization: "Bearer " + getToken(),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ amount, description: desc }),
  }).then(loadExpenses);
}

function loadExpenses() {
  fetch(`${API}/expenses/group/${groupId}`, {
    headers: { Authorization: "Bearer " + getToken() },
  })
    .then((res) => res.json())
    .then((list) => {
      const div = document.getElementById("expense-list");
      div.innerHTML = "";

      list.forEach((e) => {
        div.innerHTML += `
                <p><b>${e.description}</b> - $${e.amount}  
                <br><small>${e.created_at}</small></p>
                <div class="divider"></div>
            `;
      });
    });
}

window.onload = loadExpenses;
