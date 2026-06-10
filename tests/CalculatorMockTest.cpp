#include "OperationLogger.hpp"

#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

class MockOperationLogger : public OperationLogger {
public:
    MOCK_METHOD(void, logSuccess, (const std::string& expression, int result), (override));
    MOCK_METHOD(void, logFailure, (const std::string& expression, const std::string& reason), (override));
};

TEST(CalculatorServiceMockTest, LogsSuccessWhenExpressionIsValid) {
    ::testing::StrictMock<MockOperationLogger> logger;
    CalculatorService service{logger};

    EXPECT_CALL(logger, logSuccess("2+3", 5)).Times(1);

    EXPECT_EQ(service.evaluate("2+3"), 5);
}

TEST(CalculatorServiceMockTest, LogsFailureWhenExpressionIsInvalid) {
    ::testing::StrictMock<MockOperationLogger> logger;
    CalculatorService service{logger};

    EXPECT_CALL(logger, logFailure("2/0", ::testing::HasSubstr("division"))).Times(1);

    EXPECT_THROW(static_cast<void>(service.evaluate("2/0")), std::invalid_argument);
}
