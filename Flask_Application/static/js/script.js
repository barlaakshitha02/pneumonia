
const uploadForm = document.getElementById("uploadForm");
const imageInput = document.getElementById("imageInput");

const previewImage = document.getElementById("previewImage");

const loadingSection = document.getElementById("loadingSection");

const resultSection = document.getElementById("resultSection");

const resultImage = document.getElementById("resultImage");

const predictionText = document.getElementById("predictionText");

const confidenceText = document.getElementById("confidenceText");


// ===============================
// Enhanced for input file
// ===============================

const uploadArea = document.getElementById("uploadArea");
const browseBtn = document.getElementById("browseBtn");
const loadingImage = document.getElementById("loadingImage");
const progressBar = document.getElementById("progressBar");
const loadingText = document.getElementById("loadingText");


const generateReportBtn = document.getElementById("generateReportBtn");
const patientName = document.getElementById("patientName");
const patientAge = document.getElementById("patientAge");
const patientGender = document.getElementById("patientGender");


browseBtn.addEventListener("click", () => {

    imageInput.click();

});
// ===============================
// Image Preview
// ===============================

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) return;

    const imageUrl = URL.createObjectURL(file);

    console.log(imageUrl);

    previewImage.src = imageUrl;

    previewImage.classList.remove("d-none");

    previewImage.style.display = "block";

});



uploadArea.addEventListener("dragover", (e) => {

    e.preventDefault();

    uploadArea.classList.add("dragover");

});

uploadArea.addEventListener("dragleave", () => {

    uploadArea.classList.remove("dragover");

});

uploadArea.addEventListener("drop", (e) => {

    e.preventDefault();

    uploadArea.classList.remove("dragover");

    imageInput.files = e.dataTransfer.files;

    imageInput.dispatchEvent(new Event("change"));

});

// ===============================
// Upload Form Submit
// ===============================

uploadForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const file = imageInput.files[0];

    if (!file) {

        alert("Please select an image.");

        return;

    }

    const formData = new FormData();

    formData.append("file", file);


    // Show Loading
    loadingImage.src = URL.createObjectURL(file);//enhanced

    loadingSection.classList.remove("d-none");

    resultSection.classList.add("d-none");


    // ===============================
    // Progress animation logic
    // ===============================

    let progress = 0;

    progressBar.style.width = "0%";
    progressBar.innerHTML = "0%";

    const messages = [

        "Reading Image...",

        "Enhancing Contrast...",

        "Extracting Features...",

        "Running VGG19...",

        "Generating Prediction..."

    ];

    let index = 0;

    const interval = setInterval(() => {

        progress += 5;

        progressBar.style.width = progress + "%";

        progressBar.innerHTML = progress + "%";

        if (progress % 20 === 0 && index < messages.length) {

            loadingText.innerHTML = messages[index];

            index++;

        }

        if (progress >= 100) {

            clearInterval(interval);

        }

    }, 500);



    try {

        const response = await fetch("/predict", {

            method: "POST",

            body: formData

        });


        const data = await response.json();

        loadingSection.classList.add("d-none");

        resultSection.classList.remove("d-none");


        // Show Uploaded Image

        resultImage.src = URL.createObjectURL(file);

        //============================Enhanced========================
        clearInterval(interval);

        progressBar.style.width = "100%";

        progressBar.innerHTML = "100%";

        // Prediction

        predictionText.innerHTML = data.prediction;


        // Color

        if (data.prediction.toUpperCase() === "PNEUMONIA") {

            predictionText.className = "text-danger fw-bold";

        }

        else {

            predictionText.className = "text-success fw-bold";

        }


        // Confidence

        confidenceText.innerHTML = data.confidence + "%";

    }

    catch (error) {
         clearInterval(interval);
        loadingSection.classList.add("d-none");

        alert("Prediction Failed.");

        console.error(error);

    }

});





// ===============================
// Reset Page
// ===============================

function resetPage() {

    uploadForm.reset();

    previewImage.src = "";

    previewImage.classList.add("d-none");

    resultSection.classList.add("d-none");

    predictionText.innerHTML = "";

    confidenceText.innerHTML = "";

}


generateReportBtn.addEventListener("click", async () => {


    if (
        patientName.value.trim() === "" ||
        patientAge.value.trim() === "" ||
        patientGender.value === ""
    ) {

        alert("Please fill all patient details.");

        return;

    }


    const file = imageInput.files[0];


    if (!file) {

        alert("Please upload X-Ray image first.");

        return;

    }



    const formData = new FormData();



    formData.append(
        "patient_name",
        patientName.value
    );


    formData.append(
        "age",
        patientAge.value
    );


    formData.append(
        "gender",
        patientGender.value
    );


    formData.append(
        "prediction",
        predictionText.innerText
    );


    formData.append(
        "confidence",
        confidenceText.innerText.replace("%","")
    );


    formData.append(
        "file",
        file
    );



    try {


        const response = await fetch("/generate-report", {

            method:"POST",

            body:formData

        });



        if(!response.ok){

            alert("Failed to generate report.");

            return;

        }



        const blob = await response.blob();



        const url = window.URL.createObjectURL(blob);



        const downloadLink = document.createElement("a");


        downloadLink.href = url;


        downloadLink.download = "Medical_Report.pdf";


        document.body.appendChild(downloadLink);


        downloadLink.click();



        downloadLink.remove();


        window.URL.revokeObjectURL(url);



    }


    catch(error){


        console.error(error);


        alert("Something went wrong while generating report.");

    }


});