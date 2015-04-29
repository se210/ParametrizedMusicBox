import midi
import re

tracks = [1,2]
pattern = midi.read_midifile("Smbtheme.mid")
start = 0
end = 11.4

# inverse mapping
valToNote = {v: k for k, v in midi.NOTE_NAME_MAP_FLAT.items()}
pattern.make_ticks_abs();

msecPerTick = (60000 / (pattern[0][1].get_bpm() * pattern.resolution))

startTick = (start * 1000) / msecPerTick
endTick = (end * 1000) / msecPerTick

notes = set()

# determine notes

for t in tracks:
	for e in pattern[t]:
		if (e.tick < startTick):
			continue
		elif (e.tick > endTick):
			break
		try:
			notes.add(valToNote[e.get_pitch()])
		except:
			continue

formatNotes = ""
notemap = {}
index = 0
for n in notes:
	if (len(n) == 3):
		formatNotes = formatNotes + re.sub('[\_]'," ", n)
	elif (len(n) == 4):
		formatNotes = formatNotes + re.sub('[\_]', "", n)
	notemap[n] = index
	index = index + 1

#determine sequence

combinedNotes = {}
for t in tracks:
	for e in pattern[t]:
		if (e.tick < startTick):
			continue
		elif (e.tick > endTick):
			break
		if (e.name == "Note On"):
			if (e.tick in combinedNotes):
				combinedNotes[e.tick].append(e)
			else:
				combinedNotes[e.tick] = [e]

noteString = ""
for time in combinedNotes:
	row = ['o'] * len(notes)
	for e in combinedNotes[time]:
		loc = notemap[valToNote[e.get_pitch()]]
		row[loc] = 'X'
	noteString = noteString + ''.join(row)

print formatNotes
print len(notes)
print noteString
print len(noteString) / len(notes)