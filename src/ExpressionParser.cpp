#include "ExpressionParser.hpp"

#include "Calculator.hpp"

#include <cctype>
#include <stdexcept>
#include <string>

namespace {
std::string removeSpaces(const std::string& input) {
    std::string output;
    for (const char character : input) {
        if (!std::isspace(static_cast<unsigned char>(character))) {
            output.push_back(character);
        }
    }
    return output;
}

int parseInteger(const std::string& value) {
    if (value.empty()) {
        throw std::invalid_argument("empty operand");
    }

    std::size_t parsed = 0;
    int result = 0;
    try {
        result = std::stoi(value, &parsed);
    } catch (const std::exception&) {
        throw std::invalid_argument("invalid integer: " + value);
    }

    if (parsed != value.size()) {
        throw std::invalid_argument("invalid integer: " + value);
    }
    return result;
}
} // namespace

int ExpressionParser::evaluate(const std::string& expression) const {
    const std::string compact = removeSpaces(expression);
    if (compact.empty()) {
        throw std::invalid_argument("empty expression");
    }

    std::size_t operatorPosition = std::string::npos;
    char op = '\0';

    for (std::size_t i = 1; i < compact.size(); ++i) {
        const char candidate = compact[i];
        if (candidate == '+' || candidate == '-' || candidate == '*' || candidate == '/') {
            operatorPosition = i;
            op = candidate;
            break;
        }
    }

    if (operatorPosition == std::string::npos) {
        throw std::invalid_argument("operator not found");
    }

    const int left = parseInteger(compact.substr(0, operatorPosition));
    const int right = parseInteger(compact.substr(operatorPosition + 1));

    Calculator calculator;
    switch (op) {
        case '+': return calculator.add(left, right);
        case '-': return calculator.subtract(left, right);
        case '*': return calculator.multiply(left, right);
        case '/': return calculator.divide(left, right);
        default: throw std::invalid_argument("unsupported operator");
    }
}
