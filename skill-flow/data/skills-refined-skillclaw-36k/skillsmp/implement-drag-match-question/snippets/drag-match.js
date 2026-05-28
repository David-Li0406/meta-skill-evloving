/**
 * Drag and Match Component (Standalone)
 *
 * Creates a drag-and-drop matching interface with draggable items and drop zones.
 *
 * Usage in chart.html:
 *   <script src="/podsie-curriculum/components/drag-match.standalone.js"></script>
 *
 * Then in chart.js:
 *   const matcher = createDragMatcher(d3, container, {
 *     items: [{ id: "item1", content: <renderFunction> }, ...],
 *     categories: [{ id: "cat1", label: "Category 1" }, ...],
 *     state: { cat1: ["item1"], cat2: [] },
 *     onStateChange: (newState) => { ... },
 *     locked: false
 *   });
 */

(function (global) {
  "use strict";

  /**
   * Creates a drag-and-drop matching interface
   * @param {object} d3 - D3 instance
   * @param {object} container - D3 selection to append to
   * @param {object} options - Configuration options
   * @returns {object} Matcher API with update methods
   */
  function createDragMatcher(d3, container, options) {
    options = options || {};

    const items = options.items || [];
    const categories = options.categories || [];
    const initialState = options.state || {};
    const onStateChange = options.onStateChange || function () {};
    const locked = options.locked || false;
    const instruction = options.instruction || "Drag items to match them with categories:";

    let draggedItemId = null;
    let currentState = { ...initialState };

    // Main card container
    const mainCard = container
      .append("div")
      .attr("class", "drag-match-container")
      .style("background", "#ffffff")
      .style("border", "1px solid #e5e7eb")
      .style("border-radius", "16px")
      .style("padding", "24px")
      .style("box-shadow", "0 6px 16px rgba(15,23,42,0.05)")
      .style("margin-bottom", "32px");

    // Instruction text
    if (instruction) {
      mainCard
        .append("div")
        .attr("class", "instruction-text")
        .style("font-size", "16px")
        .style("font-weight", "600")
        .style("color", "#6b7280")
        .style("margin-bottom", "24px")
        .text(instruction);
    }

    // Two-column layout
    const twoColumnContainer = mainCard
      .append("div")
      .attr("class", "two-column-layout")
      .style("display", "grid")
      .style("grid-template-columns", "1fr 1fr")
      .style("gap", "32px");

    const leftColumn = twoColumnContainer
      .append("div")
      .attr("class", "left-column");

    const rightColumn = twoColumnContainer
      .append("div")
      .attr("class", "right-column");

    // Drag handlers
    function handleDragStart(itemId) {
      if (locked) return;
      draggedItemId = itemId;
    }

    function handleDragOver(event) {
      if (locked) return;
      event.preventDefault();
    }

    function handleDrop(event, categoryId) {
      if (locked) return;
      event.preventDefault();

      if (!draggedItemId) return;

      // Remove item from any existing matches
      Object.keys(currentState).forEach((key) => {
        currentState[key] = currentState[key].filter((id) => id !== draggedItemId);
      });

      // Add to new category
      if (!currentState[categoryId]) {
        currentState[categoryId] = [];
      }
      currentState[categoryId].push(draggedItemId);

      draggedItemId = null;
      render();
      onStateChange(currentState);
    }

    function removeMatch(categoryId, itemId) {
      if (locked) return;

      if (currentState[categoryId]) {
        currentState[categoryId] = currentState[categoryId].filter((id) => id !== itemId);
      }

      render();
      onStateChange(currentState);
    }

    function render() {
      // Clear columns
      leftColumn.html("");
      rightColumn.html("");

      // Render categories (drop zones) in right column
      const categoriesContainer = rightColumn
        .append("div")
        .attr("class", "categories");

      categories.forEach((category) => {
        const categoryCard = categoriesContainer
          .append("div")
          .attr("class", `category-card category-${category.id}`)
          .style("background", "#ffffff")
          .style("border", "2px solid #d1d5db")
          .style("border-radius", "12px")
          .style("padding", "16px")
          .style("margin-bottom", "16px")
          .style("min-height", "100px")
          .style("display", "flex")
          .style("flex-direction", "column")
          .style("gap", "12px");

        // Category label
        categoryCard
          .append("div")
          .style("font-weight", "600")
          .style("font-size", "15px")
          .text(category.label);

        // Drop zone
        const dropZone = categoryCard
          .append("div")
          .attr("class", `drop-zone drop-zone-${category.id}`)
          .style("border", "2px dashed #cbd5e1")
          .style("border-radius", "8px")
          .style("padding", "12px")
          .style("min-height", "80px")
          .style("background", "#ffffff")
          .style("transition", "all 0.2s");

        // Set up drop events
        const dropZoneNode = dropZone.node();
        dropZoneNode.addEventListener("dragover", handleDragOver);
        dropZoneNode.addEventListener("drop", (event) =>
          handleDrop(event, category.id)
        );

        // Render matched items in drop zone
        const matchedItemIds = currentState[category.id] || [];
        if (matchedItemIds.length > 0) {
          matchedItemIds.forEach((itemId) => {
            const matchedItem = items.find((item) => item.id === itemId);
            if (matchedItem) {
              const matchedContent = dropZone
                .append("div")
                .style("position", "relative")
                .style("margin-bottom", "12px")
                .style("padding", "12px")
                .style("border", "1px solid #e5e7eb")
                .style("border-radius", "8px")
                .style("background", "#fafafa");

              // Remove button
              if (!locked) {
                matchedContent
                  .append("button")
                  .attr("type", "button")
                  .style("position", "absolute")
                  .style("top", "8px")
                  .style("right", "8px")
                  .style("background", "#ef4444")
                  .style("color", "white")
                  .style("border", "none")
                  .style("border-radius", "4px")
                  .style("padding", "4px 8px")
                  .style("font-size", "12px")
                  .style("cursor", "pointer")
                  .text("✕ Remove")
                  .on("click", () => removeMatch(category.id, itemId));
              }

              // Render item content using provided render function
              if (typeof matchedItem.content === "function") {
                matchedItem.content(matchedContent);
              } else {
                matchedContent.append("div").text(matchedItem.content);
              }
            }
          });
        }
      });

      // Render draggable items in left column
      const availableArea = leftColumn
        .append("div")
        .attr("class", "available-items")
        .style("background", "#f3f4f6")
        .style("border-radius", "12px")
        .style("padding", "20px")
        .style("display", "flex")
        .style("flex-direction", "column")
        .style("gap", "16px");

      // Get all matched IDs
      const matchedIds = Object.values(currentState).flat();

      items.forEach((item) => {
        const isMatched = matchedIds.includes(item.id);

        const card = availableArea
          .append("div")
          .attr("class", `item-card item-card-${item.id}`)
          .attr("draggable", !locked && !isMatched)
          .style("background", isMatched ? "#e5e7eb" : "#ffffff")
          .style("border", "2px solid #d1d5db")
          .style("border-radius", "8px")
          .style("padding", "12px")
          .style("cursor", isMatched || locked ? "default" : "grab")
          .style("transition", "all 0.2s")
          .style("user-select", "none")
          .style("opacity", isMatched ? "0.5" : "1");

        if (!locked && !isMatched) {
          const cardNode = card.node();
          cardNode.addEventListener("dragstart", () =>
            handleDragStart(item.id)
          );

          card
            .on("mouseenter", function () {
              d3.select(this)
                .style("transform", "scale(1.02)")
                .style("box-shadow", "0 4px 12px rgba(0,0,0,0.1)");
            })
            .on("mouseleave", function () {
              d3.select(this)
                .style("transform", "scale(1)")
                .style("box-shadow", "none");
            });
        }

        // Render item content using provided render function
        if (typeof item.content === "function") {
          item.content(card);
        } else {
          card.append("div").text(item.content);
        }
      });
    }

    // Initial render
    render();

    // Return API
    return {
      setState: (newState) => {
        currentState = { ...newState };
        render();
      },
      getState: () => ({ ...currentState }),
      setLocked: (isLocked) => {
        locked = isLocked;
        render();
      },
      refresh: () => render(),
    };
  }

  // Expose to global scope
  global.createDragMatcher = createDragMatcher;

  // Also attach to window for explicit access
  if (typeof window !== "undefined") {
    window.DragMatch = {
      create: createDragMatcher,
    };
  }
})(this);
