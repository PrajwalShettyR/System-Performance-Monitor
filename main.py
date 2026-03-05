import customtkinter as ctk
from metrics import SystemMonitor, SIGMA_THRESHOLD
import time
import psutil

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------- GLOBAL STATE ----------------
last_net_sent = 0
last_net_recv = 0
last_time = time.time()

last_disk_read = psutil.disk_io_counters().read_bytes
last_disk_write = psutil.disk_io_counters().write_bytes

last_alert_time = 0

monitor = SystemMonitor()

graph_type = "cpu"

ram_history = []
disk_history = []


# ---------------- ALERT POPUP ----------------
def show_notification(message):

    popup = ctk.CTkToplevel(root)
    popup.title("System Alert")
    popup.geometry("280x140")

    label = ctk.CTkLabel(
        popup,
        text=message,
        font=("Segoe UI",14,"bold")
    )
    label.pack(pady=30)

    btn = ctk.CTkButton(
        popup,
        text="OK",
        command=popup.destroy
    )
    btn.pack()


# ---------------- GRAPH ----------------
class PlotManager:

    def __init__(self,parent):

        self.fig, self.ax = plt.subplots(figsize=(10,6))

        self.fig.patch.set_facecolor("#2B2B2B")
        self.ax.set_facecolor("#2B2B2B")

        self.ax.tick_params(colors="#BBBBBB")
        self.ax.grid(True,alpha=0.2)

        self.ax.set_ylim(0,100)

        self.canvas = FigureCanvasTkAgg(self.fig,master=parent)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True,fill="both",padx=20,pady=20)

        self.line, = self.ax.plot([],[],color="#4CC9F0",linewidth=2)

    def update_plot(self):

        if graph_type == "cpu":
            history = monitor.cpu_history
            title = "CPU Usage"
            color = "#22c55e"     # green
            fill = "#22c55e"

        elif graph_type == "ram":
            history = ram_history
            title = "RAM Usage"
            color = "#3b82f6"     # blue
            fill = "#3b82f6"

        else:
            history = disk_history
            title = "Disk Usage"
            color = "#ef4444"     # red
            fill = "#ef4444"


        N = len(history)

        if N < 2:
            return


        self.ax.clear()

        self.ax.set_facecolor("#2B2B2B")
        self.ax.set_ylim(0,100)

        self.ax.set_title(title,color="white")
        self.ax.set_ylabel("Usage %",color="#BBBBBB")
        self.ax.set_xlabel("Time",color="#BBBBBB")

        self.ax.tick_params(colors="#BBBBBB")
        self.ax.grid(True,alpha=0.2)


        x = list(range(N))

        # main line
        self.ax.plot(x, history, color=color, linewidth=2)

        # faded area under graph
        self.ax.fill_between(
            x,
            history,
            color=fill,
            alpha=0.15
        )


        self.canvas.draw_idle()


# ---------------- UI HELPER ----------------
def create_metric_row(parent,name,progress=True):

    frame = ctk.CTkFrame(parent,corner_radius=8)
    frame.pack(fill="x",pady=8,padx=10)

    name_label = ctk.CTkLabel(
        frame,
        text=name,
        font=("Segoe UI",14,"bold")
    )
    name_label.pack(side="left",padx=10)

    value_label = ctk.CTkLabel(
        frame,
        text="Loading...",
        font=("Segoe UI",14)
    )
    value_label.pack(side="right",padx=10)

    bar=None

    if progress:
        bar = ctk.CTkProgressBar(parent)
        bar.pack(fill="x",padx=15,pady=(0,10))

    return value_label,bar


# ---------------- GRAPH BUTTONS ----------------
def set_graph(type):
    global graph_type
    graph_type = type


