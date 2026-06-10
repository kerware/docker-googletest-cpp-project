# Correction — `src/ExpressionParser.cpp`

Dans la détection d'opérateur, ajouter `%` :

```cpp
if (candidate == '+' || candidate == '-' || candidate == '*' || candidate == '/' || candidate == '%') {
```

Dans le `switch`, ajouter :

```cpp
case '%': return calculator.modulo(left, right);
```
