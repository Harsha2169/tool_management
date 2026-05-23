# Tooling Master Records Management

## Overview
REST API application for managing industrial injection moulding tool master records. Built with Python, FastAPI, SQLAlchemy, and Alembic with PostgreSQL.

## Project Structure

```
tooling_management/
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
│       └── 001_create_tooling_tables.py
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   └── crud/
├── data_dictionary.csv
├── er_diagram.md
└── requirements.txt
```

## API Endpoints

### Tool Master (CRUD)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/tools | List tools (paginated, filterable) |
| GET | /api/v1/tools/{tool_id} | Get tool details |
| POST | /api/v1/tools | Create tool |
| PUT | /api/v1/tools/{tool_id} | Update tool |
| DELETE | /api/v1/tools/{tool_id} | Soft delete tool |

### Production (Sub-resource)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/tools/{tool_id}/productions | List production entries |
| POST | /api/v1/tools/{tool_id}/productions | Add production entry |
| PUT | /api/v1/tools/{tool_id}/productions/{id} | Update entry |
| DELETE | /api/v1/tools/{tool_id}/productions/{id} | Delete entry |

### Performance (Sub-resource)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/tools/{tool_id}/performances | List performance records |
| POST | /api/v1/tools/{tool_id}/performances | Add record |
| PUT | /api/v1/tools/{tool_id}/performances/{id} | Update record |
| DELETE | /api/v1/tools/{tool_id}/performances/{id} | Delete record |

### Params (Sub-resource)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/tools/{tool_id}/params | List parameters |
| POST | /api/v1/tools/{tool_id}/params | Add parameter |
| PUT | /api/v1/tools/{tool_id}/params/{id} | Update parameter |
| DELETE | /api/v1/tools/{tool_id}/params/{id} | Delete parameter |

### Maintenance (Sub-resource)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/tools/{tool_id}/maintenances | List records |
| POST | /api/v1/tools/{tool_id}/maintenances | Add record |
| PUT | /api/v1/tools/{tool_id}/maintenances/{id} | Update record |
| DELETE | /api/v1/tools/{tool_id}/maintenances/{id} | Delete record |

### Lookups
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/lookups/tool-types | Tool type options |
| GET | /api/v1/lookups/control-units | Control unit options |
| GET | /api/v1/lookups/asset-owners | Asset owner options |
| GET | /api/v1/lookups/life-statuses | Life status options |

## Tech Stack
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Database:** PostgreSQL
