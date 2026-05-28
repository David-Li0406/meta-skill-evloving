#!/usr/bin/env node
/**
 * Performance benchmarks for JavaScript/TypeScript implementation of The Universal Axiom
 */

const fs = require('fs');
const path = require('path');
const { UniversalAxiom, AxiomSimulator, fibonacciSequence } = require('../dist/javascript/universal-axiom');


/**
 * Run a benchmark function multiple times and collect statistics
 */
function benchmark(func, iterations = 1000, warmup = 100) {
    // Warmup
    for (let i = 0; i < warmup; i++) {
        func();
    }

    // Actual benchmark
    const times = [];
    for (let i = 0; i < iterations; i++) {
        const start = process.hrtime.bigint();
        func();
        const end = process.hrtime.bigint();
        times.push(Number(end - start) / 1e9); // Convert to seconds
    }

    const sorted = times.slice().sort((a, b) => a - b);
    const mean = times.reduce((a, b) => a + b, 0) / times.length;
    const median = sorted[Math.floor(sorted.length / 2)];

    // Calculate standard deviation
    const variance = times.reduce((sum, time) => sum + Math.pow(time - mean, 2), 0) / times.length;
    const stdev = Math.sqrt(variance);

    return {
        mean,
        median,
        stdev,
        min: sorted[0],
        max: sorted[sorted.length - 1],
        iterations
    };
}


/**
 * Benchmark functions
 */

function benchmarkBasicComputationN1() {
    const axiom = new UniversalAxiom({ n: 1 });
    axiom.computeIntelligence();
}

function benchmarkBasicComputationN10() {
    const axiom = new UniversalAxiom({ n: 10 });
    axiom.computeIntelligence();
}

function benchmarkBasicComputationN20() {
    const axiom = new UniversalAxiom({ n: 20 });
    axiom.computeIntelligence();
}

function benchmarkEvolution10Steps() {
    const axiom = new UniversalAxiom({ n: 1 });
    for (let i = 0; i < 10; i++) {
        axiom.evolve();
    }
}

function benchmarkEvolution100Steps() {
    const axiom = new UniversalAxiom({ n: 1 });
    for (let i = 0; i < 100; i++) {
        axiom.evolve();
    }
}

function benchmarkFibonacciGenerationN12() {
    fibonacciSequence(12);
}

function benchmarkFibonacciGenerationN50() {
    fibonacciSequence(50);
}

function benchmarkStateAccess() {
    const axiom = new UniversalAxiom({ n: 10 });
    axiom.getState();
}

function benchmarkContradictionResolution() {
    const axiom = new UniversalAxiom({ n: 5, subjectivity: 0.8 });
    const simulator = new AxiomSimulator(axiom);
    simulator.simulateContradictionResolution(1.5, 5);
}


/**
 * Format time in appropriate units
 */
function formatTime(seconds) {
    if (seconds < 1e-6) {
        return `${(seconds * 1e9).toFixed(2)} ns`;
    } else if (seconds < 1e-3) {
        return `${(seconds * 1e6).toFixed(2)} µs`;
    } else if (seconds < 1) {
        return `${(seconds * 1e3).toFixed(2)} ms`;
    } else {
        return `${seconds.toFixed(2)} s`;
    }
}


/**
 * Print benchmark results
 */
function printResults(name, results) {
    console.log(`\n${name}`);
    console.log(`  Mean:       ${formatTime(results.mean)}`);
    console.log(`  Median:     ${formatTime(results.median)}`);
    console.log(`  Std Dev:    ${formatTime(results.stdev)}`);
    console.log(`  Min:        ${formatTime(results.min)}`);
    console.log(`  Max:        ${formatTime(results.max)}`);
    console.log(`  Ops/sec:    ${(1/results.mean).toFixed(2)}`);
    console.log(`  Iterations: ${results.iterations}`);
}


/**
 * Export results to JSON
 */
function exportResults(results) {
    const exportData = {
        language: 'javascript',
        timestamp: Date.now() / 1000,
        benchmarks: {}
    };

    for (const [name, data] of Object.entries(results)) {
        exportData.benchmarks[name] = {
            mean_seconds: data.mean,
            median_seconds: data.median,
            stdev_seconds: data.stdev,
            ops_per_second: 1/data.mean
        };
    }

    const outputFile = path.join(__dirname, 'results_javascript.json');
    fs.writeFileSync(outputFile, JSON.stringify(exportData, null, 2));
    console.log(`\nResults exported to: ${outputFile}`);
}


/**
 * Main benchmark runner
 */
function main() {
    console.log('='.repeat(60));
    console.log('JavaScript Universal Axiom Performance Benchmarks');
    console.log('='.repeat(60));

    const benchmarks = [
        ['Basic Computation (n=1)', benchmarkBasicComputationN1, 1000],
        ['Basic Computation (n=10)', benchmarkBasicComputationN10, 1000],
        ['Basic Computation (n=20)', benchmarkBasicComputationN20, 1000],
        ['Evolution (10 steps)', benchmarkEvolution10Steps, 100],
        ['Evolution (100 steps)', benchmarkEvolution100Steps, 10],
        ['Fibonacci Generation (n=12)', benchmarkFibonacciGenerationN12, 1000],
        ['Fibonacci Generation (n=50)', benchmarkFibonacciGenerationN50, 1000],
        ['State Access', benchmarkStateAccess, 1000],
        ['Contradiction Resolution', benchmarkContradictionResolution, 100],
    ];

    const resultsSummary = {};

    for (const [name, func, iterations] of benchmarks) {
        process.stdout.write(`\nRunning: ${name}...`);
        const results = benchmark(func, iterations, Math.min(100, Math.floor(iterations/10)));
        console.log(' Done');
        printResults(name, results);
        resultsSummary[name] = results;
    }

    console.log('\n' + '='.repeat(60));
    console.log('Summary');
    console.log('='.repeat(60));
    console.log(`\n${'Benchmark'.padEnd(40)} ${'Mean Time'.padEnd(15)} ${'Ops/sec'.padEnd(10)}`);
    console.log('-'.repeat(60));

    for (const [name, results] of Object.entries(resultsSummary)) {
        console.log(`${name.padEnd(40)} ${formatTime(results.mean).padEnd(15)} ${(1/results.mean).toFixed(2).padEnd(10)}`);
    }

    console.log('\n' + '='.repeat(60));

    // Export results
    exportResults(resultsSummary);
}


if (require.main === module) {
    main();
}


module.exports = { benchmark, formatTime };
