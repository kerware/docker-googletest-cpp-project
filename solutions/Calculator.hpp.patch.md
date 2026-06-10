# Correction — `include/Calculator.hpp`

Ajouter la méthode :

```cpp
int modulo(int left, int right) const;
```

Version attendue :

```cpp
class Calculator {
public:
    int add(int left, int right) const;
    int subtract(int left, int right) const;
    int multiply(int left, int right) const;
    int divide(int left, int right) const;
    int modulo(int left, int right) const;
};
```
