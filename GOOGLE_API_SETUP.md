# 🔑 Configuración de Google AI Studio API Key

## Paso 1: Obtener tu API Key

1. Visita [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Click en "Get API Key" o "Create API Key"
4. Copia tu API key (ejemplo: `AIzaSy...`)

## Paso 2: Configurar en el Proyecto

### Opción A: Archivo .env (Recomendado)

1. Crea un archivo `.env` en la raíz del proyecto:
```bash
cp .env.example .env
```

2. Abre `.env` y pega tu API key:
```env
DATABASE_URL=postgresql://finanzas_zz74_user:OY8LbDEk5eUbY9qJWtuRwnTy956vEOV0@dpg-d498208dl3ps73fr5cq0-a.oregon-postgres.render.com/finanzas_zz74
GOOGLE_API_KEY=AIzaSy_TU_KEY_AQUI
DEBUG=True
```

### Opción B: Variable de Entorno del Sistema

**Windows PowerShell:**
```powershell
$env:GOOGLE_API_KEY="AIzaSy_TU_KEY_AQUI"
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="AIzaSy_TU_KEY_AQUI"
```

## Paso 3: Verificar Configuración

Ejecuta el script de prueba:
```bash
python test_sistema.py
```

Deberías ver:
```
✅ GOOGLE_API_KEY configurada
✅ API de Google AI funcional
📋 Modelos disponibles: X
```

## Paso 4: Probar los Agentes

Ejecuta el ejemplo de protocolos:
```bash
python ejemplos_protocolos.py
```

Esto inicializará todos los agentes con sus respectivos modelos Gemini.

## Modelos Disponibles

El sistema usa los siguientes modelos de Gemini:

| Agente | Modelo | Características |
|--------|--------|-----------------|
| Planificador | gemini-2.0-flash | Rápido, ideal para planificación |
| Ejecutor | gemini-2.5-flash | Balance velocidad/calidad |
| Notificador | gemini-2.0-flash | Rápido para alertas |
| Interfaz | gemini-2.0-flash | Rápido para formateo |
| Knowledge Base | gemini-2.5-pro | Potente para análisis complejo |
| Monitor | gemini-2.0-flash | Rápido para monitoreo |

## Límites y Cuotas

### Tier Gratuito de Google AI Studio
- **Requests por minuto**: 60
- **Requests por día**: 1,500
- **Tokens por minuto**: 1,000,000

Si necesitas más, considera:
- Google AI Studio Pro
- Vertex AI (producción)

## Solución de Problemas

### Error: "API key not valid"
```
❌ Error: API key not valid. Please pass a valid API key.
```

**Solución**:
1. Verifica que copiaste la key completa
2. Verifica que no tenga espacios al inicio/final
3. Regenera la key en Google AI Studio

### Error: "User location is not supported"
```
❌ Error: User location is not supported for the API use.
```

**Solución**:
- Google AI Studio no está disponible en tu región
- Usa VPN o considera Vertex AI

### Error: "Quota exceeded"
```
❌ Error: Resource has been exhausted (e.g. check quota).
```

**Solución**:
- Espera unos minutos (límite por minuto)
- Verifica tu cuota en Google AI Studio
- Considera upgrade si necesitas más

## Seguridad

### ⚠️ IMPORTANTE: Proteger tu API Key

**Nunca hagas esto:**
```python
# ❌ MAL: Hard-coded en el código
GOOGLE_API_KEY = "AIzaSy..."
```

**Siempre haz esto:**
```python
# ✅ BIEN: Desde variable de entorno
import os
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
```

### .gitignore

Asegúrate de que `.env` esté en `.gitignore`:
```
# .gitignore
.env
.env.local
```

### Para Deploy en Render

1. Ve a tu servicio en Render
2. Environment → Add Environment Variable
3. Key: `GOOGLE_API_KEY`
4. Value: Tu API key
5. Save Changes

## Verificación Final

Ejecuta este comando para verificar todo:
```bash
python -c "from config import GOOGLE_API_KEY; import google.generativeai as genai; genai.configure(api_key=GOOGLE_API_KEY); print('✅ Google AI configurado correctamente')"
```

## Recursos Adicionales

- [Google AI Studio](https://makersuite.google.com/)
- [Documentación Gemini API](https://ai.google.dev/docs)
- [Guía de Python SDK](https://ai.google.dev/tutorials/python_quickstart)
- [Límites y Cuotas](https://ai.google.dev/pricing)

## Contacto

Si tienes problemas con la configuración:
1. Revisa la documentación en `/docs`
2. Ejecuta `python test_sistema.py` para diagnóstico
3. Verifica los logs de la aplicación

---

**Nota**: La API key de Google AI Studio es gratuita para desarrollo y pruebas, pero tiene límites de uso. Para producción, considera Google Cloud Vertex AI.
