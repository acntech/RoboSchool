import pytest

from src.features.printout import print_image
from src.features.printout import add


def test_printout():
    test_return_message = print_image()
    assert test_return_message == "successful print"


@pytest.fixture
def give_numbers(request):
    a = 2
    b = 3
    yield a, b

    def tear_down():
        print('Delete the files')

    print(a, b)


def test_add(give_numbers):
    a, b = give_numbers
    assert add(a, b) == 5