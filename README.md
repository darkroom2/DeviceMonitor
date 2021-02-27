# DeviceMonitor

Biblioteka do monitorowania różnego rodzaju urządzeń.

Zadanie:
---

Zaprojektować i zaimplementować wraz z testami bibliotekę DeviceMonitor do monitorowania różnego rodzaju urządzeń.

Monitorowanie urządzeń ma polegać na możliwości ciągłego odczytania zdefiniowanej dla danego typu urządzenia listy parametrów.  
Zakładamy, że parametry urządzeń nie zmieniają się szybko (raz na kilka sekund) i nie ma potrzeby wykrywać wszystkich zmian tych parametrów a jedynie znać w miarę aktualną wartość parametrów.  
Możliwe typy parametrów to ```string```, ```int```, ```float```, ```bool```.  
Każde monitorowane urządzenie ma mieć przypisany identyfikator, z którym powiązane będą jego parametry.

__Przykład 1.__  
Jest dany typ zasilacza lamp lotniskowych który umożliwia odczytanie aktualnego prądu wyjściowego oraz napięcia wyjściowego.
Zakładając, że są trzy zasilacze do monitorowania a ich identyfikatory to ```{1, 2, 3}```, DeviceMonitor powinien umożliwiać
pobranie aktualnych wartości prądu i napięcia wyjściowego ze wszystkich zasilaczy w postaci:
```python
{
  '1': {'output_current': 0.5, 'output_voltage': 450},
  '2': {'output_current': 0.6, 'output_voltage': 449},
  '3': {'output_current': 0.4, 'output_voltage': 451}
}
```

Należy również dostarczyć przykładową implementację dla urządzenia symulowanego poprzez plik tekstowy (jeden plik dla jednego urządzenia).
W pliku tekstowym w postaci JSON będą umieszczone parametry urządzenia wraz z jego parametrami, np.:
```json
{
  "voltage": 666,
  "current": 4
}
```
Zmiana wartości parametrów powinna być możliwa w trakcie działania programu i odzwierciedlana w wartości zwracanej przez metodę ```get_statuses()```.

1. Narzędzie powinno dostarczać następujący interfejs api:
    * metoda ```start()``` - uruchamia DeviceMonitor w oddzielnym wątku
    * metoda ```stop()``` - zatrzymuje wątek DeviceMonitor
    * metoda ```get_statuses()``` - zwraca słownik z monitorowanymi urządzeniami (jak w przykładzie 1)
    

2. Metody ```start()```, ```stop()```, ```get_statuses()``` powinny być thread-safe, w szczególności metody ```start()``` i ```stop()``` wołane będą z głównego wątku aplikacji używającej DeviceMonitor a metoda ```get_statuses()``` może być wywoływana z dowolnego innego wątku aplikacji.
   

3. Narzędzie powinno umożliwiać łatwe dodawanie nowych typów urządzeń. Istotne jest, aby dodanie obsługi nowego typu urządzenia nie wymagało zmian w kodzie samej biblioteki.
   

4. Wymagane jest dostarczenie testowego skryptu używającego biblioteki DeviceMonitor wraz z symulowanym urządzeniem który będzie wypisywał co sekundę parametry tego urządzenia.
   

5. Kod powinien być w 100% pokryty testami jednostkowymi.


Odpowiadając na pytania:
1) można tak założyć. Można też skorzystać z jakiegoś dodatkowego pliku konfiguracyjnego który powiąże id ze ścieżką do pliku. Biblioteka sama w sobie nie powinna raczej nadawać id'ków.
2) Zakładamy że lista parameterów dla danego typu urządzenia jest statycznie zdefiniowana. Konkretnie, w przypadku symulowanego poprzez plik tekstowy urządzenia lista parameterów nie zależy od zawartość pliku. Jeżeli jakiegoś parameteru nie ma w pliku to w rezultacie funkcji get_statuses wartość parametru powinna być None, a jeżeli są w pliku nieznane parametry to są one ignorowane.
3) Plik tesktowy z parameterami dotyczy tylko i wyłącznie urządzenia symulowanego (czyli jednego z wielu typów urządzeń). Dodanie nowego typu urządzenia oznacza, że np. będzie można odczytywać parametery z pralki automatycznej poprzez protokół MQTT. Chodzi o to, żeby dodanie obsługi takiego nowego typu urządzenia było proste z punktu widzenia programisty. Po za tym można założyć że lista urządzeń do monitorowania jest zdefiniowana w momencie uruchamiania programu i nie zmienia się w trakcie jego działania, ale na tej liście mogą się znajdowąć urządzenia różnego typu. 

Typ urządzenia jest zdefiniowany poprzez zestaw jego parameterów do monitorowania oraz sposób w jakim można się z nim komunikować. Przykładowo może to być zasilacz CCR z którym komunikujemy się po magistrali RS485 i protokołem JBUS. Może to być moduł monitorowania sygnałów logicznych z którym komunikujemy się poprzez MODBUS TCP. Biblioteka DeviceMonitor ma być elementem pośredniczącym pomiędzy dowolnym urządzeniem który chcemy monitorować a jakimś systemem prezentujacym wartości monitorowanych parameterów.

Typ urządzania które symulujemy poprzez plik tekstowy jest tylko i wyłącznie przykładem implementacji jednego z wielu możliwych typów urządzenia. Jego celem jest tylko i wyłącznie zaprezentowanie działania samej biblioteki DeviceMonitor.