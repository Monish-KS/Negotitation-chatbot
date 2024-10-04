# Negotiation Chatbot

A FastAPI-based negotiation chatbot designed to facilitate price negotiations for products through user interaction. The bot uses generative AI to respond to user offers and provide counteroffers in a friendly, professional manner.

## Table of Contents

- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Setting Up the App](#setting-up-the-app)
- [Running the App](#running-the-app)
- [API Endpoints](#api-endpoints)
  - [Initiate Negotiation](#initiate-negotiation)
  - [Make an Offer](#make-an-offer)
- [Commands Used](#commands-used)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project is a negotiation chatbot built with FastAPI and Google’s generative AI API. It allows users to initiate negotiations for products, make offers, and receive AI-generated responses that facilitate the negotiation process.

## Requirements

To run this project, you need to have the following installed:

- Python 3.7 or higher
- FastAPI
- Uvicorn
- Pydantic
- google-generativeai
- python-dotenv

You can install the necessary Python packages using pip:

```powershell
pip install fastapi uvicorn pydantic google-generativeai python-dotenv
```
Setting Up the App
Clone the Repository

Clone the repository to your local machine:
```powershell
git clone https://github.com/yourusername/negotiation-chatbot.git
cd negotiation-chatbot
```

Create a Virtual Environment (Optional)
It is recommended to create a virtual environment to manage dependencies:
```powershell
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
Install Requirements

Install the required packages:
```powershell
pip install -r requirements.txt
```
Set Up Environment Variables

Create a .env file in the root of your project directory and add your Google API key:

```
GOOGLE_API_KEY=your_google_api_key_here
```
Running the App
To run the FastAPI application, use Uvicorn:
```
cd app
python -m uvicorn main:app --reload
```
Visit http://127.0.0.1:8000/docs in your web browser to access the API documentation and try out the endpoints interactively.

API Endpoints

Initiate Negotiation
Endpoint: POST /initiate

Request Body:

```json
{
  "negotiation_id": "negotiation123",
  "product_name": "headphone",
  "base_price": 100.0
}
```
Response:
```json
{
  "message": "Hi there! I'm a negotiation bot, and I'm here to help you find the best possible deal..."
}
```

Make an Offer
Endpoint: POST /offer
Request Body:
```json
{
  "negotiation_id": "negotiation123",
  "user_offer": 80.0,
  "user_message": "I think this is a fair price!"
}
```
Response:
```json
{
  "message": "Hi there! Thanks for your offer. I understand that you're interested in our headphones..."
}
```
Commands Used
Here are some example commands for interacting with the API using PowerShell:

Initiate Negotiation
```powershell
$response = curl -Method POST "http://127.0.0.1:8000/initiate" `
    -Headers @{ "Content-Type" = "application/json" } `
    -Body '{"negotiation_id": "negotiation123", "product_name": "headphone", "base_price": 100.0}'
```
Make an Offer
```powershell
$response = curl -Method POST "http://127.0.0.1:8000/offer" `
    -Headers @{ "Content-Type" = "application/json" } `
    -Body '{"negotiation_id": "negotiation123", "user_offer": 80.0, "user_message": "I think this is a fair price!"}'
```
Contributing
Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.


### Explanation of the Sections

1. **Project Overview**: Provides a brief description of what the project is about.
2. **Requirements**: Lists the necessary dependencies and how to install them.
3. **Setting Up the App**: Step-by-step instructions for cloning the repository, setting up a virtual environment, and installing dependencies.
4. **Running the App**: Instructions on how to run the FastAPI application.
5. **API Endpoints**: Details about the available API endpoints, including request and response formats.
6. **Commands Used**: Example commands to interact with the API.
7. **Contributing**: Encourages collaboration and contributions from others.
8. **License**: Specifies the licensing for the project.
