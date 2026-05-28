import org.apache.spark.sql.SparkSession
import static org.apache.spark.sql.functions.lit
import org.slf4j.LoggerFactory

def logger = LoggerFactory.getLogger("reconciliation.sample.SampleOrderIds")
def toMb = { long bytes -> (bytes / (1024L * 1024L)) }
def toPercent = { val ->
    if (val == null) return "n/a"
    try {
        return ((val as BigDecimal).setScale(1, BigDecimal.ROUND_HALF_UP)).toString()
    } catch (Exception e) {
        return val.toString()
    }
}
def getUtilization = {
    def smap = ec.factory.getStatusMap(true)
    def util = smap?.Utilization ?: [:]
    return [load: toPercent(util.LoadPercent), heap: toPercent(util.HeapPercent), disk: toPercent(util.DiskPercent)]
}
def logStatus = { String stage ->
    Runtime rt = Runtime.getRuntime()
    long total = rt.totalMemory()
    long free = rt.freeMemory()
    long used = total - free
    long max = rt.maxMemory()
    def util = getUtilization()
    logger.info("${stage} heap used=${toMb(used)}MB total=${toMb(total)}MB max=${toMb(max)}MB heapPct=${util.heap}% load=${util.load}% disk=${util.disk}%")
}
def showDf = { df, String label, Integer limit ->
    def cols = df.columns()
    logger.info("${label} columns: ${cols ? cols.join(', ') : 'n/a'}")
    logger.info("${label} schema:")
    df.printSchema()
    int rowLimit = (limit != null ? limit as int : 5)
    if (rowLimit <= 0) {
        long rowCount = df.count()
        int showCount = rowCount > Integer.MAX_VALUE ? Integer.MAX_VALUE : (int) rowCount
        logger.info("${label} rows (all; count=${rowCount}):")
        df.show(showCount, false)
    } else {
        logger.info("${label} rows (first ${rowLimit}):")
        df.show(rowLimit, false)
    }
}
def logPriceSetDf = { df, String label, Integer limit ->
    def totalPriceSetField = df.schema().fields().find { it.name() == "totalPriceSet" }
    if (totalPriceSetField == null) {
        logger.info("${label}: column totalPriceSet not present")
        return
    }
    def totalPriceSetType = totalPriceSetField.dataType()
    if (!(totalPriceSetType instanceof org.apache.spark.sql.types.StructType)) {
        logger.info("${label}: totalPriceSet is not a struct")
        return
    }
    def totalPriceSetFields = totalPriceSetType.fieldNames()
    if (!totalPriceSetFields.contains("presentmentMoney")) {
        logger.info("${label}: presentmentMoney not present; available fields=${totalPriceSetFields ? totalPriceSetFields.join(', ') : 'n/a'}")
        return
    }
    def priceSetDf = df.selectExpr(
            "totalPriceSet.presentmentMoney.amount",
            "totalPriceSet.presentmentMoney.currencyCode"
    )
    showDf(priceSetDf, label, limit)
}

String omsField = omsOrderIdField ?: orderIdField ?: "shopify_order_id"
String shopifyField = shopifyOrderIdField ?: orderIdField ?: "shopify_order_id"

def resolvePath = { String location ->
    def rr = ec.resource.getLocationReference(location)
    if (rr != null && rr.supportsUrl()) {
        def url = rr.getUrl()
        if (url != null) return url.toString()
    }
    return location
}

String omsPath = resolvePath(omsLocation)
String shopifyPath = resolvePath(shopifyLocation)

