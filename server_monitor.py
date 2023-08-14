import psutil
import flask
import time
import plotly.graph_objs as go
import plotly.offline

from flask import Flask, render_template

app = Flask(__name__, static_folder='templates')

@app.route('/')
def index():
    # Add code here to retrieve server performance data using psutil
    # Store the data in suitable variables to pass to the template
    # Example data for demonstration purposes
    cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
    cores = list(range(len(cpu_percents)))
    start_time = time.time()  # Record the start time
    cpu_usage = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    total_memory = memory.total
    available_memory = memory.available
    memory_usage = memory.percent
    disk_usage = psutil.disk_usage('/')
    total_disk_space = disk_usage.total
    used_disk_space = disk_usage.used
    free_disk_space = disk_usage.free
    disk_space_usage = disk_usage.percent
    network_stats = psutil.net_io_counters()
    bytes_sent = network_stats.bytes_sent
    bytes_received = network_stats.bytes_recv
    packets_sent = network_stats.packets_sent
    packets_received = network_stats.packets_recv
    end_time = time.time()  # Record the end time
    response_time = end_time - start_time  # Calculate response time in seconds

    # Memory usage
    memory = psutil.virtual_memory()
    memory_used = memory.used / (1024 ** 2)  # Convert to MB
    memory_available = memory.available / (1024 ** 2)  # Convert to MB
    memory_percent = memory.percent

    memory_plot_div = create_memory_plot(memory_used, memory_available)

    # CPU usage
    cpu_plot_div = create_cpu_plot(cores, cpu_percents)

    return render_template('dashboard_template.html',
                           memory_plot_div=memory_plot_div,
                           cpu_plot_div=cpu_plot_div,
                           memory_percent=memory_percent, cpu_usage=cpu_usage,
                           total_memory=total_memory, available_memory=available_memory,
                           memory_usage=memory_usage, total_disk_space=total_disk_space,
                           used_disk_space=used_disk_space, free_disk_space=free_disk_space,
                           disk_space_usage=disk_space_usage, bytes_sent=bytes_sent,
                           bytes_received=bytes_received, packets_sent=packets_sent,
                           packets_received=packets_received, response_time=response_time)

def create_memory_plot(used, available):
    data = go.Bar(x=['Used', 'Available'], y=[used, available])
    layout = go.Layout(title='Memory Utilization', xaxis={'title': 'Memory Type'}, yaxis={'title': 'Memory (MB)'})
    fig = go.Figure(data=[data], layout=layout)
    plot_div = plotly.offline.plot(fig, output_type='div', show_link=False)
    return plot_div

def create_cpu_plot(cores, cpu_percents):
    data = go.Bar(x=cores, y=cpu_percents)
    layout = go.Layout(title='CPU Usage', xaxis={'title': 'Each CPU Core'}, yaxis={'title': 'Usage (%)'})
    fig = go.Figure(data=[data], layout=layout)
    plot_div = plotly.offline.plot(fig, output_type='div', show_link=False)
    return plot_div

if __name__ == '__main__':
    app.run(debug=True)  # debug=True for development mode
