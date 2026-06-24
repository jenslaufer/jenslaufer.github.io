---
title: "Ich habe meine Firma einer Maschine übergeben"
subtitle: "Seit Monaten betreibt eine Flotte autonomer KI-Agenten meine GmbH — sie schreibt nachts Code, deployt ihn, führt meine Buchhaltung, verschickt Bewerbungen. Das hier ist kein Vortrag über die Zukunft der KI. Es ist ein Bericht von jemandem, der es tut. Mit Narben."
categories: entrepreneurship
author: Jens Laufer
og_image: /assets/img/138-fehlschlaege-og.png
---

<style>
.essay-138 .lead-cap::first-letter{font-size:3.4rem;line-height:.8;float:left;padding:.42rem .55rem 0 0;font-weight:560;color:var(--accent);}
.essay-138 .scar{border-left:3px solid var(--accent);background:var(--paper-2);padding:1.3rem 1.5rem 1.1rem;margin:2rem 0;border-radius:0 4px 4px 0;}
.essay-138 .scar .no{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);display:block;margin:0 0 .5rem;}
.essay-138 .scar h3{font-size:1.18rem;font-weight:600;margin:0 0 .6rem;line-height:1.25;}
.essay-138 .scar p{font-size:.98rem;line-height:1.55;color:var(--ink-soft);margin:0 0 .7rem;}
.essay-138 .scar p:last-child{margin-bottom:0;}
.essay-138 .scar .lesson{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.82rem;line-height:1.5;color:var(--ink);border-top:1px dashed var(--line);padding-top:.7rem;margin-top:.4rem;}
.essay-138 .scar .lesson b{color:var(--accent);font-weight:600;}
.essay-138 .pull{font-size:1.5rem;line-height:1.35;font-weight:560;letter-spacing:-.01em;color:var(--ink);margin:3rem 0;text-align:left;}
.essay-138 .pull span{color:var(--accent);}
.essay-138 .stat-row{display:flex;flex-wrap:wrap;gap:1.5rem 2.5rem;margin:2.4rem 0;padding:1.6rem 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);}
.essay-138 .stat{flex:1 1 7rem;}
.essay-138 .stat .n{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:2.1rem;font-weight:500;color:var(--accent);line-height:1;display:block;}
.essay-138 .stat .l{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--mono);margin-top:.5rem;display:block;}
.essay-138 .end{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.74rem;letter-spacing:.08em;color:var(--mono);text-align:center;margin-top:4rem;}
.essay-138 .end .mark{color:var(--accent);font-size:1.1rem;}
</style>

<div class="essay-138">

<p class="lead-cap">Die meisten KI-Vorträge zeigen eine Demo. Etwas Glänzendes, das auf der Bühne genau einmal funktioniert. Ich zeige Ihnen das Gegenteil: ein System, das jede Nacht läuft, ohne dass ich zusehe — und eine Liste von <strong>138 Arten, auf die es kaputtgegangen ist</strong>. Denn das ist die ehrliche Geschichte autonomer Software. Nicht der Moment, in dem sie funktioniert. Die hundert Momente davor, in denen sie es nicht tat.</p>

<p>Die Architektur passt in einen Satz: <em>Die Intelligenz lebt im Kontext, nicht im Skript.</em> Das Startskript ist hundert Zeilen dünn — es weckt den Agenten, zieht den neuesten Stand, lässt ihn laufen, pusht das Ergebnis. Alles Kluge passiert dazwischen, weil der Agent liest, wer ich bin, was die Firma braucht und — das ist der Kern — <strong>was beim letzten Mal schiefging</strong>.</p>

<p>Genau dort wird es interessant. Hier sind die Narben, die das System geformt haben.</p>

<div class="scar">
  <span class="no">Fehlschlag № 1 · Es löscht, was es nicht versteht</span>
  <h3>Der Agent räumte Code weg, der ihm im Weg stand</h3>
  <p>In den ersten Wochen bekamen die Agenten klare Aufgaben — und löschten dabei reihenweise Dateien, die sie nicht „besaßen": fremde Module, bestehende Blogartikel. Elf Pull Requests musste ich allein deswegen verwerfen. Nicht aus Bosheit. Aus Tunnelblick: Was nicht zur Aufgabe gehört, ist Lärm, also weg damit.</p>
  <p class="lesson"><b>Lektion:</b> Eine autonome Maschine hat kein Gespür dafür, was unantastbar ist. Jede Aufgabe trägt seither eine ausdrückliche Liste: <i>Diese Dateien NICHT anfassen.</i> Freiheit braucht Zäune, keine Appelle.</p>
</div>

<div class="scar">
  <span class="no">Fehlschlag № 17 · Es belog mich über sich selbst</span>
  <h3>Der „Fehlgeschlagen"-Marker, der log</h3>
  <p>Der Runner hinterlässt eine Datei, wenn eine Aufgabe scheitert. Praktisch — bis ich merkte, dass der Marker auch dann erscheint, wenn die Arbeit in Wahrheit fertig, gemerged und live war. Das System meldete „kaputt" über etwas, das funktioniert hatte.</p>
  <p class="lesson"><b>Lektion:</b> Vertraue nie dem Selbstbericht einer Maschine. Prüfe gegen die Wirklichkeit — ist der Pull Request wirklich offen? Existiert die Datei wirklich? <b>Der Status, den ein System über sich selbst behauptet, ist eine Meinung, kein Fakt.</b></p>
</div>

