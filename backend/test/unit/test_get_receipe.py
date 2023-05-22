import pytest
from unittest.mock import patch
import src.static.diets as diets
from src.controllers.receipecontroller import ReceipeController


@pytest.fixture
def sut(receipe, available_items, diet, readiness):
    with patch("src.controllers.receipecontroller.calculate_readiness") as mocked_calculate_readiness:
        mocked_calculate_readiness.return_value = readiness
        mocked_sut = ReceipeController()
        return mocked_sut


# Test #1 get_receipe_readiness, recipe not available on selected diet
@pytest.mark.unit
@pytest.mark.parametrize('receipe, available_items, diet',
                         [
                             ({"name": "Recipe 1", "diets": [diets.Diet.VEGAN]}, {
                              "ingredient1": 5, "ingredient2": 3}, diets.from_string("vegetarian"))
                         ]
                         )
def test_get_receipe_readiness_not_available(sut, receipe, available_items, diet):
    res = sut.get_receipe_readiness(receipe, available_items, diet)
    assert res is None


# Test #2 get_receipe_readiness, readiness below 0.1 (Boundary Value)
@pytest.mark.unit
@pytest.mark.parametrize('receipe, available_items, diet',
                         [
                             ({"name": "Recipe 2", "diets": [diets.Diet.VEGETARIAN]}, {
                              "ingredient1": 2, "ingredient2": 3}, diets.from_string("vegetarian"))
                         ]
                         )
def test_get_receipe_readiness_low_readiness(sut, receipe, available_items, diet):
    res = sut.get_receipe_readiness(receipe, available_items, diet)
    assert res is None


# Test 3, 4, 5, get_receipe_readiness, readiness between 0 and 1 (Boundary Values)
@pytest.mark.unit
@pytest.mark.parametrize('receipe, available_items, diet, readiness',
                         [
                             ({"name": "Recipe 3", "diets": [diets.Diet.VEGAN]}, {
                              "ingredient1": 5, "ingredient2": 3}, diets.from_string("vegan"), 0.1),
                             ({"name": "Recipe 4", "diets": [diets.Diet.VEGETARIAN]}, {
                              "ingredient1": 5, "ingredient2": 3}, diets.from_string("vegetarian"), 0.2),
                             ({"name": "Recipe 5", "diets": [diets.Diet.VEGAN]}, {
                              "ingredient1": 5, "ingredient2": 3}, diets.from_string("vegan"), 0.9)
                         ]
                         )
def test_get_receipe_readiness(sut, receipe, available_items, diet, readiness):
    res = sut.get_receipe_readiness(receipe, available_items, diet)
    assert res == readiness


# Test #6 get_receipe_readiness, readiness above 1 (Boundary Value)
@pytest.mark.unit
@pytest.mark.parametrize('receipe, available_items, diet',
                         [
                             ({"name": "Recipe 6", "diets": [diets.Diet.VEGAN]}, {
                              "ingredient1": 5, "ingredient2": 3}, diets.from_string("vegan"))
                         ]
                         )
def test_get_receipe_readiness_invalid_readiness(sut, receipe, available_items, diet):
    res = sut.get_receipe_readiness(receipe, available_items, diet)
    assert res is None
