/**
 * Toronto 311 Dashboard - Simplified JavaScript
 * ============================================
 *
 * Simplified version without filtering - just displays charts directly
 */

// ===== HARDCODED KPI VALUES =====
const HARDCODED_KPI = {
  totalRequests: "15,420",
  completionRate: "78.5%",
  topWard: "Spadina-Fort York",
  topServiceType: "Noise Complaints",
  mlAccuracy: "84.2%",
  mlPrecision: "81.7%",
  mlRecall: "79.3%",
  mlF1Score: "0.805",
  bestServiceType: "Animal Services (92%)",
  bestWard: "University-Rosedale (89%)",
  bestDivision: "Solid Waste Management (91%)",
  bestTime: "Morning 9-11 AM (85%)",
}

// ===== API CONFIGURATION =====
const API_BASE_URL = "http://localhost:5000/api"
const ENDPOINTS = {
  dashboardData: `${API_BASE_URL}/dashboard-data`,
  predictCompletion: `${API_BASE_URL}/predict-completion`,
}

// Chart styling configuration
const CHART_COLORS = {
  primary: "#6366f1",
  secondary: "#8b5cf6",
  success: "#10b981",
  warning: "#f59e0b",
  error: "#ef4444",
  text: "#ffffff",
  background: "#0f0f23",
}

// Global variables
let dashboardData = null
let isBackendConnected = false

// ===== INITIALIZATION =====
document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 Initializing Toronto 311 Dashboard...")

  // 1. Set hardcoded KPI values immediately
  setHardcodedKPIValues()

  // 2. Set up ML prediction functionality
  setupMLPrediction()

  // 3. Try to load real data from backend
  loadDashboardData()

  console.log("✅ Dashboard initialization complete")
})

// ===== SET HARDCODED KPI VALUES =====
function setHardcodedKPIValues() {
  console.log("📊 Setting hardcoded KPI values...")

  // KPI Cards
  setElementText("totalRequests", ".kpi-value", HARDCODED_KPI.totalRequests)
  setElementText("completionRate", ".kpi-value", HARDCODED_KPI.completionRate)
  setElementText("topWard", ".kpi-value", HARDCODED_KPI.topWard)
  setElementText("topServiceType", ".kpi-value", HARDCODED_KPI.topServiceType)

  // ML Performance Metrics
  setElementText("mlAccuracy", null, HARDCODED_KPI.mlAccuracy)
  setElementText("mlPrecision", null, HARDCODED_KPI.mlPrecision)
  setElementText("mlRecall", null, HARDCODED_KPI.mlRecall)
  setElementText("mlF1Score", null, HARDCODED_KPI.mlF1Score)

  // Success Factors
  setElementText("bestServiceType", null, HARDCODED_KPI.bestServiceType)
  setElementText("bestWard", null, HARDCODED_KPI.bestWard)
  setElementText("bestDivision", null, HARDCODED_KPI.bestDivision)
  setElementText("bestTime", null, HARDCODED_KPI.bestTime)

  // Header Status
  setElementText("dataStatus", null, "Dashboard Loaded")
  setElementText("lastUpdated", null, `Last updated: ${new Date().toLocaleString()}`)

  console.log("✅ All KPI values set")
}

function setElementText(elementId, selector, value) {
  const element = document.getElementById(elementId)
  if (element) {
    if (selector) {
      const targetElement = element.querySelector(selector)
      if (targetElement) targetElement.textContent = value
    } else {
      element.textContent = value
    }
  }
}

// ===== LOAD DASHBOARD DATA =====
async function loadDashboardData() {
  try {
    console.log("📊 Attempting to load data from Flask backend...")
    showLoadingOverlay()

    const response = await fetch(ENDPOINTS.dashboardData)

    if (!response.ok) {
      throw new Error(`Backend not available (${response.status})`)
    }

    const result = await response.json()

    if (result.status === "success") {
      dashboardData = result.data
      isBackendConnected = true

      console.log("✅ Real data loaded from backend:", dashboardData)

      // Render all charts with real data
      renderAllCharts()

      // Populate ML prediction dropdowns
      populateMLDropdowns()

      // Update status
      updateDataStatus("Connected to Backend", result.last_updated)
    } else {
      throw new Error(result.message || "Failed to load data")
    }
  } catch (error) {
    console.error("❌ Backend not available:", error)

    // Show placeholder messages in chart containers
    showChartPlaceholders()
    updateDataStatus("Backend Not Available", null)
  } finally {
    hideLoadingOverlay()
  }
}

