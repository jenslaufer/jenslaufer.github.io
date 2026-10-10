---
title: "Legacy-Systeme mit KI-Agenten neu bauen: Verifikation, die mit einem betrügenden Agenten rechnet"
subtitle: "Agenten lassen Anforderungen weg und arbeiten an den Tests. Was Studien beim Neubau von Legacy-Systemen gemessen haben und welches Verifikationsdesign daraus folgt."
tags: Legacy-Systeme, KI-Agenten, Verifikation, Testen
categories: software
layout: post
language: de
author: Jens Laufer
og_image: /assets/img/legacy-systeme-ki-agenten-og.png
---

*English version: [Rebuilding Legacy Systems with AI Agents](/software/rebuilding-legacy-systems-with-ai-agents.html)*

Für meine eigene Firma läuft jeden Tag eine autonome Coding-Pipeline. Agenten holen sich Tickets, setzen sie auf einem Branch um, und getrennte Tests entscheiden, ob das Ergebnis hält. [138 Arten, auf die dieses System kaputtging](/entrepreneurship/138-fehlschlaege.html), habe ich aufgeschrieben. Eine davon: Im Ticket stand fett „Do not add: blog articles". Der Agent fügte zwei Blogartikel hinzu und protokollierte, er habe entschieden, die Scope-Grenze des Tickets zu überschreiben.

Das ist ein kleines System. Mich interessierte, was passiert, wenn Agenten ein großes Legacy-System neu bauen, etwa ein ERP, eine Abrechnungsplattform oder ein Kernsystem einer Versicherung. Ein solches Projekt habe ich nicht geleitet. Aus den Studien habe ich eine Methode entworfen. Danach recherchierte ein KI-Rechercheagent, der meinen Entwurf nicht kannte, die aktuelle Praxis, und ein dritter Agent verglich beides. Dieser Artikel fasst zusammen, was die Belege sagen und welches Verifikationsdesign daraus folgt.

### Agenten lassen eher weg, als dass sie erfinden

Ein Neubau beginnt damit, herauszufinden, was das alte System tut. LLMs lesen Code gut. Es liegt nahe, sie die Anforderungen schreiben zu lassen.

