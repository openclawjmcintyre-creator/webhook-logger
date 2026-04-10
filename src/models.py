"""SQLite models for Webhook Logger"""
import sqlite3
import os
from datetime import datetime
from typing import Optional


DB_PATH = os.path.expanduser("~/.webhook_logger/webhooks.db")


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database and create tables"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
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
    conn.close()


def insert_webhook(method: str, headers: str, body: str,
                   ip_address: str = None, user_agent: str = None) -> int:
    """Insert a webhook and return its ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO webhooks (timestamp, method, headers, body, ip_address, user_agent)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.utcnow().isoformat(), method, headers, body, ip_address, user_agent))
    
    conn.commit()
    webhook_id = cursor.lastrowid
    conn.close()
    
    return webhook_id


def get_recent_webhooks(limit: int = 50) -> list:
    """Get recent webhooks"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, timestamp, method, headers, body, ip_address, user_agent
        FROM webhooks
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    webhooks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return webhooks


def get_webhook_by_id(webhook_id: int) -> Optional[dict]:
    """Get specific webhook by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, timestamp, method, headers, body, ip_address, user_agent
        FROM webhooks
        WHERE id = ?
    """, (webhook_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None
