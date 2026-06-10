# Correction — tests

## `tests/CalculatorTest.cpp`

```cpp
TEST(CalculatorTest, ComputesModulo) {
    Calculator calculator;
    EXPECT_EQ(calculator.modulo(10, 3), 1);
}

TEST(CalculatorTest, ThrowsWhenModuloByZero) {
    Calculator calculator;
    EXPECT_THROW(static_cast<void>(calculator.modulo(10, 0)), std::invalid_argument);
}
```

## `tests/CalculatorParameterizedTest.cpp`

Ajouter un cas :

```cpp
ExpressionCase{"10%3", 1}
```

## `tests/CalculatorMockTest.cpp`

```cpp
TEST(CalculatorServiceMockTest, LogsSuccessForModuloExpression) {
    ::testing::StrictMock<MockOperationLogger> logger;
    CalculatorService service{logger};

    EXPECT_CALL(logger, logSuccess("10%3", 1)).Times(1);

    EXPECT_EQ(service.evaluate("10%3"), 1);
}
```
