Projekt przestawia ukazanie działania algorytmów planowania oraz algorytmów zastępowania stron. 

W pliku GUI.py znajduje się interfejs graficzny, w którym można wybrać sobie algorytm i potem zobaczyć jego symulacje. 

W pliku input.txt znajdują się dane wejściowe dla algorytmów planowania: 
- 1 linijka to czas przybycia (arrival time)
- 2 linijka to czas wykonywania (execution time)
- 3 linijka to priorytet (im niższy priorytet, tym proces jest ważniejszy)
- 4 linijka to quant dla algorytmów priorytetowych (po jakim czasie oczekiwania należy priorytet obniżyć)
- 5 linijka to ziarno dla algorytmu Round Robin

W pliku input_replacement.txt znajdują się dane wejściowe dla algorytmów zastępowania stron:
- 1 linijka to wszystkie numery stron
- 2 linijka to długość ramki

Z widoku GUI mamy do wyboru algorytmy planowania:
- FCFS (First-Come-First-Serve):
    FCFS jest prostym algorytmem planowania, w którym procesy są obsługiwane w kolejności ich przyjścia. Pierwszy proces, który przybył, jest pierwszy do obsługi. Jest to non-preemptive, co oznacza, że procesy nie      są   przerywane, dopóki nie zakończą swojego wykonania.
- FCFS z priorytetem (First-Come-First-Serve z priorytetem):
  Jest to rozszerzenie FCFS, które uwzględnia priorytety procesów. Procesy są obsługiwane zgodnie z ich priorytetem, ale nadal stosuje się zasadę FCFS, jeśli mają taki sam priorytet.
 - SJF (Shortest Job First):
  SJF to algorytm planowania, w którym proces z najkrótszym czasem wykonania jest wybierany do obsługi jako pierwszy. Moja wersja to wersja non-preemptive czyli proces czeka, aż zakończy się przed przejściem do       następnego.

(W plikach typu FCFS_algorithm.py itd. znajdują się dokładnie zaprogramowane te algorytmy, natomiast w GUI tylko jest już wygląd, wszelkie dane były generowane w tamtym pliku)

Z widoku GUI mamy także do wyboru algorytmy zastępowania stron:
 - FIFO (First-In-First-Out):
  FIFO to prosty algorytm zastępowania stron, w którym najstarsza strona (najwcześniej załadowana) jest usuwana, gdy konieczne jest przydzielanie nowej strony. Jest to non-preemptive, co oznacza, że strona nie      zostanie zastąpiona, jeśli nadal jest używana.

 - OPT (Optimal):
  OPT to idealny, teoretyczny algorytm zastępowania stron, który zawsze usuwa tę stronę, która nie będzie używana najdłuższy czas w przyszłości. Niestety, jest to algorytm niemożliwy do zaimplementowania w       
  praktyce, ponieważ wymaga znajomości przyszłego używania stron.

 - LRU (Least Recently Used):
  LRU to algorytm, który usuwa stronę, która nie była używana od najdłuższego czasu. W przypadku jego implementacji konieczne jest śledzenie czasu ostatniego użycia dla każdej strony.

 - LFU (Least Frequently Used):
  LFU to algorytm, który usuwa stronę, która była używana najrzadziej. Wymaga śledzenia liczby użycia każdej strony.


**W folderze dist znajduje się wersja .exe tego GUI, która przedstawia dokładnie ukazane symulacje**
