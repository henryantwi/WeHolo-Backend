# Deployment Guide

This guide provides instructions for deploying the WeHolo platform to production environments.

## Deployment Options

WeHolo can be deployed in several ways:

1. **Docker Deployment**: Recommended for most production environments
2. **Manual Deployment**: For environments where Docker is not available
3. **Cloud Deployment**: For deploying to cloud platforms like AWS, Azure, or Google Cloud

## Docker Deployment

### Prerequisites

- Docker 20.10.x or later
- Docker Compose 2.x or later
- A domain name (for HTTPS)
- At least 2GB of RAM and 1 CPU core

### Deployment Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/henryantwi/weholo-project.git
   cd weholo-project
   ```

2. **Configure Environment Variables**

   Create `.env.web` for the web service:

   ```
   # API configuration
   API_V1_STR=/api
   SECRET_KEY=your-secure-secret-key
   ACCESS_TOKEN_EXPIRE_MINUTES=11520

   # Database
   DATABASE_URL=postgresql://weholo:strong-password@db:5432/weholo

   # CORS
   BACKEND_CORS_ORIGINS=["https://your-domain.com"]

   # API Keys
   AKOOL_API_KEY=your-akool-api-key
   SOUL_MACHINES_API_KEY=your-soul-machines-api-key

   # Debug mode
   DEBUG=False
   ENVIRONMENT=production
   ```

   Create `.env.db` for the database service:

   ```
   POSTGRES_USER=weholo
   POSTGRES_PASSWORD=strong-password
   POSTGRES_DB=weholo
   ```

   Replace the placeholder values with your actual configuration.

3. **Configure Docker Compose for Production**

   Create a `docker-compose.prod.yml` file:

   ```yaml
   version: '3.8'

   services:
     web:
       build: .
       restart: always
       ports:
         - "8000:8000"
       env_file:
         - .env.web
       depends_on:
         - db
       volumes:
         - ./app:/app/app
         - ./alembic:/app/alembic
       command: >
         bash -c "alembic upgrade head && 
                 uvicorn main:app --host 0.0.0.0 --port 8000"

     db:
       image: postgres:14
       restart: always
       volumes:
         - postgres_data:/var/lib/postgresql/data
       env_file:
         - .env.db
       ports:
         - "5432:5432"

   volumes:
     postgres_data:
   ```

4. **Build and Start the Containers**

   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

5. **Set Up HTTPS with Nginx**

   Install Nginx:

   ```bash
   sudo apt update
   sudo apt install nginx
   ```

   Create an Nginx configuration file:

   ```
   server {
       listen 80;
       server_name your-domain.com;
       return 301 https://$host$request_uri;
   }

   server {
       listen 443 ssl;
       server_name your-domain.com;

       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_prefer_server_ciphers on;
       ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   Set up SSL certificates with Let's Encrypt:

   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

6. **Verify the Deployment**

   Visit `https://your-domain.com/docs` to verify that the API is running correctly.

### Updating the Deployment

To update the deployment with new code:

1. Pull the latest changes:

   ```bash
   git pull origin main
   ```

2. Rebuild and restart the containers:

   ```bash
   docker-compose -f docker-compose.prod.yml down
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

## Manual Deployment

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Nginx or another web server
- A domain name (for HTTPS)

### Deployment Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/henryantwi/weholo-project.git
   cd weholo-project
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file:

   ```
   # API configuration
   API_V1_STR=/api
   SECRET_KEY=your-secure-secret-key
   ACCESS_TOKEN_EXPIRE_MINUTES=11520

   # Database
   DATABASE_URL=postgresql://username:password@localhost:5432/weholo

   # CORS
   BACKEND_CORS_ORIGINS=["https://your-domain.com"]

   # API Keys
   AKOOL_API_KEY=your-akool-api-key
   SOUL_MACHINES_API_KEY=your-soul-machines-api-key

   # Debug mode
   DEBUG=False
   ENVIRONMENT=production
   ```

5. **Set Up the Database**

   ```bash
   # Create the database
   sudo -u postgres psql -c "CREATE DATABASE weholo;"
   sudo -u postgres psql -c "CREATE USER username WITH PASSWORD 'password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE weholo TO username;"

   # Apply migrations
   alembic upgrade head
   ```

6. **Set Up a Systemd Service**

   Create a service file at `/etc/systemd/system/weholo.service`:

   ```
   [Unit]
   Description=WeHolo API
   After=network.target

   [Service]
   User=your-user
   Group=your-user
   WorkingDirectory=/path/to/weholo-project
   Environment="PATH=/path/to/weholo-project/.venv/bin"
   ExecStart=/path/to/weholo-project/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start the service:

   ```bash
   sudo systemctl enable weholo
   sudo systemctl start weholo
   ```

7. **Set Up Nginx and HTTPS**

   Follow the same Nginx and Let's Encrypt setup as in the Docker deployment.

## Cloud Deployment

### AWS Deployment

#### Using Elastic Beanstalk

1. **Install the EB CLI**

   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**

   ```bash
   eb init -p python-3.8 weholo
   ```

3. **Configure Environment Variables**

   Create a `.ebextensions/01_environment.config` file:

   ```yaml
   option_settings:
     aws:elasticbeanstalk:application:environment:
       API_V1_STR: /api
       SECRET_KEY: your-secure-secret-key
       ACCESS_TOKEN_EXPIRE_MINUTES: 11520
       DATABASE_URL: postgresql://username:password@your-rds-endpoint:5432/weholo
       BACKEND_CORS_ORIGINS: '["https://your-domain.com"]'
       DEBUG: False
       ENVIRONMENT: production
   ```

4. **Create an RDS Database**

   Create a PostgreSQL RDS instance through the AWS console or CLI.

5. **Deploy the Application**

   ```bash
   eb create weholo-production
   ```

6. **Set Up HTTPS**

   Configure HTTPS through the AWS Elastic Beanstalk console or by adding an HTTPS listener to your load balancer.

### Azure Deployment

#### Using Azure App Service

1. **Install the Azure CLI**

   ```bash
   # Follow instructions at https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
   ```

2. **Create a Resource Group**

   ```bash
   az group create --name weholo-group --location eastus
   ```

3. **Create an App Service Plan**

   ```bash
   az appservice plan create --name weholo-plan --resource-group weholo-group --sku B1 --is-linux
   ```

4. **Create a PostgreSQL Database**

   ```bash
   az postgres server create --resource-group weholo-group --name weholo-db --location eastus --admin-user username --admin-password password --sku-name GP_Gen5_2
   ```

5. **Create a Web App**

   ```bash
   az webapp create --resource-group weholo-group --plan weholo-plan --name weholo-app --runtime "PYTHON|3.8"
   ```

6. **Configure Environment Variables**

   ```bash
   az webapp config appsettings set --resource-group weholo-group --name weholo-app --settings API_V1_STR=/api SECRET_KEY=your-secure-secret-key ACCESS_TOKEN_EXPIRE_MINUTES=11520 DATABASE_URL=postgresql://username:password@weholo-db.postgres.database.azure.com:5432/weholo BACKEND_CORS_ORIGINS='["https://your-domain.com"]' DEBUG=False ENVIRONMENT=production
   ```

7. **Deploy the Application**

   ```bash
   az webapp deployment source config-local-git --resource-group weholo-group --name weholo-app
   git remote add azure <git-url-from-previous-command>
   git push azure main
   ```

## Monitoring and Maintenance

### Logging

Configure logging to a file or a service like Logstash, Fluentd, or CloudWatch:

```python
# In app/core/logging.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=10485760, backupCount=5
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(levelname)s: %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
```

### Backups

Set up regular database backups:

```bash
# Create a backup script
cat > backup.sh << 'EOF'
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/path/to/backups"
POSTGRES_CONTAINER="weholo-db"
POSTGRES_USER="weholo"
POSTGRES_DB="weholo"

mkdir -p $BACKUP_DIR

docker exec $POSTGRES_CONTAINER pg_dump -U $POSTGRES_USER $POSTGRES_DB | gzip > $BACKUP_DIR/weholo_$TIMESTAMP.sql.gz
EOF

chmod +x backup.sh

# Add to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * /path/to/backup.sh") | crontab -
```

### Health Checks

Set up health checks to monitor the application:

```bash
# Create a health check script
cat > health_check.sh << 'EOF'
#!/bin/bash
HEALTH_ENDPOINT="https://your-domain.com/api/health"
SLACK_WEBHOOK="https://hooks.slack.com/services/your-webhook-url"

response=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_ENDPOINT)

if [ $response -ne 200 ]; then
  curl -X POST -H 'Content-type: application/json' --data '{"text":"Health check failed! Status code: '$response'"}' $SLACK_WEBHOOK
fi
EOF

chmod +x health_check.sh

# Add to crontab
(crontab -l 2>/dev/null; echo "*/5 * * * * /path/to/health_check.sh") | crontab -
```

## Security Considerations

1. **Keep Software Updated**

   Regularly update dependencies to patch security vulnerabilities:

   ```bash
   pip install -U pip
   pip install -U -r requirements.txt
   ```

2. **Secure Environment Variables**

   Never commit sensitive environment variables to version control.

3. **Use HTTPS**

   Always use HTTPS in production.

4. **Set Up a Firewall**

   Restrict access to only necessary ports:

   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

5. **Regular Security Audits**

   Perform regular security audits of your deployment.

## Troubleshooting

### Common Issues

1. **Database Connection Issues**

   - Check that the database server is running
   - Verify that the DATABASE_URL is correct
   - Check network connectivity between the application and database

2. **Application Not Starting**

   - Check the application logs
   - Verify that all required environment variables are set
   - Check that the port is not already in use

3. **HTTPS Not Working**

   - Check that SSL certificates are correctly installed
   - Verify that Nginx is properly configured
   - Check that the certificates have not expired

### Getting Help

If you encounter issues that you cannot resolve, refer to:

- The project documentation
- The project issue tracker
- Community forums for the technologies used (FastAPI, PostgreSQL, etc.)