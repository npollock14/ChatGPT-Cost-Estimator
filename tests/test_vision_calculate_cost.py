import pytest

from chatgpt_cost_estimator.vision_cost_estimator import calculate_vision_cost


@pytest.mark.parametrize(
    "width, height, low_res, expected",
    [
        (512, 512, False, 0.00255),
        (1024, 512, False, 0.00425),
        (1025, 512, False, 0.00595),
        (513, 512, False, 0.00425),
        (513, 512, True, 0.00085),
        (10_000, 512, False, 0.00765),
        (10_000, 10_000, False, 0.00765),
    ],
)
def test_calculate_cost(width, height, low_res, expected):
    assert calculate_vision_cost(width, height, low_res) == expected