# ---------------- UPDATE LOOP ----------------
def update_metrics():

    global last_net_sent,last_net_recv,last_time
    global last_disk_read,last_disk_write,last_alert_time

    metrics = monitor.fetch_metrics()

    current_time=time.time()
    diff=current_time-last_time


    # NETWORK
    if diff>0:

        MB=1024*1024

        upload=(metrics["net_sent"]-last_net_sent)/diff/MB
        download=(metrics["net_recv"]-last_net_recv)/diff/MB

        net_up_label.configure(text=f"{upload:.1f} MB/s")
        net_down_label.configure(text=f"{download:.1f} MB/s")

    last_net_sent=metrics["net_sent"]
    last_net_recv=metrics["net_recv"]


    # CPU
    cpu_percent=metrics["cpu_percent"]
    cpu_label.configure(text=f"{cpu_percent:.1f}% | {metrics['cpu_freq']}")
    cpu_bar.set(cpu_percent/100)


    # RAM
    ram_percent=metrics["ram_percent"]
    ram_label.configure(text=f"{metrics['ram_used']} / {metrics['ram_total']} ({ram_percent:.1f}%)")
    ram_bar.set(ram_percent/100)

    ram_history.append(ram_percent)
    if len(ram_history)>300:
        ram_history.pop(0)


    # DISK
    disk_percent=metrics["disk_percent"]
    disk_label.configure(text=f"{metrics['disk_used']} / {metrics['disk_total']} ({disk_percent:.1f}%)")
    disk_bar.set(disk_percent/100)

    disk_history.append(disk_percent)
    if len(disk_history)>300:
        disk_history.pop(0)


    # DISK IO
    disk_io=psutil.disk_io_counters()

    read_speed=(disk_io.read_bytes-last_disk_read)/diff/1024/1024
    write_speed=(disk_io.write_bytes-last_disk_write)/diff/1024/1024

    disk_read_label.configure(text=f"{read_speed:.1f} MB/s")
    disk_write_label.configure(text=f"{write_speed:.1f} MB/s")

    last_disk_read=disk_io.read_bytes
    last_disk_write=disk_io.write_bytes



    # TOP PROCESSES
    try:

        psutil.cpu_percent(interval=None)

        processes = []

        for p in psutil.process_iter(['name', 'cpu_percent']):
            try:
                name = p.info.get('name', 'Unknown')
                cpu = p.info.get('cpu_percent', 0) or 0

                processes.append((name, cpu))

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue


        processes = sorted(processes, key=lambda x: x[1], reverse=True)[:5]

        text = "\n".join([f"{name[:18]:18} {cpu:>5.1f}%" for name, cpu in processes])

        process_label.configure(text=text if text else "Scanning...")

    except Exception:
        process_label.configure(text="Scanning processes...")


    # ALERT
    alert=metrics.get("alert","N/A")
    alert_label.configure(text=alert)

    if "ANOMALY" in alert:

        alert_label.configure(text_color="red")

        if time.time()-last_alert_time>10:
            show_notification("CPU Anomaly Detected")
            last_alert_time=time.time()


    plot_manager.update_plot()

    last_time=current_time

    root.after(1000,update_metrics)


# ---------------- MAIN WINDOW ----------------
root=ctk.CTk()
root.title("System Performance Monitor")
root.geometry("1400x750")


title = ctk.CTkLabel(
    root,
    text="System Performance Monitor",
    font=("Segoe UI",26,"bold")
)
title.pack(pady=20)


main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both",expand=True,padx=20,pady=10)


# LEFT PANEL
metrics_frame = ctk.CTkFrame(main_frame,width=300)
metrics_frame.pack(side="left",fill="y",padx=15,pady=15)


cpu_label,cpu_bar=create_metric_row(metrics_frame,"CPU")
ram_label,ram_bar=create_metric_row(metrics_frame,"RAM")
disk_label,disk_bar=create_metric_row(metrics_frame,"Disk")

disk_read_label,_=create_metric_row(metrics_frame,"Disk Read",False)
disk_write_label,_=create_metric_row(metrics_frame,"Disk Write",False)

net_up_label,_=create_metric_row(metrics_frame,"Upload",False)
net_down_label,_=create_metric_row(metrics_frame,"Download",False)


process_label=ctk.CTkLabel(
    metrics_frame,
    text="Loading...",
    font=("Consolas",13),
    justify="left"
)
process_label.pack(pady=10)


# GRAPH PANEL
graph_frame = ctk.CTkFrame(main_frame)
graph_frame.pack(side="right",fill="both",expand=True,padx=15,pady=15)


button_frame = ctk.CTkFrame(graph_frame)
button_frame.pack(pady=10)

ctk.CTkButton(button_frame,text="CPU",width=80,
              command=lambda:set_graph("cpu")).pack(side="left",padx=5)

ctk.CTkButton(button_frame,text="RAM",width=80,
              command=lambda:set_graph("ram")).pack(side="left",padx=5)

ctk.CTkButton(button_frame,text="Disk",width=80,
              command=lambda:set_graph("disk")).pack(side="left",padx=5)


plot_manager=PlotManager(graph_frame)


# STATUS BAR
status_frame=ctk.CTkFrame(root,height=40)
status_frame.pack(fill="x",padx=10,pady=5)

alert_label=ctk.CTkLabel(
    status_frame,
    text="Initializing...",
    font=("Segoe UI",13,"bold")
)
alert_label.pack(pady=5)


update_metrics()

root.mainloop()