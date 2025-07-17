# URL Shortener Service by Muhammad Yahya

This is a simple RESTful API to shorten long URLs, built with Python, Flask, and MySQL.

> **Note:** All application code lives on the `dev` branch. This `main` branch only contains this README.

## Getting Started

1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/yourname-innovaxel-lastname.git
   cd yourname-innovaxel-lastname

2. **Set up the branches**    
    
    * You should already be on main, containing only this file.
    * To work with the code, switch to the dev branch:

        ```bash
        git checkout dev

3. **Install dependencies**
    
    ```bash
    pip install -r requirements.txt

4. **Configure the Database**
    
    * Make sure MySQL is running
    * Create the database and table:
       
        ```sql
        CREATE DATABASE url_shortener;
        USE url_shortener;
        CREATE TABLE urls (
            id INT AUTO_INCREMENT PRIMARY KEY,
            original_url TEXT NOT NULL,
            short_code VARCHAR(10) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            access_count INT DEFAULT 0
        );
    
    * Update the MySQL credentials in `config.py`.

5. **Run the Flask app**

    ```bash
    python app.py

## API Endpoints

* POST /shorten
Create a new short URL
Body: { "url": "https://long.url/path" }

* GET /shorten/`shortCode`
Retrieve the original URL

* PUT /shorten/`shortCode`
Update the URL
Body: { "url": "https://new.url/path" }

* DELETE /shorten/`shortCode`
Delete the short URL

* GET /shorten/`shortCode`/stats
Get access statistics

* GET /`shortCode`
Redirect to the original URL

