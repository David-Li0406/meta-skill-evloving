package reconciliation.sample

import org.moqui.context.ExecutionContext
import org.moqui.entity.EntityValue
import java.sql.Timestamp

/**
 * Script to test Rule Engine services.
 */
def testRuleEngine() {
    ExecutionContext ec = context.ec
    // Login to satisfy "must be logged in" check
    ec.user.loginUser("john.doe", "moqui")
    // Disable Authz to allow entity access for unauthorized user
    ec.artifactExecution.disableAuthz()
    // DEBUG: Check if class is loadable
    try {
        Class c = Class.forName("reconciliation.sample.RuleServices")
        ec.logger.info("Successfully loaded class: " + c.getName())
    } catch (ClassNotFoundException e) {
        ec.logger.error("FAILED TO LOAD CLASS reconciliation.sample.RuleServices", e)
    }

    // 1. Create a Test RuleSet and Rule
    String ruleSetId = "TEST_RS_01"
    
    // Check if exists
    EntityValue existing = ec.entity.find("darpan.rule.RuleSet").condition("ruleSetId", ruleSetId).one()
    if (!existing) {
        ec.entity.makeValue("darpan.rule.RuleSet")
            .set("ruleSetId", ruleSetId)
            .set("ruleSetName", "Test Rule Set")
            .set("createdDate", new Timestamp(System.currentTimeMillis()))
            .create()
    }
    
    // Create Rule 1: Allow only 'Active' status
    String ruleId = "TEST_RULE_01"
    EntityValue existingRule = ec.entity.find("darpan.rule.Rule").condition("ruleId", ruleId).one()
    
    String logic = """
    rule "Check Blocked Status"
    when
        m : java.util.Map( this["status"] == "Blocked" )
    then
        results.add(["rule": "Check Blocked Status", "data": m, "error": "Status is Blocked"]);
    end
    """
    
    if (!existingRule) {
        ec.entity.makeValue("darpan.rule.Rule")
            .set("ruleId", ruleId)
            .set("ruleSetId", ruleSetId)
            .set("ruleText", "Status must not be Blocked")
            .set("ruleLogic", logic)
            .set("sequenceNum", 1L)
            .set("enabled", "Y")
            .create()
    } else {
        existingRule.set("ruleLogic", logic).set("enabled", "Y").update()
    }

    // Create Rule 2: Check Pending Status (Auto-parsed)
    String ruleId2 = "TEST_RULE_AUTO_01"
    EntityValue rule2 = ec.entity.find("darpan.rule.Rule").condition("ruleId", ruleId2).one()
    if (!rule2) {
         ec.entity.makeValue("darpan.rule.Rule")
            .set("ruleId", ruleId2)
            .set("ruleSetId", ruleSetId)
            .set("ruleText", "status is 'Pending'")
            .set("ruleLogic", null) // Ensure logic is null to trigger parser
            .set("sequenceNum", 2L)
            .set("enabled", "Y")
            .create()
    } else {
        rule2.set("ruleLogic", null).set("ruleText", "status is 'Pending'").set("enabled", "Y").update()
    }
    
    // 2. Compile
    Map compileResult = ec.service.sync().name("reconciliation.ReconciliationSampleServices.compile#RuleSet")
        .parameter("ruleSetId", ruleSetId)
        .call()
        
    if (compileResult.error) {
        return [error: "Compilation failed: " + compileResult.error]
    }
    
    // 3. Prepare Data
    List<Map> testData = []
    
    // Load OMS Data (Source of Truth for Status)
    int matchedCount = 0
    Map<String, String> omsStatusMap = [:]
    try {
        org.moqui.resource.ResourceReference omsRr = ec.resource.getLocationReference("component://darpan/data/sample/omsData.json")
        if (omsRr.getExists()) {
            ec.logger.info("Reading omsData.json...")
            List omsList = (List) new groovy.json.JsonSlurper().parseText(omsRr.getText())
            for (def item : omsList) {
                if (item.shopify_order_id && item.status_id) {
                    omsStatusMap.put((String) item.shopify_order_id, (String) item.status_id)
                }
            }
            ec.logger.info("Loaded ${omsStatusMap.size()} OMS records.")
        } else {
            ec.logger.error("omsData.json not found!")
            return [error: "OMS File not found"]
        }
    } catch (Exception e) {
        ec.logger.error("Error reading OMS data", e)
        return [error: "OMS Data load failed: " + e.getMessage()]
    }

    // Load Shopify Data
    try {
        org.moqui.resource.ResourceReference shopifyRr = ec.resource.getLocationReference("component://darpan/data/sample/shopifyData.json")
        if (shopifyRr.getExists()) {
            ec.logger.info("Reading shopifyData.json...")
            List shopifyList = (List) new groovy.json.JsonSlurper().parseText(shopifyRr.getText())
            
            ec.logger.info("Found ${shopifyList.size()} Shopify records.")
            
            // Remove limit for full check
            // int limit = 5000
            
            for (int i = 0; i < shopifyList.size(); i++) {
                Map shopifyOrder = (Map) shopifyList[i]
                String orderId = shopifyOrder.shopify_order_id
                
                // Merge OMS Status
                if (orderId) {
                    if (omsStatusMap.containsKey(orderId)) {
                        shopifyOrder.put("status_id", omsStatusMap.get(orderId))
                        matchedCount++
                    } else {
                        // Mark as missing in OMS or unknown
                        shopifyOrder.put("status_id", "UNKNOWN")
                    }
                    testData.add(shopifyOrder)
                }
            }
            ec.logger.info("Prepared ${testData.size()} merged records (Matched: ${matchedCount}).")

        } else {
             ec.logger.error("shopifyData.json not found!")
             return [error: "Shopify File not found"]
        }
    } catch (Exception e) {
        ec.logger.error("Error reading Shopify data", e)
        return [error: "Shopify Data load failed: " + e.getMessage()]
    }
    
    // 4. Execute Rules
    Map execResult = ec.service.sync().name("reconciliation.ReconciliationSampleServices.execute#Rules")
        .parameter("ruleSetId", ruleSetId)
        .parameter("dataList", testData)
        .call()
        

    // 4. Verification Check
    int issuesCount = 0
    List<Map> sampleIssues = []
    
    if (execResult.results) {
        List<Map> allResults = (List<Map>) execResult.results
        List<Map> issues = allResults.findAll { it.syncIssue == true }
        issuesCount = issues.size()
        sampleIssues = issues.take(10)
    }

    Map outputMap = [
        totalProcessed: testData.size(),
        syncIssuesFound: issuesCount,
        sampleIssues: sampleIssues,
        matchedCount: matchedCount,
        omsMapSize: omsStatusMap.size(),
        allResults: execResult.results // Optional: dump all for debugging
    ]

    // Write to file for verification
    File outputFile = new File(ec.factory.runtimePath + "/log/rule_test_output.json")
    com.fasterxml.jackson.databind.ObjectMapper mapper = new com.fasterxml.jackson.databind.ObjectMapper()
    mapper.enable(com.fasterxml.jackson.databind.SerializationFeature.INDENT_OUTPUT)
    mapper.writeValue(outputFile, outputMap)

    ec.logger.info("Test Run Complete. Results written to: " + outputFile.absolutePath)

    return outputMap
}

testRuleEngine()
