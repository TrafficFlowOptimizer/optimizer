# TrafficFlowOptimizer - moduł Optymalizator

## Opis
Moduł jest częścią odpowiedzialną za wyznaczanie optymalnych cykli świateł.\
Wykorzystuje on program napisany w języku MiniZinc, z wykorzystaniem solvera [CBC](https://github.com/coin-or/Cbc), zaś w przypadku gdy jest on niedostępny, wykorzystuje domyślny solver [Gecode](https://www.gecode.org/).


## Jak uruchomić moduł

Optymalizator można uruchomić na dwa sposoby.
Zalecanym sposobem jest uruchomienie lokalnie, jednak w razie problemów możliwe jest również wykorzystanie Dockera

### Lokalnie

* katalog projektu należy otworzyć w ulubionym IDE (przykładowo PyCharm)
* uruchomić [aplikację](python/Server.py) z konfiguracją używającą zmiennych z pliku [.env](.env) (w Idea można użyć do tego [plugin](https://plugins.jetbrains.com/plugin/7861-envfile)) 

### Za pomocą Dockera

* uruchomić Dockera
* w katalogu projektu: `docker compose up`

## Dokumentacja

* [MiniZinc](https://reactjs.org/](https://www.minizinc.org/)https://www.minizinc.org/).
