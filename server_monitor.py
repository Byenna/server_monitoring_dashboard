import psutil
import flask
import time
import plotly.graph_objs as go
import plotly.offline
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_PASSWORD
import requests

# Define the URL of your Flask app
url = 'http://localhost:5000/check_metrics'  # Replace with the actual URL of your app

# Send a POST request
response = requests.post(url)

# Print the response
print(response.text)


from flask import Flask, render_template, request

app = Flask(__name__, static_folder='templates')

@app.route('/')
def index():
    # Add code here to retrieve server performance data using psutil
    # Store the data in suitable variables to pass to the template
    # Example data for demonstration purposes
    
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

  

    return render_template('dashboard_template.html',
                           cpu_usage=cpu_usage,
                           total_memory=total_memory, available_memory=available_memory,
                           memory_usage=memory_usage, total_disk_space=total_disk_space,
                           used_disk_space=used_disk_space, free_disk_space=free_disk_space,
                           disk_space_usage=disk_space_usage, bytes_sent=bytes_sent,
                           bytes_received=bytes_received, packets_sent=packets_sent,
                           packets_received=packets_received, response_time=response_time)

@app.route('/visualizations')
def visualizations():
    cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
    cores = list(range(len(cpu_percents)))

      # Memory usage
    memory = psutil.virtual_memory()
    memory_used = memory.used / (1024 ** 2)  # Convert to MB
    memory_available = memory.available / (1024 ** 2)  # Convert to MB
    memory_percent = memory.percent

    memory_plot_div = create_memory_plot(memory_used, memory_available)

    # CPU usage
    cpu_plot_div = create_cpu_plot(cores, cpu_percents)
    # Add code here to retrieve and pass data for visualizations if needed
    return render_template('visualizations.html',
                           memory_plot_div=memory_plot_div,
                           cpu_plot_div=cpu_plot_div,
                           memory_percent=memory_percent)

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

@app.route('/check_metrics', methods=['POST'])
def check_metrics():
    cpu_usage = get_cpu_usage()  # Implement a function to retrieve CPU usage

    if cpu_usage > 90:  # Your threshold value
        subject = 'Alert: High CPU Usage'
        message = f'CPU usage is {cpu_usage}%, which is above the threshold.'
        send_email_alert(subject, message)

    return 'Metrics checked'

def send_email_alert(subject, message):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'recipient@example.com'
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


if __name__ == '__main__':
    app.run(debug=True)  # debug=True for development mode
