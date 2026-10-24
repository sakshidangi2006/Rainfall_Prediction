
const API_URL = "http://127.0.0.1:8000";

const button = document.getElementById("predictButton");
const subdivisionSelect = document.getElementById("subdivision");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const error = document.getElementById("error");
const predictionValue = document.getElementById("predictionValue");

// Load the exact subdivisions supported by the trained model.
async function loadSubdivisions() {
    try {
        const response = await fetch(`${API_URL}/subdivisions`);

        if (!response.ok) {
            throw new Error("Could not load subdivisions.");
        }

        const data = await response.json();

        subdivisionSelect.replaceChildren(
            new Option("Select a subdivision", "")
        );

        data.subdivisions.forEach((name) => {
            subdivisionSelect.add(new Option(name, name));
        });

    } catch (err) {
        console.error("Subdivision loading error:", err);

        subdivisionSelect.replaceChildren(
            new Option("Unable to load subdivisions", "")
        );

        error.textContent =
            "Could not load subdivisions. Check that the API is running.";
        error.classList.remove("hidden");
    }
}

loadSubdivisions();

button.addEventListener("click", async function () {
    error.classList.add("hidden");
    result.classList.add("hidden");

    const subdivision = subdivisionSelect.value;

    if (!subdivision) {
        error.textContent = "Please select a subdivision.";
        error.classList.remove("hidden");
        return;
    }

    const inputIds = ["year1", "year2", "year3", "year4", "year5"];
    const values = inputIds.map((id) =>
        document.getElementById(id).value.trim()
    );

    if (values.some((value) => value === "")) {
        error.textContent =
            "Please enter rainfall values for all five years.";
        error.classList.remove("hidden");
        return;
    }

    const rainfall = values.map(Number);

    if (rainfall.some((value) => !Number.isFinite(value) || value < 0)) {
        error.textContent =
            "Enter valid, non-negative rainfall values.";
        error.classList.remove("hidden");
        return;
    }

    const requestData = {
        subdivision: subdivision,
        annual_lag1: rainfall[0],
        annual_lag2: rainfall[1],
        annual_lag3: rainfall[2],
        annual_lag4: rainfall[3],
        annual_lag5: rainfall[4]
    };

    loading.classList.remove("hidden");
    button.disabled = true;

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            const detail = data.detail;
            throw new Error(
                typeof detail === "string"
                    ? detail
                    : "Prediction request failed."
            );
        }

        const prediction = Number(
            data.predicted_next_year_annual_rainfall_mm
        );

        if (!Number.isFinite(prediction)) {
            throw new Error("The API returned an invalid prediction.");
        }

        predictionValue.textContent = prediction.toFixed(2);
        document.getElementById("resultSubdivision").textContent = subdivision;
        result.classList.remove("hidden");

    } catch (err) {
        console.error("Prediction error:", err);

        error.textContent =
            err.message || "Unable to connect to the prediction API.";
        error.classList.remove("hidden");

    } finally {
        loading.classList.add("hidden");
        button.disabled = false;
    }
});
