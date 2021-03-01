# DeviceMonitor

Biblioteka do monitorowania różnego rodzaju urządzeń.

Zadanie:
===

Zaprojektować i zaimplementować wraz z testami bibliotekę DeviceMonitor do monitorowania różnego rodzaju urządzeń.

Monitorowanie urządzeń ma polegać na możliwości ciągłego odczytania zdefiniowanej dla danego typu urządzenia listy parametrów.  
Zakładamy, że parametry urządzeń nie zmieniają się szybko (raz na kilka sekund) i nie ma potrzeby wykrywać wszystkich zmian tych parametrów a jedynie znać w miarę aktualną wartość parametrów.  
Możliwe typy parametrów to ```string```, ```int```, ```float```, ```bool```.  
Każde monitorowane urządzenie ma mieć przypisany identyfikator, z którym powiązane będą jego parametry.

**Przykład 1.**  
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

FAQ:
---

*"Każde monitorowane urządzenie ma mieć przypisany identyfikator, z którym powiązane będą jego parametry."*

**P:** W zadaniu, każde urządzenie posiada swój identyfikator, czy biblioteka ma go sama przypisać? Bo jeśli biblioteka sama przypisuje, to może być trudno później fizycznie zidentyfikować urządzenie, jeśli wymagałoby naprawy lub wymiany. W związku z tym, czy mogę założyć, że identyfikator urządzenia zawarty jest np. w nazwie pliku z odczytami parametrów danego urządzenia?

**O:** Można tak założyć. Można też skorzystać z jakiegoś dodatkowego pliku konfiguracyjnego który powiąże id ze ścieżką do pliku. Biblioteka sama w sobie nie powinna raczej nadawać id'ków.

*"Monitorowanie urządzeń ma polegać na możliwości ciągłego odczytania zdefiniowanej dla danego typu urządzenia listy parametrów."*

**P:** Czy biblioteka ma monitorować wszystkie parametry zawarte w pliku tekstowym, czy ma być możliwość zdefiniowania własnej listy tj. podzbioru dostępnych w pliku parametrów, które mają być monitorowane?

**O:** Zakładamy, że lista parametrów dla danego typu urządzenia jest statycznie zdefiniowana. Konkretnie, w przypadku symulowanego poprzez plik tekstowy urządzenia lista parametrów nie zależy od zawartość pliku. Jeżeli jakiegoś parametru nie ma w pliku to w rezultacie funkcji get_statuses wartość parametru powinna być None, a jeżeli są w pliku nieznane parametry to są one ignorowane.

*"Narzędzie powinno umożliwiać łatwe dodawanie nowych typów urządzeń. Istotne jest, aby dodanie obsługi nowego typu urządzenia nie wymagało zmian w kodzie samej biblioteki."*

**P:** Pytanie łączy się z poprzednim. Czy dodanie nowego typu ma polegać na dodaniu do listy monitorowanych urządzeń konkretnego "urządzenia" (wraz z jego identyfikatorem, listą parametrów oraz ścieżką do pliku z którego odczytywane są parametry)?

**O:** Plik tekstowy z parametrami dotyczy wyłącznie urządzenia symulowanego (czyli jednego z wielu typów urządzeń). Dodanie nowego typu urządzenia oznacza, że np. będzie można odczytywać parametry z pralki automatycznej poprzez protokół MQTT. Chodzi o to, żeby dodanie obsługi takiego nowego typu urządzenia było proste z punktu widzenia programisty. Poza tym można założyć, że lista urządzeń do monitorowania jest zdefiniowana w momencie uruchamiania programu i nie zmienia się w trakcie jego działania, ale na tej liście mogą się znajdować urządzenia różnego typu.

**P:** Co to jest 'typ urządzenia'?

