import os
import tempfile

from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    jsonify,
    send_file
)

from werkzeug.utils import secure_filename

from services.predictor import predict_image

from services.report_generator import generate_pdf

routes = Blueprint("routes", __name__)


@routes.route("/")
def home():
    return render_template("index.html")


@routes.route("/predict", methods=["POST"])
def predict():

    # Check file
    if "file" not in request.files:
        return jsonify({
            "error": "No file uploaded."
        }), 400

    file = request.files["file"]

    # Empty filename
    if file.filename == "":
        return jsonify({
            "error": "Please choose an image."
        }), 400

    # Save image
    filename = secure_filename(file.filename)

    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(upload_path)

    # Prediction
    prediction, confidence = predict_image(upload_path)

    return jsonify({

        "prediction": prediction,

        "confidence": round(confidence * 100, 2),

        "image": filename

    })

@routes.route("/generate-report", methods=["POST"])
def generate_report():

    try:

        patient_name = request.form["patient_name"]

        age = request.form["age"]

        gender = request.form["gender"]

        prediction = request.form["prediction"]

        confidence = request.form["confidence"]

        image = request.files["file"]

        reports_folder = os.path.join(
            current_app.root_path,
            "reports"
        )

        os.makedirs(reports_folder, exist_ok=True)

        temp_image = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(image.filename)[1]
        )
        temp_image.close()
        image.save(temp_image.name)

        pdf_path = os.path.join(

            reports_folder,

            f"{patient_name.replace(' ', '_')}_Medical_Report.pdf"

        )

        generate_pdf(

            patient_name=patient_name,

            age=age,

            gender=gender,

            prediction=prediction,

            confidence=confidence,

            image_path=temp_image.name,

            output_path=pdf_path

        )

        if os.path.exists(temp_image.name):
            os.remove(temp_image.name)

            return send_file(

                pdf_path,

                as_attachment=True,

                download_name=f"{patient_name.strip().replace(' ', '_')}_Medical_Report.pdf"

            )

    except Exception as e:
        print("REPORT ERROR:", e)
        return jsonify({

            "error": str(e)

        }), 500



    