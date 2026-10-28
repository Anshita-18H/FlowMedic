import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page count: 'Page X of Y'
    along with a clean running header and footer.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Suppress header and footer on cover page (page 1)
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(54, 750, "FLOWMEDIC")
            self.setFont("Helvetica", 8)
            self.drawString(115, 750, "|   Autonomous Workflow Recovery & Incident Remediation Platform")

            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, letter[0] - 54, 742)

            # Footer
            self.line(54, 45, letter[0] - 54, 45)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#94a3b8"))
            self.drawString(54, 32, "Confidential · Internal Engineering & Architecture Roadmap")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(letter[0] - 54, 32, page_text)

        self.restoreState()


def parse_phase_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {
        'title': '',
        'planned_time': '',
        'status': '',
        'design_ref': '',
        'objective': '',
        'checklist': [],
        'entrance_criteria': [],
        'exit_criteria': [],
        'completion_record': []
    }

    lines = content.split('\n')
    current_section = None
    buffer = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# '):
            data['title'] = stripped[2:].strip()
        elif stripped.startswith('**Planned time:**'):
            # e.g. **Planned time:** 25 minutes · **Status:** IN PROGRESS
            m = re.search(r'\*\*Planned time:\*\*\s*([^*·]+)', stripped)
            if m:
                data['planned_time'] = m.group(1).strip()
            m_status = re.search(r'\*\*Status:\*\*\s*(.+)$', stripped)
            if m_status:
                data['status'] = m_status.group(1).strip()
        elif stripped.startswith('**Design reference:**'):
            data['design_ref'] = stripped.replace('**Design reference:**', '').strip()
        elif stripped.startswith('## Objective'):
            current_section = 'objective'
            buffer = []
        elif stripped.startswith('## Checklist'):
            if current_section == 'objective':
                data['objective'] = ' '.join(buffer).strip()
            current_section = 'checklist'
            buffer = []
        elif stripped.startswith('## Entrance criteria'):
            current_section = 'entrance'
            buffer = []
        elif stripped.startswith('## Exit criteria'):
            current_section = 'exit'
            buffer = []
        elif stripped.startswith('## Completion record'):
            current_section = 'completion'
            buffer = []
        else:
            if current_section == 'objective':
                if stripped:
                    buffer.append(stripped)
            elif current_section == 'checklist':
                if stripped.startswith('- ['):
                    checked = stripped.startswith('- [x]')
                    item_text = stripped[5:].strip()
                    data['checklist'].append((checked, item_text))
            elif current_section == 'entrance':
                if stripped.startswith('- '):
                    data['entrance_criteria'].append(stripped[2:].strip())
            elif current_section == 'exit':
                if stripped.startswith('- '):
                    data['exit_criteria'].append(stripped[2:].strip())
            elif current_section == 'completion':
                if stripped.startswith('- '):
                    parts = stripped[2:].split(':', 1)
                    if len(parts) == 2:
                        k, v = parts[0].strip(), parts[1].strip()
                        data['completion_record'].append((k, v))
                    else:
                        data['completion_record'].append(('', stripped[2:].strip()))

    return data