logStatus("compare bulk orders: before Spark session")
SparkSession spark = null
try {
    spark = SparkSession.builder()
            .appName(sparkAppName ?: "ReconciliationSampleOrderCompare")
            .master(sparkMaster ?: "local[*]")
            .getOrCreate()

    def reader = spark.read().option("multiLine", "true")
    logger.info("loading OMS bulk data from ${omsPath} using id field '${omsField}'")
    def omsRaw = reader.json(omsPath)
    def omsDf = omsRaw.selectExpr("${omsField} as order_id")
            .filter("order_id IS NOT NULL AND length(trim(order_id)) > 0")
            .dropDuplicates()

    logger.info("loading Shopify bulk data from ${shopifyPath} using id field '${shopifyField}'")
    logStatus("compare bulk orders: after load OMS")
    def shopifyRaw = reader.json(shopifyPath)
    def shopifyDf
    def shopifyExplodedDf
    def shopifyNodeDf
    if (shopifyRaw.schema().fieldNames().contains("data")) {
        shopifyExplodedDf = shopifyRaw.selectExpr("explode(data.orders.edges) as edge")
        if (logShopifyExplodedRows) {
            showDf(shopifyExplodedDf, "shopify exploded edges", shopifyExplodedRowLimit)
        }
        def logShopifyNodeView = logShopifyNodeRows || logShopifyPriceSetRows
        if (logShopifyNodeView) {
            shopifyNodeDf = shopifyExplodedDf.selectExpr("edge.node.*")
        }
        if (logShopifyNodeRows) {
            showDf(shopifyNodeDf, "shopify exploded node.*", shopifyNodeRowLimit)
        }
        if (logShopifyPriceSetRows) {
            logPriceSetDf(shopifyNodeDf, "shopify totalPriceSet.presentmentMoney", shopifyPriceSetRowLimit)
        }
        shopifyDf = shopifyExplodedDf.selectExpr("edge.node.${shopifyField} as order_id")
    } else {
        shopifyExplodedDf = shopifyRaw
        if (logShopifyExplodedRows) {
            showDf(shopifyExplodedDf, "shopify raw rows (no data field)", shopifyExplodedRowLimit)
        }
        def logShopifyNodeView = logShopifyNodeRows || logShopifyPriceSetRows
        if (logShopifyNodeView) {
            shopifyNodeDf = shopifyExplodedDf
        }
        if (logShopifyNodeRows && !logShopifyExplodedRows) {
            showDf(shopifyNodeDf, "shopify raw rows (no data field)", shopifyNodeRowLimit)
        }
        if (logShopifyPriceSetRows) {
            logPriceSetDf(shopifyNodeDf, "shopify totalPriceSet.presentmentMoney", shopifyPriceSetRowLimit)
        }
        shopifyDf = shopifyRaw.selectExpr("${shopifyField} as order_id")
    }
    shopifyDf = shopifyDf.filter("order_id IS NOT NULL AND length(trim(order_id)) > 0")
            .dropDuplicates()
    if (logShopifySampleRows) {
        logger.info("shopify order_id columns: ${shopifyDf.columns().join(', ')}")
        logger.info("shopify sample order_ids (first 5 rows):")
        shopifyDf.show(5, false)
    }
    if (logInputCounts) {
        logger.info("loaded bulk order id sets: omsUniqueIds=${omsDf.count()} shopifyUniqueIds=${shopifyDf.count()}")
    }
    logStatus("compare bulk orders: after load + dedupe")

    def onlyInOmsDf = omsDf.join(shopifyDf, "order_id", "left_anti").select("order_id")
    def onlyInShopifyDf = shopifyDf.join(omsDf, "order_id", "left_anti").select("order_id")
    logStatus("compare bulk orders: after anti-joins")

    onlyInOms = onlyInOmsDf.collect().collect { row -> row.get(0)?.toString() }
    onlyInShopify = onlyInShopifyDf.collect().collect { row -> row.get(0)?.toString() }

    onlyInOmsCount = onlyInOms.size()
    onlyInShopifyCount = onlyInShopify.size()
    logger.info("comparison results: onlyInOms=${onlyInOmsCount} onlyInShopify=${onlyInShopifyCount}")
    logStatus("compare bulk orders: after collect results")
} finally {
    if (spark != null) {
        spark.stop()
        logger.info("compare bulk orders: Spark session stopped")
    }
}
