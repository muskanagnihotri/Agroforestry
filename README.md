 ## Agroforestry Program Management Application

 ## Overview

This Flask-based web application is designed to manage data for an Agroforestry Program. The application includes role-based access control for different team members, allowing Field Executives, Field Managers, and a Senior Manager to perform tasks relevant to their roles. The system enables data entry, updates, and visualization of farmer and implementation details.

## Features

## Role-Based Access Control:

Field Executives can add farmer and implementation details.

Field Managers can view data reported to them.

Senior Managers can view, update, and delete all data.

## CRUD Operations:

Add, view, update, and delete farmer and implementation data.

## Authentication:

Users must log in with valid credentials to access the system.

## Session Management:

Sessions are used to maintain user authentication and role-based access.

## Login Credentials:

Field Executive: exec_a / pass_a, exec_b / pass_b

Field Manager: mgr_c / pass_c, mgr_d / pass_d

Senior Manager: senior_mgr / pass_e

## Functionalities:

## Field Executives:

Navigate to the "Add Farmer Data" page after login to input farmer details.

## Field Managers:

View the data reported to them on the dashboard.

## Senior Managers:

Access the dashboard to view, update, or delete all data.

## Routes

/ - Redirects to the login page.

/login - User login.

/dashboard - Dashboard for Field Managers and Senior Managers.

/add_farm_data - Add farmer data (Field Executives only).

/update_farm_data/<int:id> - Update farmer data (Senior Manager only).

/delete_farm_data/<int:id> - Delete farmer data (Senior Manager only).

/logout - Log out of the application.

## Notes

Ensure the secret_key in the application is replaced with a secure value for production.

The application currently uses SQLite for simplicity. For scalability, consider migrating to a more robust database like PostgreSQL or MySQL.









 