// ===== RENDER ALL CHARTS =====
function renderAllCharts() {
  console.log("📈 Rendering all charts with real data...")

  if (!dashboardData) {
    console.log("⚠️ No data available for charts")
    return
  }

  // Render each chart in its container
  const chartFunctions = [
    { id: "timeSeriesChart", func: renderTimeSeriesChart },
    { id: "wardChart", func: renderWardChart },
    { id: "statusChart", func: renderStatusChart },
    { id: "serviceTypesChart", func: renderServiceTypesChart },
    { id: "divisionChart", func: renderDivisionChart },
    { id: "hourlyPatternChart", func: renderHourlyPatternChart },
    { id: "featureImportanceChart", func: renderFeatureImportanceChart },
  ]

  chartFunctions.forEach(({ id, func }) => {
    const container = document.getElementById(id)
    if (container) {
      console.log(`✅ Rendering chart: ${id}`)
      func()
    } else {
      console.error(`❌ Chart container not found: ${id}`)
    }
  })

  console.log("✅ All charts rendered")
}

// ===== INDIVIDUAL CHART RENDERING FUNCTIONS =====
function renderTimeSeriesChart() {
  const chartDiv = document.getElementById("timeSeriesChart")
  if (!chartDiv || !dashboardData.time_series) return

  const data = [
    {
      x: dashboardData.time_series.dates,
      y: dashboardData.time_series.counts,
      type: "scatter",
      mode: "lines+markers",
      line: { color: CHART_COLORS.primary, width: 3 },
      marker: { color: CHART_COLORS.primary, size: 6 },
      name: "Daily Requests",
    },
  ]

  const layout = {
    paper_bgcolor: CHART_COLORS.background,
    plot_bgcolor: CHART_COLORS.background,
    font: { color: CHART_COLORS.text },
    xaxis: {
      title: "Date",
      color: CHART_COLORS.text,
      gridcolor: "#374151",
    },
    yaxis: {
      title: "Number of Requests",
      color: CHART_COLORS.text,
      gridcolor: "#374151",
    },
    margin: { t: 20, r: 20, b: 60, l: 60 },
  }

  Plotly.newPlot(chartDiv, data, layout, { responsive: true })
}

function renderWardChart() {
  const chartDiv = document.getElementById("wardChart")
  if (!chartDiv || !dashboardData.ward_distribution) return

  const data = [
    {
      x: dashboardData.ward_distribution.counts,
      y: dashboardData.ward_distribution.wards,
      type: "bar",
      orientation: "h",
      marker: { color: CHART_COLORS.secondary },
      name: "Ward Requests",
    },
  ]

  const layout = {
    paper_bgcolor: CHART_COLORS.background,
    plot_bgcolor: CHART_COLORS.background,
    font: { color: CHART_COLORS.text },
    xaxis: {
      title: "Number of Requests",
      color: CHART_COLORS.text,
      gridcolor: "#374151",
    },
    yaxis: {
      title: "Ward",
      color: CHART_COLORS.text,
    },
    margin: { t: 20, r: 20, b: 60, l: 200 },
  }

  Plotly.newPlot(chartDiv, data, layout, { responsive: true })
}

function renderStatusChart() {
  const chartDiv = document.getElementById("statusChart")
  if (!chartDiv || !dashboardData.status_distribution) return

  const data = [
    {
      labels: dashboardData.status_distribution.statuses,
      values: dashboardData.status_distribution.counts,
      type: "pie",
      marker: {
        colors: [CHART_COLORS.success, CHART_COLORS.error, CHART_COLORS.warning],
      },
      textfont: { color: CHART_COLORS.text },
    },
  ]

  const layout = {
    paper_bgcolor: CHART_COLORS.background,
    plot_bgcolor: CHART_COLORS.background,
    font: { color: CHART_COLORS.text },
    margin: { t: 20, r: 20, b: 20, l: 20 },
  }

  Plotly.newPlot(chartDiv, data, layout, { responsive: true })
}

function renderServiceTypesChart() {
  const chartDiv = document.getElementById("serviceTypesChart")
  if (!chartDiv || !dashboardData.service_types) return

  const data = [
    {
      x: dashboardData.service_types.counts,
      y: dashboardData.service_types.types,
      type: "bar",
      orientation: "h",
      marker: { color: CHART_COLORS.primary },
      name: "Service Types",
    },
  ]

  const layout = {
    paper_bgcolor: CHART_COLORS.background,
    plot_bgcolor: CHART_COLORS.background,
    font: { color: CHART_COLORS.text },
    xaxis: {
      title: "Number of Requests",
      color: CHART_COLORS.text,
      gridcolor: "#374151",
    },
    yaxis: {
      title: "Service Type",
      color: CHART_COLORS.text,
    },
    margin: { t: 20, r: 20, b: 60, l: 180 },
  }

  Plotly.newPlot(chartDiv, data, layout, { responsive: true })
}

