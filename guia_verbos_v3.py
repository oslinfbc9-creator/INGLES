# ============================================================
# GUÍA DE VERBOS DEL INGLÉS - v3
# Cada verbo = 2 tablas apiladas (conjugaciones + ejemplos)
# ============================================================
import os
import csv
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)

CARPETA = "guia_verbos_v3"
CSV_NOMBRE = "verbos.csv"
PDF_NOMBRE = "guia_verbos_v3.pdf"

# ============================================================
# DATOS: cada verbo = 9 elementos
# (base, pasado, participio, ing, significado,
#  ej_base, ej_pasado, ej_participio, ej_ing)
# ============================================================
VERBOS = [
    ("be", "was/were", "been", "being", "ser/estar",
     "I want to be a doctor.",
     "She was tired yesterday.",
     "I have been to Paris twice.",
     "He is being very kind today."),
    ("have", "had", "had", "having", "tener",
     "I have two brothers.",
     "We had pizza last night.",
     "She has had that car for years.",
     "I am having lunch right now."),
    ("do", "did", "done", "doing", "hacer",
     "I do my homework every day.",
     "He did the dishes yesterday.",
     "Have you done your work?",
     "She is doing yoga."),
    ("say", "said", "said", "saying", "decir",
     "Always say the truth.",
     "She said hello to me.",
     "I have said it many times.",
     "He is saying something important."),
    ("go", "went", "gone", "going", "ir",
     "I go to school by bus.",
     "We went to the beach.",
     "She has gone home already.",
     "They are going to travel."),
    ("get", "got", "gotten", "getting", "obtener/conseguir",
     "I want to get a new job.",
     "He got a nice gift.",
     "She has gotten good results.",
     "It is getting colder."),
    ("make", "made", "made", "making", "hacer/fabricar",
     "Let's make a cake.",
     "She made dinner last night.",
     "I have made a decision.",
     "He is making a phone call."),
    ("know", "knew", "known", "knowing", "saber/conocer",
     "I know the answer.",
     "She knew him in college.",
     "I have known her for years.",
     "He is knowing the truth now."),
    ("think", "thought", "thought", "thinking", "pensar",
     "I think it's a good idea.",
     "She thought about it.",
     "I have thought about you.",
     "He is thinking of moving."),
    ("take", "took", "taken", "taking", "tomar/llevar",
     "Please take this book.",
     "He took the train to work.",
     "I have taken many photos.",
     "She is taking a nap."),
    ("see", "saw", "seen", "seeing", "ver",
     "I can see the mountains.",
     "We saw a great movie.",
     "Have you seen my keys?",
     "The doctor is seeing a patient."),
    ("come", "came", "come", "coming", "venir",
     "Please come to my party.",
     "She came late again.",
     "They have come from far away.",
     "Winter is coming soon."),
    ("give", "gave", "given", "giving", "dar",
     "Give me the pen, please.",
     "She gave him a present.",
     "I have given you my answer.",
     "He is giving a speech."),
    ("want", "wanted", "wanted", "wanting", "querer",
     "I want some water.",
     "She wanted to help.",
     "I have wanted this for years.",
     "He is wanting attention today."),
    ("look", "looked", "looked", "looking", "mirar",
     "Look at the sky.",
     "He looked at me strangely.",
     "I have looked everywhere.",
     "She is looking for her keys."),
    ("use", "used", "used", "using", "usar",
     "Use this pen, please.",
     "She used my computer.",
     "I have used that app before.",
     "He is using the phone now."),
    ("work", "worked", "worked", "working", "trabajar",
     "I work in an office.",
     "She worked all weekend.",
     "I have worked here for 5 years.",
     "He is working from home."),
    ("call", "called", "called", "calling", "llamar",
     "Call me when you arrive.",
     "She called me yesterday.",
     "I have called him three times.",
     "The phone is calling right now."),
    ("need", "needed", "needed", "needing", "necesitar",
     "I need your help.",
     "We needed more time.",
     "I have needed this for weeks.",
     "She is needing some rest."),
    ("feel", "felt", "felt", "feeling", "sentir",
     "I feel happy today.",
     "She felt sad yesterday.",
     "I have felt this before.",
     "He is feeling better now."),
    ("try", "tried", "tried", "trying", "intentar",
     "Try this cake, it's great!",
     "I tried to call you.",
     "Have you tried this before?",
     "She is trying her best."),
    ("leave", "left", "left", "leaving", "dejar/salir",
     "I leave work at 6 pm.",
     "He left early today.",
     "She has left already.",
     "The train is leaving now."),
    ("put", "put", "put", "putting", "poner",
     "Put the book on the table.",
     "She put the keys here.",
     "I have put it in the drawer.",
     "He is putting on his shoes."),
    ("start", "started", "started", "starting", "empezar",
     "Start the project today.",
     "We started the meeting late.",
     "I have started a new course.",
     "The movie is starting soon."),
    ("play", "played", "played", "playing", "jugar/tocar",
     "Let's play soccer.",
     "He played guitar last night.",
     "I have played this game before.",
     "The kids are playing outside."),
]

