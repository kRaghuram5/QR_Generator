import pytest
import sys
import os
from io import BytesIO

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'QR Code Generator' in response.data

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'QR Code Generator'

def test_generate_qr_success(client):
    """Test successful QR code generation"""
    response = client.post('/generate',
                          json={'text': 'Hello World'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.mimetype == 'image/png'
    assert len(response.data) > 0  # Image data should not be empty

def test_generate_qr_with_url(client):
    """Test QR code generation with URL"""
    response = client.post('/generate',
                          json={'text': 'https://www.google.com'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.mimetype == 'image/png'
    assert len(response.data) > 0

def test_generate_qr_empty_text(client):
    """Test QR code generation with empty text"""
    response = client.post('/generate',
                          json={'text': ''},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'No text provided'

def test_generate_qr_no_text_field(client):
    """Test QR code generation without text field"""
    response = client.post('/generate',
                          json={},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_generate_qr_long_text(client):
    """Test QR code generation with long text"""
    long_text = 'A' * 500  # 500 character string
    response = client.post('/generate',
                          json={'text': long_text},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.mimetype == 'image/png'

def test_qrcode_library():
    """Test that qrcode library works correctly"""
    import qrcode
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data('test')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO to test image creation
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    assert len(img_io.getvalue()) > 0
    print("✓ QR code library test passed")

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
