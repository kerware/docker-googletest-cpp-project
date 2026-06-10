#include "ExpressionParser.hpp"

#include <gtest/gtest.h>
#include <stdexcept>

TEST(ExpressionParserTest, EvaluatesAdditionExpression) {
    ExpressionParser parser;
    EXPECT_EQ(parser.evaluate("2+3"), 5);
}

TEST(ExpressionParserTest, IgnoresSpaces) {
    ExpressionParser parser;
    EXPECT_EQ(parser.evaluate(" 12 / 3 "), 4);
}

TEST(ExpressionParserTest, HandlesNegativeLeftOperand) {
    ExpressionParser parser;
    EXPECT_EQ(parser.evaluate("-8/2"), -4);
}

TEST(ExpressionParserTest, RejectsUnknownExpression) {
    ExpressionParser parser;
    EXPECT_THROW(static_cast<void>(parser.evaluate("abc")), std::invalid_argument);
}
