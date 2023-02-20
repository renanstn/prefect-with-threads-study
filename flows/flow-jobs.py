import random
import requests

from prefect import Flow, Task


class GetListOfValues(Task):
    def run(self):
        return [random.randint(0, 100) for _ in range(100)]


class PrintValue(Task):
    def run(self, value: str):
        print("=" * 100)
        print(value)
        print("=" * 100)


class AddRandomValueToValue(Task):
    def run(self, value: list):
        url = "http://localhost:8000/random_value"
        response = requests.get(url).json()
        random_value = response.get("value")
        return value + random_value


# =============================================================================
with Flow("flow-using-jobs") as flow:
    values_a = GetListOfValues(name="get_list_of_values")
    values_a_with_random_number = AddRandomValueToValue(name="add_v1").map(
        value=values_a
    )
    PrintValue()(values_a_with_random_number)
