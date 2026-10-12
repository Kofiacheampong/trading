"""
Deployment Configuration for Scalable Investment Analysis System
Configuration for running the system at scale with distributed processing
"""

import os
from dataclasses import dataclass
from typing import List, Dict, Optional
import json


@dataclass
class DatabaseConfig:
    """Database configuration for the analysis system"""
    host: str = "localhost"
    port: int = 5432
    username: str = "analysis_user"
    password: str = ""
    database: str = "investment_analysis"
    pool_size: int = 20
    max_overflow: int = 30
    connection_timeout: int = 30


@dataclass
class CacheConfig:
    """Cache configuration for performance"""
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    cache_ttl_seconds: int = 3600  # 1 hour
    enable_local_cache: bool = True
    local_cache_size: int = 10000


@dataclass
class ProcessingConfig:
    """Processing configuration for scalability"""
    max_workers: int = 50
    worker_queue_size: int = 1000
    batch_size: int = 100
    timeout_seconds: int = 300  # 5 minutes
    retry_attempts: int = 3
    enable_async_processing: bool = True
    memory_limit_gb: int = 8


@dataclass
class DataProviderConfig:
    """Configuration for data providers"""
    primary_source: str = "yfinance"  # Options: yfinance, alpha_vantage, iex_cloud
    secondary_source: str = "alpha_vantage"
    api_keys: Dict[str, str] = None
    rate_limits: Dict[str, int] = None  # requests per minute
    fallback_enabled: bool = True
    data_refresh_interval_minutes: int = 60
    enable_caching: bool = True


@dataclass
class NotificationConfig:
    """Notification configuration"""
    email_enabled: bool = True
    webhook_url: str = ""
    slack_webhook_url: str = ""
    sms_enabled: bool = False
    notification_frequency_minutes: int = 15


@dataclass
class SecurityConfig:
    """Security configuration"""
    enable_authentication: bool = True
    jwt_secret: str = ""
    encryption_key: str = ""
    api_rate_limit: int = 100  # requests per minute per IP
    enable_ssl: bool = True
    audit_logging: bool = True


class ScaleDeploymentConfig:
    """Complete deployment configuration for scalable investment analysis"""
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.cache = CacheConfig()
        self.processing = ProcessingConfig()
        self.data_provider = DataProviderConfig()
        self.notifications = NotificationConfig()
        self.security = SecurityConfig()
        
        # Initialize with environment variables if available
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Database config
        if os.getenv('DB_HOST'):
            self.database.host = os.getenv('DB_HOST')
        if os.getenv('DB_PORT'):
            self.database.port = int(os.getenv('DB_PORT'))
        if os.getenv('DB_USER'):
            self.database.username = os.getenv('DB_USER')
        if os.getenv('DB_PASSWORD'):
            self.database.password = os.getenv('DB_PASSWORD')
        if os.getenv('DB_NAME'):
            self.database.database = os.getenv('DB_NAME')
        
        # Cache config
        if os.getenv('REDIS_HOST'):
            self.cache.redis_host = os.getenv('REDIS_HOST')
        if os.getenv('REDIS_PORT'):
            self.cache.redis_port = int(os.getenv('REDIS_PORT'))
        
        # Processing config
        if os.getenv('MAX_WORKERS'):
            self.processing.max_workers = int(os.getenv('MAX_WORKERS'))
        if os.getenv('WORKER_QUEUE_SIZE'):
            self.processing.worker_queue_size = int(os.getenv('WORKER_QUEUE_SIZE'))
        
        # Security
        if os.getenv('JWT_SECRET'):
            self.security.jwt_secret = os.getenv('JWT_SECRET')
        if os.getenv('ENCRYPTION_KEY'):
            self.security.encryption_key = os.getenv('ENCRYPTION_KEY')
    
    def to_dict(self) -> Dict:
        """Convert configuration to dictionary"""
        return {
            'database': {
                'host': self.database.host,
                'port': self.database.port,
                'username': self.database.username,
                'database': self.database.database,
                'pool_size': self.database.pool_size,
                'max_overflow': self.database.max_overflow,
                'connection_timeout': self.database.connection_timeout
            },
            'cache': {
                'redis_host': self.cache.redis_host,
                'redis_port': self.cache.redis_port,
                'redis_db': self.cache.redis_db,
                'cache_ttl_seconds': self.cache.cache_ttl_seconds,
                'enable_local_cache': self.cache.enable_local_cache,
                'local_cache_size': self.cache.local_cache_size
            },
            'processing': {
                'max_workers': self.processing.max_workers,
                'worker_queue_size': self.processing.worker_queue_size,
                'batch_size': self.processing.batch_size,
                'timeout_seconds': self.processing.timeout_seconds,
                'retry_attempts': self.processing.retry_attempts,
                'enable_async_processing': self.processing.enable_async_processing,
                'memory_limit_gb': self.processing.memory_limit_gb
            },
            'data_provider': {
                'primary_source': self.data_provider.primary_source,
                'secondary_source': self.data_provider.secondary_source,
                'api_keys': self.data_provider.api_keys or {},
                'rate_limits': self.data_provider.rate_limits or {},
                'fallback_enabled': self.data_provider.fallback_enabled,
                'data_refresh_interval_minutes': self.data_provider.data_refresh_interval_minutes,
                'enable_caching': self.data_provider.enable_caching
            },
            'notifications': {
                'email_enabled': self.notifications.email_enabled,
                'webhook_url': self.notifications.webhook_url,
                'slack_webhook_url': self.notifications.slack_webhook_url,
                'sms_enabled': self.notifications.sms_enabled,
                'notification_frequency_minutes': self.notifications.notification_frequency_minutes
            },
            'security': {
                'enable_authentication': self.security.enable_authentication,
                'jwt_secret': self.security.jwt_secret,
                'encryption_key': self.security.encryption_key,
                'api_rate_limit': self.security.api_rate_limit,
                'enable_ssl': self.security.enable_ssl,
                'audit_logging': self.security.audit_logging
            }
        }
    
    def save_to_file(self, filepath: str):
        """Save configuration to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'ScaleDeploymentConfig':
        """Load configuration from JSON file"""
        config = cls()
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Load database config
        db_data = data.get('database', {})
        config.database.host = db_data.get('host', config.database.host)
        config.database.port = db_data.get('port', config.database.port)
        config.database.username = db_data.get('username', config.database.username)
        config.database.password = db_data.get('password', config.database.password)
        config.database.database = db_data.get('database', config.database.database)
        config.database.pool_size = db_data.get('pool_size', config.database.pool_size)
        config.database.max_overflow = db_data.get('max_overflow', config.database.max_overflow)
        config.database.connection_timeout = db_data.get('connection_timeout', config.database.connection_timeout)
        
        # Load cache config
        cache_data = data.get('cache', {})
        config.cache.redis_host = cache_data.get('redis_host', config.cache.redis_host)
        config.cache.redis_port = cache_data.get('redis_port', config.cache.redis_port)
        config.cache.redis_db = cache_data.get('redis_db', config.cache.redis_db)
        config.cache.cache_ttl_seconds = cache_data.get('cache_ttl_seconds', config.cache.cache_ttl_seconds)
        config.cache.enable_local_cache = cache_data.get('enable_local_cache', config.cache.enable_local_cache)
        config.cache.local_cache_size = cache_data.get('local_cache_size', config.cache.local_cache_size)
        
        # Continue loading other configs similarly...
        
        return config


# Kubernetes Deployment Configuration
KUBERNETES_DEPLOYMENT = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: investment-analysis-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: investment-analysis-api
  template:
    metadata:
      labels:
        app: investment-analysis-api
    spec:
      containers:
      - name: analysis-api
        image: investment-analysis:latest
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: host
        - name: REDIS_HOST
          valueFrom:
            secretKeyRef:
              name: redis-secret
              key: host
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: investment-analysis-service
spec:
  selector:
    app: investment-analysis-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
"""

