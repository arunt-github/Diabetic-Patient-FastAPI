document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("diabetesForm");

  form.addEventListener("submit", function(event) {
      event.preventDefault();

      const formData = new FormData(form);
      const data = {
          Name : formData.get("name"),
          Pregnancies: formData.get("pregnancies"),
          Glucose: formData.get("glucose"),
          BloodPressure: formData.get("bloodPressure"),
          SkinThickness: formData.get("skinThickness"),
          Insulin: formData.get("insulin"),
          Bmi: formData.get("bmi"),
          DiabetesPedigreeFunction: formData.get("diabetesPedigreeFunction"),
          Age: formData.get("age")
      };

      fetch("/submit", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(result => {
          alert(JSON.stringify(result));
      })
      .catch(error => {
          console.error("Error:", error);
      });
  });
});
