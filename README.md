# Little Lemon Restaurant API

This repository contains the **Little Lemon Restaurant API**, developed using **Django** and **Django REST Framework (DRF)**. The API provides user management, menu item management, cart functionality, and order processing features.

---

## Features and Endpoints

### User Authentication and Token Management
| Endpoint                 | Role      | Method | Purpose                                                     |
|--------------------------|-----------|--------|-------------------------------------------------------------|
| `/api/auth/users/`       | All Users | POST   | Registers a new user.                                       |
| `/api/auth/token/login/` | All Users | POST   | Logs in the user and generates an authentication token.     |
| `/api/auth/token/logout/`| All Users | POST   | Logs out the user and invalidates the authentication token. |

---

### User Group Management
| Endpoint                          | Role      | Method | Purpose                                                                 |
|-----------------------------------|-----------|--------|-------------------------------------------------------------------------|
| `/api/groups/manager/users/`      | Manager   | GET    | Returns all users in the manager group.                                |
| `/api/groups/manager/users/`      | Manager   | POST   | Assigns a user to the manager group.                                   |
| `/api/groups/manager/users/{id}/` | Manager   | DELETE | Removes a user from the manager group.                                 |
| `/api/groups/delivery-crew/users/`| Manager   | GET    | Returns all users in the delivery crew group.                          |
| `/api/groups/delivery-crew/users/`| Manager   | POST   | Assigns a user to the delivery crew group.                             |
| `/api/groups/delivery-crew/users/{id}/` | Manager | DELETE | Removes a user from the delivery crew group.                          |

---

### Menu Item Management
| Endpoint                    | Role          | Method       | Purpose                                                               |
|-----------------------------|---------------|--------------|-----------------------------------------------------------------------|
| `/api/menu-items/`          | Customer/Manager | GET        | Lists all menu items.                                                |
| `/api/menu-items/`          | Manager       | POST         | Creates a new menu item.                                              |
| `/api/menu-items/{id}/`     | Customer/Manager | GET        | Retrieves a specific menu item.                                       |
| `/api/menu-items/{id}/`     | Manager       | PUT/PATCH   | Updates the menu item.                                                |
| `/api/menu-items/{id}/`     | Manager       | DELETE      | Deletes the menu item.                                                |

---

### Cart Management
| Endpoint               | Role      | Method | Purpose                                                   |
|------------------------|-----------|--------|-----------------------------------------------------------|
| `/api/cart/menu-items/`| Customer  | GET    | Retrieves the current cart items for the authenticated user. |
| `/api/cart/menu-items/`| Customer  | POST   | Adds a menu item to the cart. Calculates total and unit price automatically. |
| `/api/cart/menu-items/`| Customer  | DELETE | Clears all cart items for the authenticated user.         |

---

### Order Management
| Endpoint              | Role          | Method      | Purpose                                                                                        |
|-----------------------|---------------|-------------|------------------------------------------------------------------------------------------------|
| `/api/orders/`        | Customer      | GET         | Returns all orders created by the authenticated user.                                          |
| `/api/orders/`        | Customer      | POST        | Creates a new order using the current cart items and clears the cart.                         |
| `/api/orders/`        | Manager       | GET         | Returns all orders with order details for all users.                                          |
| `/api/orders/`        | Delivery Crew | GET         | Returns all orders assigned to the delivery crew.                                             |
| `/api/orders/{id}/`   | Customer      | GET         | Returns all items for the specified order if it belongs to the authenticated user.            |
| `/api/orders/{id}/`   | Manager       | PUT/PATCH   | Updates the order, assigns a delivery crew, or updates the order status.                     |
| `/api/orders/{id}/`   | Manager       | DELETE      | Deletes the specified order.                                                                  |
| `/api/orders/{id}/`   | Delivery Crew | PATCH       | Updates the status of the assigned order (out for delivery or delivered).                    |

---

## Project Setup Instructions

### Prerequisites
- Python 
- Django 
- Django REST Framework
- Pipenv for virtual environment management


