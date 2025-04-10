# Toyoflex - Paperless Machine Engineering Request Form

## Project Goals
This project aims to digitize and streamline the process of submitting and managing machine engineering requests.

## User Roles and Permissions
- **Manager**: Can approve or reject requests.
- **Supervisor**: Can review and approve requests after manager approval.
- **Engineer**: Can view and work on assigned requests.
- **Staff**: Can submit and track their own requests.

## Features
- User authentication and profile management.
- Submission of machine engineering requests with file uploads.
- Dashboard for tracking request statuses.
- Role-based access control for request management.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd toyoflexPMDwebsite
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
6. Access the application at `http://127.0.0.1:8000`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for discussion.
