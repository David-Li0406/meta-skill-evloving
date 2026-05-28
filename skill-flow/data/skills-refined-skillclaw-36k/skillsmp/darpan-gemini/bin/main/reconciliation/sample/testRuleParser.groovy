package reconciliation.sample

import org.slf4j.Logger
import org.slf4j.LoggerFactory

def testParser() {
    Logger logger = LoggerFactory.getLogger("testRuleParser")
    
    Map<String, String> testCases = [
        "status is 'Blocked'": "this[\"status\"] == 'Blocked'",
        "amount > 100": "this[\"amount\"] > 100",
        "price less than 50.00": "this[\"price\"] < 50.00",
        "category is not 'Shoes'": "this[\"category\"] != 'Shoes'",
        "description contains 'Error'": "this[\"description\"] != null && this[\"description\"].toString().contains('Error')"
    ]
    
    testCases.each { input, expected ->
        String result = RuleConditionParser.parseCondition(input)
        if (result == expected) {
            println "PASS: '${input}' -> '${result}'"
        } else {
            println "FAIL: '${input}'\n  Exp: ${expected}\n  Got: ${result}"
        }
    }
}

testParser()
