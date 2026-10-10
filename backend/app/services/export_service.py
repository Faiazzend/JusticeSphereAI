import os
from typing import List, Dict, Any
from datetime import datetime, timezone
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from app.config import settings


class ExportService:
    """Exports redlined contracts into DOCX format with native Word Track Changes revision XML."""

    @staticmethod
    def _add_revision_token(paragraph, text: str, token_type: str, change_id: int):
        """Injects genuine OpenXML w:ins and w:del Track Changes revisions into Word paragraph."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        author = "ContractMind Legal AI"

        if token_type == "delete":
            del_elem = OxmlElement('w:del')
            del_elem.set(qn('w:id'), str(change_id))
            del_elem.set(qn('w:author'), author)
            del_elem.set(qn('w:date'), timestamp)

            r_elem = OxmlElement('w:r')
            rPr = OxmlElement('w:rPr')
            strike = OxmlElement('w:strike')
            color = OxmlElement('w:color')
            color.set(qn('w:val'), 'DC2626')
            rPr.append(strike)
            rPr.append(color)
            r_elem.append(rPr)

            del_text = OxmlElement('w:delText')
            del_text.text = text + " "
            r_elem.append(del_text)
            del_elem.append(r_elem)
            paragraph._p.append(del_elem)

        elif token_type == "insert":
            ins_elem = OxmlElement('w:ins')
            ins_elem.set(qn('w:id'), str(change_id))
            ins_elem.set(qn('w:author'), author)
            ins_elem.set(qn('w:date'), timestamp)

            r_elem = OxmlElement('w:r')
            rPr = OxmlElement('w:rPr')
            u = OxmlElement('w:u')
            u.set(qn('w:val'), 'single')
            color = OxmlElement('w:color')
            color.set(qn('w:val'), '16A34A')
            rPr.append(u)
            rPr.append(color)
            r_elem.append(rPr)

            t_elem = OxmlElement('w:t')
            t_elem.text = text + " "
            r_elem.append(t_elem)
            ins_elem.append(r_elem)
            paragraph._p.append(ins_elem)

        else:
            run = paragraph.add_run(text + " ")
            run.font.color.rgb = RGBColor(30, 41, 59)

    @staticmethod
    def export_to_docx(
        contract_title: str,
        redlines: List[Dict[str, Any]],
        output_filename: str
    ) -> str:
        """
        Creates a Word (.docx) document displaying original clauses and native Track Changes revisions.
        """
        doc = Document()

        # Title
        title_heading = doc.add_heading(f"Contract Redline Review: {contract_title}", level=0)
        p_sub = doc.add_paragraph("Generated autonomously by ContractMind Legal AI Engine (Track Changes XML Enabled)\n")
        p_sub.runs[0].font.italic = True
        p_sub.runs[0].font.color.rgb = RGBColor(128, 128, 128)

        # Overview Table
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = "Section"
        hdr_cells[1].text = "Severity"
        hdr_cells[2].text = "Redline Type"
        hdr_cells[3].text = "Status"

        for rl in redlines:
            row_cells = table.add_row().cells
            row_cells[0].text = str(rl.get("section_number", "N/A"))
            row_cells[1].text = str(rl.get("risk_severity", "MEDIUM"))
            row_cells[2].text = str(rl.get("diff_type", "REPLACE"))
            accepted = rl.get("accepted")
            status_text = "Accepted" if accepted is True else ("Rejected" if accepted is False else "Pending Review")
            row_cells[3].text = status_text

        doc.add_paragraph("\n")

        # Detailed Clauses with Native Word Revisions
        change_id_counter = 100
        for rl in redlines:
            sec_num = rl.get("section_number", "Clause")
            severity = rl.get("risk_severity", "MEDIUM")
            rationale = rl.get("legal_rationale", "")
            tokens = rl.get("diff_tokens", [])

            h = doc.add_heading(f"Section {sec_num} [Severity: {severity}]", level=2)

            # Redline text paragraph
            p = doc.add_paragraph()
            p.add_run("Redlined Text (OpenXML Revisions):\n").bold = True

            if tokens:
                for token in tokens:
                    text_str = token.get("text", "")
                    t_type = token.get("type", "equal")
                    change_id_counter += 1
                    ExportService._add_revision_token(p, text_str, t_type, change_id_counter)
            else:
                p.add_run(rl.get("suggested_text", ""))

            # Legal rationale block
            p_rat = doc.add_paragraph()
            r_run = p_rat.add_run(f"Legal Rationale: {rationale}")
            r_run.font.italic = True
            r_run.font.color.rgb = RGBColor(75, 85, 99)

            doc.add_paragraph("-" * 40)

        out_path = os.path.join(settings.EXPORT_DIR, output_filename)
        doc.save(out_path)
        return out_path


export_service = ExportService()
