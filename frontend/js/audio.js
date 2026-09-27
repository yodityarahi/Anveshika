/**
 * Bharat Quest - Native Web Audio API Procedural Synthesizer
 * Zero external audio files required. Rich ancient ambient & game sound effects.
 */
class AncientAudioEngine {
  constructor() {
    this.ctx = null;
    this.muted = localStorage.getItem('bq_muted') === 'true';
  }

  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.ctx = new AudioContext();
      }
    }
  }

  resume() {
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  toggleMute() {
    this.muted = !this.muted;
    localStorage.setItem('bq_muted', this.muted);
    return this.muted;
  }

  // Tactile stone button click
  playClick() {
    if (this.muted) return;
    this.init();
    this.resume();
    if (!this.ctx) return;

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const now = this.ctx.currentTime;

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(320, now);
    osc.frequency.exponentialRampToValueAtTime(80, now + 0.08);

    gain.gain.setValueAtTime(0.15, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(now);
    osc.stop(now + 0.08);
  }

  // Golden discovery / artifact chime
  playChime() {
    if (this.muted) return;
    this.init();
    this.resume();
    if (!this.ctx) return;

    const freqs = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
    const now = this.ctx.currentTime;

    freqs.forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const start = now + idx * 0.06;

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, start);

      gain.gain.setValueAtTime(0.12, start);
      gain.gain.exponentialRampToValueAtTime(0.001, start + 0.45);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(start);
      osc.stop(start + 0.45);
    });
  }

  // Deep resonant ancient gong / entrance resonance
  playGong() {
    if (this.muted) return;
    this.init();
    this.resume();
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    const osc1 = this.ctx.createOscillator();
    const osc2 = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(146.83, now); // D3
    osc1.frequency.exponentialRampToValueAtTime(110.00, now + 1.2); // A2

    osc2.type = 'triangle';
    osc2.frequency.setValueAtTime(220.00, now); // A3
    osc2.frequency.exponentialRampToValueAtTime(164.81, now + 1.2); // E3

    gain.gain.setValueAtTime(0.25, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 1.4);

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(this.ctx.destination);

    osc1.start(now);
    osc2.start(now);
    osc1.stop(now + 1.4);
    osc2.stop(now + 1.4);
  }

  // Victorious Level-Up Fanfare
  playLevelUp() {
    if (this.muted) return;
    this.init();
    this.resume();
    if (!this.ctx) return;

    const notes = [
      { f: 392.00, d: 0.12 }, // G4
      { f: 523.25, d: 0.12 }, // C5
      { f: 659.25, d: 0.14 }, // E5
      { f: 783.99, d: 0.35 }  // G5 long
    ];
    let cur = this.ctx.currentTime;

    notes.forEach(note => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(note.f, cur);

      gain.gain.setValueAtTime(0.2, cur);
      gain.gain.exponentialRampToValueAtTime(0.001, cur + note.d);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(cur);
      osc.stop(cur + note.d);
      cur += note.d * 0.85;
    });
  }

  playFanfare() {
    this.playLevelUp();
  }
}

const audio = new AncientAudioEngine();
window.audio = audio;