def generate_pdf():
    docs_dir = r"d:\saboot\FlowMedic\docs"
    phases_dir = os.path.join(docs_dir, "PHASES")
    output_pdf = os.path.join(docs_dir, "FlowMedic_All_Phases_Consolidated.pdf")

    # Document setup
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    content_width = letter[0] - 108  # 504 pt

    # Base Styles
    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#0f172a")     # Slate 900
    c_secondary = colors.HexColor("#334155")   # Slate 700
    c_accent = colors.HexColor("#0284c7")      # Sky 600
    c_teal = colors.HexColor("#0d9488")        # Teal 600
    c_card_bg = colors.HexColor("#f8fafc")     # Slate 50
    c_border = colors.HexColor("#e2e8f0")      # Slate 200
    c_muted = colors.HexColor("#64748b")       # Slate 500

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#0f172a")
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#475569")
    )

    h1_style = ParagraphStyle(
        'PhaseHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a")
    )

    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155")
    )

    body_bold = ParagraphStyle(
        'CustomBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    objective_style = ParagraphStyle(
        'ObjectiveText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1e293b")
    )

    tag_style = ParagraphStyle(
        'TagStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # ==========================================
    # 1. COVER / TITLE HERO
    # ==========================================
    story.append(Spacer(1, 30))
    # Brand Pill
    brand_pill = Table(
        [[Paragraph("<font color='#0284c7'><b>FLOWMEDIC ENGINEERING SPECIFICATION</b></font>", ParagraphStyle('BP', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#0284c7")))]],
        colWidths=[content_width],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#e0f2fe")),
            ('PADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ])
    )
    story.append(brand_pill)
    story.append(Spacer(1, 16))

    story.append(Paragraph("Complete Project Phases Roadmap", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Phases 00 through 07 — Technical Architecture, Implementation Checklists & Validation Gates", subtitle_style))
    story.append(Spacer(1, 16))

    # Metadata Card
    meta_data = [
        [
            Paragraph("<b>Repository:</b> FlowMedic", body_style),
            Paragraph("<b>Stack:</b> Next.js 15 · Postgres (Neon) · AI Agent", body_style)
        ],
        [
            Paragraph("<b>Date:</b> October 2026", body_style),
            Paragraph("<b>Overall Status:</b> Phase 00 (Foundation) In Progress", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[content_width/2, content_width/2])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 22))

    # ==========================================
    # 2. MASTER PHASE DIRECTORY TABLE
    # ==========================================
    story.append(Paragraph("Master Phase Execution Matrix", h2_style))
    story.append(Spacer(1, 4))

    phase_files = [f"phase-0{i}.md" for i in range(8)]
    matrix_rows = [
        [
            Paragraph("<b>Phase</b>", body_bold),
            Paragraph("<b>Name & Scope</b>", body_bold),
            Paragraph("<b>Est. Time</b>", body_bold),
            Paragraph("<b>Current Status</b>", body_bold)
        ]
    ]

    parsed_phases = []
    for pf in phase_files:
        p_path = os.path.join(phases_dir, pf)
        p_data = parse_phase_file(p_path)
        parsed_phases.append(p_data)

        # Status badge color
        status = p_data['status'].upper()
        if "IN PROGRESS" in status:
            status_html = "<font color='#b45309'><b>IN PROGRESS</b></font>"
        elif "COMPLETE" in status:
            status_html = "<font color='#15803d'><b>COMPLETE</b></font>"
        else:
            status_html = "<font color='#64748b'>NOT STARTED</font>"

        short_title = p_data['title'].replace("Phase ", "")
        phase_num = short_title.split("—")[0].strip() if "—" in short_title else ""
        phase_name = short_title.split("—")[1].strip() if "—" in short_title else short_title

        matrix_rows.append([
            Paragraph(f"<b>Phase {phase_num}</b>", body_style),
            Paragraph(phase_name, body_style),
            Paragraph(p_data['planned_time'], body_style),
            Paragraph(status_html, body_style)
        ])

    matrix_table = Table(matrix_rows, colWidths=[65, 230, 85, 124])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(matrix_table)
    story.append(Spacer(1, 16))

    # Status Legend Box
    legend_text = (
        "<b>Status Legend:</b> "
        "<b><font color='#b45309'>IN PROGRESS</font></b>: Active engineering work underway; "
        "<b><font color='#64748b'>NOT STARTED</font></b>: Scoped and planned; "
        "<b><font color='#15803d'>COMPLETE</font></b>: All exit criteria validated with concrete evidence."
    )
    legend_p = Paragraph(legend_text, ParagraphStyle('Legend', parent=body_style, fontSize=8.5, leading=12, textColor=c_muted))
    story.append(legend_p)

    story.append(PageBreak())

    # ==========================================
    # 3. DETAILED PHASES (00 - 07)
    # ==========================================
    for idx, p in enumerate(parsed_phases):
        phase_elements = []

        # Header Box with Phase Title and Status Badge
        status = p['status'].upper()
        if "IN PROGRESS" in status:
            badge_bg = colors.HexColor("#fef3c7")
            badge_fg = "#b45309"
            badge_border = colors.HexColor("#fde68a")
        elif "COMPLETE" in status:
            badge_bg = colors.HexColor("#dcfce7")
            badge_fg = "#15803d"
            badge_border = colors.HexColor("#bbf7d0")
        else:
            badge_bg = colors.HexColor("#f1f5f9")
            badge_fg = "#475569"
            badge_border = colors.HexColor("#e2e8f0")

        badge_p = Paragraph(f"<font color='{badge_fg}'><b>{status}</b></font>", ParagraphStyle('BadgeP', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, alignment=1))

        header_cell_left = [
            Paragraph(p['title'], h1_style),
            Spacer(1, 4),
            Paragraph(f"<font color='#64748b'><b>Planned Duration:</b> {p['planned_time']}</font>", body_style)
        ]
        if p['design_ref']:
            header_cell_left.append(Paragraph(f"<font color='#0284c7'><b>Reference:</b> {p['design_ref']}</font>", body_style))

        header_table = Table(
            [[header_cell_left, badge_p]],
            colWidths=[content_width - 110, 110]
        )
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BACKGROUND', (1,0), (1,0), badge_bg),
            ('BOX', (1,0), (1,0), 1, badge_border),
            ('TOPPADDING', (1,0), (1,0), 6),
            ('BOTTOMPADDING', (1,0), (1,0), 6),
            ('LEFTPADDING', (0,0), (0,0), 0),
        ]))
        phase_elements.append(header_table)
        phase_elements.append(Spacer(1, 8))
        phase_elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#cbd5e1"), spaceBefore=4, spaceAfter=10))

        # Objective Callout Card
        phase_elements.append(Paragraph("Objective", h2_style))
        obj_table = Table([[Paragraph(p['objective'], objective_style)]], colWidths=[content_width])
        obj_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
            ('LINELEFT', (0,0), (0,0), 3.5, colors.HexColor("#0284c7")),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        phase_elements.append(obj_table)
        phase_elements.append(Spacer(1, 10))

        # Checklist
        if p['checklist']:
            phase_elements.append(Paragraph("Phase Checklist & Deliverables", h2_style))
            chk_rows = []
            for checked, text in p['checklist']:
                if checked:
                    icon = "<font color='#15803d'><b>[DONE]</b></font>"
                    row_bg = colors.HexColor("#f0fdf4")
                else:
                    icon = "<font color='#94a3b8'><b>[TODO]</b></font>"
                    row_bg = colors.HexColor("#ffffff")
                chk_rows.append([
                    Paragraph(icon, ParagraphStyle('Icon', parent=body_style, fontSize=8, fontName='Helvetica-Bold')),
                    Paragraph(text, body_style)
                ])

            chk_table = Table(chk_rows, colWidths=[48, content_width - 48])
            chk_table.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 0.5, c_border),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ]))
            phase_elements.append(chk_table)
            phase_elements.append(Spacer(1, 10))

        # Criteria: Entrance and Exit Side by Side or Stacked
        crit_rows = []
        ent_items = "<br/>".join([f"• {item}" for item in p['entrance_criteria']]) if p['entrance_criteria'] else "None specified."
        exit_items = "<br/>".join([f"• {item}" for item in p['exit_criteria']]) if p['exit_criteria'] else "None specified."

        crit_data = [
            [
                Paragraph("<b>Entrance Criteria (Prerequisites)</b>", ParagraphStyle('H2G', parent=h2_style, fontSize=10)),
                Paragraph("<b>Exit Criteria (Validation Gates)</b>", ParagraphStyle('H2G2', parent=h2_style, fontSize=10))
            ],
            [
                Paragraph(ent_items, body_style),
                Paragraph(exit_items, body_style)
            ]
        ]
        crit_table = Table(crit_data, colWidths=[content_width/2 - 4, content_width/2 + 4])
        crit_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor("#f8fafc")),
            ('BACKGROUND', (1,0), (1,0), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        phase_elements.append(crit_table)
        phase_elements.append(Spacer(1, 10))

        # Completion Record
        if p['completion_record']:
            phase_elements.append(Paragraph("Completion Record & Audit", h2_style))
            comp_rows = []
            for k, v in p['completion_record']:
                # Clean links [text](../path) -> text
                clean_v = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'<b>\1</b>', v)
                comp_rows.append([
                    Paragraph(f"<b>{k}</b>", ParagraphStyle('CK', parent=body_style, fontSize=8.5, fontName='Helvetica-Bold', textColor=colors.HexColor("#1e293b"))),
                    Paragraph(clean_v, ParagraphStyle('CV', parent=body_style, fontSize=8.5, textColor=colors.HexColor("#334155")))
                ])

            comp_table = Table(comp_rows, colWidths=[120, content_width - 120])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#f8fafc")),
                ('BOX', (0,0), (-1,-1), 1, c_border),
                ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ]))
            phase_elements.append(comp_table)

        story.extend(phase_elements)
        if idx < len(parsed_phases) - 1:
            story.append(PageBreak())

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated {output_pdf}")

if __name__ == "__main__":
    generate_pdf()

