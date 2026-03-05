import psutil
import math

# ---------------- CONSTANTS ----------------
LEARNING_PERIOD = 150
SIGMA_THRESHOLD = 3


class SystemMonitor:

    def __init__(self):

        self.cpu_history = []
        self.ram_history = []

        self.is_learning = True

        self.metrics = {}

        # For disk I/O speed calculation
        self.last_disk_read = psutil.disk_io_counters().read_bytes
        self.last_disk_write = psutil.disk_io_counters().write_bytes


    def fetch_metrics(self):

        # -------- CPU --------
        cpu_percent = psutil.cpu_percent(interval=None)

        cpu_freq_info = psutil.cpu_freq()
        cpu_freq = cpu_freq_info.current / 1000 if cpu_freq_info else 0


        # -------- RAM --------
        ram = psutil.virtual_memory()

        GB = 1024**3

        ram_used_gb = ram.used / GB
        ram_total_gb = ram.total / GB
        ram_percent = ram.percent


        # -------- DISK USAGE --------
        try:
            disk = psutil.disk_usage(psutil.disk_partitions()[0].mountpoint)
        except Exception:
            disk = psutil.disk_usage('/')

        disk_used_gb = disk.used / GB
        disk_total_gb = disk.total / GB
        disk_percent = disk.percent


        # -------- NETWORK --------
        net = psutil.net_io_counters()


        # -------- DISK I/O --------
        disk_io = psutil.disk_io_counters()

        read_speed = disk_io.read_bytes - self.last_disk_read
        write_speed = disk_io.write_bytes - self.last_disk_write

        self.last_disk_read = disk_io.read_bytes
        self.last_disk_write = disk_io.write_bytes


        # -------- STORE METRICS --------
        self.metrics = {

            "cpu_percent": cpu_percent,
            "cpu_freq": f"{cpu_freq:.2f} GHz",

            "ram_used": f"{ram_used_gb:.1f} GB",
            "ram_total": f"{ram_total_gb:.1f} GB",
            "ram_percent": ram_percent,

            "disk_used": f"{disk_used_gb:.0f} GB",
            "disk_total": f"{disk_total_gb:.0f} GB",
            "disk_percent": disk_percent,

            "disk_read": read_speed / (1024 * 1024),
            "disk_write": write_speed / (1024 * 1024),

            "net_sent": net.bytes_sent,
            "net_recv": net.bytes_recv,
        }


        self._analyze_data()

        return self.metrics


    def _analyze_data(self):

        cpu_val = self.metrics["cpu_percent"]
        ram_val = self.metrics["ram_percent"]


        # -------- STORE HISTORY --------
        self.cpu_history.append(cpu_val)
        self.ram_history.append(ram_val)

        if len(self.cpu_history) > LEARNING_PERIOD:
            self.cpu_history.pop(0)
            self.ram_history.pop(0)


        # -------- LEARNING PHASE --------
        if len(self.cpu_history) < LEARNING_PERIOD:

            self.is_learning = True

            self.metrics["alert"] = (
                f"Learning Normal Behavior... "
                f"({len(self.cpu_history)}/{LEARNING_PERIOD}s)"
            )

            return


        self.is_learning = False
        self.metrics["alert"] = "System Status: OK"


        # -------- CALCULATE MEAN --------
        cpu_mean = sum(self.cpu_history) / LEARNING_PERIOD
        ram_mean = sum(self.ram_history) / LEARNING_PERIOD


        # -------- CALCULATE STD DEV --------
        cpu_std = math.sqrt(
            sum((x - cpu_mean) ** 2 for x in self.cpu_history) / LEARNING_PERIOD
        )

        ram_std = math.sqrt(
            sum((x - ram_mean) ** 2 for x in self.ram_history) / LEARNING_PERIOD
        )


        # Store for graph usage
        self.metrics["cpu_mean"] = cpu_mean
        self.metrics["cpu_std_dev"] = cpu_std
        self.metrics["ram_mean"] = ram_mean
        self.metrics["ram_std_dev"] = ram_std


        # -------- ANOMALY DETECTION --------
        if cpu_val > cpu_mean + (SIGMA_THRESHOLD * cpu_std):

            self.metrics["alert"] = f"HIGH CPU ANOMALY: {cpu_val:.1f}%"

        elif ram_val > ram_mean + (SIGMA_THRESHOLD * ram_std):

            self.metrics["alert"] = f"HIGH RAM ANOMALY: {ram_val:.1f}%"


# ---------------- TEST BLOCK ----------------
if __name__ == "__main__":

    monitor = SystemMonitor()

    print("Testing metrics collection...")

    data = monitor.fetch_metrics()

    print("CPU:", data["cpu_percent"])
    print("RAM:", data["ram_percent"])
    print("Alert:", data["alert"])