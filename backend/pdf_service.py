
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(
    filename,
    transcript,
    summary,
    key_points,
    mcqs,
    viva
):
    # Ensure the exports directory exists
    os.makedirs("exports", exist_ok=True)

    # Create PDF path
    pdf_path = os.path.join("exports", f"{filename}.pdf")

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(pdf_path)

    story = []

    story.append(
        Paragraph("ECE Smart Lecture Assistant", styles["Title"])
    )
    story.append(Spacer(1, 12))

    story.append(Paragraph("Transcript", styles["Heading1"]))
    story.append(
        Paragraph(
            transcript.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )
    story.append(Spacer(1, 12))

    story.append(Paragraph("Study Notes", styles["Heading1"]))
    story.append(
        Paragraph(
            summary.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )
    story.append(Spacer(1, 12))

    story.append(Paragraph("Key Points", styles["Heading1"]))

    for point in key_points:
        safe_point = (
            str(point).replace("&", "&amp;")
            .replace("<", "&lt;").replace(">", "&gt;")
        )
        story.append(Paragraph(f"- {safe_point}", styles["BodyText"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("MCQs", styles["Heading1"]))

    for i, mcq in enumerate(mcqs):
        question = (
            str(mcq["question"]).replace("&", "&amp;")
            .replace("<", "&lt;").replace(">", "&gt;")
        )
        story.append(
            Paragraph(f"<b>Q{i + 1}. {question}</b>", styles["BodyText"])
        )

        for option in mcq["options"]:
            safe_option = (
                str(option).replace("&", "&amp;")
                .replace("<", "&lt;").replace(">", "&gt;")
            )
            story.append(Paragraph(safe_option, styles["BodyText"]))

        answer = (
            str(mcq["answer"]).replace("&", "&amp;")
            .replace("<", "&lt;").replace(">", "&gt;")
        )
        story.append(
            Paragraph(f"<b>Answer:</b> {answer}", styles["BodyText"])
        )
        story.append(Spacer(1, 8))

    story.append(Paragraph("Viva Questions", styles["Heading1"]))

    for question in viva:
        safe_question = (
            str(question).replace("&", "&amp;")
            .replace("<", "&lt;").replace(">", "&gt;")
        )
        story.append(
            Paragraph(f"- {safe_question}", styles["BodyText"])
        )

    doc.build(story)

    return pdf_path