POSICION_DIRECCION = [
    ("stand", "stood", "stood", "standing", "estar de pie",
     "Please stand in line.",
     "He stood by the window.",
     "She has stood there for hours.",
     "We are standing on the platform."),
    ("sit", "sat", "sat", "sitting", "estar sentado",
     "Please sit down.",
     "She sat on the chair.",
     "I have sat here all morning.",
     "He is sitting on the sofa."),
    ("go", "went", "gone", "going", "ir (dirección)",
     "We go into the room.",
     "They went to the park.",
     "She has gone upstairs.",
     "He is going downtown."),
    ("come", "came", "come", "coming", "venir",
     "Come here, please.",
     "She came towards me.",
     "He has come from the airport.",
     "The bus is coming down the street."),
    ("walk", "walked", "walked", "walking", "caminar",
     "Walk towards the exit.",
     "We walked around the lake.",
     "I have walked this path before.",
     "They are walking on the beach."),
    ("run", "ran", "run", "running", "correr",
     "Run to the finish line!",
     "He ran around the park.",
     "She has run a marathon.",
     "The kids are running outside."),
    ("move", "moved", "moved", "moving", "moverse",
     "Move forward slowly.",
     "We moved to a new house.",
     "They have moved to another city.",
     "The car is moving away."),
    ("enter", "entered", "entered", "entering", "entrar",
     "Enter through the front door.",
     "She entered the room quietly.",
     "He has entered the competition.",
     "Guests are entering the hall."),
    ("turn", "turned", "turned", "turning", "girar",
     "Turn right at the corner.",
     "He turned towards me.",
     "She has turned the page.",
     "The car is turning left."),
    ("climb", "climbed", "climbed", "climbing", "subir/escalar",
     "Climb the stairs slowly.",
     "We climbed the mountain.",
     "They have climbed this before.",
     "He is climbing the ladder."),
]


# ============================================================
# FUNCIONES
# ============================================================
def crear_carpeta():
    os.makedirs(CARPETA, exist_ok=True)
    os.chdir(CARPETA)
    print(f"📁 Carpeta: {os.getcwd()}")


def guardar_csv():
    with open(CSV_NOMBRE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["base", "pasado", "participio", "ing", "significado",
                    "ej_base", "ej_pasado", "ej_participio", "ej_ing"])
        w.writerows(VERBOS)
    print(f"💾 CSV: {CSV_NOMBRE} ({len(VERBOS)} verbos)")


