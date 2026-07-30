
from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import TA_CENTER

from reportlab.lib import colors

from reportlab.lib.colors import Color

from datetime import datetime

import os
import random
import qrcode



# ==================================================
# Generate Report ID
# ==================================================

def generate_report_id(patient_name):

    return (
        "PD-"
        + datetime.now().strftime("%Y%m%d")
        + "-"
        + patient_name[:3].upper()
        + str(random.randint(1000,9999))
    )



# ==================================================
# Generate QR Code
# ==================================================

def generate_qr(report_id):

    qr_folder = os.path.join(
        "static",
        "report_assets"
    )


    os.makedirs(
        qr_folder,
        exist_ok=True
    )


    qr_path = os.path.join(
        qr_folder,
        report_id + ".png"
    )


    qr = qrcode.QRCode(

        version=1,

        box_size=5,

        border=2

    )


    qr.add_data(

        "Pneumonia Detection AI Report Verification ID: "
        + report_id

    )


    qr.make(

        fit=True

    )


    qr_image = qr.make_image()


    qr_image.save(qr_path)


    return qr_path




# ==================================================
# Footer
# ==================================================

def add_footer(canvas, doc):

    canvas.saveState()

     # ==========================
    # WATERMARK
    # ==========================
    canvas.setFillColor(Color(0.7, 0.7, 0.7, alpha=0.20))
    canvas.setFont("Helvetica-Bold", 48)

    canvas.translate(300, 420)      # Center of A4 page
    canvas.rotate(45)

    canvas.drawCentredString(
        0,
        0,
        "AI GENERATED"
    )

    # Restore rotation
    canvas.rotate(-45)
    canvas.translate(-300, -420)

    canvas.setFont(
        "Helvetica",
        9
    )

    canvas.setFillColor(colors.black)
    canvas.drawString(

        40,

        30,

        "Pneumonia Detection AI - Confidential Medical Report"

    )


    canvas.drawRightString(

        550,

        30,

        f"Page {doc.page}"

    )


    canvas.restoreState()




# ==================================================
# Generate PDF
# ==================================================

