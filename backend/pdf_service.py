
import os
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet

# Always use a stable directory relative to the project root
BASE_DIR = Path(__file__).resolve().parent.parent
EXPORT_DIR = BASE_DIR / "exports"


def create_pdf(
    filename,
    transcript,
    summary,
    key_points,
    mcqs,
    viva,
):
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    safe_filename = Path(filename).stem
    pdf_path = EXPORT_DIR / f"{safe_filename}.pdf"

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(pdf_path))
    story = []

    def add_paragraph(text, style="BodyText"):
        safe_text = escape(str(text)).replace("\n", "<br/>")
        story.append(Paragraph(safe_text, styles[style]))

    add_paragraph("ECE Smart Lecture Assistant", "Title")
    story.append(Spacer(1, 16))

    add_paragraph("Transcript", "Heading1")
    add_paragraph(transcript)
    story.append(Spacer(1, 12))

    add_paragraph("Study Notes", "Heading1")
    add_paragraph(summary)
    story.append(Spacer(1, 12))

    add_paragraph("Key Points", "Heading1")
    for point in key_points:
        add_paragraph(f"• {point}")

    story.append(Spacer(1, 12))
    add_paragraph("MCQs", "Heading1")

    for i, mcq in enumerate(mcqs, start=1):
        add_paragraph(f"Q{i}. {mcq['question']}")
        for option in mcq["options"]:
            add_paragraph(option)
        add_paragraph(f"Answer: {mcq['answer']}")
        story.append(Spacer(1, 8))

    add_paragraph("Viva Questions", "Heading1")
    for question in viva:
        add_paragraph(f"• {question}")

    doc.build(story)
    return str(pdf_path)
