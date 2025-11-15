"""
Script para actualizar la base de datos con las nuevas columnas de autenticación
"""
from sqlalchemy import create_engine, text
from database import DATABASE_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_database():
    """Agregar columnas de autenticación a la tabla usuarios"""
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Verificar si las columnas ya existen
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='usuarios' AND column_name='password_hash';
            """))
            
            if result.fetchone() is None:
                logger.info("Agregando columnas de autenticación...")
                
                # Agregar columna password_hash
                conn.execute(text("""
                    ALTER TABLE usuarios 
                    ADD COLUMN password_hash VARCHAR(255);
                """))
                
                # Agregar columna activo
                conn.execute(text("""
                    ALTER TABLE usuarios 
                    ADD COLUMN activo BOOLEAN DEFAULT TRUE;
                """))
                
                # Agregar columna ultimo_login
                conn.execute(text("""
                    ALTER TABLE usuarios 
                    ADD COLUMN ultimo_login TIMESTAMP;
                """))
                
                conn.commit()
                logger.info("✅ Migración completada exitosamente")
            else:
                logger.info("✅ Las columnas ya existen, no se requiere migración")
                
    except Exception as e:
        logger.error(f"❌ Error en la migración: {str(e)}")
        raise

if __name__ == "__main__":
    migrate_database()
