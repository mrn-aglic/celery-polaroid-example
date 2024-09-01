# celery-polaroid-example
This is a repo for some example code used for a medium story
titled Getting Celery Snapshots with Polaroid.
Here is the link:
https://medium.com/@MarinAgli1/getting-celery-snapshots-with-polaroid-3bb933c04fa0

The example shows how to use a custom camera in Celery for
capturing some queue and task information.

# Working with the repo
Building the docker images can be done with:
```shell
make build
```

Running:
```shell
make run
```

Running with multiple (4) workers:
```shell
make run-scale workers=4
```