**O:** Typ urządzenia jest zdefiniowany poprzez zestaw jego parametrów do monitorowania oraz sposób w jakim można się z nim komunikować. Przykładowo może to być zasilacz CCR z którym komunikujemy się po magistrali RS485 i protokołem JBUS. Może to być moduł monitorowania sygnałów logicznych z którym komunikujemy się poprzez MODBUS TCP. Biblioteka DeviceMonitor ma być elementem pośredniczącym pomiędzy dowolnym urządzeniem który chcemy monitorować a jakimś systemem prezentującym wartości monitorowanych parametrów. Typ urządzania, które symulujemy poprzez plik tekstowy jest wyłącznie przykładem implementacji jednego z wielu możliwych typów urządzenia. Jego celem jest wyłącznie zaprezentowanie działania samej biblioteki DeviceMonitor.

Rozwiązanie:
===
Repozytorium zawiera bibliotekę do monitorowania różnego rodzaju urządzeń.

Instalacja:
---
Zainstaluj używając programu ```pip```:  
```
pip install git+git://github.com/darkroom2/DeviceMonitor.git
```

Użycie:
---
```python
import devicemonitorlib as dm

# Lista urzadzen do monitorowania.
device_list = [
   DeviceByFile('1', ['current', 'voltage', 'pressure'], './devices/zasilacz_00001.json'),
   DeviceByFile('2', ['current', 'voltage'], './devices/zasilacz_00002.json'),
   DeviceByFile('3', ['current', 'voltage'], './devices/zasilacz_00003.json'),
   DeviceByHTTP('4', ['current', 'voltage', 'pressure'], '127.0.0.1', 6666),
]

# Jak czesto odswiezac parametry urzadzen
update_interval = 1

dm.start(update_interval, device_list)
result = dm.get_statuses()
dm.stop()
```
Wynik jest w formacie słownika, gdzie kluczami są identyfikary urządzeń, a wartościami słownik z parametrami.
```python
{
    '1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None},
    '2': {'output_current': 0.6, 'output_voltage': 449},
    '3': {'output_current': 0.4, 'output_voltage': 451}
}
```

Uwaga 1: ```device_list``` jest listą urządzeń, które mają być monitorowane. Elementami listy, powinny być obiekty posiadające atrybuty ```id``` i ```param_list``` oraz metodę ```data()```, która powinna zwracać ```string``` w formacie JSON, zawierający parametry urządzenia. Atrybut ```id``` to identyfikator urządzenia, natomiast ```param_list``` jest listą parametrów, które mają być monitorowane.  
Uwaga 2: ```update_interval``` to czas (w sekundach), co jaki ma następować odświeżanie (pobieranie) parametrów urządzeń.

Testowanie:
---
Kod biblioteki jest pokryty testami jednostkowymi. Testy znajdują się w folderze ```tests/```.

W repozytorium dostępny jest skrypt testowy ```test.py``` prezentujący działanie biblioteki. W folderze ```devices/``` znajdują się pliki tekstowe symulujące urządzenia.

Aby uruchomić skrypt testowy, należy sklonować repozytorium:  
```bash
git clone https://github.com/darkroom2/DeviceMonitor.git
```
Następnie przejść do folderu biblioteki i uruchomić skrypt ```test.py```:
```bash
cd DeviceMonitor/
```
```bash
python test.py
```
W wyniku na konsoli wypisane zostają komunikaty, takie jak:
```text
Main thread is starting the DeviceMonitor...
DeviceMonitor started successfully!
Main thread is creating a new thread with scheduler that periodically calls the get_statuses() method...
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
Thread with print scheduler started successfully!
Main thread sleeping for 5 secs while other thread prints...
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
Main thread calling get_statuses()...
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
Main thread called get_statuses() successfully!
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
Changing device parameter in file zasilacz_00001.json...
Changed voltage from 450 to 666!
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 666, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 666, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 666, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 666, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
Reverting device parameter changes...
Reverted voltage from 666 to 450!
{'1': {'output_current': 0.5, 'output_voltage': 666, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
{'1': {'output_current': 0.5, 'output_voltage': 450, 'output_pressure': None}, '2': {'output_current': 0.6, 'output_voltage': 449}, '3': {'output_current': 0.4, 'output_voltage': 451}}
Main thread stops the DeviceMonitor...
Main thread stopped the DeviceMoniotor successfully!
None
None
None
None
Main thread stops the printer thread...
Printer thread stopped successfully!
Main thread is ending...
```

TODO:
---
* ???
