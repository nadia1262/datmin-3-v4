import os
import sys
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_base_document():
    doc = Document()
    for s in doc.sections:
        s.page_width = Cm(21.0)
        s.page_height = Cm(29.7)
        s.top_margin = Cm(2.0)
        s.bottom_margin = Cm(2.0)
        s.left_margin = Cm(2.0)
        s.right_margin = Cm(1.5)
        s.header_distance = Cm(1.0)
        s.footer_distance = Cm(1.0)
    return doc

def format_run(run, font_name="Times New Roman", size_pt=11, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    format_run(run, size_pt=15, bold=True)
    return p

def add_subtitle(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    format_run(run, size_pt=13, bold=False)
    return p

def add_title_en(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(14)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    format_run(run, size_pt=11, bold=False, italic=True)
    return p

def add_author_block(doc, authors, supervisor, institution):
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(4)
    p1.paragraph_format.space_after = Pt(2)
    p1.paragraph_format.line_spacing = 1.0
    r1 = p1.add_run(authors)
    format_run(r1, size_pt=11, bold=True)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(2)
    p2.paragraph_format.line_spacing = 1.0
    r2 = p2.add_run(supervisor)
    format_run(r2, size_pt=10, italic=True)

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(0)
    p3.paragraph_format.space_after = Pt(18)
    p3.paragraph_format.line_spacing = 1.0
    r3 = p3.add_run(institution)
    format_run(r3, size_pt=10, bold=False)

def h2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text.upper())
    format_run(run, size_pt=12, bold=True)
    return p

def h3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    format_run(run, size_pt=11, bold=True)
    return p

def h4(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    format_run(run, size_pt=11, bold=True)
    return p

def body(doc, text, indent=0.75, space_after=6, italic=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if indent > 0:
        p.paragraph_format.first_line_indent = Cm(indent)
    run = p.add_run(text)
    format_run(run, size_pt=11, bold=False, italic=italic)
    return p

def body_formatted(doc, text_runs, indent=0.75, space_after=6):
    """
    text_runs is list of tuples: (text, is_bold, is_italic)
    """
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if indent > 0:
        p.paragraph_format.first_line_indent = Cm(indent)
    for t, b, it in text_runs:
        r = p.add_run(t)
        format_run(r, size_pt=11, bold=b, italic=it)
    return p

def numbered_item(doc, num_str, title_str, body_str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.first_line_indent = Cm(-0.75)

    r_num = p.add_run(num_str + " ")
    format_run(r_num, size_pt=11, bold=True)

    if title_str:
        r_title = p.add_run(title_str + ": ")
        format_run(r_title, size_pt=11, bold=True)

    r_body = p.add_run(body_str)
    format_run(r_body, size_pt=11, bold=False)
    return p

def bullet_item(doc, title_str, body_str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.first_line_indent = Cm(-0.5)

    r_bullet = p.add_run("• ")
    format_run(r_bullet, size_pt=11, bold=True)

    if title_str:
        r_title = p.add_run(title_str + ": ")
        format_run(r_title, size_pt=11, bold=True)

    r_body = p.add_run(body_str)
    format_run(r_body, size_pt=11, bold=False)
    return p

def equation(doc, eq_text, eq_num_str=""):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15

    # Use tabs or spacing for equation with right number
    r_eq = p.add_run(f"       {eq_text}")
    format_run(r_eq, font_name="Cambria Math", size_pt=11, bold=False, italic=True)

    if eq_num_str:
        # Pad with spaces to push to right margin
        spaces = " " * max(4, 80 - len(eq_text) - len(eq_num_str))
        r_num = p.add_run(f"{spaces}({eq_num_str})")
        format_run(r_num, font_name="Times New Roman", size_pt=11, bold=False)
    return p

def add_academic_table(doc, headers, data, caption, source="Sumber: Olahan Peneliti (2024)", col_widths=None, alignments=None):
    # Caption above
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(12)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.keep_with_next = True
    r_cap = p_cap.add_run(caption)
    format_run(r_cap, size_pt=10, bold=True)

    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header row
    hdr_row = table.rows[0]
    hdr_row._tr.get_or_add_trPr().append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    for j, h in enumerate(headers):
        cell = hdr_row.cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(str(h))
        format_run(r, size_pt=9.5, bold=True)

    # Data rows
    for i, row in enumerate(data):
        row_cells = table.rows[i + 1].cells
        for j, val in enumerate(row):
            cell = row_cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            if alignments and j < len(alignments):
                p.alignment = alignments[j]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            r = p.add_run(str(val))
            format_run(r, size_pt=9.0, bold=False)

    # Column widths
    if col_widths:
        for row in table.rows:
            for j, w in enumerate(col_widths):
                if j < len(row.cells):
                    row.cells[j].width = Cm(w)

    # Academic Borders (Top, Header bottom, Table bottom; no vertical)
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

    # Header bottom border thicker
    for cell in hdr_row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>
                <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>
            </w:tcBorders>
        ''')
        tcPr.append(tcBorders)

    # Source below
    if source:
        p_src = doc.add_paragraph()
        p_src.paragraph_format.space_before = Pt(3)
        p_src.paragraph_format.space_after = Pt(12)
        r_src = p_src.add_run(source)
        format_run(r_src, size_pt=9, italic=True)

    return table

def add_image_figure(doc, img_path, caption, source="Sumber: Hasil Analisis Geospasial Peneliti (2024)", width_cm=14.5):
    if not os.path.exists(img_path):
        p_err = doc.add_paragraph()
        r_err = p_err.add_run(f"[Gambar tidak ditemukan: {img_path}]")
        format_run(r_err, size_pt=10, italic=True, color_rgb=(200,0,0))
        return

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(12)
    p_img.paragraph_format.space_after = Pt(4)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Cm(width_cm))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(2)
    p_cap.paragraph_format.keep_with_next = True
    r_cap = p_cap.add_run(caption)
    format_run(r_cap, size_pt=10, bold=True)

    if source:
        p_src = doc.add_paragraph()
        p_src.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_src.paragraph_format.space_before = Pt(0)
        p_src.paragraph_format.space_after = Pt(12)
        r_src = p_src.add_run(source)
        format_run(r_src, size_pt=9, italic=True)

def add_page_break(doc):
    doc.add_page_break()
