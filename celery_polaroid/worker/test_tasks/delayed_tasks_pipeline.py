import time

from celery_polaroid.celeryapp import app


@app.task
def producer():
    # now = datetime.now().isoformat(timespec="seconds")
    # print(f"-----------------producer {now}")
    time.sleep(5)
    return "Some text"


@app.task
def consumer(text):
    # print("-----------------consumer")

    time.sleep(5)
    # print(f"The text we got is {text}")


@app.task
def pipeline():
    return (producer.s() | consumer.s()).apply_async()
