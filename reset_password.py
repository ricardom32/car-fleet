def email_reset_password_otp(otp):
 text = (
    Subject: Password Reset Request
    
    Dear [Your Name],
    
    We have received a request to reset your password for your account with [Service Name]. Please use the following One-Time Password (OTP) code to reset your password:
    
    [OTP Code]
    
    Please note that this code is valid for only 10 minutes. If you do not reset your password within this time frame, you will need to request a new OTP code.
    
    If you did not request this password reset, please contact our support team immediately.
    
    Thank you,
    [Service Name] Team) 
 return text
