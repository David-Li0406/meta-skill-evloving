#!/usr/bin/env groovy
/**
 * Test script for JSON reconciliation
 * This script tests the reconcile#JsonFiles service with test data
 */

import org.moqui.Moqui
import org.moqui.context.ExecutionContext

// Initialize Moqui
ExecutionContext ec = Moqui.getExecutionContext()

try {
    println "=" * 80
    println "Testing JSON Reconciliation Service"
    println "=" * 80
    
    def testParams = [
        json1Location: 'component://darpan/data/test/test-orders-1.json',
        json2Location: 'component://darpan/data/test/test-orders-2.json',
        schemaFileName: 'test-orders.schema.json',
        compareJsonPath: '$[*].data.orders.edges[*].node.legacyResourceId',
        json1Label: 'Orders File 1',
        json2Label: 'Orders File 2'
    ]
    
    println "\nTest Parameters:"
    println "  JSON 1: ${testParams.json1Location}"
    println "  JSON 2: ${testParams.json2Location}"
    println "  Schema: ${testParams.schemaFileName}"
    println "  JSONPath: ${testParams.compareJsonPath}"
    println ""
    
    println "Calling ReconciliationJsonServices.reconcile#JsonFiles..."
    def result = ec.service.sync().name("ReconciliationJsonServices.reconcile#JsonFiles")
            .parameters(testParams)
            .call()
    
    println "\nResults:"
    println "  Validation Passed: ${result.validationPassed}"
    if (result.validationErrors) {
        println "  Validation Errors:"
        result.validationErrors.each { err ->
            println "    - ${err}"
        }
    }
    println "  Total Differences: ${result.differenceCount}"
    println "  Only in JSON 1: ${result.onlyInJson1Count}"
    println "  Only in JSON 2: ${result.onlyInJson2Count}"
    println "  Output File: ${result.diffLocation}"
    
    if (result.onlyInJson1) {
        println "\n  IDs only in JSON 1:"
        result.onlyInJson1.each { id ->
            println "    - ${id}"
        }
    }
    
    if (result.onlyInJson2) {
        println "\n  IDs only in JSON 2:"
        result.onlyInJson2.each { id ->
            println "    - ${id}"
        }
    }
    
    println "\n" + "=" * 80
    println "Test Complete!"
    println "Check the output file for full reconciliation results:"
    println "  ${result.diffLocation}"
    println "=" * 80
    
} catch (Exception e) {
    println "\nERROR: ${e.message}"
    e.printStackTrace()
} finally {
    // Cleanup
    if (ec != null) ec.destroy()
}
