"""SQLite models for Webhook Logger"""
import sqlite3
import os
from datetime import datetime
from typing import Optional


def get_db_path():
    """Get database path from environment or default to /data/webhooks.db"""
    return os.environ.get('WEBHOOK_DB_PATH', '/data/webhooks.db')


def get_connection():
    """Get database connection with proper error handling"""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database and create tables"""
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS webhooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                method TEXT NOT NULL,
                headers TEXT,
                body TEXT,
                ip_address TEXT,
                user_agent TEXT
            )
        """)
        
        conn.commit()
    finally:
        conn.close()


def insert_webhook(method: str, headers: str, body: str,
                   ip_address: str = None, user_agent: str = None) -> int:
    """Insert a webhook and return its ID with proper cleanup"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO webhooks (timestamp, method, headers, body, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (datetime.utcnow().isoformat(), method, headers, body, ip_address, user_agent))
        
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_recent_webhooks(limit: int = 50) -> list:
    """Get recent webhooks with proper cleanup"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, method, headers, body, ip_address, user_agent
            FROM webhooks
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_webhook_by_id(webhook_id: int) -> Optional[dict]:
    """Get specific webhook by ID with proper cleanup"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, method, headers, body, ip_address, user_agent
            FROM webhooks
            WHERE id = ?
        """, (webhook_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
