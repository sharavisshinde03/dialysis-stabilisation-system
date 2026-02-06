function setPatient() {
  const payload = {
    name: document.getElementById("pname").value,
    id: document.getElementById("pid").value,
    age: document.getElementById("page").value,
    gender: document.getElementById("pgender").value,
    hours: document.getElementById("timeInput").value
  };

  fetch("/set_patient", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
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
    .then(res => res.json())
    .then(data => {
      if (data.patient) {
        document.getElementById("patientInfo").innerText =
          `${data.patient.name} | ${data.patient.age} | ${data.patient.gender}`;
      }

      document.getElementById("bloodFlow").innerText =
        data.blood_flow + " ml/min";

      document.getElementById("arterialPressure").innerText =
        data.arterial_pressure + " mmHg";

      document.getElementById("venousPressure").innerText =
        data.venous_pressure + " mmHg";

      document.getElementById("vibration").innerText =
        data.vibration + " g";

      document.getElementById("remainingTime").innerText =
        data.remaining_time;

      document.getElementById("status").innerText =
        data.system_state;

      const log = document.getElementById("alertLog");
      log.innerHTML = "";
      data.alerts.forEach(a => {
        log.innerHTML += `<li>[${a.time}] ${a.message}</li>`;
      });

      document.body.style.background =
        data.system_state === "EMERGENCY_STOP" ? "#ffcccc" : "white";
    });
}

setInterval(fetchData, 1000);
