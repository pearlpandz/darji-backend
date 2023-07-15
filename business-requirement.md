**Authentication Flow**

1. Register
    - [ ] Oauth
    - [ ] Google
    - [ ] Facebook
2. Get Otp, if Register by social accounts
    - [ ] Get Otp by mobil number
3. Verify Mobile Number
    - [ ] Send otp to mobile
    - [ ] Verify otp with db otp, if match update as verified
4. Login
    - [ ] Oauth
    - [ ] Google
    - [ ] Facebook
5. Forget Password
    - [ ] Get Otp by mobil number
    - [ ] Verify Mobile Number with OTP
    - [ ] Set Password (UI should send only one password; other validation UI needs to handle), Then redirect to Login page