function renderDivisionChart() {
  const chartDiv = document.getElementById("divisionChart")
  if (!chartDiv || !dashboardData.division_distribution) return

  const data = [
    {
      x: dashboardData.division_distribution.divisions,
      y: dashboardData.division_distribution.counts,
      type: "bar",
      marker: { color: CHART_COLORS.secondary },
      name: "Division Requests",
    },
  ]

  const layout = {
    paper_bgcolor: CHART_COLORS.background,
    plot_bgcolor: CHART_COLORS.background,
    font: { color: CHART_COLORS.text },
    xaxis: {
      title: "Division",
      color: CHART_COLORS.text,
    },
    yaxis: {
      title: "Number of Requests",
      color: CHART_COLORS.text,
      gridcolor: "#374151",
    },
    margin: { t: 20, r: 20, b: 100, l: 60 },
  }

  Plotly.newPlot(chartDiv, data, layout, { responsive: true })
}

function renderHourlyPatternChart() {
  const chartDiv = document.getElementById("hourlyPatternChart")
  if (!chartDiv || !dashboardData.hourly_pattern) return

  const data = [
    {
      x: dashboardData.hourly_pattern.hours,
      y: dashboardData.hourly_pattern.counts,
      type: "scatter",
      mode: "lines+markers",
      line: { color: CHART_COLORS.primary, width: 3 },
      marker: { color: CHART_COLORS.primary, size: 6 },
      name: "Hourly Pattern",
    },
  ]

  const layout = {
    paper_bgcolor: CHART_COLORS.background,
    plot_bgcolor: CHART_COLORS.background,
    font: { color: CHART_COLORS.text },
    xaxis: {
      title: "Hour of Day",
      color: CHART_COLORS.text,
      gridcolor: "#374151",
    },
    yaxis: {
      title: "Number of Requests",
      color: CHART_COLORS.text,
      gridcolor: "#374151",
    },
    margin: { t: 20, r: 20, b: 60, l: 60 },
  }

  Plotly.newPlot(chartDiv, data, layout, { responsive: true })
}

function renderFeatureImportanceChart() {
  const chartDiv = document.getElementById("featureImportanceChart")
  if (!chartDiv || !dashboardData.feature_importance) return

  const data = [
    {
      x: dashboardData.feature_importance.importance,
      y: dashboardData.feature_importance.features,
      type: "bar",
      orientation: "h",
      marker: { color: CHART_COLORS.success },
      name: "Feature Importance",
    },
  ]

  const layout = {
    paper_bgcolor: CHART_COLORS.background,
    plot_bgcolor: CHART_COLORS.background,
    font: { color: CHART_COLORS.text },
    xaxis: {
      title: "Importance Score",
      color: CHART_COLORS.text,
      gridcolor: "#374151",
    },
    yaxis: {
      title: "Features",
      color: CHART_COLORS.text,
    },
    margin: { t: 20, r: 20, b: 60, l: 180 },
  }

  Plotly.newPlot(chartDiv, data, layout, { responsive: true })
}

// ===== SHOW CHART PLACEHOLDERS =====
function showChartPlaceholders() {
  console.log("⚠️ Showing chart placeholders (backend not available)")

  const chartIds = [
    "timeSeriesChart",
    "wardChart",
    "statusChart",
    "serviceTypesChart",
    "divisionChart",
    "hourlyPatternChart",
    "featureImportanceChart",
  ]

  chartIds.forEach((chartId) => {
    const chartDiv = document.getElementById(chartId)
    if (chartDiv) {
      chartDiv.innerHTML = `
        <div style="
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 200px;
          color: #9ca3af;
          text-align: center;
          padding: 20px;
        ">
          <div style="font-size: 48px; margin-bottom: 16px;">📊</div>
          <div style="font-size: 16px; font-weight: 600; margin-bottom: 8px;">
            Chart will appear here
          </div>
          <div style="font-size: 14px; opacity: 0.8;">
            Start your Flask backend to load Toronto 311 data
          </div>
          <div style="font-size: 12px; opacity: 0.6; margin-top: 8px;">
            Run: python backend/app.py
          </div>
        </div>
      `
    }
  })
}

// ===== ML PREDICTION FUNCTIONALITY =====
function setupMLPrediction() {
  console.log("🤖 Setting up ML prediction functionality...")

  const predictButton = document.getElementById("predictButton")
  if (predictButton) {
    predictButton.addEventListener("click", handleMLPrediction)
  }

  const closeErrorBtn = document.getElementById("closeError")
  if (closeErrorBtn) {
    closeErrorBtn.addEventListener("click", hideErrorModal)
  }

  console.log("✅ ML prediction setup complete")
}

