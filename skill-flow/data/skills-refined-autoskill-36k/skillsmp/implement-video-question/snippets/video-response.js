/**
 * Video Response Question Pattern
 *
 * Complete pattern for questions where students watch a video and provide
 * a written response/explanation.
 *
 * Dependencies: Assumes createVideoPlayer() and createExplanationCard()
 * are available in the global scope (inline them into chart.js)
 */

/**
 * Creates a complete video response question layout
 *
 * @param {Object} d3 - D3.js instance
 * @param {Object} container - D3 selection of container element
 * @param {Object} config - Configuration object
 * @param {string} config.videoUrl - URL to the video file (MP4, WebM)
 * @param {string} config.videoDescription - Description text shown above video
 * @param {string} config.promptText - Question/prompt for the response
 * @param {string} config.placeholderText - Placeholder text for textarea
 * @param {number} [config.responseRows=6] - Number of rows for textarea
 * @param {string} config.stateKey - Key in chartState to store response (e.g., "explanation")
 * @param {boolean} config.locked - Whether interactivity is locked
 * @param {string} [config.introTitle] - Optional intro card title
 * @param {string} [config.introContent] - Optional intro card content
 * @returns {Object} - Object with textarea reference for state restoration
 */
function createVideoResponseQuestion(d3, container, config) {
  const {
    videoUrl,
    videoDescription,
    promptText,
    placeholderText = "Type your answer here...",
    responseRows = 6,
    stateKey,
    locked,
    introTitle = null,
    introContent = null
  } = config;

  // Optional intro card
  if (introTitle || introContent) {
    const introCard = createStandardCard(d3, container, {
      size: "large",
      title: introTitle || ""
    });

    if (introContent) {
      introCard.append("p").text(introContent);
    }
  }

  // Video player
  createVideoPlayer(d3, container, videoUrl, {
    description: videoDescription,
    autoplay: false,
    controls: true
  });

  // Response card
  const responseCard = createExplanationCard(d3, container, {
    prompt: promptText,
    placeholder: placeholderText,
    value: chartState[stateKey] || "",
    onChange: (value) => {
      chartState[stateKey] = value;
      sendChartState();
    },
    locked: locked,
    rows: responseRows
  });

  return {
    // Return textarea for state restoration if needed
    updateResponse: (value) => {
      // This is handled by createExplanationCard internally
      // But expose if manual updates are needed
      chartState[stateKey] = value;
    }
  };
}

/**
 * Example usage pattern for chart.js:
 *
 * // 1. Define state
 * function createDefaultState() {
 *   return {
 *     explanation: ""
 *   };
 * }
 *
 * // 2. Build layout
 * function buildLayout(d3, containerSelector) {
 *   const container = d3.select(containerSelector);
 *   container.html("").style("padding", "20px").style("overflow", "auto");
 *
 *   createVideoResponseQuestion(d3, container, {
 *     videoUrl: "https://example.com/video.mp4",
 *     videoDescription: "Watch this explanation of proportional relationships",
 *     promptText: "What is the main concept explained in the video?",
 *     placeholderText: "Describe the main concept in your own words...",
 *     responseRows: 6,
 *     stateKey: "explanation",
 *     locked: interactivityLocked,
 *     introTitle: "Video Reflection",
 *     introContent: "Watch the video carefully and answer the question below."
 *   });
 * }
 *
 * // 3. State restoration (if needed beyond createExplanationCard's internal handling)
 * function applyInitialState(state) {
 *   Object.assign(chartState, state);
 *   buildLayout(d3, containerSelector);
 * }
 *
 * // 4. Interactivity control
 * function setInteractivity(enabled) {
 *   interactivityLocked = !enabled;
 *   buildLayout(d3, containerSelector);
 * }
 */

/**
 * Multi-question variation:
 *
 * function buildLayout(d3, containerSelector) {
 *   const container = d3.select(containerSelector);
 *   container.html("").style("padding", "20px").style("overflow", "auto");
 *
 *   // Intro
 *   const introCard = createStandardCard(d3, container, {
 *     size: "large",
 *     title: "Video Reflection"
 *   });
 *   introCard.append("p").text("Watch the video and answer the questions below.");
 *
 *   // Video
 *   createVideoPlayer(d3, container, "https://example.com/video.mp4", {
 *     description: "Proportional relationships explained"
 *   });
 *
 *   // Multiple response cards
 *   const questions = [
 *     { prompt: "1. What is the main concept?", key: "response1" },
 *     { prompt: "2. How does this relate to what you know?", key: "response2" },
 *     { prompt: "3. Give an example from real life.", key: "response3" }
 *   ];
 *
 *   questions.forEach(q => {
 *     createExplanationCard(d3, container, {
 *       prompt: q.prompt,
 *       value: chartState[q.key] || "",
 *       onChange: (value) => {
 *         chartState[q.key] = value;
 *         sendChartState();
 *       },
 *       locked: interactivityLocked,
 *       rows: 4
 *     });
 *   });
 * }
 */
