# CKAN Data ETL Pipeline with Apache Airflow

โปรเจค ETL Pipeline สำหรับดึงข้อมูลจาก Thailand Open Data (CKAN API) โดยใช้ Apache Airflow บน Docker

## 🚀 Features

- ดึงข้อมูลจาก CKAN API (opend.data.go.th)
- แปลงข้อมูลด้วย Pandas
- โหลดข้อมูลเข้า PostgreSQL
- Schedule รันอัตโนมัติทุกวัน
- รองรับภาษาไทย (UTF-8)

## 📋 Prerequisites

- Docker Desktop
- Docker Compose
- RAM อย่างน้อย 4GB
- พื้นที่ disk อย่างน้อย 10GB

## 🔧 Installation

1. Clone repository:
```bash
git clone <your-repo-url>
cd Airflow-master
```

2. เริ่มต้น Airflow:
```bash
docker compose up -d
```

3. รอให้ services เริ่มต้นเสร็จ (ประมาณ 1-2 นาที)

## 🌐 การเข้าถึง

### Airflow Web UI
- URL: http://localhost:8080
- Username: `airflow`
- Password: `airflow`

### PostgreSQL Database
**Airflow Metadata:**
- Host: localhost
- Port: 5432 (internal)
- Database: airflow
- User: airflow
- Password: airflow

**Data Storage:**
- Host: localhost
- Port: 5433
- Database: recalls_db
- User: admin
- Password: admin

## 📁 โครงสร้างโปรเจค

```
Airflow-master/
├── dags/                    # Airflow DAGs
│   └── crypto_etl_dag.py   # CKAN ETL Pipeline
├── data/                    # Data storage
├── logs/                    # Airflow logs
├── plugins/                 # Airflow plugins
├── config/                  # Airflow configuration
├── analyze_data.py         # Data analysis script
├── cleanse_data.py         # Data cleansing script
├── convert_to_excel.py     # Excel conversion
├── test_api.py             # API testing
├── docker-compose.yaml     # Docker Compose config
├── Dockerfile              # Custom Airflow image
└── requirements.txt        # Python dependencies
```

## 🎯 DAG: ckan_data_etl

ETL Pipeline ที่ประกอบด้วย 3 tasks:

1. **Extract** - ดึงข้อมูลจาก CKAN API
2. **Transform** - แปลงข้อมูลและบันทึกเป็น CSV
3. **Load** - โหลดข้อมูลเข้า PostgreSQL

**Schedule:** รันทุกวัน เวลา 00:00

## 📝 คำสั่งที่ใช้บ่อย

### เริ่มต้น Services
```bash
docker compose up -d
```

### ดูสถานะ
```bash
docker compose ps
```

### ดู Logs
```bash
# ทั้งหมด
docker compose logs

# Service เฉพาะ
docker compose logs airflow-webserver
docker compose logs airflow-scheduler

# Real-time
docker compose logs -f
```

### หยุด Services
```bash
# หยุดและเก็บข้อมูล
docker compose down

# หยุดและลบข้อมูลทั้งหมด
docker compose down -v
```

### Restart Services
```bash
docker compose restart
```

## 🔍 Troubleshooting

### Container ไม่ขึ้น
```bash
docker compose logs
docker compose restart
```

### Port ซ้ำกัน
```bash
# Windows
netstat -ano | findstr :8080
netstat -ano | findstr :5433
```

### DAG ไม่แสดงใน UI
```bash
docker compose restart airflow-scheduler
```

## 📚 เอกสารเพิ่มเติม

- [PROJECT_STATUS.md](PROJECT_STATUS.md) - สรุปสถานะโปรเจคโดยละเอียด
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 👤 Author

- **Name:** SPOON
- **Email:** rujipob.c@ku.th

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Apache Airflow
- Thailand Open Data (opend.data.go.th)
- Docker Community
