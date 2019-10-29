from flask import Flask
from flask_restful import Resource, Api
import boto3
import requests
import time, threading
from threading import Thread
import os
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

max_number_of_threads = 15
thread_limiter = threading.BoundedSemaphore(max_number_of_threads)


def rate_limitter(max_per_second: int):
    """Limits rate of function call to `max_per_second`."""
    min_interval = 1.0 / float(max_per_second)
    lock = threading.Lock()

    def decorate(func):
        last_time_called = [0.0]

        def function_call(args, **kargs):
            lock.acquire()
            elapsed = time.perf_counter() - last_time_called[0]
            wait = min_interval - elapsed
            if wait > 0:
                time.sleep(wait)
            lock.release()
            ret = func(args, **kargs)
            last_time_called[0] = time.perf_counter()
            return ret

        return function_call

    return decorate


class MessageHandler(threading.Thread):
    def run(self, message, api_endpoint: str):
        thread_limiter.acquire()
        try:
            reqeust_completed = self.api_request(
                message=message, api_endpoint=api_endpoint
            )
            if reqeust_completed:
                self.delete_message(message)
        finally:
            thread_limiter.release(),

    @rate_limitter(10)
    def api_request(self, message, api_endpoint: str):
        headers = {"Content-Type": "application/json"}
        try:
            r = requests.post(
                url=api_endpoint, json=message, headers=headers, timeout=10
            )
        except requests.exceptions.RequestException as e:
            logging.error(f"Could not complete request {e}")
            return False
        if r.status_code == requests.codes.ok:
            return True
        else:
            return False

    def delete_message(self, message):
        """ Removes message from queue after succesfull handling"""
        message.delete()


class QueueConsumer:
    def __init__(self):
        self.running = False
        self.api_endpoint = None
        self.queue_name = None
        self.region_name = None
        self.configure()

    def configure(self):
        try:
            self.api_endpoint = os.environ("API_ENDPOINT")
            self.queue_name = os.environ("QUEUE_NAME")
            self.region_name = os.environ("REGION_NAME")

        except Exception:
            logging.error("Environment variables not available")
        self.sqs = boto3.resource("sqs", region_name="eu-central-1")
        self.queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)

    def start(self):
        self.running = True
        main_thread = Thread(target=self.start_listening, daemon=True)
        main_thread.start()

    def stop(self):
        self.running = False

    def status(self):

        status = {
            "running": self.running,
            "endpoint": self.api_endpoint,
            "queue_name": self.queue_name,
        }
        logging.info(status)
        return status

    def start_listening(self):
        while self.running:
            messages = self.queue.receive_messages(WaitTimeSeconds=5)
            for message in messages:
                MessageHandler().run(message=message, api_endpoint=self.api_endpoint)


application = Flask(__name__)
api = Api(application)
que_consumer = QueueConsumer()

""" Api Resources """


class StatusQueue(Resource):
    def get(self):
        return {"status": que_consumer.status()}


class StartQueue(Resource):
    def get(self):
        que_consumer.start()
        return {"status": "queue-consumer started"}


class StopQueue(Resource):
    def get(self):
        que_consumer.stop()
        return {"status": "queue-consumer stopped"}


""" Api routes """
api.add_resource(StatusQueue, "/status")
api.add_resource(StartQueue, "/start")
api.add_resource(StopQueue, "/stop")

if __name__ == "__main__":
    application.debug = False
    application.run()
