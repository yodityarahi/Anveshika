/**
 * Bharat Quest - Centralized API Service Wrapper
 */
class ApiService {
  constructor(baseUrl = '') {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };

    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers
      }
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP Error ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (err) {
      console.error(`API Error on [${options.method || 'GET'} ${endpoint}]:`, err);
      throw err;
    }
  }

  // Health Check
  async getHealth() {
    return this.request('/api/health');
  }

  // Auth & Profile
  async register(userData) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
  }

  async login(credentials) {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    });
  }

  async getProfile(username) {
    return this.request(`/api/user/profile/${encodeURIComponent(username)}`);
  }

  async updateProfile(username, data) {
    return this.request(`/api/user/profile/${encodeURIComponent(username)}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async awardProgress(username, data) {
    return this.request(`/api/user/profile/${encodeURIComponent(username)}/award`, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // Civilization & Locations
  async getCivilizations() {
    return this.request('/api/ivc/civilizations');
  }

  async getIvcOverview() {
    return this.request('/api/ivc/overview');
  }

  async getIvcStory() {
    return this.request('/api/ivc/story');
  }

  async getLocations() {
    return this.request('/api/ivc/locations');
  }

  // Quests
  async getQuests(civilizationId = 'ivc', username = null) {
    let url = `/api/quests?civilization_id=${encodeURIComponent(civilizationId)}`;
    if (username) url += `&username=${encodeURIComponent(username)}`;
    return this.request(url);
  }

  async getQuestDetail(questId) {
    return this.request(`/api/quests/${encodeURIComponent(questId)}`);
  }

  async submitQuest(questId, username, submission) {
    return this.request(`/api/quests/${encodeURIComponent(questId)}/submit`, {
      method: 'POST',
      body: JSON.stringify({
        username: username,
        submission: submission
      })
    });
  }

  // Museum Artifacts
  async getMuseumArtifacts(username = null, civilizationId = 'ivc') {
    let url = `/api/museum/artifacts?civilization_id=${encodeURIComponent(civilizationId)}`;
    if (username) url += `&username=${encodeURIComponent(username)}`;
    return this.request(url);
  }

  async getArtifactDetail(artifactId, username = null) {
    let url = `/api/museum/artifacts/${encodeURIComponent(artifactId)}`;
    if (username) url += `?username=${encodeURIComponent(username)}`;
    return this.request(url);
  }

  async discoverArtifact(artifactId, username) {
    return this.request(`/api/museum/discover/${encodeURIComponent(artifactId)}`, {
      method: 'POST',
      body: JSON.stringify({ username: username })
    });
  }

  // AI / ML Personalization Engine (Phase 9)
  async getAiDashboard(username) {
    return this.request(`/api/ai/dashboard/${encodeURIComponent(username)}`);
  }

  async getAiRecommendations(username) {
    return this.request(`/api/ai/recommendations/${encodeURIComponent(username)}`);
  }

  async getAiDifficulty(username) {
    return this.request(`/api/ai/difficulty/${encodeURIComponent(username)}`);
  }

  async getAiLearningProgress(username) {
    return this.request(`/api/ai/learning-progress/${encodeURIComponent(username)}`);
  }

  async simulateAiPersonalization(params) {
    return this.request('/api/ai/simulate', {
      method: 'POST',
      body: JSON.stringify(params)
    });
  }

  // Gamification & Progression (Phase 8)
  async getGamificationStatus(username) {
    return this.request(`/api/gamification/status/${encodeURIComponent(username)}`);
  }

  async exploreLocation(username, locationId) {
    return this.request('/api/gamification/explore-location', {
      method: 'POST',
      body: JSON.stringify({
        username: username,
        location_id: locationId
      })
    });
  }

  async evaluateBadges(username) {
    return this.request(`/api/gamification/evaluate/${encodeURIComponent(username)}`, {
      method: 'POST'
    });
  }

  async getAllBadges() {
    return this.request('/api/gamification/badges');
  }

  async getAllLevels() {
    return this.request('/api/gamification/levels');
  }

  async getSecretArchive() {
    return this.request('/api/gamification/lore/secret-archive');
  }

  // Final Challenge (Phase 10)
  async getFinalChallengeContent() {
    return this.request('/api/final-challenge/content');
  }

  async submitFinalChallenge(username, decisions) {
    return this.request('/api/final-challenge/submit', {
      method: 'POST',
      body: JSON.stringify({
        username: username,
        decisions: decisions
      })
    });
  }

  async getFinalChallengeStatus(username) {
    return this.request(`/api/final-challenge/status/${encodeURIComponent(username)}`);
  }

  // Heritage Guide Chatbot
  async chatHeritageGuide(message, username = 'Arjun') {
    return this.request('/api/ai/heritage-guide/chat', {
      method: 'POST',
      body: JSON.stringify({
        message: message,
        username: username
      })
    });
  }
}

const api = new ApiService();
window.api = api;