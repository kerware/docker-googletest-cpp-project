#include "OperationLogger.hpp"

#include "ExpressionParser.hpp"

#include <exception>

int CalculatorService::evaluate(const std::string& expression) const {
    try {
        ExpressionParser parser;
        const int result = parser.evaluate(expression);
        logger_.logSuccess(expression, result);
        return result;
    } catch (const std::exception& exception) {
        logger_.logFailure(expression, exception.what());
        throw;
    }
}
