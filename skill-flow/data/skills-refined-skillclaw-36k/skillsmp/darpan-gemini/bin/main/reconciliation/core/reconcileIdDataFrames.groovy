import org.apache.spark.sql.Dataset
import org.slf4j.LoggerFactory

def logger = LoggerFactory.getLogger("darpan.reconciliation.core.DataFrameReconciliation")

// Validate inputs
if (!df1 || !df2) {
    throw new IllegalArgumentException("df1 and df2 DataFrames are required")
}

String idCol = idColumnName?.toString() ?: "compare_id"
String df1LabelStr = df1Label?.toString() ?: "DataFrame 1"
String df2LabelStr = df2Label?.toString() ?: "DataFrame 2"

logger.info("Starting DataFrame reconciliation: df1Label=${df1LabelStr} df2Label=${df2LabelStr} idColumn=${idCol}")

// Perform anti-joins to find differences (all operations stay in Spark)
// left_anti = rows in left DataFrame that have no match in right DataFrame
def onlyInDf1Temp = df1.join(df2, df1(idCol) === df2(idCol), "left_anti")
                        .select(df1(idCol).as(idCol))
                        .distinct()

def onlyInDf2Temp = df2.join(df1, df1(idCol) === df2(idCol), "left_anti")
                        .select(df2(idCol).as(idCol))
                        .distinct()

// Get counts (triggers computation but keeps data in Spark)
def count1 = onlyInDf1Temp.count()
def count2 = onlyInDf2Temp.count()

onlyInDf1 = onlyInDf1Temp
onlyInDf2 = onlyInDf2Temp
onlyInDf1Count = count1
onlyInDf2Count = count2
differenceCount = count1 + count2

logger.info("DataFrame reconciliation complete: onlyIn${df1LabelStr}=${count1} onlyIn${df2LabelStr}=${count2} total=${differenceCount}")
logger.info("Results returned as DataFrames - no data collected to driver memory")
