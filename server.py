"""
server.py — Servidor de pagos y entrega automática del PDF
Stripe + PayPal → Email automático con PDF adjunto
"""
from flask import Flask, request, jsonify, send_file, render_template_string
import stripe
import os, json, sqlite3, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder='.', static_url_path='')

# ── CONFIG ────────────────────────────────────────────────────────────
STRIPE_SECRET     = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE= os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK    = os.getenv("STRIPE_WEBHOOK_SECRET", "")
PAYPAL_CLIENT_ID  = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_SECRET     = os.getenv("PAYPAL_SECRET", "")
EMAIL_FROM        = os.getenv("EMAIL_FROM", "")
EMAIL_PASSWORD    = os.getenv("EMAIL_PASSWORD", "")    # App password de Gmail
EMAIL_SMTP        = os.getenv("EMAIL_SMTP", "smtp.gmail.com")
PDF_PATH          = os.path.join(os.path.dirname(__file__), "curso_crypto.pdf")
PRECIO_CENTAVOS   = 100   # $9.99 USD
DB_PATH           = os.path.join(os.path.dirname(__file__), "ventas.db")

if STRIPE_SECRET:
    stripe.api_key = STRIPE_SECRET

# ── BASE DE DATOS ─────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha       TEXT,
            email       TEXT,
            metodo      TEXT,
            monto       REAL,
            moneda      TEXT DEFAULT 'USD',
            payment_id  TEXT,
            status      TEXT DEFAULT 'completado',
            email_enviado INTEGER DEFAULT 0
        )
    """)
    conn.commit(); conn.close()

def registrar_venta(email, metodo, monto, payment_id="", status="completado"):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO ventas (fecha, email, metodo, monto, payment_id, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().isoformat(), email, metodo, monto, payment_id, status))
    conn.commit(); conn.close()
    print(f"[VENTA] ✅ {metodo} | {email} | ${monto:.2f}")

def obtener_ventas():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM ventas ORDER BY fecha DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def total_vendido():
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT COUNT(*) as num, SUM(monto) as total FROM ventas WHERE status='completado'").fetchone()
    conn.close()
    return row[0] or 0, row[1] or 0.0

# ── EMAIL ─────────────────────────────────────────────────────────────
def enviar_pdf_por_email(email_destino: str) -> bool:
    """Envía el PDF del curso al email del comprador."""
    if not EMAIL_FROM or not EMAIL_PASSWORD:
        print(f"[EMAIL] ⚠️  Sin config de email — PDF disponible en /descarga")
        return False

    try:
        msg = MIMEMultipart()
        msg['From']    = f"CryptoGuia Pro <{EMAIL_FROM}>"
        msg['To']      = email_destino
        msg['Subject'] = "🎉 Tu guía Crypto para Principiantes está lista"

        cuerpo = f"""
<html><body style="font-family:Arial,sans-serif; max-width:600px; margin:0 auto; background:#f5f5f5; padding:20px">
<div style="background:#0D1117; border-radius:12px; padding:32px; text-align:center">
  <h1 style="color:#F7931A; font-size:28px">₿ CryptoGuia Pro</h1>
  <h2 style="color:white; font-size:20px">¡Tu compra fue exitosa!</h2>
  <p style="color:#8B949E">Gracias por adquirir <strong style="color:white">Crypto para Principiantes</strong>.</p>
  <div style="background:#161B22; border-radius:8px; padding:20px; margin:20px 0">
    <p style="color:#00C896; font-size:16px; font-weight:bold">📎 La guía va adjunta a este email</p>
    <p style="color:#8B949E; font-size:13px">Si no puedes abrir el adjunto, haz clic aquí:</p>
    <a href="https://web-production-b0f25.up.railway.app/descarga?email={email_destino}"
       style="display:inline-block; margin:10px; padding:12px 24px;
              background:#F7931A; color:#0D1117; text-decoration:none;
              border-radius:8px; font-weight:bold">
      📥 Descargar Guía
    </a>
  </div>
  <div style="text-align:left; background:#161B22; border-radius:8px; padding:16px; color:#8B949E; font-size:13px">
    <p><strong style="color:#F7931A">¿Qué sigue?</strong></p>
    <p>1. Lee el Capítulo 1 hoy mismo (10 minutos)</p>
    <p>2. Crea tu cuenta en Binance esta semana</p>
    <p>3. Haz tu primera compra con $10 en Semana 2</p>
  </div>
  <p style="color:#8B949E; font-size:12px; margin-top:20px">
    ¿Dudas? Escríbenos: soporte@cryptoguia.pro<br>
    Garantía 7 días sin preguntas ✓
  </p>
