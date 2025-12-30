"""add_initial_user

Revision ID: 5a025f5b928c
Revises: e6672e5da324
Create Date: 2025-12-30 12:12:13.475854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5a025f5b928c'
down_revision: Union[str, Sequence[str], None] = 'e6672e5da324'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    hashed_password = '$2b$12$U3qPZoPBep0.ivlaLs.yJOrsmjieLftvJb/7EiSsUVNDdCaGn1tiK'
    
    op.execute(f"""
        INSERT INTO users (email, hashed_password, created_at)
        VALUES ('admin@test.com', '{hashed_password}', NOW())
        ON CONFLICT (email) DO NOTHING;
    """)
    
    op.execute("""
        INSERT INTO tasks (title, description, status, created_at, owner_id)
        SELECT 
            'Comprar ingredientes para la comida', 
            'Ir al supermercado y comprar verduras, carne y arroz', 
            'pending', 
            NOW() - INTERVAL '2 hours', 
            u.id
        FROM users u WHERE u.email = 'admin@test.com';
        
        INSERT INTO tasks (title, description, status, created_at, owner_id)
        SELECT 
            'Llamar al dentista', 
            'Agendar cita para limpieza dental', 
            'pending', 
            NOW() - INTERVAL '1 day', 
            u.id
        FROM users u WHERE u.email = 'admin@test.com';
        
        INSERT INTO tasks (title, description, status, created_at, owner_id)
        SELECT 
            'Hacer ejercicio', 
            'Ir al gimnasio por 1 hora', 
            'in_progress', 
            NOW() - INTERVAL '30 minutes', 
            u.id
        FROM users u WHERE u.email = 'admin@test.com';
        
        INSERT INTO tasks (title, description, status, created_at, owner_id)
        SELECT 
            'Leer libro', 
            'Terminar de leer el capítulo 5', 
            'done', 
            NOW() - INTERVAL '3 days', 
            u.id
        FROM users u WHERE u.email = 'admin@test.com';
        
        INSERT INTO tasks (title, description, status, created_at, owner_id)
        SELECT 
            'Organizar escritorio', 
            'Limpiar y ordenar el área de trabajo', 
            'done', 
            NOW() - INTERVAL '1 week', 
            u.id
        FROM users u WHERE u.email = 'admin@test.com';
    """)


def downgrade() -> None:
    op.execute("DELETE FROM tasks WHERE owner_id IN (SELECT id FROM users WHERE email = 'admin@test.com');")
    op.execute("DELETE FROM users WHERE email = 'admin@test.com';")
