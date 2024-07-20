import psutil
from flask import Flask, render_template
import time
app = Flask(__name__)

@app.route("/")
def index():
    time.sleep(1)  # Wait for 1 second to get accurate CPU usage
    cpu_metric = psutil.cpu_percent(interval=1)  # Measure over 1 second
    mem_metric = psutil.virtual_memory().percent
    Message = None
    if cpu_metric > 80 or mem_metric > 80:
        Message = "High CPU or Memory Detected, scale up!!!"
    return render_template("index.html", cpu_metric=cpu_metric, mem_metric=mem_metric, message=Message)

if __name__=='__main__':
    app.run(debug=True, host = '0.0.0.0')