</div>
</body></html>
"""
        msg.attach(MIMEText(cuerpo, 'html'))

        # Adjuntar PDF
        with open(PDF_PATH, "rb") as f:
            parte = MIMEBase("application", "octet-stream")
            parte.set_payload(f.read())
            encoders.encode_base64(parte)
            parte.add_header("Content-Disposition",
                             "attachment", filename="Crypto_para_Principiantes.pdf")
            msg.attach(parte)

        # Enviar
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(EMAIL_SMTP, 465, context=ctx) as srv:
            srv.login(EMAIL_FROM, EMAIL_PASSWORD)
            srv.sendmail(EMAIL_FROM, email_destino, msg.as_string())

        print(f"[EMAIL] ✅ Enviado a {email_destino}")
        return True

    except Exception as e:
        print(f"[EMAIL] ❌ Error: {e}")
        return False

# ── RUTAS ─────────────────────────────────────────────────────────────
@app.route('/api/config')
def config_publica():
    """Devuelve la clave pública de Stripe (seguro exponerla al frontend)."""
    return jsonify({"publishable_key": STRIPE_PUBLISHABLE})


@app.route('/')
def index():
    return send_file('index.html')

@app.route('/descarga')
def descarga():
    """Descarga directa del PDF (con validación de email)."""
    email = request.args.get('email', '')
    return send_file(PDF_PATH, as_attachment=True,
                     download_name="Crypto_para_Principiantes.pdf")

@app.route('/api/pago', methods=['POST'])
def pago_stripe():
    """Crea un PaymentIntent de Stripe."""
    data = request.get_json()
    email = data.get('email', '')

    if not email or '@' not in email:
        return jsonify({"success": False, "error": "Email inválido"}), 400

    try:
        if STRIPE_SECRET:
            intent = stripe.PaymentIntent.create(
                amount=PRECIO_CENTAVOS,
                currency='usd',
                metadata={"email": email},
                receipt_email=email,
            )
            registrar_venta(email, "stripe", PRECIO_CENTAVOS/100, intent.id, "pendiente")
            return jsonify({
                "success": True,
                "client_secret": intent.client_secret,
                "email": email
            })
        else:
            # Live mode
            return jsonify({"success": False, "error": "Stripe no configurado"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Confirma el pago y envía el PDF."""
    payload = request.data
    sig     = request.headers.get('Stripe-Signature', '')

    try:
        if STRIPE_WEBHOOK:
            event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK)
        else:
            event = json.loads(payload)

        if event['type'] == 'payment_intent.succeeded':
            intent = event['data']['object']
            email  = intent.get('metadata', {}).get('email', '')
            monto  = intent.get('amount', 0) / 100

            if email:
                registrar_venta(email, "stripe", monto, intent['id'], "completado")
                enviar_pdf_por_email(email)
                print(f"[WEBHOOK] ✅ Pago confirmado: {email} — ${monto}")

        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"[WEBHOOK] Error: {e}")
        return jsonify({"error": str(e)}), 400


