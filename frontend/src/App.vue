<template>
  <div class="app">
    <div class="container">
      <header class="header">
        <h1 class="title">📝 Internship Daily Diary Generator</h1>
        <p class="subtitle">Transform your raw work summary into professional diary entries</p>
      </header>

      <div class="input-section">
        <div class="input-group">
          <label for="summary">✍️ Enter your full day summary</label>
          <textarea
            id="summary"
            v-model="summary"
            placeholder="Paste your raw full-day work summary here..."
            class="summary-textarea"
            rows="8"
          ></textarea>
        </div>

        <div class="input-group">
          <label for="apiKey">🔑 OpenAI API Key (optional if set in .env)</label>
          <input
            type="password"
            id="apiKey"
            v-model="apiKey"
            placeholder="Leave empty if using .env file"
            class="api-input"
          />
        </div>

        <div class="button-group">
          <button
            @click="handleGenerate"
            :disabled="loading"
            class="btn btn-primary"
          >
            {{ loading ? '🔄 Generating...' : '🚀 Generate Diary Entry' }}
          </button>
          <button
            @click="handleClear"
            class="btn btn-secondary"
          >
            🗑️ Clear All
          </button>
        </div>
      </div>

      <div v-if="error" class="error-message">
        ⚠️ {{ error }}
      </div>

      <div v-if="result" class="result-section">
        <div class="result-header">
          <h2>✨ Generated Diary Entry</h2>
        </div>

        <div class="fields-section">
          <h3>📑 Individual Fields</h3>
          <div
            v-for="fieldName in fieldOrder"
            :key="fieldName"
            v-show="result.fields[fieldName] && (fieldName !== 'Skills' || result.fields[fieldName].trim())"
            class="field-card"
          >
            <div class="field-header">
              <h4>{{ fieldIcons[fieldName] || '📌' }} {{ fieldName }}</h4>
              <button
                @click="copyToClipboard(result.fields[fieldName], fieldName)"
                class="btn-copy"
              >
                {{ copiedField === fieldName ? '✅ Copied!' : '📋 Copy' }}
              </button>
            </div>
            <div class="field-content">
              <p v-for="(line, idx) in result.fields[fieldName].split('\n')" :key="idx">
                {{ line || '\u00A0' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      summary: '',
      apiKey: '',
      loading: false,
      result: null,
      error: null,
      copiedField: null,
      fieldIcons: {
        'Work Summary': '💼',
        'Learnings / Outcomes': '🎓',
        'Blockers / Risks': '⚠️',
        'Skills': '🛠️',
        'Reference Links': '🔗'
      },
      fieldOrder: ['Work Summary', 'Learnings / Outcomes', 'Blockers / Risks', 'Skills', 'Reference Links']
    }
  },
  methods: {
    async handleGenerate() {
      if (!this.summary.trim()) {
        this.error = 'Please enter your work summary'
        return
      }

      this.loading = true
      this.error = null
      this.result = null

     try {
      const base = process.env.VUE_APP_API_URL || ''
      const response = await axios.post(`${base}/api/generate`, {
      summary: this.summary,
      api_key: this.apiKey || undefined
      })
      this.result = response.data
      } catch (err) {
      this.error = err.response?.data?.error || 'An error occurred. Please try again.'
      } finally {
      this.loading = false
      }
    },
    handleClear() {
      this.summary = ''
      this.result = null
      this.error = null
      this.copiedField = null
    },
    async copyToClipboard(text, fieldName) {
      try {
        await navigator.clipboard.writeText(text)
        this.copiedField = fieldName
        setTimeout(() => {
          this.copiedField = null
        }, 2000)
      } catch (err) {
        // Fallback for older browsers
        const textarea = document.createElement('textarea')
        textarea.value = text
        textarea.style.position = 'fixed'
        textarea.style.opacity = '0'
        document.body.appendChild(textarea)
        textarea.select()
        document.execCommand('copy')
        document.body.removeChild(textarea)
        this.copiedField = fieldName
        setTimeout(() => {
          this.copiedField = null
        }, 2000)
      }
    }
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  padding: 2rem 1rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
  color: white;
}

.title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  font-weight: 300;
}

.input-section {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  margin-bottom: 2rem;
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 1rem;
}

.api-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.api-input:focus,
.summary-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.summary-textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  min-height: 200px;
  transition: all 0.3s ease;
}

.button-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 3.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
  border: 2px solid #e0e0e0;
}

.btn-secondary:hover {
  background: #e8e8e8;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 1rem 1.5rem;
  border-radius: 10px;
  margin-bottom: 2rem;
  border-left: 4px solid #c33;
  font-weight: 500;
}

.result-section {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  margin-top: 2rem;
}

.result-header {
  margin-bottom: 2rem;
}

.result-header h2 {
  color: #333;
  font-size: 2rem;
}

.fields-section {
  margin-top: 2rem;
}

.fields-section h3 {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.field-card {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 15px;
  border-left: 4px solid #667eea;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.field-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.field-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.field-header h4 {
  color: #333;
  font-size: 1.2rem;
  margin: 0;
}

.btn-copy {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.btn-copy:hover {
  background: #5568d3;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.field-content {
  color: #555;
  line-height: 1.8;
  font-size: 1rem;
  min-height: 250px;
  max-height: 800px;
  overflow-y: auto;
  padding: 1.5rem;
  background: #fafafa;
  border-radius: 8px;
}

.field-content p {
  margin: 0.75rem 0;
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .input-section,
  .result-section {
    padding: 1.5rem;
  }

  .button-group {
    grid-template-columns: 1fr;
  }

}
</style>

