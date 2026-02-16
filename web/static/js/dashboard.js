function setPatient() {
  const payload = {
    name: pname.value,
    age: page.value,
    gender: pgender.value,
    hours: timeInput.value
  };

  fetch("/set_patient", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  }).then(() => {
    patientInfo.innerText =
      `${payload.name} | Age ${payload.age} | ${payload.gender}`;
  });
}

function startSystem() {
  fetch("/start", { method: "POST" });
}

function stopSystem() {
  fetch("/stop", { method: "POST" });
}

function fetchData() {
  fetch("/data")
    .then(r => r.json())
    .then(d => {
      bloodFlow.innerText = d.blood_flow + " ml/min";
      arterialPressure.innerText = d.arterial_pressure + " mmHg";
      venousPressure.innerText = d.venous_pressure + " mmHg";
      vibration.innerText = d.vibration + " g";
      remainingTime.innerText = d.remaining_time;
      status.innerText = d.system_state;

      document.body.style.background =
        d.system_state === "EMERGENCY_STOP" ? "#7f1d1d" : "#0f172a";

      alertLog.innerHTML = "";
      d.alerts.forEach(a =>
        alertLog.innerHTML += `<li>[${a.time}] ${a.message}</li>`
      );
    });
}
function showDashboardPopup(message, type) {
  const popup = document.getElementById("alertPopup");
  popup.innerText = message;
  popup.className = `popup ${type}`;
  popup.classList.remove("hidden");

  setTimeout(() => {
    popup.classList.add("hidden");
  }, 5000);
}

setInterval(fetchData, 1000);