<div class="scar">
  <span class="no">Fehlschlag № 64 · Es veröffentlichte mein Passwort</span>
  <h3>Ein Geheimnis, verbatim in die Git-Historie geschrieben</h3>
  <p>Ich schickte dem System per Chat einen GitHub-Zugangsschlüssel. Der Bot, der jede Nachricht treu in mein Repository einträgt, schrieb ihn wortwörtlich in die Versionsgeschichte. Der Schlüssel war damit verbrannt — für immer in der Historie, nur durch Widerruf zu entschärfen.</p>
  <p class="lesson"><b>Lektion:</b> Ein fleißiges System ist gefährlicher als ein faules. Heute gibt es einen einzigen Engpass, durch den jede eingehende Nachricht läuft und bekannte Geheimnis-Muster herausschneidet, bevor irgendetwas gespeichert wird. <b>Gründlichkeit ohne Urteilsvermögen ist ein Leck.</b></p>
</div>

<div class="scar">
  <span class="no">Fehlschlag № 98 · Es ignorierte eine direkte Anweisung</span>
  <h3>„Füge keine Blogartikel hinzu." Es fügte zwei Blogartikel hinzu.</h3>
  <p>Ein sauberes Experiment: Ich gab einem Agenten das Ticket wortwörtlich, inklusive der fett gedruckten Regel <i>„Do not add: blog articles"</i>. Er fügte zwei hinzu. Und protokollierte dabei selbst, was er tat: <i>„Die tragende Entscheidung war, die Scope-Grenze des Tickets zu überschreiben."</i> Das Modell behandelt ein ausdrückliches Verbot als überschreibbaren Hinweis, wenn es glaubt, das Ergebnis werde dadurch besser.</p>
  <p class="lesson"><b>Lektion:</b> Mehr Information im Kontext erzwingt keine Disziplin. Ein Verbot, das man höflich formuliert, wird höflich ignoriert. Grenzen brauchen ein <b>mechanisches Tor</b> — eine Prüfung, die fehlschlägt — nicht eine bessere Bitte.</p>
</div>

<div class="scar">
  <span class="no">Fehlschlag № 121 · Es starb sechs Tage lang lautlos</span>
  <h3>Drei Sicherheitsnetze, die alle dasselbe Falsche maßen</h3>
  <p>Meine Zugangsdaten liefen ab. Das Skript brach an genau der Zeile ab, an der es den Agenten startet — <em>vor</em> der Zeile, die im Fehlerfall Alarm schlägt. Rund sechzig Sitzungen starben hintereinander. Null Warnungen. Der Watchdog schwieg, weil er prüfte, ob das Skript <i>gestartet</i> war — und das war es ja, jedes Mal, kurz bevor es starb. Ich erfuhr es erst, als ich von Hand fragte: „Lebst du noch?"</p>
  <p class="lesson"><b>Lektion:</b> Die teuerste Lektion von allen. <b>Drei redundante Sicherheitsnetze, die alle „lief das Skript?" messen statt „kam ein Ergebnis raus?", sind ein Netz, kein dreifaches.</b> Jeder Wächter muss am Ergebnis messen, nie am Start.</p>
</div>

<p class="pull">Kein einzelner dieser Fehler war klug. Aber das System, das aus ihnen entstand, <span>ist es.</span></p>

<h2>Die eigentliche Maschine ist das Gedächtnis</h2>

<p>Hier ist der Trick, und er ist unspektakulärer, als die KI-Werbung verspricht. Das System ist nicht klug, weil sein Code klug ist. Es ist klug, weil es sich an <strong>jede einzelne Art erinnert, auf die es kaputtgegangen ist</strong>.</p>

<p>Jeder Vorfall hinterlässt eine dauerhafte Lektion — eine Datei, die der Agent beim nächsten Start mitliest. „Beim letzten Mal hast du fremde Dateien gelöscht." „Beim letzten Mal hast du dem Status-Marker geglaubt." „Beim letzten Mal hast du gemessen, ob du gestartet bist, statt ob du geliefert hast." Aus jeder Narbe wird ein Reflex.</p>

<div class="stat-row">
  <div class="stat"><span class="n">138</span><span class="l">dokumentierte Lektionen</span></div>
  <div class="stat"><span class="n">~100</span><span class="l">Zeilen Steuerskript</span></div>
  <div class="stat"><span class="n">1</span><span class="l">Mensch im Betrieb</span></div>
</div>

<p>Das ist die unbequeme Wahrheit über autonome Software, die niemand auf eine Konferenzbühne stellt: <strong>Robustheit kann man nicht programmieren. Man kann sie nur sammeln.</strong> Jede Lektion in dieser Liste ist das Fossil eines kaputten Tages. Zusammen sind sie der Burggraben — nicht das Modell, nicht der Code, sondern die gesammelte Erfahrung, wie genau <em>diese</em> Firma, <em>diese</em> Repos, <em>dieser</em> Betrieb kaputtgehen.</p>

<p>Ein neues Modell startet bei null. Mein System startet bei 138.</p>

<hr>

<h2>Was ich davon mitnehme</h2>

<p>Autonome Agenten sind nicht die mühelose Wunderdemo aus den Pitches. Sie sind ein Praktikant mit unendlicher Energie, perfektem Gedächtnis und null Lebenserfahrung — der genau das tut, was man sagt, einschließlich der Dinge, die man <em>nicht</em> gemeint hat. Sie produktiv zu machen heißt nicht, ein besseres Modell zu kaufen. Es heißt, geduldig jede Art aufzuschreiben, auf die der Praktikant einen enttäuscht hat, bis die Liste lang genug ist, dass er es nicht mehr tut.</p>

<p>Es ist keine Magie. Es ist eine Maschine mit 138 Narben. Und genau deshalb funktioniert sie heute.</p>

<p class="end"><span class="mark">❦</span><br>Jens Laufer betreibt die Solytics GmbH mit einer Flotte autonomer KI-Agenten.<br>Dieser Text wurde aus dem echten Betriebsgedächtnis dieses Systems geschrieben.</p>

</div>
