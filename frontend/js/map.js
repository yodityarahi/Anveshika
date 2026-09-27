/**
 * Bharat Quest - Interactive Ancient India Map Controller
 * Phase 3: National Heritage Map with Unlocked Indus Valley Civilization
 */
class BharatMapController {
  constructor() {
    this.sites = {
      'mohenjo-daro': {
        name: 'Mohenjo-daro (Mound of the Dead)',
        region: 'Sindh (Indus River Basin)',
        importance: 'The Great Bath, Assembly Hall, and advanced corbelled subterranean drainage system.',
        artifacts: ['Pashupati Seal', 'The Dancing Girl', 'Priest-King Statuette']
      },
      'harappa': {
        name: 'Harappa (The Gateway City)',
        region: 'Punjab (Ravi River Basin)',
        importance: 'First excavated IVC metropolis; famed for Great Granaries, orthogonal grid streets, and terracotta workshops.',
        artifacts: ['Terracotta Bullock Cart', 'Red Sandstone Torso', 'Granary Storage Platforms']
      },
      'lothal': {
        name: 'Lothal (The Maritime Dockyard)',
        region: 'Gujarat (Gulf of Khambhat)',
        importance: "World's earliest known tidal dockyard connected to ancient Arabian Sea and Mesopotamian trade routes.",
        artifacts: ['Standardized Chert Weights', 'Bead Making Furnaces', 'Persian Gulf Button Seal']
      },
      'dholavira': {
        name: 'Dholavira (The Island City)',
        region: 'Kutch, Gujarat',
        importance: 'Sophisticated rock-cut water reservoirs, rainwater harvesting cascades, and the 10-symbol Indus Signboard.',
        artifacts: ['Giant Indus Signboard', 'Stone Pillar Bases', 'Terracotta Water Pipes']
      },
      'kalibangan': {
        name: 'Kalibangan (Black Bangles)',
        region: 'Rajasthan (Ghaggar-Hakra Basin)',
        importance: "World's earliest ploughed agricultural field furrows, sacrificial fire altars, and terracotta bangles.",
        artifacts: ['Fire Altars', 'Cylindrical Seal', 'Etched Carnelian Beads']
      },
      'rakhigarhi': {
        name: 'Rakhigarhi (The Mega Metropolis)',
        region: 'Haryana (Drishadvati Basin)',
        importance: 'Largest known IVC site spanning over 350 hectares, showcasing deep stratigraphy from early to mature Harappan phases.',
        artifacts: ['Lapis Lazuli Inlays', 'Gold Foil Ornaments', 'Burial Ceramic Sets']
      }
    };
  }

  init() {
    console.log("Initializing Interactive National Heritage Map...");
    this.bindEvents();
  }

  bindEvents() {
    const ivcRegion = document.getElementById('mapRegionIvc');
    if (ivcRegion) {
      ivcRegion.addEventListener('mouseenter', () => this.onHoverIvc());
      ivcRegion.addEventListener('mouseleave', () => this.resetHover());
      ivcRegion.addEventListener('click', () => this.selectCivilization('ivc'));
    }

    // Locked Regions
    const lockedRegions = document.querySelectorAll('.locked-region');
    lockedRegions.forEach(reg => {
      const civId = reg.getAttribute('data-civ-id');
      const name = reg.getAttribute('data-civ-name') || 'Ancient Era';
      reg.addEventListener('mouseenter', () => this.onHoverLocked(name));
      reg.addEventListener('mouseleave', () => this.resetHover());
      reg.addEventListener('click', () => this.selectLockedCivilization(name));
    });

    // Site Pins
    const pins = document.querySelectorAll('.site-pin');
    pins.forEach(pin => {
      const siteId = pin.getAttribute('data-site');
      pin.addEventListener('mouseenter', () => this.onHoverSite(siteId));
      pin.addEventListener('mouseleave', () => this.resetHover());
      pin.addEventListener('click', (e) => {
        e.stopPropagation();
        this.selectSite(siteId);
      });
    });
  }