# Dockerfile configuration
DOCKERFILE_CONTENT = '''
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "scalable_investment_analysis.py"]
'''

# Requirements file for dependencies
REQUIREMENTS_CONTENT = '''pandas>=1.5.0
numpy>=1.21.0
yfinance>=0.2.18
asyncio
requests>=2.28.0
sqlalchemy>=2.0.0
redis>=4.5.0
pydantic>=2.0.0
fastapi>=0.100.0
uvicorn>=0.22.0
concurrent-log-handler>=0.9.20
psycopg2-binary>=2.9.5
cryptography>=41.0.0
'''

def generate_deployment_files():
    """Generate deployment configuration files"""
    
    # Create config object and save
    config = ScaleDeploymentConfig()
    config.save_to_file('deployment_config.json')
    
    # Create kubernetes deployment file
    with open('k8s-deployment.yaml', 'w') as f:
        f.write(KUBERNETES_DEPLOYMENT)
    
    # Create Dockerfile
    with open('Dockerfile', 'w') as f:
        f.write(DOCKERFILE_CONTENT)
    
    # Create requirements file
    with open('requirements.txt', 'w') as f:
        f.write(REQUIREMENTS_CONTENT)
    
    print("Deployment configuration files generated:")
    print("- deployment_config.json")
    print("- k8s-deployment.yaml")
    print("- Dockerfile")
    print("- requirements.txt")


def main():
    """Generate deployment configuration files"""
    print("Generating deployment configuration for scalable investment analysis system...")
    
    generate_deployment_files()
    
    print("\nDeployment configuration generated successfully!")
    print("\nTo deploy at scale:")
    print("1. Configure your infrastructure (database, Redis, etc.)")
    print("2. Update deployment_config.json with your specific settings")
    print("3. Build and push Docker image")
    print("4. Deploy to Kubernetes cluster using k8s-deployment.yaml")
    print("5. Monitor performance and scale as needed")
    
    print("\nKey scalability features:")
    print("- Parallel processing with configurable worker pools")
    print("- Distributed caching with Redis")
    print("- Database connection pooling")
    print("- Asynchronous processing capabilities")
    print("- Configurable batch sizes for efficient processing")
    print("- Rate limiting and fallback mechanisms")


if __name__ == "__main__":
    main()