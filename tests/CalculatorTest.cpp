#include "Calculator.hpp"

#include <gtest/gtest.h>
#include <stdexcept>

TEST(CalculatorTest, AddsTwoPositiveNumbers) {
    Calculator calculator;
    EXPECT_EQ(calculator.add(2, 3), 5);
}

TEST(CalculatorTest, SubtractsNumbers) {
    Calculator calculator;
    EXPECT_EQ(calculator.subtract(10, 4), 6);
}

TEST(CalculatorTest, MultipliesByZero) {
    Calculator calculator;
    EXPECT_EQ(calculator.multiply(42, 0), 0);
}

TEST(CalculatorTest, DividesTwoNumbers) {
    Calculator calculator;
    ASSERT_EQ(calculator.divide(10, 2), 5);
}

TEST(CalculatorTest, ThrowsWhenDividingByZero) {
    Calculator calculator;
    EXPECT_THROW(static_cast<void>(calculator.divide(10, 0)), std::invalid_argument);
}
