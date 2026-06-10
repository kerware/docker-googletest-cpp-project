#include "Calculator.hpp"

int Calculator::add(int left, int right) const {
    return left + right;
}

int Calculator::subtract(int left, int right) const {
    return left - right;
}

int Calculator::multiply(int left, int right) const {
    return left * right;
}

int Calculator::divide(int left, int right) const {
    if (right == 0) {
        throw std::invalid_argument("division by zero");
    }
    return left / right;
}
