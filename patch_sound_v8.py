snd = open('sound.py', encoding='utf-8').read()
head = snd.split('# cues')[0]
tail = '''# cues (match index.html v8; every time is in film seconds)
put(0.0, boom(), 0.9); put(0.0, swell(0.9, 700), 0.35)                       # 150 slam, dots light up
for b in range(1, 3): put(b * BEAT, thock(150 + b * 25), 0.4)
put(1.5, whoosh(1.0, 900), 0.5)                                               # ripple
for t in (2.8, 5.0, 8.6, 14.0, 16.0, 22.4, 26.5): put(t - 0.3, whoosh(0.5, 1000), 0.45); put(t, thock(130, 0.3), 0.55)   # cuts
for t in (4.6, 8.1, 13.6, 15.6, 22.0, 26.1): put(t, whoosh(0.8, 1300), 0.55)  # wipes
for k, t in enumerate((3.0, 3.3, 3.6)): put(t, thock(170 + k * 30), 0.5)       # problem cards
put(3.8, whoosh(0.4, 1100), 0.3)                                              # word swap
put(4.4, swell(0.6, 1200), 0.5); put(5.0, boom(), 0.8)                        # reveal
put(5.0, pad((130.81, 196, 261.63, 329.63), 3.0, a=0.15, fc=900), 0.7)
put(6.05, thock(240, 0.15), 0.45); put(6.25, thock(200, 0.2), 0.35)           # tap a person, the pill opens
put(7.35, thock(240, 0.15), 0.45); put(7.45, swell(0.5, 1000), 0.25)          # View, sheet slides up
put(8.95, swell(0.5, 900), 0.2)                                               # recording starts
put(12.2, thock(240, 0.15), 0.45); put(12.2, bloom(392, 1.3), 0.3); put(12.25, swell(0.5, 1500), 0.18)   # stop: timer done, check, confetti
put(12.4, thock(210, 0.18), 0.3); put(13.0, thock(210, 0.18), 0.35); put(13.0, bloom(329.63, 1.4), 0.25)  # processing, profile card
for i in range(11): put(14.1 + i * 0.1, whoosh(0.35, 1100), 0.16); put(14.38 + i * 0.1, thock(170 + i * 10, 0.18), 0.22)   # cards fly in from the edges
put(16.2, swell(0.6, 1000), 0.3); put(16.9, thock(170, 0.25), 0.4)             # profile sheet slides up, grows full screen
put(17.3, swell(1.6, 900), 0.22)                                              # profile scrolls
put(19.65, thock(240, 0.15), 0.45); put(19.75, bloom(392, 1.4), 0.25)          # tap play, playback starts
put(22.7, thock(240, 0.15), 0.45); put(22.9, thock(200, 0.2), 0.3)             # tap the ask bar, text box opens
for i in range(0, 45, 2): put(23.0 + i * 0.031, thock(300 + (i % 3) * 20, 0.05), 0.06)   # soft key taps while typing
put(24.5, thock(240, 0.15), 0.45); put(24.6, swell(0.8, 900), 0.28); put(24.7, thock(180, 0.25), 0.5)    # send, results
put(25.3, thock(240, 0.15), 0.45); put(25.5, thock(180, 0.25), 0.5)            # tap Draft a message, draft appears
put(26.5, boom(), 0.9); put(26.5, pad((130.81, 196, 261.63, 329.63), 3.8, a=0.3, fc=1000), 0.75); put(26.5, sub(65.41, 3.4), 0.5)
put(26.7, bloom(329.63, 1.4), 0.3); put(26.7, swell(0.8, 1300), 0.3)           # sparkle in
put(28.2, thock(240, 0.15), 0.4)                                              # last thumb tap
for k, t in enumerate((28.0, 28.4, 28.8)): put(t, thock(160 + k * 28, 0.22), 0.45)   # Capture. Ask. Act.
put(29.2, bloom(392, 1.2), 0.22)
out = out[:int(SR * DUR)]
out = lp(out, 7000, 2)
out *= np.minimum(1, (DUR - tt(DUR)[:len(out)]) / 1.2)
out = np.tanh(out * 1.1)
sf.write('out/audio.wav', out.astype(np.float32), SR)
f = np.abs(np.fft.rfft(out)); fr = np.fft.rfftfreq(len(out), 1 / SR)
print('spectral centroid Hz:', int((f * fr).sum() / f.sum()), '| energy above 2kHz: %.2f%%' % (100 * (f[fr > 2000] ** 2).sum() / (f ** 2).sum()))
'''
open('sound.py', 'w', encoding='utf-8').write(head + tail)
print('sound.py updated')
