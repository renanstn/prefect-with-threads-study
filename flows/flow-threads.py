import random
import requests
import threading

from prefect import Flow, Task


class GetListOfValues(Task):
    def run(self):
        return [random.randint(0, 100) for _ in range(100)]


class PrintValue(Task):
    def run(self, value: str):
        print("=" * 100)
        print(value)
        print("=" * 100)


class RefactoredAddRandomValueToValue(Task):
    def get_data_and_sum(self, value: int):
        url = "http://localhost:8000/random_value"
        response = requests.get(url).json()
        self.values_to_return.append(value + response.get("value"))

    def run(self, values: list):
        self.values_to_return = []
        threads = []

        # Create and start threads
        for value in values:
            thread = threading.Thread(target=self.get_data_and_sum, args=(value,))
            threads.append(thread)
            thread.start()

        # Join threads, so the main function will wait for them to finish
        for thread in threads:
            thread.join()

        return self.values_to_return


# =============================================================================
with Flow("flow-using-threads") as flow:
    values_a = GetListOfValues(name="get_list_of_values")
    values_a_with_random_number = RefactoredAddRandomValueToValue(
        name="add_v2"
    )(values=values_a)
    PrintValue()(values_a_with_random_number)
