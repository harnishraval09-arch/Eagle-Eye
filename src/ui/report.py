"""Builds the expert report once, then renders it as HTML, Markdown or PDF."""
from datetime import date
from html import escape
from io import BytesIO


def build(ctx):
    c, o, sc, cl = ctx["case"], ctx["obs"], ctx["score"], ctx["cls"]
    L = [("title", "Expert opinion report: document examination"),
         ("meta", f"Case {c.get('no', '-')}   Examiner {c.get('examiner', '-')}   {date.today():%d %b %Y}"),
         ("h", "1. Document examined"),
         ("p", f"{ctx['file']} ({c.get('type', '-')}), received {c.get('date', '-')}."),
         ("h", "2. Methods applied")]
    L += [("li", m["title"]) for m in ctx["modules"]] + [("li", "Examiner visual observations"), ("h", "3. Findings")]
    for m in ctx["modules"]:
        bad = [k for k in m["checks"] if k["status"] != "pass"]
        L.append(("h2", m["title"]))
        L += [("li", f"{k['status'].upper()}: {k['name']}. {k['detail']}") for k in bad] or [("p", "No anomalies flagged.")]
    L += [("h", "4. Examiner observations"),
          ("li", f"Signature comparison: {o.get('sig', '-')}"),
          ("li", f"Paper: {', '.join(o.get('paper', [])) or 'none recorded'}"),
          ("li", f"Ink and printing: {', '.join(o.get('ink', [])) or 'none recorded'}"),
          ("li", f"Stamps and seals: {o.get('seal', '-')}")]
    if o.get("notes"):
        L.append(("p", o["notes"]))
    L += [("h", "5. Classification and confidence"),
          ("p", f"Anomaly type: {cl['type']} ({cl['category']}). Forgery confidence: {sc['score']}/100 ({sc['level']}).")]
    L += [("li", x) for x in sc["reasoning"]]
    L.append(("h", "6. Standards and references (demo data, verify before citing)"))
    L += [("li", x) for x in ctx["std"].get("ASTM_E2388", [])]
    L.append(("h", "7. Similar cases (demo data, verify before citing)"))
    L += [("li", f"{p['case']}, relevance {p['relevance']:.2f}. {p['summary']}") for p in ctx["prec"]] or [("p", "None found.")]
    L += [("h", "8. Indicative legal provisions"),
          ("p", "BNS s.336 (forgery) and s.340 (using a forged document as genuine). Indicative only; the examiner or counsel must verify."),
          ("h", "9. Limitations"),
          ("p", "Automated indicators support, and do not replace, examiner judgement. Results depend on file quality and on the reference material available."),
          ("h", "10. Declaration"),
          ("p", "I have reviewed the findings above and this opinion reflects my professional judgement."),
          ("p", "Signature: ______________________   Date: ______________")]
    return L


def to_markdown(L):
    pre = {"title": "# ", "meta": "*", "h": "\n## ", "h2": "\n### ", "p": "", "li": "- "}
    return "\n".join(f"{pre[k]}{t}{'*' if k == 'meta' else ''}" for k, t in L)


def to_html(L):
    tag = {"title": "h1", "meta": "p", "h": "h3", "h2": "h4", "p": "p", "li": "li"}
    out, inl = [], False
    for k, t in L:
        if k == "li" and not inl:
            out.append("<ul>"); inl = True
        if k != "li" and inl:
            out.append("</ul>"); inl = False
        out.append(f"<{tag[k]}>{escape(t)}</{tag[k]}>")
    if inl:
        out.append("</ul>")
    return '<div class="ee-page">' + "".join(out) + "</div>"


def build_pdf(ctx):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate
    ss = getSampleStyleSheet()
    sty = {"title": ss["Title"], "meta": ss["Italic"], "h": ss["Heading2"], "h2": ss["Heading3"],
           "p": ss["BodyText"], "li": ParagraphStyle("li", parent=ss["BodyText"], leftIndent=14)}
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50, title="Expert report")
    doc.build([Paragraph(escape(t), sty[k], bulletText="-" if k == "li" else None) for k, t in build(ctx)])
    return buf.getvalue()
