// OTP System for Login
(function() {
    'use strict';
    
    // Show OTP Modal
    window.showOTPModal = function(otpCode) {
        const modal = document.getElementById('otpModal');
        const otpCodeText = document.getElementById('otpCodeText');
        
        if (modal && otpCodeText) {
            otpCodeText.textContent = otpCode;
            modal.style.display = 'flex';
        }
    };
    
    // Close OTP Modal
    window.closeOTPModal = function() {
        const modal = document.getElementById('otpModal');
        if (modal) {
            modal.style.display = 'none';
        }
    };
    
    // Copy OTP from Modal
    window.copyOTPFromModal = function() {
        const otpCodeText = document.getElementById('otpCodeText');
        const otpInput = document.getElementById('otpCode');
        
        if (otpCodeText) {
            const otpCode = otpCodeText.textContent;
            
            // Copy to clipboard using modern API
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(otpCode).then(function() {
                    alert('✓ OTP copied to clipboard!\n\nCode: ' + otpCode);
                    
                    // Fill the input field
                    if (otpInput) {
                        otpInput.value = otpCode;
                        otpInput.dispatchEvent(new Event('input'));
                    }
                    
                    // Close modal
                    closeOTPModal();
                }).catch(function(err) {
                    console.error('Copy failed:', err);
                    fallbackCopy(otpCode);
                });
            } else {
                fallbackCopy(otpCode);
            }
        }
        
        function fallbackCopy(text) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-9999px';
            document.body.appendChild(textArea);
            textArea.select();
            
            try {
                document.execCommand('copy');
                alert('✓ OTP copied to clipboard!\n\nCode: ' + text);
                
                if (otpInput) {
                    otpInput.value = text;
                    otpInput.dispatchEvent(new Event('input'));
                }
                
                closeOTPModal();
            } catch (err) {
                alert('Please manually copy the code: ' + text);
            }
            
            document.body.removeChild(textArea);
        }
    };
    
    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        
        // Get all elements
        const emailInput = document.getElementById('emailInput');
        const roleInput = document.getElementById('role');
        const sendOtpBtn = document.getElementById('sendOtpBtn');
        const resendOtpBtn = document.getElementById('resendOtpBtn');
        const otpGroup = document.getElementById('otpGroup');
        const otpInput = document.getElementById('otpCode');
        const submitBtn = document.getElementById('submitBtn');
        
        // Check if we're on login page
        if (!emailInput || !sendOtpBtn) {
            return;
        }
        
        console.log('OTP System initialized');
        
        let otpVerified = false;
        
        // Send OTP function
        function sendOTP(isResend) {
            const email = emailInput.value.trim();
            const role = roleInput.value;
            
            console.log('Sending OTP to:', email, 'Role:', role);
            
            if (!email) {
                alert('Please enter your email address');
                return;
            }
            
            // Basic email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Please enter a valid email address');
                return;
            }
            
            // Get button to update
            const btn = isResend ? resendOtpBtn : sendOtpBtn;
            const originalHTML = btn.innerHTML;
            
            // Show loading
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            btn.disabled = true;
            
            // Get CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Send request
            fetch('/send-login-otp/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    email: email,
                    role: role
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('OTP Response:', data);
                
                if (data.success) {
                    // Show OTP field
                    otpGroup.style.display = 'block';
                    
                    // Update send button
                    sendOtpBtn.innerHTML = '<i class="fas fa-check"></i> Sent';
                    sendOtpBtn.classList.add('verified');
                    sendOtpBtn.disabled = true;
                    
                    // Show resend button
                    resendOtpBtn.style.display = 'block';
                    resendOtpBtn.disabled = false;
                    resendOtpBtn.innerHTML = '<i class="fas fa-redo"></i> Resend OTP';
                    
                    // Focus on OTP input
                    otpInput.focus();
                    
                    // Show OTP in custom modal
                    showOTPModal(data.otp);
                    
                } else {
                    alert('✗ ' + data.message);
                    btn.innerHTML = originalHTML;
                    btn.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error sending OTP. Please try again.');
                btn.innerHTML = originalHTML;
                btn.disabled = false;
            });
        }
        
        // Verify OTP function
        function verifyOTP() {
            const email = emailInput.value.trim();
            const code = otpInput.value.trim();
            
            console.log('Verifying OTP:', code);
            
            if (code.length !== 6) {
                return;
            }
            
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch('/verify-login-otp/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    email: email,
                    otp_code: code
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Verify Response:', data);
                
                if (data.success) {
                    // Mark as verified
                    otpVerified = true;
                    
                    // Visual feedback
                    otpInput.style.borderColor = '#10b981';
                    otpInput.style.background = '#d1fae5';
                    
                    // Enable submit button
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Sign In';
                    submitBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                    
                    alert('✓ Email verified successfully!');
                    
                } else {
                    // Show error
                    otpInput.style.borderColor = '#ef4444';
                    otpInput.style.background = '#fee2e2';
                    alert('✗ ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error verifying OTP. Please try again.');
            });
        }
        
        // Event listeners
        sendOtpBtn.addEventListener('click', function() {
            sendOTP(false);
        });
        
        resendOtpBtn.addEventListener('click', function() {
            // Clear OTP input
            otpInput.value = '';
            otpInput.style.borderColor = '';
            otpInput.style.background = '';
            otpVerified = false;
            
            // Disable submit
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-lock"></i> Verify Email First';
            submitBtn.style.background = '#9ca3af';
            
            // Send new OTP
            sendOTP(true);
        });
        
        // Auto-verify when 6 digits entered
        otpInput.addEventListener('input', function() {
            // Only allow numbers
            this.value = this.value.replace(/[^0-9]/g, '');
            
            // Auto-verify when 6 digits
            if (this.value.length === 6) {
                verifyOTP();
            }
        });
        
        // Prevent form submission if OTP not verified
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', function(e) {
                if (!otpVerified) {
                    e.preventDefault();
                    alert('Please verify your email with OTP first');
                    return false;
                }
            });
        }
        
        console.log('OTP System ready');
    });
    
})();
