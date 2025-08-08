
function handleRegister(event) {
  event.preventDefault();
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const confirm = document.getElementById('confirm').value;

  if (password !== confirm) {
    alert("Passwords do not match!");
    return false;
  }

  localStorage.setItem("user", JSON.stringify({ name, email, password }));
  alert("Registration successful!");
  window.location.href = "signin.html";
  return false;
}

function handleLogin(event) {
  event.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const user = JSON.parse(localStorage.getItem("user"));

  if (!user || user.email !== email || user.password !== password) {
    alert("Invalid credentials!");
    return false;
  }

  alert("Login successful!");
  window.location.href = "index.html";
  return false;
}
