#include "ExpressionParser.hpp"

#include <exception>
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "Usage: calculator_cli \"2+3\"\n";
        return 2;
    }

    try {
        ExpressionParser parser;
        std::cout << parser.evaluate(argv[1]) << '\n';
        return 0;
    } catch (const std::exception& exception) {
        std::cerr << "Error: " << exception.what() << '\n';
        return 1;
    }
}