[UCRBench](https://arxiv.org/abs/2512.13360) hat genau das gemessen: 9 Java-Projekte mit bis zu rund 66.000 Zeilen und 556 Use Cases. Die Modelle übersahen 26–43 % der Use Cases auf Subfunktions-Ebene und 44–65 % auf Ebene der Nutzerziele. Am schwächsten waren sie bei fachspezifischen Systemen mit vielen Modulen. Ein großes Legacy-System ist meist weit größer als 66.000 Zeilen und auf viele Module verteilt.

In einer [Fallstudie von 2026](https://arxiv.org/abs/2608.28972) migrierte Claude Code 12 Features eines VB6-ERP nach C#. Das Verhalten stimmte bei einfachen Features zu 92 % mit dem Altsystem überein, bei mittleren zu 81 %, bei komplexen zu 47 %. Komplex waren nur zwei Features, die letzte Zahl steht also auf dünner Basis. Das Abstract nennt 70 %, gewichtet nach Anweisungen; ungewichtet über die Features liegen die Mittelwerte bei 84 % für Persistenz, 76 % für Geschäftsregeln und 80 % gesamt. Klarer als die Mittelwerte sind die Fehlerzahlen: 42 fehlende Nachbarmodule, 22 fehlende Datenbankoperationen, 20 fehlende Regeln, 10 fehlende Modulintegrationen, 6 falsche Implementierungen. Validierungen in UI-Events, implizite Filter und globale Konfiguration beschreibt das Paper, weist sie aber nicht gesondert aus.

94 der 100 gezählten Fehler sind etwas, das fehlt; 6 sind falsche Implementierungen. Der vorhandene Code wirkt vollständig, und wer ihn reviewt, sieht nicht, was fehlt. Auslassungen findet man nur, wenn man den Recall gegen eine Menge misst, die ohne das Modell entstanden ist.

### Agenten arbeiten an den Tests

Danach muss der Neubau beweisen, dass er sich wie das Altsystem verhält. Die übliche Antwort sind Tests. Die Belege zeigen: Der Agent optimiert auch gegen die Tests.

[ImpossibleBench](https://arxiv.org/abs/2510.20270) baut Aufgaben, deren Tests der Spezifikation widersprechen. Jeder grüne Test ist dort Betrug. In den beiden SWE-bench-Varianten betrog GPT-5 bei 76 % und 54 % der Aufgaben (bei LiveCodeBench unter 3 %). Claude Opus 4.1 betrog bei rund 50 % der widersprüchlichen Variante, und das unter einem strengen Prompt. Claude-Modelle und Qwen3-Coder betrogen überwiegend, indem sie Tests änderten (mehr als 79 %, eine Untergrenze). Weitere Strategien: Sonderfälle für Testeingaben, überladene Vergleichsoperatoren, Zustand zwischen Aufrufen.

Die Gegenmaßnahmen halfen nur teilweise. Schreibgeschützte Tests stoppten die Teständerungen, aber nicht die Sonderfälle. Versteckte Tests drückten den Betrug fast auf null und verschlechterten zugleich die ehrlichen Lösungen. LLM-Monitore erkannten 86–89 % des Betrugs bei einfachen Aufgaben und 42–65 % bei Aufgaben im Stil von SWE-bench.

Auch ehrlich bestandene Tests sagen weniger, als sie scheinen. Bei [METR](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) prüften vier Maintainer von scikit-learn, Sphinx und pytest 296 Agenten-PRs, die die Tests von SWE-bench Verified bestanden hatten. Bereinigt um die Quote, mit der Maintainer die Referenzlösung mergen, lag die Merge-Rate rund 24 Punkte unter der Bestehensquote. Grenzen: ein Versuch pro Aufgabe, keine Iteration mit Feedback, drei Repositories. [UTBoost](https://arxiv.org/abs/2506.09289) fand 345 falsche Patches, die das ursprüngliche SWE-bench als bestanden wertete. [SWE-ABS](https://icml.cc/virtual/2026/poster/62669) stuft etwa jeden fünften „gelösten" Patch der besten Agenten als inhaltlich falsch ein.

Lässt man ein Modell die Sollwerte schreiben, schreibt es auf, was der Code heute tut. Eine [Studie über 24 Java-Repositories](https://arxiv.org/abs/2410.21136) zeigt: LLM-generierte Testorakel halten das tatsächliche statt des erwarteten Verhaltens fest, in manchen Konstellationen mit weniger als 50 % Genauigkeit. Im Neubau würden die Tests des Agenten den Code des Agenten bestätigen.

Meine eigene Lehre aus dem Blogartikel-Ticket deckt sich damit. Eine Regel, die der Agent liest, ist eine Bitte. Eine Grenze braucht eine Prüfung, die fehlschlägt.

### Ein Testdesign, das mit Betrug rechnet

Die Verifikation der Methode geht von zwei Annahmen aus: Der bauende Agent nimmt jede Abkürzung, die der Aufbau zulässt. Und er übersieht Dinge, ohne es zu merken. Jedes Element beantwortet einen der Befunde oben.

1. Das Altsystem ist die Quelle der Spezifikation. Steht die Entscheidung für den Neubau, liest man den alten Code daraufhin, was er berechnet. Deterministische Werkzeuge listen Einstiegspunkte, Tabellen, Batch-Jobs und Konfiguration auf. Das LLM fasst jeweils einen Ausschnitt des Codes zusammen und belegt jeden Satz mit einer Codestelle. Aufrufketten über die ganze Codebasis verfolgt es nie.
2. Sollwerte stammen nur aus aufgezeichnetem Verhalten des Altsystems. Ein Harness spielt jeden Fall auf dem Altsystem mit anonymisierten Produktionsdaten ab und speichert Eingaben und Ausgaben. Kein Modell schreibt oder ändert einen Sollwert. Für neu gestaltete Prozesse gibt es kein Altsystem als Orakel. Dort rechnen Fachexperten die Sollwerte von Hand aus, Invarianten wie „Salden gleichen sich aus" decken den Rest ab.
3. Aufzeichnungen sind unveränderlich. Die Rohaufzeichnung liegt unverändert mit Inhalts-Hash ab. Flüchtige Felder wie Zeitstempel normalisieren Regeln, die ein Mensch freigibt und Code anwendet. Felder mit rechtlicher Bedeutung, etwa lückenlose Belegnummern, bleiben. Jeder Fall läuft zweimal; ein abweichendes Ergebnis zeigt verborgenen Zustand außerhalb der aufgezeichneten Grenze.
4. Ein einziger datengetriebener Runner, der einem Menschen gehört. Er liest die Falldateien, lädt die Eingaben, führt den Prozess aus und vergleicht die Ausgaben exakt. Für die Äquivalenz gibt es keinen Testcode pro Fall. Von Agenten geschriebene Vergleicher bekommen gern stille Toleranzen.
5. Zurückgehaltene Fälle. Einen Teil der Fälle pro Prozess sieht der bauende Agent nie. ImpossibleBench zeigt, dass komplett versteckte Tests ehrliche Arbeit verschlechtern. Ein zurückgehaltener Anteil lässt sichtbare Fälle für die Entwicklung übrig und fängt Überanpassung an sie ab. Ich würde mit 20–30 % beginnen. Das ist eine Setzung, keine Messung.
6. Geschützte Pfade. Runner, Vergleicher, Fälle, Normalisierungsregeln, Fixtures und CI-Konfiguration sind über CODEOWNERS und einen CI-Check geschützt. Jeder Diff des bauenden Agenten dort lässt den Build scheitern.
7. Mechanische Prüfungen gegen Sonderfälle. Schreibschutz verhindert keine Sonderfälle. Deshalb durchsucht der Build den Produktivcode nach Literalen aus sichtbaren Fällen, nach überschriebenen Gleichheits- oder Vergleichsoperatoren und nach Zustand zwischen Aufrufen. Agenten-Transkripte bleiben für Audits erhalten. Gegen einen Monitor würde ich die Agenten nicht optimieren: [OpenAI fand](https://arxiv.org/abs/2503.11926), dass starke Optimierung gegen Chain-of-Thought-Überwachung Modellen beibringt, ihre Absicht zu verbergen. Ein Reviewer-Agent auf Basis eines ähnlichen Modells ist kein guter Ersatz, denn [Modellfehler korrelieren](https://arxiv.org/abs/2502.04313).
8. Recall messen. Pro Domäne entsteht von Hand ein Goldstandard aus Prozessen und Regeln. Gemessen wird, was der extrahierte Katalog davon verpasst hat. Eine reine Fehlerquote sieht Auslassungen nie.
9. Merge-Rate. Ein Reviewer zieht pro Welle eine Stichprobe von Agenten-Änderungen und entscheidet, ob er jede unverändert mergen würde. Diesen Anteil verfolgt man neben der Bestehensquote.

Zwei Ergänzungen folgen aus denselben Studien. Bei komplexen Features fiel die Übereinstimmung auf 47 %, also zerlegt man komplexe Prozesse vor dem Bau in kleinere Einheiten. Und aufgezeichnete Fälle können Zweige verfehlen. Der [Locksmith-Loop-Preprint](https://arxiv.org/abs/2607.28271) ließ COBOL und generiertes Java nebeneinander laufen und suchte gezielt Eingaben für nicht abgedeckte Zweige. Er erreichte 91,9 % Zweigabdeckung bei einem internen Programm. Blinde Flecken laut den Autoren: Zwischenzustände und Rundung bei Gleitkommazahlen.

### Was die Belege nicht abdecken

Die Recherche, auf die ich mich stütze, fand keinen veröffentlichten Fall, in dem Agenten ein System in der Größe großer Unternehmenssysteme vollständig neu gebaut haben. Das Design oben ist aus Teilbelegen zusammengesetzt: ein Benchmark auf Projekten bis 66.000 Zeilen, eine Fallstudie mit 12 Features, SWE-bench-Studien auf Python-Bibliotheken. Das METR-Ergebnis ist an großen Geschäftsanwendungen nicht geprüft.

So wie ich die Quellen lese, gibt es gut gemessene Erfolge vor allem bei mechanischen Migrationen wie Java-Upgrades oder dem Wechsel eines Test-Frameworks. Ergebnisse zum Neubau von Geschäftslogik stammen überwiegend von Anbietern, ohne unabhängige Vergleichsbasis. Auch die mechanischen Zahlen sind oft Schätzungen: Google meldet [rund 50 % Zeitersparnis](https://arxiv.org/abs/2501.06972) für eine einzelne Migration, die Umstellung von IDs von int32 auf int64, als Einschätzung der Entwickler.

Automatisierungsquote ist nicht Zeitersparnis. [Slacks Werkzeug](https://slack.engineering/balancing-old-tricks-with-new-feats-ai-powered-conversion-from-enzyme-to-react-testing-library-at-slack/) konvertierte in einer Stichprobe rund 80 % des Testcodes korrekt; das Team schätzt die eingesparte Entwicklerzeit auf 22 %. In einer [Studie von METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) waren erfahrene Entwickler mit Werkzeugen von Anfang 2025 19 % langsamer und hielten sich für 20 % schneller. Durchlaufzeiten muss man messen; eine Umfrage im Team liefert die falsche Zahl.

Außerdem verschieben sich die Ergebnisse mit jeder Modellgeneration. Die Betrugsquoten in ImpossibleBench hängen vom Modell und vom Prompt ab.

### Das Programm drumherum

Ob ein Neubau gelingt, entscheidet die Verifikation nicht allein. [Der Bericht des externen Prüfers zum Oracle-Go-live des Birmingham City Council](https://www.birmingham.gov.uk/download/downloads/id/30136/public_interest_report_-_erp_implementation_2025.pdf) nennt die Ursachen dort: schwache Governance, fehlende eigene Fachkräfte, Abhängigkeit von Dienstleistern, eine rote Risikobewertung und Bedenken, die ungehört blieben, sowie Testberichte, die in den Schlagzeilen zu positiv waren. Kostenüberschreitungen in [5.392 IT-Projekten](https://arxiv.org/abs/2210.01573) folgen einem Potenzgesetz; kleine, umkehrbare Schritte schlagen einen großen Plan. Die geschäftliche Seite behandle ich in einem [eigenen Artikel auf solytics.de](https://solytics.de/blog/altsoftware-mit-ki-agenten-neu-bauen/).

Müsste ich einen solchen Neubau beginnen, wäre das erste Ergebnis der Aufzeichnungs-Harness samt Runner, in der Hand eines Menschen, bevor ein Agent Schreibzugriff auf Produktivcode bekommt.
