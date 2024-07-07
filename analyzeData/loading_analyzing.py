import logging
import json
import datetime
import time
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd


class TimeValueLogger:
    def __init__(self, log_file='logfile.log'):
        self.log_file = log_file
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger()
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(self.file_handler)

    def log(self, values):
        if not isinstance(values, dict) or not all(key in values for key in ["preprocess", "inference", "postprocess"]):
            raise ValueError("Values must be a dictionary with keys 'preprocess', 'inference', and 'postprocess'.")

        current_time = datetime.datetime.now().isoformat()
        log_entry = {"time": current_time, **values}
        self.logger.info(json.dumps(log_entry))
        self.file_handler.flush()  # Немедленно сбросить буфер


class GraphBuilder:
    def __init__(self, log_file='logfile.log'):
        self.log_file = log_file

    def read_logs(self):
        with open(self.log_file, 'r') as file:
            logs = []
            for line in file:
                try:
                    logs.append(json.loads(line.strip()))
                except Exception:
                    pass
        return logs

    def plot_graphs(self):
        logs = self.read_logs()
        times = [log['time'] for log in logs]
        preprocess_values = [log['preprocess'] for log in logs]
        inference_values = [log['inference'] for log in logs]
        postprocess_values = [log['postprocess'] for log in logs]

        fig = make_subplots(rows=1, cols=1)

        fig.add_trace(go.Scatter(x=times, y=preprocess_values, mode='lines', name='Preprocess'))
        fig.add_trace(go.Scatter(x=times, y=inference_values, mode='lines', name='Inference'))
        fig.add_trace(go.Scatter(x=times, y=postprocess_values, mode='lines', name='Postprocess'))

        fig.update_layout(
            title='Image processing',
            xaxis_title='Time',
            yaxis_title='Values',
            legend_title='Stages'
        )

        return fig.to_html(full_html=False)

    def plot_request_rate(self):
        logs = self.read_logs()
        times = [log['time'] for log in logs]

        # Преобразуем строки времени в объекты datetime
        times = pd.to_datetime(times)

        # Создаем DataFrame и группируем по минутам
        df = pd.DataFrame(times, columns=['time'])
        df.set_index('time', inplace=True)
        request_counts = df.resample('T').size()  # 'T' означает минутное разрешение

        fig = make_subplots(rows=1, cols=1)

        fig.add_trace(go.Scatter(x=request_counts.index, y=request_counts.values, mode='lines+markers',
                                 name='Requests per Minute'))

        fig.update_layout(
            title='Requests per Minute',
            xaxis_title='Time',
            yaxis_title='Number of Requests',
            legend_title='Requests'
        )

        return fig.to_html(full_html=False)


if __name__ == '__main__':
    graph_builder = GraphBuilder()

    graph_builder.plot_graphs()
    graph_builder.plot_request_rate()
