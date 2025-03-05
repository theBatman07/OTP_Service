# OTP Service using FastAPI

## Description
This project implements an OTP-based login service using FastAPI. It provides endpoints to generate, resend, and verify one-time passwords (OTPs) with secure generation and proper handling of edge cases such as OTP expiration, rate limiting, and maximum verification attempts.

## Features
- **OTP Generation:** Securely generate a 4-digit OTP using Python's `secrets` module.
- **OTP Expiration:** OTPs are valid for a configurable time period (default is 5 minutes).
- **Resend OTP:** Allows OTP resending after a 60-second delay.
- **OTP Verification:** Verifies user input, tracks failed attempts, and invalidates the OTP after 3 unsuccessful tries.
- **Documentation:** Interactive API documentation is automatically generated via Swagger UI.

## Tech Stack
- **Programming Language:** Python
- **Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Security:** Python's `secrets` module for cryptographically secure OTP generation
- **Data Storage:** In-memory storage (for demo purposes (: )

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/otp-service.git
   cd otp-service
   ```

2. **Set Up a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   On Windows use: venv\Scripts\activate
   On Linux use: source venv/bin/activate  
   ```

3. **Install Dependencies:**
   Install all the required depencies by running the following command:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Service

Start the FastAPI service using Uvicorn by running the following command:
```bash
uvicorn main:app --reload
```
This command starts the server with live reload enabled, so any code changes will automatically restart the server.

## API Endpoints

### Generate OTP
- **URL:** `/otp/generate`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "phone_number": "+1234567890"
  }
  ```
- **Description:** Generates and (for demonstration purposes) returns a secure 4-digit OTP. (In production, the OTP should be sent via SMS or email.)

### Resend OTP
- **URL:** `/otp/resend`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "phone_number": "+1234567890"
  }
  ```
- **Description:** Resends the OTP if 60 seconds have passed since the last request.

### Verify OTP
- **URL:** `/otp/verify`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "phone_number": "+1234567890",
    "otp": "1234"
  }
  ```
- **Description:** Verifies the provided OTP. If the OTP is incorrect, it increments a failed attempt counter. The OTP expires after 5 minutes or after 3 failed attempts.

## Testing the API

You can test the endpoints using tools like **Postman** or **cURL**.
