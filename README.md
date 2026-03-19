# 💰 CryptoGuia Pro — Tienda Digital

Vende el PDF "Crypto para Principiantes" a $9.99 con pagos via Stripe y PayPal.
Los pagos llegan directo a tu cuenta. El PDF se entrega automáticamente por email.

---

## ⚡ Instalación rápida

```bash
# 1. Instalar dependencias
pip install flask stripe requests python-dotenv

# 2. Generar el PDF del curso
python3 genera_pdf.py

# 3. Configurar pagos
cp .env.example .env
nano .env   # Pon tus keys de Stripe y PayPal

# 4. Lanzar servidor local
python3 server.py
```

Abre http://localhost:5000 para ver tu tienda.

---

## 🔑 Configurar Stripe (tarjeta de crédito)

1. Crea cuenta en https://stripe.com (gratis)
2. Dashboard → Developers → API Keys
3. Copia la **Secret Key** (sk_live_...) al `.env`
4. Para webhooks: Dashboard → Webhooks → Add endpoint
   - URL: `https://tudominio.com/api/stripe-webhook`
   - Evento: `payment_intent.succeeded`

**Comisión Stripe:** 2.9% + $0.30 por transacción
**En $9.99:** recibes ~$9.40

---

## 🔑 Configurar PayPal

1. Crea cuenta en https://developer.paypal.com
2. Dashboard → My Apps → Create App
3. Copia Client ID y Secret al `.env`
4. En producción cambia las URLs de sandbox a live

**Comisión PayPal:** 3.49% + $0.49 por transacción
**En $9.99:** recibes ~$9.15

---

## 📧 Configurar Email automático (Gmail)

1. Ve a https://myaccount.google.com/apppasswords
2. Crea un App Password para "Mail"
3. Pégalo en `.env` como `EMAIL_PASSWORD`

El PDF se envía automáticamente tras cada pago exitoso.

---

## 🌐 Subir a internet (gratis)

### Opción A: Railway (recomendado)
```bash
# Instalar Railway CLI
npm install -g @railway/cli
railway login
railway up
```

### Opción B: Render
1. Sube el código a GitHub
2. Ve a render.com → New Web Service
3. Conecta tu repo y despliega

---

## 📊 Ver tus ventas

Abre: http://localhost:5000/admin

Muestra:
- Total de ventas
- Ingresos totales
- Historial de compradores

---

## 💡 Estrategia para primeras ventas

1. **TikTok/Instagram:** Publica tips de crypto gratis, vende la guía
2. **Grupos de Facebook:** Comunidades de inversión en México/LATAM  
3. **Reddit:** r/MexicoFinanciero, r/colombia, r/argentina
4. **Twitter/X:** Threads sobre crypto con CTA al final

Con 100 ventas al mes = **$940 USD** netos.
