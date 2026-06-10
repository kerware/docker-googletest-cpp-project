#include "ExpressionParser.hpp"

#include <gtest/gtest.h>
#include <cctype>
#include <string>

struct ExpressionCase {
    std::string expression;
    int expected;
};

class ExpressionParameterizedTest : public ::testing::TestWithParam<ExpressionCase> {};

TEST_P(ExpressionParameterizedTest, EvaluatesExpression) {
    ExpressionParser parser;
    const auto& param = GetParam();

    EXPECT_EQ(parser.evaluate(param.expression), param.expected);
}

std::string PrintExpressionCase(const ::testing::TestParamInfo<ExpressionCase>& info) {
    std::string name = info.param.expression;
    for (char& character : name) {
        if (!std::isalnum(static_cast<unsigned char>(character))) {
            character = '_';
        }
    }
    return "expr_" + name;
}

INSTANTIATE_TEST_SUITE_P(
    NominalExpressions,
    ExpressionParameterizedTest,
    ::testing::Values(
        ExpressionCase{"1+2", 3},
        ExpressionCase{"10-4", 6},
        ExpressionCase{"6*7", 42},
        ExpressionCase{"20/5", 4},
        ExpressionCase{"-8/2", -4}),
    PrintExpressionCase);
