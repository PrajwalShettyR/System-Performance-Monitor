# System Performance Monitor

A comprehensive Python-based system performance monitoring tool that tracks CPU, memory, disk, and network metrics in real-time.

## Description

A lightweight and efficient system performance monitoring application built with **Python**. This tool provides real-time monitoring of system resources including CPU usage, memory consumption, disk I/O, and network traffic. The application features an intuitive interface and detailed logging capabilities for performance history tracking.

**Key Features:**
- Real-time system metrics monitoring
- CPU, memory, disk, and network tracking
- Process-level resource consumption analysis
- Customizable alerts for threshold breaches
- Detailed logging and history
- Lightweight with minimal resource overhead

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.7+ |
| Monitoring | psutil |
| Logging | Python logging module |
| Data Format | JSON, CSV |
| Database | SQLite (optional) |

---

## File Structure

```
System-Performance-Monitor/
│
├── main.py                 # Main application entry point
├── monitor.py              # Core monitoring module
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── logs/                   # Log files directory
│   └── monitor.log         # Performance logs
├── data/                   # Data export directory
│   ├── metrics.json        # JSON export format
│   └── metrics.csv         # CSV export format
├── README.md              # Project documentation
└── .gitignore             # Git ignore file
```

---

## Installation Instructions

### Prerequisites
- **Python** (v3.7 or higher)
- **pip** (Python package manager)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PrajwalShettyR/System-Performance-Monitor.git
   cd System-Performance-Monitor
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage Examples

### Basic Usage

```bash
python main.py
```

### With Custom Arguments

```bash
python main.py --interval 5 --duration 300 --output json
```

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--interval` | Update interval in seconds | 2 |
| `--duration` | Total monitoring duration in seconds | Continuous |
| `--output` | Output format (console, json, csv) | console |
| `--log-level` | Logging level (DEBUG, INFO, WARNING) | INFO |

---

## Configuration

Edit `config.py` to customize monitoring parameters:

```python
# Monitoring Settings
INTERVAL = 2                    # seconds between updates
DURATION = None                 # None = continuous

# Alert Thresholds
CPU_THRESHOLD = 80              # percentage
MEMORY_THRESHOLD = 85           # percentage
DISK_THRESHOLD = 90             # percentage

# Logging
LOG_FILE = "logs/monitor.log"
LOG_LEVEL = "INFO"
```

---

## Output Examples

### Console Output
```
=== System Performance Monitor ===
CPU Usage: 45.2%
  - Core 0: 42.1%
  - Core 1: 48.3%

Memory: 8.4 GB / 16 GB (52.5%)
  - Available: 7.6 GB
  - Used: 8.4 GB

Disk: 250 GB / 500 GB (50.0%)
  - Root: /dev/sda1 (65%)
  - Home: /dev/sda2 (35%)

Network:
  - eth0: ↓ 2.5 MB/s | ↑ 1.2 MB/s
  - eth1: ↓ 0.8 MB/s | ↑ 0.4 MB/s
```


## Running the Application

### Terminal Execution
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run monitor
python main.py

# Run with options
python main.py --interval 5 --output json
```

---

## Future Enhancements

- [ ] Web dashboard interface
- [ ] Email/SMS alerts
- [ ] Database integration for long-term storage
- [ ] GPU monitoring support
- [ ] Docker containerization
- [ ] RESTful API endpoint
- [ ] Multi-system monitoring

---

## Error Codes & Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: psutil` | Run `pip install -r requirements.txt` |
| `Permission denied` | Run with sudo/admin privileges |
| `No output displayed` | Check log file in `logs/monitor.log` |

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Author

Created by **[PrajwalShettyR](https://github.com/PrajwalShettyR)**

---

## Support

For issues, questions, or suggestions, please open an [issue](https://github.com/PrajwalShettyR/System-Performance-Monitor/issues) in the repository.
