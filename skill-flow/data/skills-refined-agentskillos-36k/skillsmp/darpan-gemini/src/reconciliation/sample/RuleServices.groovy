package reconciliation.sample

import org.moqui.context.ExecutionContext
import org.kie.api.KieServices
import org.kie.api.builder.KieBuilder
import org.kie.api.builder.KieFileSystem
import org.kie.api.builder.Message
import org.kie.api.runtime.KieContainer
import org.kie.api.runtime.KieSession
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import java.util.List
import java.util.Map

// Helper to get logger in script
Logger getLogger() {
    return LoggerFactory.getLogger("reconciliation.sample.RuleServices")
}

def compileRuleSet() {
    ExecutionContext ec = context.ec
    Logger logger = getLogger()
    String ruleSetId = context.ruleSetId
    
    logger.info("compileRuleSet called for ${ruleSetId}")
    return [kieContainer: null]
}

def executeRules() {
    ExecutionContext ec = context.ec
    Logger logger = getLogger()
    
    String ruleSetId = context.ruleSetId
    List<Map> dataList = (List<Map>) context.dataList

    logger.info("Executing rules for RuleSet: ${ruleSetId} with ${dataList?.size()} items")

    if (!dataList) return [results: []]

    try {
        // 1. Setup Drools Services
        KieServices ks = KieServices.Factory.get()
        KieFileSystem kfs = ks.newKieFileSystem()

        // 2. Hardcoded DRL for testing
        String drl = """
            package reconciliation.sample
            import java.util.Map

            // Rule 1: Check if legacyResourceId exists (Processed)
            rule "Check Shopify Order Processed"
            when
                \$m : Map( this["legacyResourceId"] != null )
            then
                \$m.put("ruleEngineProcessed", true);
                \$m.put("ruleStatus", "Present");
            end
            
            // Rule 2: High Value Check (Amount > 100)
            // Note: Data maps from JSON might need type casting or flexible check
            rule "Check High Value Order"
            when
                \$m : Map( this["totalPriceSet"] != null )
            then
                // Extract nested logical check inside 'then' block for simplicity in this POC or use complex DRL access
                // For POC, let's just mark it checked if price set exists, logic matching extraction:
                // totalPriceSet.presentmentMoney.amount
                
                \$m.put("priceChecked", "Active");
                
                // Example of simple logic in consequence (not ideal for pure DRL but works for POC)
                Map priceSet = (Map) \$m.get("totalPriceSet");
                if (priceSet != null) {
                    Map money = (Map) priceSet.get("presentmentMoney");
                    if (money != null) {
                        String amtStr = (String) money.get("amount");
                        if (amtStr != null) {
                             try {
                                 double val = Double.parseDouble(amtStr);
                                 if (val > 100.0) {
                                     \$m.put("isHighValue", true);
                                 }
                             } catch (Exception e) {
                                 // ignore
                             }
                        }
                    }
                }
            end

            // Rule 3: Check Order Cancelled (Shopify Side)
            rule "Check Shopify Cancelled"
            when
                \$m : Map( this["cancelledAt"] != null )
            then
                \$m.put("isShopifyCancelled", true);
            end

            // Rule 4: Check OMS Cancelled
            rule "Check OMS Cancelled"
            when
                \$m : Map( this["status_id"] == "ORDER_CANCELLED" )
            then
                \$m.put("isOmsCancelled", true);
            end

            // Rule 5: Sync Issue - Shopify Cancelled, OMS Not
            rule "Sync Issue: Shopify Cancelled but OMS Active"
            when
                \$m : Map( this["cancelledAt"] != null && this["status_id"] != "ORDER_CANCELLED" )
            then
                \$m.put("syncIssue", true);
                \$m.put("syncIssueReason", "Shopify cancelled but OMS status is " + \$m.get("status_id"));
            end

            // Rule 6: Sync Issue - OMS Cancelled, Shopify Not
            rule "Sync Issue: OMS Cancelled but Shopify Active"
            when
                \$m : Map( this["cancelledAt"] == null && this["status_id"] == "ORDER_CANCELLED" )
            then
                \$m.put("syncIssue", true);
                \$m.put("syncIssueReason", "OMS cancelled but Shopify active");
            end


        """

        kfs.write("src/main/resources/simple.drl", drl)

        // 3. Build
        KieBuilder kb = ks.newKieBuilder(kfs)
        kb.buildAll()
        if (kb.getResults().hasMessages(Message.Level.ERROR)) {
            String errorMsg = "Drools Build Errors: " + kb.getResults().toString()
            logger.error(errorMsg)
            return [error: errorMsg]
        }

        KieContainer kContainer = ks.newKieContainer(kb.getKieModule().getReleaseId())
        KieSession kSession = kContainer.newKieSession()

        // 4. Execute
        for (Map data : dataList) {
            kSession.insert(data)
        }
        
        int fired = kSession.fireAllRules()
        logger.info("Fired ${fired} rules.")
        kSession.dispose()

        List mismatches = dataList.findAll { it.get("syncIssue") == true }
        return [results: mismatches]

    } catch (Throwable t) {
        logger.error("Error executing rules", t)
        return [error: "Rule execution failed: " + t.getMessage()]
    }
}

def executeRuleSetJson() {
    ExecutionContext ec = context.ec
    String jsonData = context.jsonData
    if (!jsonData) return [results: []]
    
    try {
        Object parsed = new groovy.json.JsonSlurper().parseText(jsonData)
         List<Map> dataList = []
         if (parsed instanceof List) {
             dataList = (List<Map>) parsed
         } else if (parsed instanceof Map) {
             dataList.add((Map) parsed)
         }
         
         context.put("dataList", dataList)
         return executeRules()
    } catch (Exception e) {
        return [error: "Invalid JSON Data: " + e.getMessage()]
    }
}
