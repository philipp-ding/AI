# Replication of the Weizenbaums ELIZA Chatbot

## Abstract
App can be found here:
https://philipp-ding-ai-deploy-elisa-on-streamlit-ni7sei.streamlit.app/

## Table of Contents
**[Einführung](##Einführung)**<br>
**[Kernkonzepte von ELIZA](##Kernkonzepte-von-ELIZA[^1])**<br>
**[Erste Implementierung](##Erste-Implementierung)**<br>
**[Implementierung eines UI](##Implementierung-eines-UI)**<br>

## Einführung
ELIZA ist ein 1966 von Josef Weizenbaum vorgestellter Chatbot[^1], der Im Originalskript einen Psychotherapeut nach Rogers imitiert. Ziel ist es anhand geschickter Umformulierungen der Benutzereingabe den Menschen - meist anhand von Frage - zum Nachdenken zu bewegen und ihn somit auf den Grund seiner Gefühlslage zu führen.

## Kernkonzepte von ELIZA[^1]
Die Umsetzung von ELIZA basiert auf den folgenden fünf Kernpunkten:
1. Identifizierung von Key-words: Mithilfe eines Scans der Benutzereingabe von links nach rechts werden zuerst bestimmte vorher definierte Schlüsselwörter gesucht. An Satzzeichen wird die Benutzereingabe getrennt und zuerst der erste Bestandteil nach Schlüsselwörtern überprüft. Ziel ist es, das wichtigste key-word zu finden und mit diesem bestimmte Transformationsregeln durchzuführen.
2. Herausfinden des minimalen Kontexts: Hierbei geht es darum, einen groben Überblick über den Kontext vor allem in Bezug auf Personalpronomen zu bekommen. Beispielsweise soll der Satz "It seems to me that you're mad" aus Nutzerperspektive von ELIZA zu "It seems to you that I'm mad" umgewandelt werden.
3. Transformationsregeln: Bei der Transformationsregel geht es darum den Satz die Nutzereingabe anhand von auf den Key-words definierten Regeln in eine Ausgabe umzuformen. Falls "seems" im vorherigen Beispiel als keyword gelistet wäre und eine Transformationsregel dazu "It seems to me (0)" --> "Why do you think (0)?" ist, lautet der vorherige Satz folglich: "Why do you think, that I'm mad?".
4. Generierung von Antworten ohne keywords: Damit laufend eine Konversation gestaltet werden kann muss ELIZA ebenfalls dazu in der Lage sein Standartantworten zu generieren, falls in der Nutzereingabe keine Schlüsselwörter vorhanden sind. Ein Beispiel könnte "Please go on" sein oder "Why (0)", wobei 0 die gesamte Benutzereingabe nach Transformation des minimalen Kontext darstellt.  
5. Editierbarkeit: Bei der Editierbarkeit geht es vor allem darum, dass unterschiedliche Skripte in Bezug auf die Transformationsregeln möglich sind. Dies kann damit erreicht werden, dass die Transformationsregeln in einer externen Datei liegen und in das Programm bei Beginn geladen werden. Somit müssen für einen neuen Anwendungsfall nur die Transformationsregeln geändert werden und nicht das Programm.

## Erste Implementierung
Nach einer Studie des Original-Papers und dem Verstehen des Workflows erfolgte eine erste Implementierung. Aufwendig und repetitiv bei ELIZA ist vor allem das Erstellen der unterschiedlichen Transformationsregeln. Dies kann einem aber wie in meinem Fall durch neuere Chatbots abgenommen werden (Stichwort ChatGPT - die Zusammenfassung des Chatverlaufs befindet sich ebenfalls im Repo: TODO Link einfügen). Mithilfe einiger Fragen, Ausbesserung einiger kleiner Fehler und leichter Verbesserungen steht so auch schon die erste Version 0.1 unseres ELIZA-chatbots. 
Die Konversation kann über die cmd und den Aufruf des Skripts erfolgen oder durch Starten des Skriptes in einer Programmierumgebung. Für die bisher sehr rudimentären Regeln und die wenigen Zeilen an Code stellt sich das Programm ganz geschickt an und die Kommunikation wirkt echt/ macht bereits Spaß (TODO: Formulierung.)

Durch das Einlesen der externen Python Skripte mit den Transformationsregeln ist die Editierbarkeit (Umsetzung von Kernkonzept: 5) und erste Transformationsregeln (3) gegeben. Standartantworten sind ebenfalls vorhanden, falls keine dieser Transformationsregeln zutrifft (4). Der minimale Kontext wird über ein Dictionary gemapped und erkannt (2). Bei den Key-Words (1) gibt es aktuell noch kleine Unterschiede zum Original. Hierbei sind die Key-Words noch nicht mit einer Bewertung zur Wichtigkeit versehen, sondern lediglich die Reihenfolge innerhalbe der Liste bestimmt, welche Transformationsregel angewendet wird. Außerdem ist das Anwendung in der Konsole aktuell noch nicht sehr benutzerfreundlich. Diese Punkte sollen im Folgenden ausgeglichen werden.

## Implementierung eines UI
Die Implementierung einer einfach Chat-Webapp findet mit dem Frameworks Streamlit statt. Dies ermöglicht mithilfe von Python Skripten grafische Benutzeroberflächen zu implementieren und über die Streamlit-Community-Cloud direkt zu deployen [^2]. Die App kann [hier](https://philipp-ding-ai-deploy-elisa-on-streamlit-ni7sei.streamlit.app/) getestet werden.

[^1]: https://doi.org/10.1145/365153.365168
[^2]: https://www.bigdata-insider.de/was-ist-streamlit-a-974962/
