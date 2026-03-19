"""
genera_pdf.py — Crea el PDF del curso "Crypto para Principiantes"
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "curso_crypto.pdf")

# ── COLORES ────────────────────────────────────────────────────────────
NARANJA      = colors.HexColor("#F7931A")   # Color Bitcoin
AZUL_OSCURO  = colors.HexColor("#0D1117")
AZUL_MED     = colors.HexColor("#1A2332")
VERDE        = colors.HexColor("#00C896")
BLANCO       = colors.white
GRIS         = colors.HexColor("#8B949E")
GRIS_CLARO   = colors.HexColor("#F0F0F0")
AMARILLO     = colors.HexColor("#FFD700")


def crear_estilos():
    styles = getSampleStyleSheet()

    estilos = {
        "portada_titulo": ParagraphStyle(
            "portada_titulo", fontSize=36, textColor=NARANJA,
            alignment=TA_CENTER, fontName="Helvetica-Bold",
            leading=44, spaceAfter=10
        ),
        "portada_sub": ParagraphStyle(
            "portada_sub", fontSize=18, textColor=BLANCO,
            alignment=TA_CENTER, fontName="Helvetica",
            leading=24, spaceAfter=6
        ),
        "portada_precio": ParagraphStyle(
            "portada_precio", fontSize=14, textColor=VERDE,
            alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=4
        ),
        "capitulo": ParagraphStyle(
            "capitulo", fontSize=22, textColor=NARANJA,
            fontName="Helvetica-Bold", leading=28,
            spaceBefore=20, spaceAfter=10,
            borderPad=6
        ),
        "subtitulo": ParagraphStyle(
            "subtitulo", fontSize=15, textColor=AZUL_OSCURO,
            fontName="Helvetica-Bold", leading=20,
            spaceBefore=14, spaceAfter=6
        ),
        "cuerpo": ParagraphStyle(
            "cuerpo", fontSize=11, textColor=colors.HexColor("#2D2D2D"),
            fontName="Helvetica", leading=17,
            alignment=TA_JUSTIFY, spaceAfter=8
        ),
        "bullet": ParagraphStyle(
            "bullet", fontSize=11, textColor=colors.HexColor("#2D2D2D"),
            fontName="Helvetica", leading=16,
            leftIndent=20, spaceAfter=4,
            bulletIndent=10
        ),
        "tip": ParagraphStyle(
            "tip", fontSize=11, textColor=AZUL_OSCURO,
            fontName="Helvetica-BoldOblique", leading=16,
            leftIndent=15, spaceAfter=6, backColor=colors.HexColor("#FFF8E7"),
            borderPad=8
        ),
        "advertencia": ParagraphStyle(
            "advertencia", fontSize=11, textColor=colors.HexColor("#8B0000"),
            fontName="Helvetica-Bold", leading=16,
            leftIndent=15, spaceAfter=6
        ),
        "codigo": ParagraphStyle(
            "codigo", fontSize=10, textColor=VERDE,
            fontName="Courier-Bold", leading=14,
            leftIndent=20, backColor=AZUL_MED, spaceAfter=6
        ),
        "pie_pagina": ParagraphStyle(
            "pie_pagina", fontSize=9, textColor=GRIS,
            alignment=TA_CENTER, fontName="Helvetica"
        ),
        "indice": ParagraphStyle(
            "indice", fontSize=12, textColor=AZUL_OSCURO,
            fontName="Helvetica", leading=20, spaceAfter=4
        ),
        "destacado": ParagraphStyle(
            "destacado", fontSize=13, textColor=NARANJA,
            fontName="Helvetica-Bold", leading=18,
            alignment=TA_CENTER, spaceAfter=8
        ),
    }
    return estilos


def encabezado_pagina(canvas, doc):
    """Dibuja encabezado y pie en cada página."""
    canvas.saveState()
    w, h = letter

    # Barra superior naranja
    canvas.setFillColor(NARANJA)
    canvas.rect(0, h - 28, w, 28, fill=1, stroke=0)
    canvas.setFillColor(BLANCO)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(40, h - 18, "CRYPTO PARA PRINCIPIANTES")
    canvas.setFont("Helvetica", 10)
    canvas.drawRightString(w - 40, h - 18, "Guia Completa 2024")

    # Pie de página
    canvas.setFillColor(AZUL_MED)
    canvas.rect(0, 0, w, 25, fill=1, stroke=0)
    canvas.setFillColor(GRIS)
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(w / 2, 8, f"Pagina {doc.page}  |  cryptoguia.pro")
    canvas.setFillColor(NARANJA)
    canvas.drawString(40, 8, "Bitcoin")
    canvas.setFillColor(VERDE)
    canvas.drawRightString(w - 40, 8, "Ethereum")

    canvas.restoreState()


def portada(canvas, doc):
    """Página de portada especial."""
    canvas.saveState()
    w, h = letter

    # Fondo oscuro
    canvas.setFillColor(AZUL_OSCURO)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)

    # Degradado simulado con rectángulos
    for i in range(20):
        alpha = i / 20
        r = int(13 + alpha * 20)
        g = int(17 + alpha * 15)
        b = int(23 + alpha * 30)
        canvas.setFillColorRGB(r/255, g/255, b/255)
        canvas.rect(0, i * (h/20), w, h/20 + 1, fill=1, stroke=0)

    # Círculo decorativo naranja
    canvas.setFillColor(colors.HexColor("#F7931A22"))
    canvas.circle(w/2, h*0.55, 180, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#F7931A11"))
    canvas.circle(w/2, h*0.55, 240, fill=1, stroke=0)

    # Símbolo Bitcoin grande
    canvas.setFillColor(NARANJA)
    canvas.setFont("Helvetica-Bold", 90)
    canvas.drawCentredString(w/2, h*0.50, "B")

    # Líneas decorativas
    canvas.setStrokeColor(NARANJA)
    canvas.setLineWidth(2)
    canvas.line(60, h*0.72, w-60, h*0.72)
    canvas.line(60, h*0.30, w-60, h*0.30)

    # Título principal
    canvas.setFillColor(NARANJA)
    canvas.setFont("Helvetica-Bold", 38)
    canvas.drawCentredString(w/2, h*0.78, "CRYPTO PARA")
    canvas.drawCentredString(w/2, h*0.72, "PRINCIPIANTES")

    # Subtítulo
    canvas.setFillColor(BLANCO)
    canvas.setFont("Helvetica", 16)
    canvas.drawCentredString(w/2, h*0.64, "La guia definitiva para empezar a")
    canvas.drawCentredString(w/2, h*0.60, "invertir en criptomonedas en 2024")

    # Precio
    canvas.setFillColor(VERDE)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(w/2, h*0.53, "Valor: $9.99 USD")

    # Barra inferior
    canvas.setFillColor(NARANJA)
    canvas.rect(0, 0, w, 50, fill=1, stroke=0)
    canvas.setFillColor(AZUL_OSCURO)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(w/2, 18,
        "Estrategias reales | Sin jerga tecnica | Resultados desde el dia 1")

    canvas.restoreState()


def generar_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        rightMargin=50, leftMargin=50,
        topMargin=55, bottomMargin=45,
        title="Crypto para Principiantes",
        author="CryptoGuia Pro",
        subject="Guia de inversion en criptomonedas para principiantes"
    )

    E = crear_estilos()
    story = []

    # ══════════════════════════════════════════════════════
    # PORTADA (se maneja con onFirstPage)
    # ══════════════════════════════════════════════════════
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # PÁGINA 2: ÍNDICE
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("CONTENIDO DEL CURSO", E["capitulo"]))
    story.append(HRFlowable(width="100%", thickness=2, color=NARANJA))
    story.append(Spacer(1, 12))

    indice = [
        ("01", "Que es el crypto y por que importa", "3"),
        ("02", "Las 5 criptomonedas mas seguras para empezar", "5"),
        ("03", "Como crear tu primera wallet", "8"),
        ("04", "Binance: Tu primera compra paso a paso", "10"),
        ("05", "Estrategia de inversion para principiantes", "13"),
        ("06", "Gestion de riesgo: Como no perder todo", "16"),
        ("07", "DCA: La estrategia mas simple y efectiva", "18"),
        ("08", "Errores que cometen todos los principiantes", "20"),
        ("09", "Herramientas esenciales gratuitas", "22"),
        ("10", "Plan de accion para tus primeros 30 dias", "24"),
    ]

    for num, titulo, pag in indice:
        story.append(Paragraph(
            f"<b><font color='#F7931A'>{num}</font></b>  {titulo} "
            f"<font color='#8B949E'>{'.' * (45 - len(titulo))} {pag}</font>",
            E["indice"]
        ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # CAP 1: QUE ES CRYPTO
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("01. QUE ES EL CRYPTO Y POR QUE IMPORTA", E["capitulo"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NARANJA))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Las criptomonedas son dinero digital que funciona sin bancos ni gobiernos. "
        "En lugar de que un banco controle tus transacciones, una red de miles de "
        "computadoras alrededor del mundo verifica y registra cada movimiento en algo "
        "llamado blockchain.", E["cuerpo"]
    ))
    story.append(Paragraph(
        "Piensalo asi: el dinero tradicional es como un cuaderno contable guardado "
        "en el banco. El crypto es ese mismo cuaderno pero copiado en millones de "
        "computadoras al mismo tiempo. Nadie puede alterarlo, nadie puede censurarlo, "
        "y no necesitas permiso de nadie para usarlo.", E["cuerpo"]
    ))

    story.append(Paragraph("Por que la gente invierte en crypto:", E["subtitulo"]))
    bullets_cap1 = [
        "Potencial de crecimiento: Bitcoin paso de $0.01 en 2010 a $73,000 en 2024",
        "Proteccion contra la inflacion: A diferencia del peso o dolar, Bitcoin tiene oferta limitada",
        "Accesibilidad: Puedes empezar con $10 desde tu telefono",
        "Descentralizacion: Tu dinero, tus reglas, sin intermediarios",
        "Mercado 24/7: Opera los 365 dias del ano, a cualquier hora",
    ]
    for b in bullets_cap1:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {b}", E["bullet"]))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "DATO CLAVE: Si hubieras invertido $100 en Bitcoin en 2015, "
        "hoy tendrias mas de $50,000 USD.", E["tip"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "ADVERTENCIA: El crypto es volatil. Puede subir 50% en un mes "
        "y bajar 40% en el siguiente. NUNCA inviertas dinero que no puedas "
        "permitirte perder.", E["advertencia"]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # CAP 2: LAS 5 CRIPTOS
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("02. LAS 5 CRIPTOMONEDAS MAS SEGURAS PARA EMPEZAR", E["capitulo"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NARANJA))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Existen mas de 20,000 criptomonedas. La MAYORIA son basura. "
        "Como principiante, debes concentrarte en las que tienen anos de historial, "
        "alta liquidez y equipos solidos. Estas son las 5 mas seguras:", E["cuerpo"]
    ))

    datos_crypto = [
        ["#", "Cripto", "Simbolo", "Riesgo", "Para que sirve"],
        ["1", "Bitcoin", "BTC", "Bajo", "Reserva de valor, 'oro digital'"],
        ["2", "Ethereum", "ETH", "Bajo-Med", "Contratos inteligentes, DeFi"],
        ["3", "BNB", "BNB", "Medio", "Fees baratos en Binance"],
        ["4", "Solana", "SOL", "Medio", "Transacciones ultra rapidas"],
        ["5", "USDC/USDT", "Stables", "Muy bajo", "Valor fijo = $1 USD"],
    ]

    tabla = Table(datos_crypto, colWidths=[30, 80, 65, 80, 230])
    tabla.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NARANJA),
        ("TEXTCOLOR",    (0,0), (-1,0), BLANCO),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,0), 11),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("ALIGN",        (4,1), (4,-1), "LEFT"),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",     (0,1), (-1,-1), 10),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[GRIS_CLARO, BLANCO]),
        ("GRID",         (0,0), (-1,-1), 0.5, GRIS),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
    ]))
    story.append(tabla)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Recomendacion para empezar con $21:", E["subtitulo"]))
    distribucion = [
        ["Cripto", "Porcentaje", "Monto ($21)", "Razon"],
        ["Bitcoin (BTC)",  "50%", "$10.50", "Base solida, menor riesgo"],
        ["Ethereum (ETH)", "30%", "$6.30",  "Alto potencial de crecimiento"],
        ["BNB",            "20%", "$4.20",  "Fees baratos en Binance"],
    ]
    t2 = Table(distribucion, colWidths=[120, 90, 90, 185])
    t2.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), AZUL_MED),
        ("TEXTCOLOR",     (0,0), (-1,0), NARANJA),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0), (-1,-1), 10),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#F0FFF8"), BLANCO]),
        ("GRID",          (0,0), (-1,-1), 0.5, GRIS),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(t2)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # CAP 3: WALLET
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("03. COMO CREAR TU PRIMERA WALLET", E["capitulo"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NARANJA))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Una wallet (billetera) es donde guardas tus criptomonedas. "
        "Existen dos tipos principales:", E["cuerpo"]
    ))

    story.append(Paragraph("Wallets Custodiales (recomendado para principiantes)", E["subtitulo"]))
    story.append(Paragraph(
        "La exchange (como Binance) guarda las llaves por ti. Es como una cuenta "
        "bancaria: facil de usar pero dependes de la plataforma.", E["cuerpo"]
    ))
    story.append(Paragraph("Ventajas: Simple, soporte tecnico, recuperas acceso si pierdes contrasena.", E["bullet"]))
    story.append(Paragraph("Desventajas: No tienes control total, riesgo si la exchange quiebra.", E["bullet"]))

    story.append(Paragraph("Wallets No Custodiales (para avanzados)", E["subtitulo"]))
    story.append(Paragraph(
        "Tu controlas las llaves privadas completamente. Nadie mas puede acceder. "
        "Opciones populares: MetaMask (navegador), Trust Wallet (movil), Ledger (hardware).", E["cuerpo"]
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "REGLA DE ORO: 'Not your keys, not your coins'. Si quieres seguridad "
        "maxima para grandes cantidades, usa wallet propia. Para empezar, Binance esta bien.", E["tip"]
    ))

    story.append(Paragraph("Pasos para crear wallet en Binance:", E["subtitulo"]))
    pasos = [
        ("1", "Ve a binance.com y click en 'Registrarse'"),
        ("2", "Ingresa tu email y crea una contrasena segura (mayusculas + numeros + simbolos)"),
        ("3", "Verifica tu email con el codigo que te enviaron"),
        ("4", "Completa la verificacion KYC (foto de tu ID)"),
        ("5", "Activa autenticacion de 2 factores (Google Authenticator)"),
        ("6", "Listo - ya tienes tu wallet en Binance"),
    ]
    for num, paso in pasos:
        story.append(Paragraph(
            f"<b><font color='#F7931A'>Paso {num}:</font></b> {paso}", E["bullet"]
        ))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "SEGURIDAD CRITICA: Nunca compartas tu seed phrase (12-24 palabras) "
        "con NADIE. Ni soporte tecnico, ni amigos, ni tu mismo por email.", E["advertencia"]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # CAP 4: PRIMERA COMPRA
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("04. BINANCE: TU PRIMERA COMPRA PASO A PASO", E["capitulo"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NARANJA))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Binance es el exchange mas grande del mundo con mas de 120 millones "
        "de usuarios. Aqui te explico como hacer tu primera compra:", E["cuerpo"]
    ))

    pasos_compra = [
        ("Depositar fondos", "Ve a 'Comprar Crypto' > 'Tarjeta de credito/debito'. "
         "Puedes depositar desde $10 USD con Visa o Mastercard."),
        ("Elegir el par", "En el apartado 'Mercados', busca BTC/USDT o ETH/USDT. "
         "Siempre opera contra USDT (dolar digital estable)."),
        ("Tipo de orden", "Para principiantes: usa 'Orden de Mercado'. "
         "Compra al precio actual sin complicaciones."),
        ("Cantidad", "Ingresa cuanto USDT quieres gastar. Minimo: $10. "
         "Binance cobra 0.1% de comision por operacion."),
        ("Confirmar", "Revisa el resumen, confirma con tu 2FA y listo. "
         "Tu crypto aparece en tu wallet en segundos."),
    ]

    for titulo_paso, desc in pasos_compra:
        story.append(Paragraph(f"<b><font color='#F7931A'>{titulo_paso}:</font></b> {desc}", E["bullet"]))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "COMISIONES EN BINANCE: Spot trading = 0.1% | Con BNB = 0.075% | "
        "Deposito con tarjeta = ~1.8%", E["tip"]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # CAP 5: ESTRATEGIA
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("05. ESTRATEGIA DE INVERSION PARA PRINCIPIANTES", E["capitulo"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NARANJA))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "La mayoria de principiantes pierde dinero por no tener estrategia. "
        "Aqui te presento las 3 estrategias mas efectivas ordenadas de menor "
        "a mayor complejidad:", E["cuerpo"]
    ))

    estrategias = [
        ("ESTRATEGIA 1: HODL (Hold On for Dear Life)",
         "Compras y mantienes a largo plazo (1-4 anos). "
         "Ideal para BTC y ETH. Historicamente, quien mantiene 4+ anos siempre ha ganado.",
         "Muy Bajo", "10/10 para principiantes"),
        ("ESTRATEGIA 2: DCA (Dollar Cost Averaging)",
         "Inviertes una cantidad fija cada semana/mes sin importar el precio. "
         "$20 cada lunes en BTC, por ejemplo. Elimina el estres de 'cuando comprar'.",
         "Bajo", "9/10 para principiantes"),
        ("ESTRATEGIA 3: Swing Trading",
         "Compras en zonas de soporte y vendes en resistencias. "
         "Requiere analisis tecnico basico. Para cuando ya tengas 3+ meses de experiencia.",
         "Medio-Alto", "5/10 para principiantes"),
    ]

    for nombre, desc, riesgo, puntuacion in estrategias:
        story.append(Paragraph(nombre, E["subtitulo"]))
        story.append(Paragraph(desc, E["cuerpo"]))
        story.append(Paragraph(
            f"Nivel de riesgo: <b>{riesgo}</b>  |  Recomendacion: <b>{puntuacion}</b>",
            E["tip"]
        ))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # CAP 6: GESTION DE RIESGO
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("06. GESTION DE RIESGO: COMO NO PERDER TODO", E["capitulo"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NARANJA))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "El 90% de traders principiantes pierde dinero en el primer ano. "
        "La razon: no gestionan el riesgo. Estas reglas te protegeran:", E["cuerpo"]
    ))

    reglas = [
        ("Regla del 1-2%",
         "Nunca arriesgues mas del 1-2% de tu capital en una sola operacion. "
         "Con $100, tu riesgo maximo por trade es $2."),
        ("Diversificacion",
         "No pongas todo en una sola cripto. Distribuye entre BTC, ETH y "
         "stablecoins para reducir volatilidad."),
        ("Stop Loss obligatorio",
         "Siempre define tu punto de salida ANTES de comprar. Si cae 5-8%, vende. "
         "No esperes 'que se recupere'."),
        ("Fondo de emergencia primero",
         "NUNCA inviertas dinero que necesitas. Primero 3-6 meses de gastos en ahorros, "
         "luego invierte el excedente."),
        ("No uses apalancamiento",
         "El trading con apalancamiento (futuros) puede liquidarte en minutos. "
         "Como principiante: JAMAS uses futuros ni margin trading."),
        ("Emociones fuera",
         "El FOMO (miedo a quedarte fuera) y el FUD (miedo, incertidumbre) son "
         "tus peores enemigos. Sigue tu plan, no las emociones."),
    ]

    for titulo_r, desc_r in reglas:
        story.append(Paragraph(
            f"<b><font color='#F7931A'>{titulo_r}:</font></b> {desc_r}", E["bullet"]
        ))
        story.append(Spacer(1, 5))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # CAP 7: DCA
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("07. DCA: LA ESTRATEGIA MAS SIMPLE Y EFECTIVA", E["capitulo"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NARANJA))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Dollar Cost Averaging (DCA) significa invertir una cantidad fija "
        "de manera periodica, sin importar si el precio esta alto o bajo. "
        "Esta estrategia elimina el mayor error del principiante: intentar "
        "predecir el mercado.", E["cuerpo"]
    ))

    story.append(Paragraph("Ejemplo practico con $50/mes:", E["subtitulo"]))

    dca_data = [
        ["Mes", "Precio BTC", "Inversion", "BTC Comprado", "BTC Total"],
        ["Enero",    "$45,000", "$50", "0.00111", "0.00111"],
        ["Febrero",  "$38,000", "$50", "0.00132", "0.00243"],
        ["Marzo",    "$52,000", "$50", "0.00096", "0.00339"],
        ["Abril",    "$61,000", "$50", "0.00082", "0.00421"],
        ["Mayo",     "$55,000", "$50", "0.00091", "0.00512"],
        ["TOTAL",    "Prom: $50,200", "$250", "0.00512 BTC", "Valor: $281"],
    ]
    t3 = Table(dca_data, colWidths=[60, 90, 75, 100, 160])
    t3.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),  (-1,0),  NARANJA),
        ("BACKGROUND",    (0,-1), (-1,-1), AZUL_MED),
        ("TEXTCOLOR",     (0,0),  (-1,0),  BLANCO),
        ("TEXTCOLOR",     (0,-1), (-1,-1), VERDE),
        ("FONTNAME",      (0,0),  (-1,0),  "Helvetica-Bold"),
        ("FONTNAME",      (0,-1), (-1,-1), "Helvetica-Bold"),
        ("FONTNAME",      (0,1),  (-1,-2), "Helvetica"),
        ("FONTSIZE",      (0,0),  (-1,-1), 10),
        ("ALIGN",         (0,0),  (-1,-1), "CENTER"),
        ("ROWBACKGROUNDS",(0,1),  (-1,-2), [GRIS_CLARO, BLANCO]),
        ("GRID",          (0,0),  (-1,-1), 0.5, GRIS),
        ("TOPPADDING",    (0,0),  (-1,-1), 6),
        ("BOTTOMPADDING", (0,0),  (-1,-1), 6),
    ]))
    story.append(t3)
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Invertiste $250 y tienes $281. Una ganancia de 12.4% "
        "sin estresarte por el precio diario.", E["destacado"]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # CAP 8: ERRORES
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("08. ERRORES QUE COMETEN TODOS LOS PRINCIPIANTES", E["capitulo"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NARANJA))
    story.append(Spacer(1, 8))

    errores = [
        ("Comprar en el maximo por FOMO",
         "Ver una cripto subir 200% y comprar en el pico. "
         "Solucion: usa DCA y no persigas rallies."),
        ("Vender en el minimo por panico",
         "Vender todo cuando el mercado cae 30%. "
         "El mercado crypto SIEMPRE ha recuperado historicamente."),
        ("Invertir en 'shitcoins' prometedoras",
         "Caer en proyectos con 'promesas increibles' y sin historial. "
         "El 95% de altcoins llegan a cero. Queda con BTC/ETH al inicio."),
        ("No tener plan de salida",
         "No decidir de antemano a que precio venderas. "
         "Define objetivos: 'Si sube 50%, vendo la mitad'."),
        ("Poner todo el dinero de una vez",
         "Invertir todo en un solo dia. Si cae 40% el dia siguiente, "
         "psicologicamente es devastador. Usa DCA."),
        ("Ignorar los impuestos",
         "En la mayoria de paises, las ganancias crypto son gravables. "
         "Guarda registro de todas tus operaciones desde el principio."),
    ]

    for i, (titulo_e, desc_e) in enumerate(errores, 1):
        story.append(Paragraph(
            f"<b><font color='#CC0000'>ERROR #{i}: {titulo_e}</font></b>", E["subtitulo"]
        ))
        story.append(Paragraph(desc_e, E["cuerpo"]))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # CAP 9: HERRAMIENTAS
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("09. HERRAMIENTAS ESENCIALES GRATUITAS", E["capitulo"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NARANJA))
    story.append(Spacer(1, 8))

    herramientas = [
        ["Herramienta", "URL", "Para que sirve"],
        ["CoinMarketCap",  "coinmarketcap.com",  "Ver precios y rankings en tiempo real"],
        ["TradingView",    "tradingview.com",     "Graficas y analisis tecnico"],
        ["CoinGecko",      "coingecko.com",       "Datos de mercado alternativos"],
        ["Messari",        "messari.io",          "Investigacion y fundamentales"],
        ["DeFi Llama",     "defillama.com",       "Total Value Locked en DeFi"],
        ["Glassnode",      "glassnode.com",       "Datos on-chain de Bitcoin"],
        ["Fear & Greed",   "alternative.me",      "Indice de miedo y codicia"],
        ["CryptoTaxCalc",  "cryptotaxcalculator.io", "Calcular impuestos cripto"],
    ]

    t4 = Table(herramientas, colWidths=[120, 140, 225])
    t4.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),  (-1,0),  NARANJA),
        ("TEXTCOLOR",     (0,0),  (-1,0),  BLANCO),
        ("FONTNAME",      (0,0),  (-1,0),  "Helvetica-Bold"),
        ("FONTNAME",      (0,1),  (-1,-1), "Helvetica"),
        ("TEXTCOLOR",     (1,1),  (1,-1),  colors.HexColor("#0066CC")),
        ("FONTSIZE",      (0,0),  (-1,-1), 10),
        ("ALIGN",         (0,0),  (-1,-1), "LEFT"),
        ("ROWBACKGROUNDS",(0,1),  (-1,-1), [GRIS_CLARO, BLANCO]),
        ("GRID",          (0,0),  (-1,-1), 0.5, GRIS),
        ("TOPPADDING",    (0,0),  (-1,-1), 7),
        ("BOTTOMPADDING", (0,0),  (-1,-1), 7),
        ("LEFTPADDING",   (0,0),  (-1,-1), 8),
    ]))
    story.append(t4)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # CAP 10: PLAN DE ACCION
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("10. PLAN DE ACCION: TUS PRIMEROS 30 DIAS", E["capitulo"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NARANJA))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Aqui tienes un plan concreto y sin excusas para empezar hoy mismo. "
        "Sigue este calendario y en 30 dias tendras tu primera inversion activa:", E["cuerpo"]
    ))

    plan = [
        ["Semana", "Acciones", "Tiempo"],
        ["Semana 1\n(Dias 1-7)",
         "1. Crea cuenta en Binance\n2. Completa verificacion KYC\n"
         "3. Activa 2FA\n4. Lee sobre Bitcoin en bitcoin.org",
         "2-3 hrs"],
        ["Semana 2\n(Dias 8-14)",
         "1. Deposita $10-20 USD\n2. Compra tu primera fraccion de BTC\n"
         "3. Explora la plataforma\n4. Configura alertas de precio",
         "1-2 hrs"],
        ["Semana 3\n(Dias 15-21)",
         "1. Lee sobre Ethereum\n2. Compra una pequena cantidad de ETH\n"
         "3. Aprende a leer graficas basicas en TradingView",
         "2-3 hrs"],
        ["Semana 4\n(Dias 22-30)",
         "1. Configura DCA automatico en Binance\n"
         "2. Registra tus operaciones en una hoja de calculo\n"
         "3. Define tu estrategia a 6-12 meses",
         "1-2 hrs"],
    ]

    t5 = Table(plan, colWidths=[90, 340, 55])
    t5.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),  (-1,0),  NARANJA),
        ("TEXTCOLOR",     (0,0),  (-1,0),  BLANCO),
        ("FONTNAME",      (0,0),  (-1,0),  "Helvetica-Bold"),
        ("FONTNAME",      (0,1),  (-1,-1), "Helvetica"),
        ("FONTNAME",      (0,1),  (0,-1),  "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,1),  (0,-1),  NARANJA),
        ("FONTSIZE",      (0,0),  (-1,-1), 10),
        ("ALIGN",         (0,0),  (-1,-1), "LEFT"),
        ("VALIGN",        (0,0),  (-1,-1), "TOP"),
        ("ROWBACKGROUNDS",(0,1),  (-1,-1), [GRIS_CLARO, BLANCO]),
        ("GRID",          (0,0),  (-1,-1), 0.5, GRIS),
        ("TOPPADDING",    (0,0),  (-1,-1), 8),
        ("BOTTOMPADDING", (0,0),  (-1,-1), 8),
        ("LEFTPADDING",   (0,0),  (-1,-1), 8),
    ]))
    story.append(t5)

    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "RECUERDA: El mejor momento para empezar a invertir fue hace 10 anos. "
        "El segundo mejor momento es HOY.", E["destacado"]
    ))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=NARANJA))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Gracias por adquirir esta guia. Si tienes preguntas, "
        "contactanos en: soporte@cryptoguia.pro", E["pie_pagina"]
    ))
    story.append(Paragraph(
        "cryptoguia.pro  |  Todos los derechos reservados 2024", E["pie_pagina"]
    ))

    # ── CONSTRUIR PDF ──────────────────────────────────────────────────
    doc.build(
        story,
        onFirstPage=portada,
        onLaterPages=encabezado_pagina
    )
    size = os.path.getsize(OUTPUT) / 1024
    print(f"PDF generado: {OUTPUT} ({size:.0f} KB)")
    return OUTPUT


if __name__ == "__main__":
    generar_pdf()
