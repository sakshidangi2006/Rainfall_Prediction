console.log("SCRIPT.JS IS LOADED");

const button = document.getElementById("predictButton");

console.log("PREDICT BUTTON:", button);

button.addEventListener("click", async function () {


console.log("PREDICT BUTTON CLICKED");


// Get raw input values first
const input1 = document.getElementById("year1").value.trim();
const input2 = document.getElementById("year2").value.trim();
const input3 = document.getElementById("year3").value.trim();
const input4 = document.getElementById("year4").value.trim();
const input5 = document.getElementById("year5").value.trim();


// Validate empty fields
if (
    input1 === "" ||
    input2 === "" ||
    input3 === "" ||
    input4 === "" ||
    input5 === ""
) {

    document.getElementById("error").textContent =
        "Please enter rainfall values for all five years.";

    document.getElementById("error").classList.remove("hidden");

    document.getElementById("result").classList.add("hidden");

    return;
}


// Convert values to numbers
const year1 = Number(input1);
const year2 = Number(input2);
const year3 = Number(input3);
const year4 = Number(input4);
const year5 = Number(input5);


// Validate numbers
if (
    !Number.isFinite(year1) ||
    !Number.isFinite(year2) ||
    !Number.isFinite(year3) ||
    !Number.isFinite(year4) ||
    !Number.isFinite(year5)
) {

    document.getElementById("error").textContent =
        "Please enter valid rainfall numbers.";

    document.getElementById("error").classList.remove("hidden");

    return;
}


// Rainfall cannot be negative
if (
    year1 < 0 ||
    year2 < 0 ||
    year3 < 0 ||
    year4 < 0 ||
    year5 < 0
) {

    document.getElementById("error").textContent =
        "Rainfall values cannot be negative.";

    document.getElementById("error").classList.remove("hidden");

    return;
}


const requestData = {

    annual_lag1: year1,
    annual_lag2: year2,
    annual_lag3: year3,
    annual_lag4: year4,
    annual_lag5: year5

};


console.log("REQUEST DATA:", requestData);


document.getElementById("loading").classList.remove("hidden");

document.getElementById("result").classList.add("hidden");

document.getElementById("error").classList.add("hidden");


try {

    console.log("CALLING FASTAPI...");


    const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(requestData)
        }
    );


    console.log("API STATUS:", response.status);


    if (!response.ok) {

        throw new Error(
            `API returned status ${response.status}`
        );

    }


    const data = await response.json();


    console.log("API RESPONSE:", data);


    const prediction =
        Number(data.predicted_annual_rainfall_mm);


    document.getElementById("predictionValue").textContent =
        prediction.toFixed(2);


    document.getElementById("result").classList.remove("hidden");


} catch (error) {

    console.error("API ERROR:", error);


    document.getElementById("error").textContent =
        "Unable to connect to the prediction API.";

    document.getElementById("error").classList.remove("hidden");


} finally {

    document.getElementById("loading").classList.add("hidden");

}

});
