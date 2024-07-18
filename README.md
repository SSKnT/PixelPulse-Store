# PixelPulse E-commerce Website

## Description
PixelPulse is an e-commerce platform developed using Django, specializing in the sale of graphic cards. The website features seamless Stripe integration for secure payment processing and includes a Stripe webhook for real-time updates on payment notifications.

## Features
- Browse and purchase graphic cards
- User registration and authentication
- Secure payment processing with Stripe integration
- Stripe webhook for real-time payment updates
- Responsive design for optimal viewing on all devices

## Technologies Used
- Django
- Python
- HTML/CSS
- Stripe API for payment processing

## Installation
1. Clone the repository:
2. Navigate into the project directory:
3. Install dependencies:
4. Set up environment variables for Django settings (e.g., `SECRET_KEY`, `DEBUG`, `DATABASE_URL`, `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`).
5. Run migrations:
6. Start the development server:
7. Access the website at `http://localhost:8000` in your browser.

## Usage
- Browse through available graphic cards and add them to your cart.
- Create an account or log in to complete purchases securely.
- Use the Stripe payment gateway to process payments.
- Monitor payment notifications via the Stripe webhook.

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests to contribute to this project.

## License
This project is licensed under the [MIT License](LICENSE).
