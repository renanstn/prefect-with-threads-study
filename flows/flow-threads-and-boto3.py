import threading

import boto3
from prefect import Flow, Task, Parameter


class GetListOfValues(Task):
    def run(self):
        return [i for i in range(0, 100)]


class CreateBoto3Session(Task):
    def run(self, aws_access_key_id, aws_secret_access_key):
        client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        return client


class ListBuckets(Task):
    def run(self, client):
        return client.list_buckets().get("Buckets")


class ListBucketsUsingThreads(Task):
    def run(self, client, list_of_values):
        self.values_to_return = []
        threads = []

        # Create and start threads
        for value in list_of_values:
            thread = threading.Thread(
                    target=self.list_buckets, args=(client, value)
                )
            threads.append(thread)
            thread.start()
        # Join threads, so the main function will wait for them to finish
        for thread in threads:
            thread.join()

        return self.values_to_return

    def list_buckets(self, client, value):
        buckets = client.list_buckets().get("Buckets")
        self.values_to_return.append({value: buckets})


class PrintValue(Task):
    def run(self, value: str):
        print("=" * 100)
        print(value)
        print("=" * 100)


# =============================================================================
with Flow("flow-threads-and-boto3") as flow:
    aws_access_key_id = Parameter("AWS access key ID")
    aws_secret_access_key = Parameter("AWS secret access key")

    list_of_values = GetListOfValues(name="Generate list of values")()
    client = CreateBoto3Session(name="Create session")(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    # buckets = ListBuckets(name="List buckets")(client=client)
    buckets_and_values = ListBucketsUsingThreads(
        name="List buckets with threads"
    )(client=client, list_of_values=list_of_values)
    PrintValue()(value=buckets_and_values)
