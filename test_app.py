"""
Unit Tests for Food Calorie Tracker
Test validators and core functionality
"""

import pytest
from food_validators import validate_meal_name, validate_calories


class TestMealNameValidation:
    """Test meal name input validation"""
    
    def test_valid_meal_name(self):
        """Test with valid meal name"""
        valid, msg = validate_meal_name("Nasi Goreng")
        assert valid == True
        assert "Valid" in msg
    
    def test_valid_meal_name_with_numbers(self):
        """Test with valid meal name containing numbers"""
        valid, msg = validate_meal_name("Rice 100g")
        assert valid == True
    
    def test_valid_meal_name_with_dash(self):
        """Test with valid meal name containing dash"""
        valid, msg = validate_meal_name("Chicken-Satay")
        assert valid == True
    
    def test_empty_meal_name(self):
        """Test with empty meal name"""
        valid, msg = validate_meal_name("")
        assert valid == False
        assert "empty" in msg.lower()
    
    def test_whitespace_only_meal_name(self):
        """Test with whitespace only"""
        valid, msg = validate_meal_name("   ")
        assert valid == False
        assert "empty" in msg.lower()
    
    def test_meal_name_too_long(self):
        """Test with very long meal name"""
        long_name = "A" * 101
        valid, msg = validate_meal_name(long_name)
        assert valid == False
        assert "too long" in msg.lower()
    
    def test_meal_name_max_length(self):
        """Test with meal name at max length"""
        max_name = "A" * 100
        valid, msg = validate_meal_name(max_name)
        assert valid == True
    
    def test_meal_name_special_characters(self):
        """Test with invalid special characters"""
        valid, msg = validate_meal_name("Nasi!@#$")
        assert valid == False
        assert "invalid" in msg.lower()


class TestCaloriesValidation:
    """Test calories input validation"""
    
    def test_valid_calories(self):
        """Test with valid calorie value"""
        valid, msg = validate_calories(250)
        assert valid == True
        assert "Valid" in msg
    
    def test_valid_calories_string(self):
        """Test with valid calorie as string"""
        valid, msg = validate_calories("300")
        assert valid == True
    
    def test_valid_calories_float(self):
        """Test with valid calorie as float"""
        valid, msg = validate_calories(250.5)
        assert valid == True
    
    def test_negative_calories(self):
        """Test with negative calorie value"""
        valid, msg = validate_calories(-50)
        assert valid == False
        assert "negative" in msg.lower()
    
    def test_zero_calories(self):
        """Test with zero calorie value"""
        valid, msg = validate_calories(0)
        assert valid == False
        assert "greater than 0" in msg.lower()
    
    def test_calories_too_high(self):
        """Test with calorie value too high"""
        valid, msg = validate_calories(6000)
        assert valid == False
        assert "too high" in msg.lower()
    
    def test_calories_max_value(self):
        """Test with calorie at max allowed value"""
        valid, msg = validate_calories(5000)
        assert valid == True
    
    def test_calories_not_number(self):
        """Test with non-numeric input"""
        valid, msg = validate_calories("abc")
        assert valid == False
        assert "number" in msg.lower()
    
    def test_calories_none(self):
        """Test with None value"""
        valid, msg = validate_calories(None)
        assert valid == False
        assert "number" in msg.lower()


class TestEdgeCases:
    """Test edge cases"""
    
    def test_meal_name_with_comma(self):
        """Test meal name with comma"""
        valid, msg = validate_meal_name("Chicken, Rice")
        assert valid == True
    
    def test_meal_name_mixed_case(self):
        """Test meal name with mixed case"""
        valid, msg = validate_meal_name("NaSi GoReNg")
        assert valid == True
    
    def test_calories_boundary_low(self):
        """Test calories at boundary (just above 0)"""
        valid, msg = validate_calories(1)
        assert valid == True
    
    def test_calories_boundary_high(self):
        """Test calories at boundary (just below max)"""
        valid, msg = validate_calories(4999)
        assert valid == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
