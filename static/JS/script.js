// document.addEventListener('DOMContentLoaded',function(){
//   const form = document.getElementById('diabetesForm')
//   const message = document.getElementById('message')

//   form.addEventListener('submit', async function(event)
//   {
//     const formData = new FormData(event.target);
//     const data = Object.fromEntries(formData.entries());
    
//     try{
//       const response = await fetch('http://127.0.0.1:8000/submit',
//         {
//           method : 'POST',
//           headers:{'Content-Type': 'application/json',},
//           body:JSON.stringify({
//             Pregnancies: parseInt(data.pregnancies),
//             Glucose: parseInt(data.glucose),
//             BloodPressure: parseInt(data.bloodPressure),
//             SkinThickness: parseInt(data.skinThickness),
//             Insulin: parseInt(data.insulin),
//             Bmi: parseFloat(data.bmi),
//             DiabetesPedigreeFunction: parseFloat(data.diabetesPedigreeFunction),
//             Age: parseInt(data.age),
//           })
//         })
//     }
//   })

// })



document.getElementById('diabetesForm').addEventListener('submit', async function(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData.entries());

  try {
    const response = await fetch('http://127.0.0.1:8000/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        Pregnancies: parseInt(data.pregnancies),
        Glucose: parseInt(data.glucose),
        BloodPressure: parseInt(data.bloodPressure),
        SkinThickness: parseInt(data.skinThickness),
        Insulin: parseInt(data.insulin),
        Bmi: parseFloat(data.bmi),
        DiabetesPedigreeFunction: parseFloat(data.diabetesPedigreeFunction),
        Age: parseInt(data.age),
      }),
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Prediction:', result);
      alert(result.Patient);
    } else {
      console.error('Error:', response.statusText);
      alert('Failed to get prediction. Please try again.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred. Please try again.');
  }
});
