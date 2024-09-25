# Points Management API

This API allows you to manage points for different payers. You can add points, spend points, and check the balance of points for each payer. This API currently supports a singular user and ensures that points are spent based on the oldest available transactions first.

## Endpoints

This API runs on port 8000.

### 1. Add Points

- **URL:** `/add`
- **Method:** `POST`
- **Description:** Adds points for a specific payer. The transaction is inserted into the correct position in the deque based on the timestamp (oldest first). The total balance for the payer is updated accordingly.
- **Request Body:**
    ```json
    {
        "payer": "DANNON",
        "points": 300,
        "timestamp": "2022-10-31T10:00:00Z"
    }
    ```
    - **payer:** The name of the payer (e.g., "DANNON").
    - **points:** The number of points to add (can be positive or negative).
    - **timestamp:** The ISO 8601 timestamp representing when the transaction occurred.
- **Response:** Status code 200 if the transaction was successfully added.

### 2. Spend Points

- **URL:** `/spend`
- **Method:** `POST`
- **Description:** Spends points based on the oldest available points first (FIFO). It ensures no payer’s points go negative. Points are deducted from payers in the order of their transaction timestamps.
- **Request Body:**
    ```json
    {
        "points": 5000
    }
    ```
    - **points:** the total number of points to spend
- **Response Body:**
    ```json
    {
        "DANNON": -100,
        "UNILEVER": -200,
        "MILLER COORS": -4700
    }
    ```
    This is an example response showing the points deducted from each payer. Negative values indicate points were subtracted.
- **Error Handling:** If the total points available are less than the points requested, the API will return:
    - **Status Code:** 400
    - **Response:** "You do not have enough points"

### 3. Check Balance

- **URL:** `/balance`
- **Method:** `GET`
- **Description:** Fetches the current balance of points for each payer. The response shows the total points available for each payer after all transactions.

- **Request Body:**
    ```json
    {
        "DANNON": 1000,
        "UNILEVER": 0,
        "MILLER COORS": 5300
    }
    ```
    The response is a mapping of each payer to their remaining points.
- **Response:** Status code 200 if the transaction was successfully added.

### Assumptions
This API assumes that total transaction balances for each payer cannot become negative as it does not make sense that adding points can make a balance negative. Transactions are assumed to all be within the same time zone during conversion.