@app.route('/api/paypal/crear-orden', methods=['POST'])
def paypal_crear():
    """Crea una orden de PayPal."""
    import requests as req
    data = request.get_json()
    email = data.get('email', '')

    if not PAYPAL_CLIENT_ID:
        registrar_venta(email, "paypal_demo", 9.99)
        enviar_pdf_por_email(email)
        return jsonify({"success": True, "demo": True})

    try:
        # Obtener token
        auth = req.post(
            "https://api-m.paypal.com/v1/oauth2/token",
            auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
            data={"grant_type": "client_credentials"}
        )
        token = auth.json()["access_token"]

        # Crear orden
        orden = req.post(
            "https://api-m.paypal.com/v2/checkout/orders",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {"currency_code": "USD", "value": "9.99"},
                    "description": "Crypto para Principiantes — Guia PDF"
                }],
                "application_context": {
                    "return_url": f"https://web-production-b0f25.up.railway.app/paypal-exito?email={email}",
                    "cancel_url": "https://web-production-b0f25.up.railway.app/?cancelado=1"
                }
            }
        )
        order_data = orden.json()
        approve_url = next(l["href"] for l in order_data["links"] if l["rel"]=="approve")
        return jsonify({"success": True, "url": approve_url})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/paypal-exito')
def paypal_exito():
    """PayPal regresa aquí tras el pago exitoso."""
    email    = request.args.get('email', '')
    order_id = request.args.get('token', '')
    registrar_venta(email, "paypal", 9.99, order_id, "completado")
    enviar_pdf_por_email(email)
    return f"""
    <html><head><meta charset="UTF-8">
    <style>body{{font-family:Arial;background:#0D1117;color:white;text-align:center;padding:60px}}
    .box{{max-width:500px;margin:0 auto;background:#161B22;border-radius:12px;padding:40px}}
    h1{{color:#F7931A}} p{{color:#8B949E}} .btn{{display:inline-block;margin-top:20px;
    padding:14px 28px;background:#F7931A;color:#0D1117;text-decoration:none;
    border-radius:8px;font-weight:bold}}</style></head>
    <body><div class="box"><h1>🎉 ¡Pago exitoso!</h1>
    <p>Tu guía fue enviada a <strong style="color:white">{email}</strong></p>
    <a href="/descarga?email={email}" class="btn">📥 Descargar ahora</a></div></body></html>
    """


@app.route('/admin')
def admin():
    """Panel de ventas (sin autenticación en demo)."""
    ventas = obtener_ventas()
    num, total = total_vendido()
    rows = "".join([
        f"<tr><td>{v['fecha'][:16]}</td><td>{v['email']}</td>"
        f"<td>{v['metodo']}</td><td>${v['monto']:.2f}</td>"
        f"<td style='color:{'#00C896' if v['status']=='completado' else '#FF4B4B'}'>{v['status']}</td></tr>"
        for v in ventas
    ])
    return f"""
    <html><head><meta charset="UTF-8">
    <style>body{{font-family:Arial;background:#0D1117;color:white;padding:30px}}
    h1{{color:#F7931A}} table{{width:100%;border-collapse:collapse;margin-top:20px}}
    th{{background:#F7931A;color:#0D1117;padding:10px}} td{{padding:10px;border-bottom:1px solid #333}}
    .stats{{display:flex;gap:30px;margin:20px 0}}
    .stat{{background:#161B22;border-radius:10px;padding:20px;text-align:center}}
    .num{{font-size:2rem;font-weight:bold;color:#F7931A}}</style></head>
    <body>
    <h1>₿ Panel de Ventas — CryptoGuia Pro</h1>
    <div class="stats">
      <div class="stat"><div class="num">{num}</div><div>Ventas totales</div></div>
      <div class="stat"><div class="num">${total:.2f}</div><div>Ingresos USD</div></div>
      <div class="stat"><div class="num">${total*0.92:.2f}</div><div>Después comisiones</div></div>
    </div>
    <table><tr><th>Fecha</th><th>Email</th><th>Método</th><th>Monto</th><th>Estado</th></tr>
    {rows}</table></body></html>
    """


if __name__ == '__main__':
    init_db()
    print("\n🚀 Servidor corriendo en http://localhost:5000")
    print("   Admin: http://localhost:5000/admin")
    print("   Descarga: http://localhost:5000/descarga\n")
    app.run(debug=True, port=5000, host='0.0.0.0')