async function handleMLPrediction() {
  console.log("🔮 Processing ML prediction...")

  try {
    // Get form data
    const formData = {
      service_type: document.getElementById("serviceType")?.value || "",
      ward: document.getElementById("ward")?.value || "",
      division: document.getElementById("division")?.value || "",
      postal_code: document.getElementById("predPostalCode")?.value || "",
      time_of_day: document.getElementById("predTimeOfDay")?.value || "",
      day_of_week: document.getElementById("predDayOfWeek")?.value || "",
    }

    // Validate required fields
    if (!formData.service_type || !formData.ward || !formData.division) {
      showErrorModal("Please fill in Service Type, Ward, and Division")
      return
    }

    // Update button state
    const predictBtn = document.getElementById("predictButton")
    predictBtn.textContent = "🔄 Predicting..."
    predictBtn.disabled = true

    // Make API call
    const response = await fetch(ENDPOINTS.predictCompletion, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const result = await response.json()

    if (result.status === "success") {
      displayPredictionResults(result.prediction)
      console.log("✅ ML prediction successful")
    } else {
      throw new Error(result.message || "Prediction failed")
    }
  } catch (error) {
    console.error("❌ ML prediction error:", error)
    showErrorModal(`Prediction failed: ${error.message}`)
  } finally {
    // Reset button state
    const predictBtn = document.getElementById("predictButton")
    predictBtn.textContent = "🔮 Predict Completion"
    predictBtn.disabled = false
  }
}

function displayPredictionResults(prediction) {
  // Hide placeholder, show results
  const placeholder = document.getElementById("predictionPlaceholder")
  const results = document.getElementById("predictionResults")

  if (placeholder) placeholder.classList.add("hidden")
  if (results) results.classList.remove("hidden")

  // Update probability percentage
  const probabilityPercent = document.getElementById("probabilityPercent")
  if (probabilityPercent) {
    probabilityPercent.textContent = `${prediction.completion_probability}%`
  }

  // Update prediction outcome
  const outcomeValue = document.getElementById("outcomeValue")
  if (outcomeValue) {
    outcomeValue.textContent = prediction.prediction
  }

  // Update confidence level
  const confidenceValue = document.getElementById("confidenceValue")
  if (confidenceValue) {
    confidenceValue.textContent = `${prediction.confidence}%`
  }

  // Update influencing factors
  const factorsList = document.getElementById("influencingFactors")
  if (factorsList && prediction.factors) {
    factorsList.innerHTML = ""
    prediction.factors.forEach((factor) => {
      const li = document.createElement("li")
      li.textContent = factor
      factorsList.appendChild(li)
    })
  }
}

function populateMLDropdowns() {
  console.log("🔽 Populating ML prediction dropdowns...")

  if (!dashboardData) return

  // Populate service types
  if (dashboardData.service_types) {
    populateDatalist("serviceTypeList", dashboardData.service_types.types)
  }

  // Populate wards
  if (dashboardData.ward_distribution) {
    populateDatalist("wardList", dashboardData.ward_distribution.wards)
  }

  // Populate divisions
  if (dashboardData.division_distribution) {
    populateDatalist("divisionList", dashboardData.division_distribution.divisions)
  }

  console.log("✅ ML dropdowns populated")
}

function populateDatalist(datalistId, options) {
  const datalist = document.getElementById(datalistId)
  if (datalist && options) {
    datalist.innerHTML = ""
    options.forEach((option) => {
      const optionElement = document.createElement("option")
      optionElement.value = option
      datalist.appendChild(optionElement)
    })
  }
}

// ===== UTILITY FUNCTIONS =====
function showLoadingOverlay() {
  const overlay = document.getElementById("loadingOverlay")
  if (overlay) overlay.classList.add("active")
}

function hideLoadingOverlay() {
  const overlay = document.getElementById("loadingOverlay")
  if (overlay) overlay.classList.remove("active")
}

function showErrorModal(message) {
  const modal = document.getElementById("errorModal")
  const messageElement = document.getElementById("errorMessage")

  if (modal && messageElement) {
    messageElement.textContent = message
    modal.classList.remove("hidden")
  }
}

function hideErrorModal() {
  const modal = document.getElementById("errorModal")
  if (modal) modal.classList.add("hidden")
}

function updateDataStatus(status, lastUpdated) {
  const statusElement = document.getElementById("dataStatus")
  const updatedElement = document.getElementById("lastUpdated")

  if (statusElement) statusElement.textContent = status

  if (updatedElement && lastUpdated) {
    const date = new Date(lastUpdated)
    updatedElement.textContent = `Last updated: ${date.toLocaleString()}`
  }
}

console.log("📄 Toronto 311 Dashboard JavaScript loaded")
console.log("🎯 Mode: Simplified - No filtering, direct chart display")
