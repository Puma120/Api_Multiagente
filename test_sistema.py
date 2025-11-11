"""
Script de prueba para verificar la conexión a PostgreSQL y la inicialización del sistema
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """Probar conexión a la base de datos"""
    print("\n" + "="*60)
    print("🔍 PRUEBA 1: Conexión a PostgreSQL")
    print("="*60)
    
    try:
        from database import test_connection, init_db
        
        if test_connection():
            print("✅ Conexión a PostgreSQL exitosa")
            
            # Intentar inicializar base de datos
            print("\n🔧 Inicializando tablas...")
            if init_db():
                print("✅ Tablas creadas correctamente")
                return True
            else:
                print("❌ Error al crear tablas")
                return False
        else:
            print("❌ No se pudo conectar a PostgreSQL")
            print("⚠️  Verifica la variable DATABASE_URL en .env")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_google_api():
    """Probar configuración de Google AI"""
    print("\n" + "="*60)
    print("🔍 PRUEBA 2: Configuración de Google AI")
    print("="*60)
    
    try:
        from config import GOOGLE_API_KEY
        
        if GOOGLE_API_KEY and GOOGLE_API_KEY != "":
            print("✅ GOOGLE_API_KEY configurada")
            
            # Intentar importar y configurar google.generativeai
            import google.generativeai as genai
            genai.configure(api_key=GOOGLE_API_KEY)
            
            # Intentar listar modelos disponibles
            try:
                models = genai.list_models()
                print(f"✅ API de Google AI funcional")
                print(f"📋 Modelos disponibles: {len(list(models))}")
                return True
            except Exception as e:
                print(f"⚠️  API Key configurada pero hay un error: {str(e)}")
                return False
        else:
            print("❌ GOOGLE_API_KEY no configurada")
            print("⚠️  Agrega tu API key en el archivo .env")
            print("🔗 Obtén una en: https://makersuite.google.com/app/apikey")
            return False
            
    except ImportError:
        print("❌ google-generativeai no está instalado")
        print("⚠️  Ejecuta: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_agents_initialization():
    """Probar inicialización de agentes"""
    print("\n" + "="*60)
    print("🔍 PRUEBA 3: Inicialización de Agentes")
    print("="*60)
    
    try:
        from agentes import (
            PlanificadorAgent, 
            EjecutorAgent, 
            NotificadorAgent,
            InterfazAgent,
            KnowledgeBaseAgent,
            MonitorAgent
        )
        
        agentes = {
            "Planificador": PlanificadorAgent,
            "Ejecutor": EjecutorAgent,
            "Notificador": NotificadorAgent,
            "Interfaz": InterfazAgent,
            "Knowledge Base": KnowledgeBaseAgent,
            "Monitor": MonitorAgent
        }
        
        todos_ok = True
        for nombre, AgentClass in agentes.items():
            try:
                agente = AgentClass()
                print(f"✅ {nombre} inicializado correctamente")
            except Exception as e:
                print(f"❌ Error en {nombre}: {str(e)}")
                todos_ok = False
        
        return todos_ok
        
    except Exception as e:
        print(f"❌ Error al importar agentes: {str(e)}")
        return False

def test_protocols():
    """Probar protocolos de comunicación"""
    print("\n" + "="*60)
    print("🔍 PRUEBA 4: Protocolos de Comunicación")
    print("="*60)
    
    try:
        from protocolos import (
            A2AProtocol,
            ACPProtocol,
            ANPProtocol,
            AGUIProtocol,
            MCPProtocol
        )
        
        # Probar A2A
        msg_a2a = A2AProtocol.create_message(
            sender="Test",
            receiver="Test2",
            message_type="test",
            content={"test": True}
        )
        if A2AProtocol.validate_message(msg_a2a):
            print("✅ Protocolo A2A funcionando")
        
        # Probar ACP
        msg_acp = ACPProtocol.inform(
            sender="Test",
            receiver="Test2",
            fact={"test": True}
        )
        if ACPProtocol.validate_message(msg_acp):
            print("✅ Protocolo ACP funcionando")
        
        # Probar ANP
        neg_anp = ANPProtocol.create_negotiation(
            initiator="Test",
            participants=["Test2"],
            negotiation_type="task_allocation",
            subject={"test": True},
            terms={}
        )
        if ANPProtocol.validate_negotiation(neg_anp):
            print("✅ Protocolo ANP funcionando")
        
        # Probar AGUI
        msg_agui = AGUIProtocol.create_ui_message(
            agent="Test",
            action_type="display",
            component="alert",
            data={"test": True}
        )
        if AGUIProtocol.validate_message(msg_agui):
            print("✅ Protocolo AGUI funcionando")
        
        # Probar MCP
        msg_mcp = MCPProtocol.create_message(
            sender="Test",
            content_type="financial_data",
            data={"amount": 100, "currency": "MXN", "date": "2025-11-10"}
        )
        validation = MCPProtocol.validate_message(msg_mcp)
        if validation["valid"]:
            print("✅ Protocolo MCP funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en protocolos: {str(e)}")
        return False

def test_fastapi():
    """Probar que FastAPI puede iniciarse"""
    print("\n" + "="*60)
    print("🔍 PRUEBA 5: FastAPI")
    print("="*60)
    
    try:
        from main import app
        
        print("✅ Aplicación FastAPI cargada correctamente")
        print(f"📋 Nombre: {app.title}")
        print(f"📋 Versión: {app.version}")
        
        # Contar rutas
        routes = [route for route in app.routes]
        print(f"📋 Endpoints disponibles: {len(routes)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al cargar FastAPI: {str(e)}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("\n" + "="*60)
    print("🚀 SISTEMA MULTIAGENTE DE FINANZAS PERSONALES")
    print("🧪 Ejecutando Pruebas del Sistema")
    print("="*60)
    
    resultados = {
        "Base de Datos": test_database_connection(),
        "Google AI": test_google_api(),
        "Agentes": test_agents_initialization(),
        "Protocolos": test_protocols(),
        "FastAPI": test_fastapi()
    }
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    total = len(resultados)
    exitosas = sum(1 for v in resultados.values() if v)
    
    for nombre, resultado in resultados.items():
        estado = "✅ PASÓ" if resultado else "❌ FALLÓ"
        print(f"{estado:12} | {nombre}")
    
    print("="*60)
    print(f"Resultado: {exitosas}/{total} pruebas exitosas")
    
    if exitosas == total:
        print("\n🎉 ¡Todas las pruebas pasaron! El sistema está listo.")
        print("\n📝 Próximos pasos:")
        print("   1. Ejecuta: uvicorn main:app --reload --port 8000")
        print("   2. Abre: http://localhost:8000/docs")
        print("   3. Importa postman_collection_completo.json en Postman")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        print("\n💡 Consejos:")
        print("   - Verifica que DATABASE_URL esté en .env")
        print("   - Verifica que GOOGLE_API_KEY esté en .env")
        print("   - Ejecuta: pip install -r requirements.txt")
    
    print("="*60)

if __name__ == "__main__":
    main()
