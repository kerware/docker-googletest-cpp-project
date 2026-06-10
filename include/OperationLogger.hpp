#pragma once

#include <string>

class OperationLogger {
public:
    virtual ~OperationLogger() = default;
    virtual void logSuccess(const std::string& expression, int result) = 0;
    virtual void logFailure(const std::string& expression, const std::string& reason) = 0;
};

class CalculatorService {
public:
    explicit CalculatorService(OperationLogger& logger) : logger_(logger) {}

    int evaluate(const std::string& expression) const;

private:
    OperationLogger& logger_;
};
