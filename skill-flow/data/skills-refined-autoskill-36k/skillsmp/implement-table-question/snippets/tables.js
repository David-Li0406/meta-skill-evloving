/**
 * Table Component (Standalone)
 *
 * Creates standardized data tables with consistent styling.
 *
 * Usage in chart.html:
 *   <script src="../../../../../../../components/table.standalone.js"></script>
 *
 * Then in chart.js:
 *   const table = createDataTable(d3, container, {
 *     headers: ["Days", 0, 1, 3, 6, 8],
 *     rows: [
 *       { label: "Money Earned ($)", values: [0, null, null, null, null] }
 *     ],
 *     onInput: (rowIndex, colIndex, value) => { ... }
 *   });
 */

(function (global) {
  "use strict";

  /**
   * Creates a standardized data table
   * @param {object} d3 - D3 instance
   * @param {object} container - D3 selection to append table to
   * @param {object} options - Configuration options
   * @returns {object} Table API with update methods
   */
  function createDataTable(d3, container, options) {
    options = options || {};

    const headers = options.headers || [];
    const rows = options.rows || [];
    const onInput = options.onInput || function () {};
    const readOnly = options.readOnly || false;

    // Create table
    const table = container
      .append("table")
      .style("width", "100%")
      .style("border-collapse", "collapse")
      .style("text-align", "center");

    // Header row
    const headerRow = table.append("thead").append("tr");
    headers.forEach((header) => {
      headerRow
        .append("th")
        .style("padding", "12px")
        .style("border", "2px solid #d1d5db")
        .style("background", "#f3f4f6")
        .style("font-weight", "600")
        .style("font-size", "16px")
        .html(String(header));
    });

    // Data rows
    const tbody = table.append("tbody");
    const inputElements = [];

    rows.forEach((row, rowIndex) => {
      const tr = tbody.append("tr");

      // Row label
      tr.append("td")
        .style("padding", "12px")
        .style("border", "2px solid #d1d5db")
        .style("background", "#f9fafb")
        .style("font-weight", "600")
        .style("font-size", "16px")
        .html(row.label);

      // Row values
      row.values.forEach((value, colIndex) => {
        const td = tr
          .append("td")
          .style("padding", value === null ? "8px" : "12px")
          .style("border", "2px solid #d1d5db")
          .style("font-size", "16px");

        if (value === null && !readOnly) {
          // Editable input cell
          const input = td
            .append("input")
            .attr("type", "text")
            .attr("inputmode", "numeric")
            .style("width", "calc(100% - 4px)")
            .style("max-width", "80px")
            .style("padding", "8px")
            .style("border", "1px solid #cbd5e1")
            .style("border-radius", "6px")
            .style("text-align", "center")
            .style("font-size", "16px")
            .style("box-sizing", "border-box")
            .on("input", function () {
              onInput(rowIndex, colIndex, this.value);
            });

          inputElements.push({
            rowIndex,
            colIndex,
            element: input,
          });
        } else {
          // Static text cell
          td.text(value !== null ? String(value) : "");
        }
      });
    });

    // Return API
    return {
      getInputs: () => inputElements,
      setValue: (rowIndex, colIndex, value) => {
        const input = inputElements.find(
          (i) => i.rowIndex === rowIndex && i.colIndex === colIndex
        );
        if (input) {
          input.element.property("value", value);
        }
      },
      clearInputs: () => {
        inputElements.forEach((input) => {
          input.element.property("value", "");
        });
      },
    };
  }

  // Expose to global scope
  global.createDataTable = createDataTable;

  // Also attach to window for explicit access
  if (typeof window !== "undefined") {
    window.DataTable = {
      create: createDataTable,
    };
  }
})(this);
