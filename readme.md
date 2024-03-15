# Django Cryptocurrency Exchange API

This Django-based project simulates a cryptocurrency purchase api for managing purchase
orders, and account balances. Built with Django Rest Framework, it
leverages PostgreSQL for data persistence and Redis for caching, showcasing a Dockerized development environment for
ease of setup and scalability.

## Features

- **Purchase Order Registration**: Users can register orders to buy cryptocurrencies, with real-time account balance
  updates.
- **External Exchange Integration**: Simulates clearing purchase amounts with international cryptocurrency exchanges.
- **API Documentation**: Utilizes Swagger (OpenAPI) for comprehensive API documentation and interactive testing.
- **registration/authentication**: Utilizes JWT to authenticate users

## Getting Started

### Setup

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/shahamatnia/Aban.git
cd django-crypto-exchange
docker-compose up --build
```

The application, along with PostgreSQL and Redis services, will start. Access the API Documentation
at http://localhost:8000/swagger.
also check http://localhost:8000/redoc.

## Functionalities and Approaches

### Purchase Order API

The core functionality, allowing users to place orders for cryptocurrencies. This involves:

Deducting the appropriate amount from the user's account balance.
buying currency for orders meeting a threshold and storing others to be added up to the threshold

in this functionality atomicity and consistency in some flows are the most crucial issues.
we leveraged transactions and redis lua scripting due to its single pipeline nature to avoid inconsistency or any
problem that could happen by race condition

#### Registration and Authentication

along the core functionality it was crucial to haev a user registration/authentication procedure
we leveraged JWT to achieve this functionality

## Considerations

#### to maintain simplicity and avoiding over engineering for an interview task, we ignored importance of setting and getting credentials and sensitive datas from encironment variables and they are hardcoded!
#### also we implemented all procedures synchronous.
#### some assumptions has been made due to few vague aspects of the task.

# How to check functionalities?

### first Note that you could run test by running following command:

```bash
sudo docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

## if you are looking for testing further!

### note that by default project would run with local environment that causes a custom command to run and insert some prepared data into database!!

### so you will have 2 currencies: (btc: 67.00) and (aban: 4.00)

### also there is a superadmin staff user present with username: testuser and password: password123

### you could log in with these credentials and obtain (access,refresh) tokens and by using access token in your request headers browse our APIs

#

#### thank you for your time and consideration, wish you all the best. 