import org.apache.spark.sql.SparkSession
import org.slf4j.LoggerFactory

def logger = LoggerFactory.getLogger("reconciliation.sample.SampleOrderIdsDb")
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

String resolvedJdbcUrl = null
String resolvedUser = null
String resolvedPassword = null
String resolvedTable = dbTable ?: "order_header"
String resolvedColumn = orderIdColumn ?: "order_id"
String resolvedDriver = dbDriver ?: "com.mysql.cj.jdbc.Driver"
int rowLimit = (limit ?: 10) as int

if (!systemMessageRemoteId) {
    throw new IllegalArgumentException("systemMessageRemoteId is required for JDBC access")
}

def systemMessageRemote = ec.entity.find("moqui.service.message.SystemMessageRemote")
        .condition("systemMessageRemoteId", systemMessageRemoteId)
        .useCache(true)
        .one()
if (!systemMessageRemote) {
    throw new IllegalArgumentException("SystemMessageRemote ${systemMessageRemoteId} not found")
}

resolvedJdbcUrl = systemMessageRemote.sendUrl
resolvedUser = systemMessageRemote.username
resolvedPassword = systemMessageRemote.password

if (!resolvedJdbcUrl) {
    throw new IllegalArgumentException("SystemMessageRemote ${systemMessageRemoteId} is missing sendUrl for JDBC access")
}
if (!resolvedUser) {
    throw new IllegalArgumentException("SystemMessageRemote ${systemMessageRemoteId} is missing username for JDBC access")
}
if (resolvedPassword == null) {
    throw new IllegalArgumentException("SystemMessageRemote ${systemMessageRemoteId} is missing password for JDBC access")
}

String dbTableRef = resolvedTable

String safeJdbcUrl = resolvedJdbcUrl.replaceAll("(?i)password=[^&]+", "password=***")

logStatus("spark db read: before Spark session")
SparkSession spark = null
try {
    spark = SparkSession.builder()
            .appName(sparkAppName ?: "ReconciliationSampleOrderDbRead")
            .master(sparkMaster ?: "local[*]")
            .getOrCreate()

    logger.info("reading ${rowLimit} order IDs from ${dbTableRef} via ${safeJdbcUrl} for remote ${systemMessageRemoteId}")

    def df = spark.read().format("jdbc")
            .option("url", resolvedJdbcUrl)
            .option("dbtable", dbTableRef)
            .option("user", resolvedUser)
            .option("password", resolvedPassword)
            .option("driver", resolvedDriver)
            .load()
    logStatus("spark db read: after load")

    def orderIdDf = df.selectExpr("${resolvedColumn} as order_id")
            .filter("order_id IS NOT NULL")
            .limit(rowLimit)

    orderIds = orderIdDf.collect().collect { row -> row.get(0)?.toString() }
    orderIdCount = orderIds.size()
    logger.info("spark db read: fetched ${orderIdCount} order IDs")
    logStatus("spark db read: after collect")
} finally {
    if (spark != null) {
        spark.stop()
        logger.info("spark db read: Spark session stopped")
    }
}
