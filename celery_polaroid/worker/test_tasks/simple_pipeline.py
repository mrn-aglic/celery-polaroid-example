from celery_polaroid.celeryapp import app


@app.task
def producer():
    return "Some text"


@app.task
def consumer(text):
    print(f"The text we got is {text}")


@app.task
def pipeline():
    return (producer.s() | consumer.s()).apply_async()
