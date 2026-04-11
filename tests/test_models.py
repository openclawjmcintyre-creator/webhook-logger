# Webhook Logger Tests

"""Tests for SQLite models"""
import os
import tempfile
import shutil
import pytest
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import (
    init_db, insert_webhook, get_recent_webhooks,
    get_webhook_by_id, get_db_path
)


@pytest.fixture(scope="module")
def temp_db():
    """Create temporary database for testing"""
    # Use a temporary directory for test database
    test_db_path = "/tmp/test_webhook_logger/webhooks.db"
    os.makedirs(os.path.dirname(test_db_path), exist_ok=True)
    
    # Override DB_PATH for tests
    os.environ['WEBHOOK_DB_PATH'] = test_db_path
    
    # Initialize test DB
    init_db()
    
    yield test_db_path
    
    # Cleanup after tests
    shutil.rmtree(os.path.dirname(test_db_path), ignore_errors=True)


def test_get_db_path_default():
    """Test get_db_path returns /data/webhooks.db when env not set"""
    # Remove env var if set
    if 'WEBHOOK_DB_PATH' in os.environ:
        del os.environ['WEBHOOK_DB_PATH']
    
    # Reset the cached path
    import src.models
    reload = __import__('importlib').reload(src.models)
    
    assert reload.get_db_path() == '/data/webhooks.db'


def test_insert_webhook(temp_db):
    """Test inserting a webhook"""
    webhook_id = insert_webhook(
        method="POST",
        headers='{"Content-Type": "application/json"}',
        body='{"test": "data"}',
        ip_address="127.0.0.1",
        user_agent="test-agent"
    )
    
    assert webhook_id is not None
    assert webhook_id > 0


def test_get_recent_webhooks(temp_db):
    """Test getting recent webhooks"""
    # Insert a few webhooks first
    insert_webhook("POST", '{"test": "1"}', '{"event": "test1"}')
    insert_webhook("POST", '{"test": "2"}', '{"event": "test2"}')
    
    webhooks = get_recent_webhooks(limit=50)
    
    assert isinstance(webhooks, list)
    assert len(webhooks) >= 2
    assert webhooks[0]['method'] == "POST"


def test_get_webhook_by_id_valid(temp_db):
    """Test getting webhook by valid ID"""
    # Insert a webhook first
    webhook_id = insert_webhook("POST", '{"test": "1"}', '{"event": "test1"}')
    
    webhook = get_webhook_by_id(webhook_id)
    
    assert webhook is not None
    assert webhook['id'] == webhook_id
    assert webhook['method'] == "POST"


def test_get_webhook_by_id_invalid(temp_db):
    """Test getting webhook by invalid ID returns None"""
    webhook = get_webhook_by_id(999999)
    
    assert webhook is None
