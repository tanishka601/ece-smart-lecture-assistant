from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(
    filename,
    transcript,
    summary,
    key_points,
    mcqs,
    viva
):

    pdf_path = f"exports/{filename}.pdf"

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(pdf_path)

    story = []

    story.append(Paragraph("<b>ECE Smart Lecture Assistant</b>", styles["Title"]))

    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    story.append(Paragraph("<b>Transcript</b>", styles["Heading1"]))
    story.append(Paragraph(transcript.replace("\n", "<br/>"), styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Study Notes</b>", styles["Heading1"]))
    story.append(Paragraph(summary.replace("\n", "<br/>"), styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Key Points</b>", styles["Heading1"]))

    for point in key_points:
        story.append(Paragraph(f"• {point}", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>MCQs</b>", styles["Heading1"]))

    for i, mcq in enumerate(mcqs):

        story.append(
            Paragraph(
                f"<b>Q{i+1}. {mcq['question']}</b>",
                styles["BodyText"]
            )
        )

        for option in mcq["options"]:
            story.append(
                Paragraph(option, styles["BodyText"])
            )

        story.append(
            Paragraph(
                f"<b>Answer:</b> {mcq['answer']}",
                styles["BodyText"]
            )
        )

        story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Viva Questions</b>", styles["Heading1"]))

    for q in viva:
        story.append(
            Paragraph(f"• {q}", styles["BodyText"])
        )

    doc.build(story)

    return pdf_path