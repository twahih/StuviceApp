# Stuvice
## Author: Herve Twahirwa
## Contact: hervetwajean@gmail.com

## Introduction

Stuvice is a web-based platform that provides a social network and gig service for students. The platform aims to create a community among students, allowing them to connect with each other and offer/receive various services. Stuvice offers a seamless and secure way for students to access the services they need while fostering collaboration and camaraderie among students.

## Features and Functionalities

- **User Account Management**: Students can create an account on Stuvice using their email address and password. Once registered, they can log in to the platform to access the services.

- **Social Networking**: Students can connect with other students on the platform by sending and accepting friend requests. They can send messages to their friends and post updates on their profile.

- **Service Listing**: Students can list the services they offer on the platform, such as tutoring, web design, or event planning. They can set the price for their services and provide a description of what they offer.

- **Service Request**: Students can request services from other students by searching for the desired service and selecting a provider from the list of available providers. They can then send a request to the provider and negotiate the terms of the service.

- **Reviews and Ratings**: After a service is completed, students can rate and review the service provider. This feedback helps other students make informed decisions when choosing a service provider.

- **Payment Gateway**: Stuvice incorporates a secure payment gateway, allowing students to make secure payments for the services they receive from other students.

## Technology Stack

Stuvice is developed using the following technologies:

- **Front-end Development**: HTML, CSS, JavaScript
- **Back-end Development**: Python (Flask/Django)
- **Database**: MySQL
- **Machine Learning Capabilities**: Recurrent Neural Network (RNN): TensorFlow, PyTorch, or other deep learning libraries
- **Payment Gateway**: Stripe API,
- **Email Notification**: PostMark API
- **Phone Number Usage**: Twilio API
- **Hosting**: Locally, AWS, Azure, GCP, Heroku

By incorporating machine learning capabilities, specifically the use of RNN, Stuvice can leverage deep learning techniques to enhance its services, provide more accurate predictions, and deliver personalized experiences to its users. RNN can enable Stuvice to analyze sequential data, make predictions based on historical patterns, and improve the overall learning service behavior.

## Step-by-Step User Profile

To use Stuvice, follow these steps:

1. Create a user profile by signing up for an account.
2. Upload a profile picture to personalize your profile.
3. Search for services offered by other students.
4. Contact a student to request a service.
5. Negotiate the details and price of the service with the student.
6. Make a secure payment using the integrated payment system.
7. Receive the requested service from the student.
8. Provide a rating and review for the student who provided the service.

## Getting Started

To run Stuvice locally, ensure that you have Python version 3.10 or higher installed on your system. Follow these steps:

1. Create a virtual environment using the command: `python -m venv myenv`
   - On Windows, activate the virtual environment using the command: `myenv\Scripts\activate`
   - On macOS/Linux, activate the virtual environment using the command: `source myenv/bin/activate`

2. Run `pip install -r requirements.txt` to download all the necessary packages.

3. Finally, if necessary, deactivate the virtual environment:
   - On Windows, run: `myenv\Scripts\deactivate`
   - On macOS/Linux, run: `deactivate`

Alternatively, you can activate the virtual environment without running any scripts:
- On Windows, run: `myenv\Scripts\activate`
- On macOS/Linux, run: `source myenv/bin/activate`
4. Create a MySQL database by running the `Create_3nf_stuvicedb.sql` file provided in the repository.
5. Set up the connection variables in the `config.env` file. Open the file and update the following [Username] and [Passoword] with your MySQL database credentials:

Please ensure that you have the required dependencies installed and the virtual environment activated to run Stuvice successfully.

## Contributing

Contributions to Stuvice are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request. We appreciate contributions from the community to help improve Stuvice and make it even better.

When contributing, please keep the following guidelines in mind:

- Follow the project's coding style and guidelines to ensure consistency.
- If you encounter any issues or have suggestions, please open an issue on the repository. Provide as much detail as possible to help us understand and address the problem.
- If you'd like to contribute code, submit a pull request with your changes. Make sure to include a clear description of the changes and the problem they solve.

**Frontend Contributions:** We highly welcome contributions related to the frontend development of Stuvice. If you have expertise in HTML, CSS, or JavaScript, your contributions can greatly enhance the user experience and visual aesthetics of the platform. Feel free to contribute new features, improve existing components, or suggest UI/UX enhancements.

Thank you for your interest in contributing to Stuvice! Together, we can build a better platform for students.