  onHoverIvc() {
    if (window.audio) audio.playClick();
    const hoverCard = document.getElementById('mapHoverCard');
    if (!hoverCard) return;

    hoverCard.innerHTML = `
      <h4>🏛️ Indus Valley Civilization</h4>
      <p>Mature Harappan Phase (c. 2600–1900 BCE). Planned orthogonal streets, hydraulic drainage, and dockyards.</p>
      <span class="hover-hint">✨ CLICK TO ENTER CIVILIZATION & CITY</span>
    `;
    hoverCard.style.borderColor = 'var(--color-gold)';
  }

  onHoverLocked(civName) {
    const hoverCard = document.getElementById('mapHoverCard');
    if (!hoverCard) return;

    hoverCard.innerHTML = `
      <h4>🔒 ${civName}</h4>
      <p>Historical era documented for nationwide heritage scalability.</p>
      <span class="hover-hint" style="color: #E63946;">🔒 LOCKED • Focused prototype active in Indus Valley</span>
    `;
    hoverCard.style.borderColor = '#4A3A31';
  }

  onHoverSite(siteId) {
    if (window.audio) audio.playClick();
    const site = this.sites[siteId];
    const hoverCard = document.getElementById('mapHoverCard');
    if (!site || !hoverCard) return;

    hoverCard.innerHTML = `
      <h4>📍 ${site.name}</h4>
      <p>${site.importance}</p>
      <span class="hover-hint">✨ CLICK TO VIEW EXCAVATION DOSSIER</span>
    `;
    hoverCard.style.borderColor = 'var(--color-patina)';
  }

  resetHover() {
    const hoverCard = document.getElementById('mapHoverCard');
    if (!hoverCard) return;

    hoverCard.innerHTML = `
      <h4>🧭 National Heritage Exploration</h4>
      <p>Hover over geographical river basins to view ancient civilizations. The Indus Valley cradle is currently active.</p>
      <span class="hover-hint">SELECT THE GLOWING INDUS VALLEY REGION</span>
    `;
    hoverCard.style.borderColor = 'var(--border-gold)';
  }

  selectCivilization(civId) {
    if (civId === 'ivc') {
      if (window.audio) audio.playGong();
      if (window.storyController) {
        storyController.openStory(0);
      } else {
        this.openIvcIntroModal();
      }
    }
  }

  selectLockedCivilization(civName) {
    if (window.audio) audio.playClick();
    alert(`🔒 ${civName} is reserved for future expansion.\n\nFor this SIH prototype, explore the rich, interactive depth of the Indus Valley Civilization!`);
  }

  selectSite(siteId) {
    if (window.audio) audio.playChime();
    const site = this.sites[siteId];
    if (!site) return;
    this.openIvcIntroModal(site);
  }

  openIvcIntroModal(selectedSite = null) {
    const modal = document.getElementById('ivcIntroModal');
    if (!modal) return;

    const siteHighlight = document.getElementById('ivcSiteHighlightBox');
    if (selectedSite && siteHighlight) {
      siteHighlight.style.display = 'block';
      siteHighlight.innerHTML = `
        <div style="background: rgba(42, 157, 143, 0.15); border: 1px solid var(--color-patina); padding: 12px 16px; border-radius: 8px; margin-bottom: 16px;">
          <div style="font-size: 0.72rem; color: var(--color-patina); font-weight: 800; text-transform: uppercase;">Featured Excavation Site</div>
          <h4 style="font-family: var(--font-serif); color: #FFF; font-size: 1.1rem; margin: 2px 0;">${selectedSite.name}</h4>
          <p style="font-size: 0.8rem; color: #D6C7BC;">${selectedSite.importance}</p>
        </div>
      `;
    } else if (siteHighlight) {
      siteHighlight.style.display = 'none';
    }

    modal.classList.add('active');
  }

  closeIvcIntroModal() {
    const modal = document.getElementById('ivcIntroModal');
    if (modal) modal.classList.remove('active');
  }

  enterIvcCity() {
    if (window.audio) audio.playGong();
    this.closeIvcIntroModal();

    // Trigger visual journey transition to Ancient City tab
    if (window.app) {
      app.logConsole("🚀 Transitioning to Ancient Harappan City Explorer...");
      app.switchTab('tab-city');
    }
  }
}

const mapController = new BharatMapController();
window.mapController = mapController;