def crear_card_verbo(num, v, estilos):
    """Devuelve un objeto 'card' con 2 tablas apiladas por verbo."""
    base, pasado, participio, ing, signif = v[0:5]
    ej_base, ej_pasado, ej_participio, ej_ing = v[5:9]

    # --- Estilos ---
    e_titulo = ParagraphStyle('titulo_v', parent=estilos['Normal'],
                              fontSize=11, leading=13,
                              textColor=colors.white,
                              fontName='Helvetica-Bold')
    e_th = ParagraphStyle('th_v', parent=estilos['Normal'],
                          fontSize=8.5, leading=10,
                          textColor=colors.white, alignment=1,
                          fontName='Helvetica-Bold')
    e_td = ParagraphStyle('td_v', parent=estilos['Normal'],
                          fontSize=9, leading=11, alignment=1)
    e_ej_label = ParagraphStyle('ejl_v', parent=estilos['Normal'],
                                fontSize=8.5, leading=10,
                                fontName='Helvetica-Bold',
                                textColor=colors.HexColor('#1F4E79'))
    e_ej = ParagraphStyle('ej_v', parent=estilos['Normal'],
                          fontSize=8.5, leading=10.5)

    # --- Filas ---
    filas = [
        # 0: título del verbo (span 4)
        [Paragraph(f"{num}. {base} — {signif}", e_titulo), "", "", ""],
        # 1: cabecera de conjugaciones
        [Paragraph("BASE", e_th), Paragraph("PASADO", e_th),
         Paragraph("PARTICIPIO", e_th), Paragraph("-ING", e_th)],
        # 2: valores de conjugaciones
        [Paragraph(f"<b>{base}</b>", e_td), Paragraph(pasado, e_td),
         Paragraph(participio, e_td), Paragraph(ing, e_td)],
        # 3: subtítulo ejemplos (span 4)
        [Paragraph("Ejemplos de uso", e_titulo), "", "", ""],
        # 4-7: ejemplos (etiqueta + ejemplo span 3)
        [Paragraph("Base", e_ej_label), Paragraph(ej_base, e_ej), "", ""],
        [Paragraph("Pasado", e_ej_label), Paragraph(ej_pasado, e_ej), "", ""],
        [Paragraph("Participio", e_ej_label), Paragraph(ej_participio, e_ej), "", ""],
        [Paragraph("-ing", e_ej_label), Paragraph(ej_ing, e_ej), "", ""],
    ]

    tabla = Table(filas, colWidths=[3.5*cm, 5*cm, 5*cm, 13.8*cm])

    tabla.setStyle(TableStyle([
        # Fila 0: título
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
        ('LEFTPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        # Fila 1: cabecera de conjugaciones
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#3498DB')),
        ('TOPPADDING', (0, 1), (-1, 1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 4),
        # Fila 2: valores de conjugaciones
        ('BACKGROUND', (0, 2), (-1, 2), colors.white),
        ('TOPPADDING', (0, 2), (-1, 2), 6),
        ('BOTTOMPADDING', (0, 2), (-1, 2), 6),
        # Fila 3: subtítulo ejemplos
        ('SPAN', (0, 3), (-1, 3)),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#1F4E79')),
        ('LEFTPADDING', (0, 3), (-1, 3), 8),
        ('TOPPADDING', (0, 3), (-1, 3), 5),
        ('BOTTOMPADDING', (0, 3), (-1, 3), 5),
        # Filas 4-7: ejemplos
        ('SPAN', (1, 4), (-1, 4)),
        ('SPAN', (1, 5), (-1, 5)),
        ('SPAN', (1, 6), (-1, 6)),
        ('SPAN', (1, 7), (-1, 7)),
        ('BACKGROUND', (0, 4), (0, 7), colors.HexColor('#EAF2F8')),
        ('BACKGROUND', (1, 4), (-1, 7), colors.white),
        # Alternancia de fondo en ejemplos
        ('BACKGROUND', (1, 5), (-1, 5), colors.HexColor('#F8F8F8')),
        ('BACKGROUND', (1, 7), (-1, 7), colors.HexColor('#F8F8F8')),
        # Rejilla
        ('GRID', (0, 1), (-1, -1), 0.4, colors.HexColor('#B0B0B0')),
        # Alineación
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('VALIGN', (1, 4), (-1, 7), 'TOP'),
        # Padding general
        ('LEFTPADDING', (0, 1), (-1, -1), 6),
        ('RIGHTPADDING', (0, 1), (-1, -1), 6),
    ]))
    return tabla


def dibujar_pie(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(colors.grey)
    canvas_obj.drawString(1.2*cm, doc.pagesize[1] - 0.8*cm,
                         "Guía de Verbos del Inglés")
    canvas_obj.drawRightString(doc.pagesize[0] - 1.2*cm, 0.6*cm,
                               f"Página {doc.page}")
    canvas_obj.drawString(1.2*cm, 0.6*cm, "Guía de Verbos del Inglés")
    canvas_obj.restoreState()


def generar_pdf():
    doc = SimpleDocTemplate(
        PDF_NOMBRE, pagesize=landscape(A4),
        rightMargin=1.2*cm, leftMargin=1.2*cm,
        topMargin=1.5*cm, bottomMargin=1.2*cm,
    )
    estilos = getSampleStyleSheet()
    historia = []

    # --- PORTADA ---
    historia.append(Spacer(1, 2.5*cm))
    historia.append(Paragraph(
        "Guía de Verbos del Inglés",
        ParagraphStyle('t1', parent=estilos['Title'],
                       fontSize=32, textColor=colors.HexColor('#1F4E79'),
                       alignment=1)))
    historia.append(Spacer(1, 0.4*cm))
    historia.append(Paragraph(
        "Conjugaciones y ejemplos de uso",
        ParagraphStyle('t2', parent=estilos['Normal'], fontSize=14,
                       alignment=1, textColor=colors.HexColor('#555'))))
    historia.append(Spacer(1, 0.3*cm))
    historia.append(Paragraph(
        "Con sección aparte de verbos de posición y dirección",
        ParagraphStyle('t3', parent=estilos['Normal'], fontSize=11,
                       alignment=1, textColor=colors.HexColor('#888'))))
    historia.append(Spacer(1, 5*cm))
    historia.append(Paragraph(
        "<b>Fuentes de referencia:</b><br/>"
        "Cambridge University Press — <i>English Grammar in Use</i><br/>"
        "Oxford University Press — <i>Oxford Learner's Grammar</i><br/>"
        "Randolph Quirk — <i>A University Grammar of English</i>",
        ParagraphStyle('ref', parent=estilos['Normal'], fontSize=9,
                       alignment=1, textColor=colors.HexColor('#666'))))
    historia.append(PageBreak())

    # --- SECCIÓN 1 ---
    historia.append(Paragraph(
        "1. Verbos principales",
        ParagraphStyle('s1', parent=estilos['Heading1'],
                       fontSize=20, textColor=colors.HexColor('#1F4E79'))))
    historia.append(Spacer(1, 0.3*cm))
    historia.append(Paragraph(
        f"{len(VERBOS)} verbos con sus 4 conjugaciones y un ejemplo de uso por cada una.",
        ParagraphStyle('i1', parent=estilos['Normal'], fontSize=10,
                       textColor=colors.HexColor('#555'))))
    historia.append(Spacer(1, 0.5*cm))

    for i, v in enumerate(VERBOS, 1):
        card = crear_card_verbo(i, v, estilos)
        historia.append(KeepTogether([card, Spacer(1, 0.7*cm)]))

    # --- SECCIÓN 2 ---
    historia.append(PageBreak())
    historia.append(Paragraph(
        "2. Verbos de posición y dirección",
        ParagraphStyle('s2', parent=estilos['Heading1'],
                       fontSize=20, textColor=colors.HexColor('#1F4E79'))))
    historia.append(Spacer(1, 0.3*cm))
    historia.append(Paragraph(
        "Verbos que indican <b>posición</b> (estado, ubicación) o "
        "<b>dirección/movimiento</b> (desplazamiento).",
        ParagraphStyle('i2', parent=estilos['Normal'], fontSize=10,
                       textColor=colors.HexColor('#555'))))
    historia.append(Spacer(1, 0.5*cm))

    for i, v in enumerate(POSICION_DIRECCION, 1):
        card = crear_card_verbo(i, v, estilos)
        historia.append(KeepTogether([card, Spacer(1, 0.7*cm)]))

    doc.build(historia, onFirstPage=dibujar_pie, onLaterPages=dibujar_pie)
    print(f"📄 PDF: {PDF_NOMBRE}")


if __name__ == "__main__":
    print("🚀 Generando guía v3...\n")
    crear_carpeta()
    guardar_csv()
    generar_pdf()
    print("\n✅ ¡Listo! Revisa la carpeta guia_verbos_v3/")