def generate_pdf(

        patient_name,
        age,
        gender,
        prediction,
        confidence,
        image_path,
        output_path

):


    doc = SimpleDocTemplate(

        output_path,

        pagesize=A4,

        rightMargin=40,

        leftMargin=40,

        topMargin=40,

        bottomMargin=50

    )



    elements = []


    styles = getSampleStyleSheet()



    # ==================================================
    # Custom Styles
    # ==================================================

    title_style = ParagraphStyle(

        "title",

        parent=styles["Heading1"],

        alignment=TA_CENTER,

        fontSize=20,

        textColor=colors.darkblue

    )



    subtitle_style = ParagraphStyle(

        "subtitle",

        parent=styles["Normal"],

        alignment=TA_CENTER,

        fontSize=12

    )



    heading_style = ParagraphStyle(

        "heading",

        parent=styles["Heading2"],

        textColor=colors.darkblue,

        spaceAfter=8

    )



    normal_center = ParagraphStyle(

        "normal_center",

        parent=styles["Normal"],

        alignment=TA_CENTER

    )




    # ==================================================
    # Header Section
    # ==================================================


    logo_path = os.path.join(

        "static",

        "images",

        "images.png"

    )


    header_content = []



    if os.path.exists(logo_path):

        header_content.append(

            Image(

                logo_path,

                width=80,

                height=80

            )

        )



    header_content.append(

        Paragraph(

            "PNEUMONIA DETECTION AI",

            title_style

        )

    )


    header_content.append(

        Paragraph(

            "AI Assisted Chest X-Ray Diagnostic Report",

            subtitle_style

        )

    )



    header_table = Table(

        [

            [

                header_content

            ]

        ]

    )



    header_table.setStyle(

        TableStyle([

            (
                "ALIGN",
                (0,0),
                (-1,-1),
                "CENTER"
            )

        ])

    )



    elements.append(header_table)



    elements.append(

        Spacer(1,15)

    )



    elements.append(

        HRFlowable(

            width="100%",

            thickness=2,

            color=colors.darkblue

        )

    )



    elements.append(

        Spacer(1,20)

    )




    # ==================================================
    # Patient Information
    # ==================================================


    report_id = generate_report_id(patient_name)


    elements.append(

        Paragraph(

            "Patient Information",

            heading_style

        )

    )


    patient_table = Table(

        [

            [
                "Patient Name",
                patient_name
            ],

            [
                "Age",
                age
            ],

            [
                "Gender",
                gender
            ],

            [
                "Report ID",
                report_id
            ],

            [
                "Generated On",
                datetime.now().strftime("%d-%m-%Y %H:%M")
            ]

        ],

        colWidths=[150,300]

    )


    patient_table.setStyle(

        TableStyle([


            (
                "BACKGROUND",
                (0,0),
                (0,-1),
                colors.lightblue
            ),


            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),


            (
                "PADDING",
                (0,0),
                (-1,-1),
                8
            )

        ])

    )


    elements.append(patient_table)



    elements.append(

        Spacer(1,20)

    )




    # ==================================================
    # X-Ray Image
    # ==================================================


    elements.append(

        Paragraph(

            "Chest X-Ray Image",

            heading_style

        )

    )



    if os.path.exists(image_path):

        xray_image = Image(

            image_path,

            width=250,

            height=250

        )


        elements.append(

            xray_image

        )



    elements.append(

        Spacer(1,20)

    )
        # ==================================================
    # AI Diagnosis
    # ==================================================


    elements.append(

        Paragraph(

            "AI Diagnosis",

            heading_style

        )

    )



    if prediction.upper() == "NORMAL":

        diagnosis_color = colors.green

    else:

        diagnosis_color = colors.red



    diagnosis_table = Table(

        [

            [

                Paragraph(
                    "Prediction",
                    styles["Normal"]
                ),

                Paragraph(

                    f"<font color='{diagnosis_color.hexval()}'>"
                    f"<b>{prediction}</b>"
                    f"</font>",

                    styles["Normal"]

                )

            ],


            [

                Paragraph(
                    "Confidence",
                    styles["Normal"]
                ),


                Paragraph(

                    f"<font color='{diagnosis_color.hexval()}'>"
                    f"<b>{confidence}%</b>"
                    f"</font>",

                    styles["Normal"]

                )

            ]

        ],

        colWidths=[150,300]

    )



    diagnosis_table.setStyle(

        TableStyle([


            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),


            (
                "PADDING",
                (0,0),
                (-1,-1),
                10
            )


        ])

    )


    elements.append(diagnosis_table)




    # ==================================================
    # AI Observation
    # ==================================================


    elements.append(

        Spacer(1,20)

    )


    elements.append(

        Paragraph(

            "AI Observation",

            heading_style

        )

    )



    confidence_value = float(confidence)



    if prediction.upper() == "PNEUMONIA":


        if confidence_value >= 90:


            observation = """

            • Strong pneumonia-related patterns detected.<br/>
            • Abnormal lung opacity patterns identified by AI analysis.<br/>
            • High probability of pneumonia infection detected.<br/>
            • Immediate consultation with a medical professional is recommended.<br/>
            • Further clinical examination and radiological confirmation should be performed.

            """


        elif confidence_value >= 70:


            observation = """

            • Moderate pneumonia indicators detected.<br/>
            • AI identified suspicious lung patterns requiring evaluation.<br/>
            • Clinical symptoms should be correlated with this result.<br/>
            • Doctor consultation and additional tests are recommended.

            """


        else:


            observation = """

            • Possible pneumonia indicators detected with low confidence.<br/>
            • AI prediction requires clinical verification.<br/>
            • Image quality and patient history should be reviewed.<br/>
            • Medical evaluation is recommended before conclusion.

            """


    else:


        if confidence_value >= 90:


            observation = """

            • No pneumonia-related patterns detected.<br/>
            • Lung appearance classified as normal with high confidence.<br/>
            • No significant abnormal opacity detected by AI.<br/>
            • Continue routine health monitoring and follow medical advice.

            """


        elif confidence_value >= 70:


            observation = """

            • No strong pneumonia patterns detected.<br/>
            • AI confidence level is moderate.<br/>
            • Clinical symptoms should be considered along with this report.<br/>
            • Medical consultation is advised if symptoms continue.

            """


        else:


            observation = """

            • Normal classification detected with low confidence.<br/>
            • AI result may be affected by image quality.<br/>
            • Additional medical review is recommended.<br/>
            • Consider repeating imaging if clinically required.

            """



    elements.append(

        Paragraph(

            observation,

            styles["Normal"]

        )

    )





    # ==================================================
    # Confidence Score Bar
    # ==================================================


    elements.append(

        Spacer(1,20)

    )


    elements.append(

        Paragraph(

            "Confidence Score",

            heading_style

        )

    )



    max_width = 300


    filled_width = (

        confidence_value / 100

    ) * max_width



    if prediction.upper() == "NORMAL":

        bar_color = colors.green

    else:

        bar_color = colors.red




    # Filled part

    filled_bar = Table(

        [

            [""]

        ],

        colWidths=[filled_width],

        rowHeights=[15]

    )


    filled_bar.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0,0),
                (-1,-1),
                bar_color
            )

        ])

    )



    # Empty container

    confidence_bar = Table(

        [

            [

                filled_bar

            ]

        ],

        colWidths=[max_width],

        rowHeights=[15]

    )


    confidence_bar.setStyle(

        TableStyle([


            (
                "BOX",
                (0,0),
                (-1,-1),
                1,
                colors.black
            ),


            (
                "BACKGROUND",
                (0,0),
                (-1,-1),
                colors.white
            ),


            (
                "VALIGN",
                (0,0),
                (-1,-1),
                "MIDDLE"
            )


        ])

    )


    elements.append(

        confidence_bar

    )


    elements.append(

        Spacer(1,5)

    )



    scale_table = Table(

        [

            [

                "0",

                "25",

                "50",

                "75",

                "100"

            ]

        ],

        colWidths=[60,60,60,60,60]

    )


    scale_table.setStyle(

        TableStyle([

            (
                "ALIGN",
                (0,0),
                (-1,-1),
                "CENTER"
            )

        ])

    )


    elements.append(scale_table)



    elements.append(

        Paragraph(

            f"<b>{confidence}%</b> confidence level",

            styles["Normal"]

        )

    )




    # ==================================================
    # AI Model Information
    # ==================================================


    elements.append(

        Spacer(1,20)

    )


    elements.append(

        Paragraph(

            "AI Model Information",

            heading_style

        )

    )



    model_table = Table(

        [

            [
                "Model",
                "VGG19 Transfer Learning"
            ],

            [
                "Input Size",
                "128 x 128 RGB Image"
            ],

            [
                "Framework",
                "TensorFlow / Keras"
            ]

        ],

        colWidths=[150,300]

    )


    model_table.setStyle(

        TableStyle([

            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),

            (
                "PADDING",
                (0,0),
                (-1,-1),
                8
            )

        ])

    )


    elements.append(model_table)
    # --------------------------
    # Performance Metrics
    # --------------------------
    elements.append(

        Paragraph(

            "Model Performance Metrics",

            heading_style

        )

    )



    performance_table = Table(

        [

            [

                "Metric",

                "Score"

            ],


            [

                "Accuracy",

                "75.64%"

            ],


            [

                "Precision",

                "78.20%"

            ],


            [

                "Recall",

                "82.50%"

            ],


            [

                "F1 Score",

                "80.30%"

            ],


            [

                "Test Accuracy",

                "75.64%"

            ]

        ],

        colWidths=[180,250]

    )



    performance_table.setStyle(

        TableStyle([


            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),


            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.darkblue
            ),


            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),


            (
                "PADDING",
                (0,0),
                (-1,-1),
                10
            )


        ])

    )



    elements.append(performance_table)



    elements.append(

        Spacer(1,20)

    )


    # ==================================================
    # QR Verification
    # ==================================================

    elements.append(

        Paragraph(

            "Report Verification",

            heading_style

        )

    )



    qr_path = generate_qr(report_id)



    qr_table = Table(

        [

            [

                Image(

                    qr_path,

                    width=100,

                    height=100

                ),


                Paragraph(

                    "Scan QR code to verify this AI generated report."
                    "<br/><br/>"
                    "Verification ID: "
                    + report_id,

                    styles["Normal"]

                )

            ]

        ],

        colWidths=[120,300]

    )


    qr_table.setStyle(

        TableStyle([


            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),


            (
                "VALIGN",
                (0,0),
                (-1,-1),
                "MIDDLE"
            )


        ])

    )


    elements.append(qr_table)





    # ==================================================
    # Doctor Signature Area
    # ==================================================


    signature_section = []


    signature_section.append(

        Spacer(1,40)

    )



    signature_table = Table(

        [

            [

                "____________________",

                "____________________"

            ],

            [

                "AI Generated Report",

                "Doctor Signature"

            ]

        ],

        colWidths=[200,200]

    )



    signature_table.setStyle(

        TableStyle([


            (
                "ALIGN",
                (0,0),
                (-1,-1),
                "CENTER"
            )

        ])

    )


    signature_section.append(signature_table)



    elements.append(

        KeepTogether(signature_section)

    )





    # ==================================================
    # Disclaimer
    # ==================================================


    elements.append(

        Spacer(1,25)

    )


    elements.append(

        Paragraph(

            """
            <b>Disclaimer:</b> This AI-generated report is intended
            for assistance purposes only. Final diagnosis should always
            be confirmed by a qualified healthcare professional.

            """,

            styles["Normal"]

        )

    )






    # ==================================================
    # Build PDF
    # ==================================================


    doc.build(

        elements,

        onFirstPage=add_footer,

        onLaterPages=add_footer

    )
    