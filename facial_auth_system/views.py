from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods


def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Security Pass Management System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                text-align: center;
            }
            .links {
                display: flex;
                flex-direction: column;
                gap: 15px;
                margin-top: 30px;
            }
            .link-card {
                background: #3498db;
                color: white;
                padding: 20px;
                border-radius: 5px;
                text-decoration: none;
                text-align: center;
                transition: background 0.3s;
            }
            .link-card:hover {
                background: #2980b9;
            }
            .api-info {
                background: #ecf0f1;
                padding: 20px;
                border-radius: 5px;
                margin-top: 20px;
            }
            .system-info {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
                border-left: 4px solid #3498db;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔒 Security Pass Management System</h1>
            <p>Welcome to the High Security Area Access Control System. This system provides secure access management using facial recognition and multi-level security clearance.</p>
            
            <div class="system-info">
                <h3>🏢 System Features:</h3>
                <ul>
                    <li>Facial Recognition Authentication</li>
                    <li>Multi-level Security Areas (Level 1-5)</li>
                    <li>User Type Management (Admin, Security, Staff, Visitors)</li>
                    <li>Real-time Access Logging</li>
                    <li>Visitor Management System</li>
                    <li>Pass Expiry Tracking</li>
                </ul>
            </div>
            
            <div class="links">
                <a href="/admin/" class="link-card">
                    <h3>🔧 Administration Panel</h3>
                    <p>Manage users, security areas, access logs, and system configuration</p>
                </a>
                
                <a href="/api/" class="link-card" style="background: #27ae60;">
                    <h3>🔗 API Endpoints</h3>
                    <p>Access the REST API for facial authentication and system integration</p>
                </a>
            </div>

            <div class="api-info">
                <h3>📡 Available API Endpoints:</h3>
                <ul>
                    <li><strong>POST /api/register/</strong> - Register new user with facial data</li>
                    <li><strong>POST /api/authenticate/</strong> - Authenticate user with face and security number</li>
                    <li><strong>POST /api/capture-face/</strong> - Capture face encoding from webcam</li>
                    <li><strong>GET /api/profile/</strong> - Get user profile (authenticated)</li>
                    <li><strong>GET /api/access-logs/</strong> - Get access logs (authenticated)</li>
                    <li><strong>GET /api/visitor-logs/</strong> - Get visitor logs (authenticated)</li>
                    <li><strong>GET /api/security-areas/</strong> - Get list of security areas</li>
                    <li><strong>POST /api/create-admin/</strong> - Create new admin users (admin only)</li>
                </ul>
            </div>

            <div style="margin-top: 30px; text-align: center; color: #7f8c8d;">
                <p>Security Pass Management System v2.0 | High Security Access Control</p>
            </div>
        </div>
    </body>
    </html>
    """)


@require_http_methods(["GET", "POST"])
def custom_logout(request):
    """
    Custom logout view that handles both GET and POST requests
    and ensures proper session clearing
    """
    logout(request)
    # Clear session data completely
    request.session.flush()
    # Redirect to admin login page
    return redirect('/admin/login/')


def handler404(request, exception):
    """
    Custom 404 error handler
    """
    return HttpResponseNotFound("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Page Not Found - Security System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 100px auto;
                padding: 20px;
                text-align: center;
                background-color: #f5f5f5;
            }
            .error-container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #e74c3c;
                margin-bottom: 20px;
            }
            .home-link {
                display: inline-block;
                background: #3498db;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1>🔍 404 - Page Not Found</h1>
            <p>The page you're looking for doesn't exist or has been moved.</p>
            <p>This could be due to an outdated link or a typo in the URL.</p>
            <a href="/" class="home-link">Return to Homepage</a>
        </div>
    </body>
    </html>
    """)


def handler500(request):
    """
    Custom 500 error handler
    """
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Server Error - Security System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 100px auto;
                padding: 20px;
                text-align: center;
                background-color: #f5f5f5;
            }
            .error-container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #e74c3c;
                margin-bottom: 20px;
            }
            .home-link {
                display: inline-block;
                background: #3498db;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1>⚙️ 500 - Server Error</h1>
            <p>Something went wrong on our end. Our technical team has been notified.</p>
            <p>Please try again later or contact system administration if the problem persists.</p>
            <a href="/" class="home-link">Return to Homepage</a>
            <br>
            <a href="/admin/login/" class="home-link" style="background: #27ae60; margin-top: 10px;">Go to Admin Login</a>
        </div>
    </body>
    </html>
    """, status=500)
