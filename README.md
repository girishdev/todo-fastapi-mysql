## Project Versions

### V1.0.0 - Basic CRUD

- FastAPI setup
- MySQL integration
- SQLAlchemy ORM
- Pydantic validation
- Create Task
- Read Tasks
- Update Task
- Delete Task


### V2.0.0 - Clean Architecture

- Router / Service / Repository architecture
- PATCH support
- Pagination
- Task filtering
- Task search
- Improved validation


### V3.0.0 - Authentication

- User registration
- Password hashing with Argon2
- Login
- JWT authentication
- Current user endpoint
- Protected Task APIs
- User-specific tasks


### V4.0.0 - Database Migrations & Automated Testing

- Alembic integration
- Database schema migrations
- Migration upgrade / downgrade support
- Separate MySQL test database
- Pytest integration
- FastAPI TestClient
- Dependency override for test database
- Authentication API tests
- User API tests
- Task CRUD API tests
- Pagination, filtering and search tests
- Cross-user authorization tests
- 20 automated tests passing


### V5.0.0 - Dockerize Locally

- Dockerfile for FastAPI application
- Docker Compose setup
- FastAPI container
- MySQL container
- Docker networking
- Service-name based database connection
- Persistent MySQL volume
- Environment configuration with `.env.docker`
- MySQL health check
- Container dependency handling
- Alembic migrations during container startup
- Docker logs and debugging
- Port mapping
- Local Dockerized API testing
- All APIs working successfully inside Docker


### V6.0.0 - AWS Manual Deployment

Planned:

- AWS EC2 deployment
- Amazon RDS MySQL
- Docker deployment on EC2
- Production environment variables
- Security Groups
- Alembic migrations on AWS
- Public API testing