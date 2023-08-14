import psutil
import matplotlib
import flask
import time



from flask import Flask, render_template

app = Flask(__name__, static_folder='templates')

@app.route('/')
def index():
    # Add code here to retrieve server performance data using psutil
    # Store the data in suitable variables to pass to the template
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
    
    # Pass the variables containing the data to the template
    return render_template('/dashboard_template.html',
                           cpu_usage=cpu_usage,
                           total_memory=total_memory,
                           available_memory=available_memory,
                           memory_usage=memory_usage,
                           total_disk_space=total_disk_space,
                           used_disk_space=used_disk_space,
                           free_disk_space=free_disk_space,
                           disk_space_usage=disk_space_usage,
                           bytes_sent=bytes_sent,
                           bytes_received=bytes_received,
                           packets_sent=packets_sent,
                           packets_received=packets_received,
                           response_time=response_time)

if __name__ == '__main__':
    app.run()  # debug=True for development mode  

# if __name__ == '__main__':
#     app.run(debug=True)  # debug=True for development mode  