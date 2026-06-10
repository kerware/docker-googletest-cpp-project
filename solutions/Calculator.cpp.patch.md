# Correction — `src/Calculator.cpp`

Ajouter :

```cpp
int Calculator::modulo(int left, int right) const {
    if (right == 0) {
        throw std::invalid_argument("modulo by zero");
    }
    return left % right;
}
```
