import org.slf4j.LoggerFactory
import org.moqui.sftp.SftpClient


def logger = LoggerFactory.getLogger("darpan.reconciliation.automation.SftpReconciliation")

def normalize = { val -> val?.toString()?.trim() }
def normalizeHostParts = { String host ->
    def normalized = normalize(host)
    if (!normalized) return [hostPort: null, basePath: null]
    normalized = normalized.replaceFirst(/^[a-zA-Z]+:\\/\\//, "")
    while (normalized.startsWith("//")) normalized = normalized.substring(2)

    String basePath = null
    int slashIdx = normalized.indexOf("/")
    if (slashIdx >= 0) {
        basePath = normalized.substring(slashIdx)
        normalized = normalized.substring(0, slashIdx)
    }

    normalized = normalized.replaceAll(/\/+$/, "")
    if (basePath != null) {
        basePath = basePath.replaceAll(/\/+$/, "")
        if (!basePath) basePath = "/"
    }

    return [hostPort: normalized, basePath: basePath]
}
def normalizePath = { String path ->
    def cleaned = normalize(path)
    if (!cleaned) return null
    cleaned = cleaned.replaceAll(/\\+/, "/")
    cleaned = cleaned.replaceAll(/\/+$/, "")
    if (!cleaned) return "/"
    if (!cleaned.startsWith("/")) cleaned = "/" + cleaned
    return cleaned
}
def resolveHostAndPort = { String host, Object portVal, String label ->
    def hostParts = normalizeHostParts(host)
    def hostOnly = hostParts.hostPort
    def hostBasePath = normalizePath(hostParts.basePath)
    if (!hostOnly) {
        throw new IllegalArgumentException("Host required for ${label}")
    }

    Integer inlinePort = null
    int lastColon = hostOnly.lastIndexOf(":")
    if (lastColon > -1 && lastColon < hostOnly.length() - 1) {
        def portStr = hostOnly.substring(lastColon + 1)
        def hostCandidate = hostOnly.substring(0, lastColon)
        if (portStr.isInteger()) {
            inlinePort = portStr.toInteger()
            hostOnly = hostCandidate
        } else {
            throw new IllegalArgumentException("Invalid port '${portStr}' in host ${host} for ${label}")
        }
    }

    String portString = normalize(portVal) ?: "22"
    if (inlinePort != null) portString = inlinePort.toString()

    Integer portNum
    try {
        portNum = Integer.parseInt(portString)
    } catch (Exception e) {
        throw new IllegalArgumentException("Invalid port '${portString}' for ${label} (host ${host})")
    }

    return [host: hostOnly, port: portNum, basePath: hostBasePath]
}
def resolveEnumLabel = { String enumId, String fallback ->
    def normalized = normalize(enumId)
    if (!normalized) return fallback
    def enumValue = ec.entity.find("moqui.basic.Enumeration")
            .condition("enumId", normalized)
            .useCache(true)
            .one()
    def code = normalize(enumValue?.enumCode)
    if (code) return code
    def description = normalize(enumValue?.description)
    if (description) return description
    return normalized
}
def ensureDirectory = { rr ->
    if (rr == null) return rr
    if (rr.supportsExists() && rr.getExists() && rr.isDirectory()) return rr
    def dirFile = rr.getFile()
    if (dirFile != null && !dirFile.exists()) dirFile.mkdirs()
    return rr
}
def stageStream = { InputStream inputStream, stageDirRef, String label, String sourceName, String timestamp ->
    def safeName = sourceName ?: label
    safeName = safeName.replaceAll("[^A-Za-z0-9._-]", "_")
    def targetRef = stageDirRef.makeFile("${timestamp}-${label}-${safeName}")

    OutputStream outputStream
    try {
        outputStream = targetRef.getOutputStream()
        outputStream << inputStream
    } finally {
        try { outputStream?.close() } catch (Exception ignored) {}
    }

    def stagedLocation = targetRef.getFile()?.getAbsolutePath() ?: targetRef.getLocation()
    return [location: stagedLocation, name: safeName]
}

def selectSftpCandidateFile = { SftpClient client, String basePath, String label, String archiveFolderName = null ->
    List<Map> entries = []
    boolean listedDirectory = true
    try {
        entries = client.ls(basePath)
    } catch (Exception e) {
        listedDirectory = false
    }

    if (!listedDirectory) {
        def name = basePath.tokenize("/")?.last() ?: basePath
        return [refPath: basePath, name: name]
    }

    entries = entries.findAll { entry ->
        def nameVal = entry.name ?: ""
        def pathVal = entry.path ?: ""

        if (archiveFolderName) {
            if (nameVal == archiveFolderName) return false
            if (pathVal.endsWith("/${archiveFolderName}")) return false
        }

        def isFileFlag = entry.isFile == true
        def isDirFlag = (entry.isDir == true) || (entry.isDirectory == true)
        if (!isFileFlag) return false
        if (isDirFlag) return false
        return true
    }

    if (!entries) {
        return [refPath: null, name: null, message: "No files found at ${basePath} for ${label}"]
    }

    entries.sort { a, b ->
        def aTs = (a.lastModified ?: 0L)
        def bTs = (b.lastModified ?: 0L)
        def tsCompare = bTs <=> aTs
        if (tsCompare != 0) return tsCompare
        return (b.name ?: "") <=> (a.name ?: "")
    }

    def chosen = entries[0]
    def path = chosen.path ?: (basePath.endsWith("/") ? basePath + chosen.name : basePath + "/" + chosen.name)
    return [refPath: path, name: chosen.name]
}

if (!reconciliationMappingId) {
    throw new IllegalArgumentException("reconciliationMappingId is required")
}
if (!file1SystemEnumId || !file2SystemEnumId) {
    throw new IllegalArgumentException("file1SystemEnumId and file2SystemEnumId are required")
}
if (!file1SftpServerId || !file2SftpServerId) {
    throw new IllegalArgumentException("file1SftpServerId and file2SftpServerId are required")
}

def stageDirRef = ensureDirectory(ec.resource.getLocationReference(stageLocation ?: "runtime://tmp/reconciliation/automation/input"))
if (stageDirRef == null) {
    throw new IllegalStateException("Unable to resolve stage directory ${stageLocation}")
}
if (!stageDirRef.supportsWrite()) {
    throw new IllegalStateException("Stage directory ${stageDirRef.getLocation()} is not writable")
}
def stageFileObj = stageDirRef.getFile()
if (stageFileObj != null && !stageFileObj.exists()) {
    stageFileObj.mkdirs()
}

def timestamp = ec.l10n.format(ec.user.nowTimestamp, "yyyyMMdd-HHmmssSSS")

processingWarnings = []
validationErrors = []
def messages = new StringBuilder()
def logMsg = { String msg ->
    logger.info(msg)
    messages.append(ec.l10n.format(ec.user.nowTimestamp, "HH:mm:ss")).append(" ").append(msg).append("\n")
    ec.message.addMessage(msg)
}

def remoteUploadPath = null
def stageBasePath = stageLocation ?: "runtime://tmp/reconciliation/automation/input"
def defaultOutputPath = stageBasePath.endsWith("/") ? (stageBasePath + "reconciled") : (stageBasePath + "/reconciled")
def outputPathToUse = outputLocation ?: defaultOutputPath
def runtimeRoot = ec.factory?.runtimePath
if (outputPathToUse?.startsWith("/") && runtimeRoot && !outputPathToUse.startsWith(runtimeRoot)) {
    remoteUploadPath = normalizePath(outputPathToUse)
    processingWarnings << "Output location ${outputPathToUse} is treated as remote; writing locally and uploading to ${remoteUploadPath}"
    logMsg("Output location ${outputPathToUse} is treated as remote; writing locally and uploading to ${remoteUploadPath}")
    outputPathToUse = defaultOutputPath
}
def outputDirRef = ensureDirectory(ec.resource.getLocationReference(outputPathToUse))
if (outputDirRef == null || !outputDirRef.supportsWrite()) {
    processingWarnings << "Output location ${outputPathToUse} is not writable; falling back to ${defaultOutputPath}"
    logMsg("Output location ${outputPathToUse} not writable; falling back to ${defaultOutputPath}")
    outputPathToUse = defaultOutputPath
    outputDirRef = ensureDirectory(ec.resource.getLocationReference(outputPathToUse))
}
if (outputDirRef == null) {
    throw new IllegalStateException("Unable to resolve output directory ${outputPathToUse}")
}
def outputDirFile = outputDirRef.getFile()
if (outputDirFile != null && !outputDirFile.exists()) {
    if (!outputDirFile.mkdirs() && !outputDirFile.exists()) {
        processingWarnings << "Unable to create output directory ${outputDirFile.getAbsolutePath()}; using default ${defaultOutputPath}"
        logMsg("Unable to create output directory ${outputDirFile.getAbsolutePath()}; using default ${defaultOutputPath}")
        outputPathToUse = defaultOutputPath
        outputDirRef = ensureDirectory(ec.resource.getLocationReference(outputPathToUse))
        outputDirFile = outputDirRef?.getFile()
        if (outputDirFile != null && !outputDirFile.exists()) outputDirFile.mkdirs()
    }
}
if (!outputDirRef.supportsWrite()) {
    throw new IllegalStateException("Output directory ${outputDirRef.getLocation()} is not writable")
}
def outputLoc = outputDirRef.getLocation()
logMsg("Starting SFTP poll for mapping ${reconciliationMappingId}")

def prepareFile = { String label, String systemEnumId, String sftpServerId, String overridePath ->
    def server = ec.entity.find("darpan.reconciliation.SftpServer")
            .condition("sftpServerId", sftpServerId)
            .useCache(true)
            .one()
    if (!server) {
        throw new IllegalArgumentException("SFTP Server ${sftpServerId} not found for ${label}")
    }

    def hostInfo = resolveHostAndPort(server.host, server.port, "Server ${sftpServerId}")
    def cleanHost = hostInfo.host
    def cleanPort = hostInfo.port
    def hostBasePath = hostInfo.basePath
    def cleanUser = normalize(server.username)
    def cleanPass = normalize(server.password) // Assuming decrypted by Moqui entity engine if configured? Or we might need to decrypt explicitly if not handled automatically? Moqui usually handles encrypted fields automatically on get.
    def overrideClean = normalizePath(overridePath)

    if (!cleanHost || !cleanUser) {
        throw new IllegalArgumentException("Host and Username required for ${label} (Server ${sftpServerId})")
    }

    if (!cleanPass && !server.privateKey) {
        throw new IllegalArgumentException("Password or Private Key required for ${label} (Server ${sftpServerId})")
    }

    def sftpTarget = overrideClean ?: hostBasePath ?: "/"
    
    // Construct simplified SFTP config
    def sftpConfig = [host: cleanHost, port: cleanPort, basePath: sftpTarget]

    if (sftpConfig) {
        SftpClient sftpClient = new SftpClient((String) sftpConfig.host, (String) cleanUser, (int) sftpConfig.port)
        if (cleanPass) sftpClient.password((String) cleanPass)
        if (server.privateKey) sftpClient.privateKey((String) server.privateKey)
        
        logMsg("Connecting to SFTP: ${sftpConfig.host}:${sftpConfig.port} as ${cleanUser} (path: ${sftpConfig.basePath})")
        // Default to not preserving attributes to avoid permission issues unless configured otherwise (could add param later)
        // Default to not preserving attributes to avoid permission issues unless configured otherwise
        sftpClient.preserveAttributes(server.remoteAttributes == "Y")

        def selection
        def staged
        try {
            sftpClient.connect()
            selection = selectSftpCandidateFile(sftpClient, (String) sftpConfig.basePath, label, archiveSubdir)
            if (!selection.refPath) {
                String failMsg = "No file found at ${sftpConfig.basePath} matching criteria."
                logMsg(failMsg)
                return [found: false, message: failMsg, source: "sftp://${sftpConfig.host}:${sftpConfig.port}${sftpConfig.basePath}"]
            }
            logMsg("Found file: ${selection.name} (${selection.refPath})")
            InputStream inputStream = sftpClient.openStream((String) selection.refPath)
            try {
                staged = stageStream(inputStream, stageDirRef, label, selection.name, timestamp)
                logMsg("Staged file to: ${staged.location}")
            } finally {
                try { inputStream?.close() } catch (Exception ignored) {}
            }

            try {
                String baseDir = selection.refPath.contains("/") ? selection.refPath.substring(0, selection.refPath.lastIndexOf("/")) : "/"
                String archiveDir = baseDir.endsWith("/") ? baseDir + (archiveSubdir ?: "archive") : baseDir + "/" + (archiveSubdir ?: "archive")
                try {
                    sftpClient.mkdirs(archiveDir)
                } catch (Exception ignored) { }
                String archiveDest = archiveDir + "/" + (selection.name ?: selection.refPath.tokenize("/")?.last() ?: selection.refPath)
                String archiveName = archiveDest.substring(archiveDest.lastIndexOf("/") + 1)
                logMsg("Archiving remote file to ${archiveDest}")
                try {
                    sftpClient.rename(selection.refPath, archiveDest)
                } catch (Exception e) {
                    try {
                        InputStream srcStream = sftpClient.openStream(selection.refPath)
                        try {
                            sftpClient.put(archiveDir, archiveName, srcStream)
                            sftpClient.rm(selection.refPath)
                        } finally {
                            try { srcStream?.close() } catch (Exception ignored) {}
                        }
                    } catch (Exception e2) {
                        logger.warn("Unable to archive SFTP file ${selection.refPath} to ${archiveDest}: ${e2.message}")
                    }
                }
            } catch (Exception e) {
                logger.warn("Archive step failed for ${selection?.refPath ?: '(unknown)'}: ${e.message}")
            }
        } finally {
            try { sftpClient.close() } catch (Exception ignored) {}
        }

        return [
                found          : true,
                source         : "sftp://${sftpConfig.host}:${sftpConfig.port}${sftpConfig.basePath}",
                selectedName   : selection.name ?: selection.refPath,
                stagedLocation : staged.location,
                systemLabel    : resolveEnumLabel(systemEnumId, label),
                basePathUsed   : sftpConfig.basePath
        ]
    }
    
    // Fallback or unreachable code since we enforce SFTP parameters
    logMsg("Invalid configuration for ${label}")
    return [found: false, message: "Invalid SFTP configuration for ${label}"]
}

def file1Prep = prepareFile("file1", file1SystemEnumId, file1SftpServerId, file1RemotePath)
def file2Prep = prepareFile("file2", file2SystemEnumId, file2SftpServerId, file2RemotePath)

file1Source = file1Prep.source
file2Source = file2Prep.source
file1SelectedName = file1Prep.selectedName
file2SelectedName = file2Prep.selectedName
def file1BasePathUsed = file1Prep.basePathUsed
def file2BasePathUsed = file2Prep.basePathUsed

if (!file1Prep.found || !file2Prep.found) {
    dataAvailable = false
    def msg = (file1Prep.message ?: "") + (file1Prep.message && file2Prep.message ? "; " : "") + (file2Prep.message ?: "")
    if (!msg) msg = "No files found to reconcile"
    statusMessage = messages.toString() + "\nResult: " + msg
    logger.info("SFTP Poll finished: ${msg}")
    return
}

file1StagedLocation = file1Prep.stagedLocation
file2StagedLocation = file2Prep.stagedLocation
dataAvailable = true

def sparkMasterToUse = sparkMaster ?: (ec.resource.properties['spark.master'] ?: "local[*]")

def reconcileResult = ec.service.sync()
        .name("reconciliation.ReconciliationCoreServices.reconcile#FilesByMapping")
        .parameters([
                reconciliationMappingId: reconciliationMappingId,
                file1Location          : file1StagedLocation,
                file2Location          : file2StagedLocation,
                file1Name              : file1SelectedName,
                file2Name              : file2SelectedName,
                file1SystemEnumId      : file1SystemEnumId,
                file2SystemEnumId      : file2SystemEnumId,
                file1FileTypeEnumId    : file1FileTypeEnumId,
                file2FileTypeEnumId    : file2FileTypeEnumId,
                file1SchemaFileName    : file1SchemaFileName,
                file2SchemaFileName    : file2SchemaFileName,
                file1Label             : file1Prep.systemLabel ?: resolveEnumLabel(file1SystemEnumId, "File 1"),
                file2Label             : file2Prep.systemLabel ?: resolveEnumLabel(file2SystemEnumId, "File 2"),
                hasHeader              : hasHeader,
                outputLocation         : outputLoc,
                sparkMaster            : sparkMasterToUse,
                sparkAppName           : sparkAppName
        ])
        .call()

file1Type = reconcileResult.file1Type
file2Type = reconcileResult.file2Type
reconciliationType = reconcileResult.reconciliationType
diffLocation = reconcileResult.diffLocation
diffFileName = reconcileResult.diffFileName
differenceCount = reconcileResult.differenceCount
onlyInFile1Count = reconcileResult.onlyInFile1Count
onlyInFile2Count = reconcileResult.onlyInFile2Count
validationErrors = reconcileResult.validationErrors ?: []
processingWarnings = (processingWarnings ?: []) + (reconcileResult.processingWarnings ?: [])
statusMessage = "${reconciliationType ?: 'Reconciliation'} complete"

logger.info("SFTP reconciliation done: run=${reconciliationRunId ?: 'ad-hoc'} type=${reconciliationType} diff=${diffFileName} dataAvailable=${dataAvailable}")
logMsg("Reconciliation complete. Diff: ${diffFileName}. Counts: Only1=${onlyInFile1Count}, Only2=${onlyInFile2Count}, Diff=${differenceCount}")

// Upload Result to SFTP (Server 1)
// Upload Result to SFTP (Server 1)
try {
    def resultFile = null
    if (diffLocation) {
        resultFile = ec.resource.getLocationReference(diffLocation)
    } else {
         resultFile = ec.resource.getLocationReference(outputLoc + "/" + diffFileName)
    }

    if (resultFile && (!resultFile.supportsExists() || resultFile.getExists())) {
        def server = ec.entity.find("darpan.reconciliation.SftpServer")
            .condition("sftpServerId", file1SftpServerId)
            .useCache(true)
            .one()
        if (server) {
            def hostInfo = resolveHostAndPort(server.host, server.port, "Server ${file1SftpServerId}")
            def cleanHost = hostInfo.host
            def cleanPort = hostInfo.port
            def remoteResultDir = normalizePath(remoteUploadPath ?: file1BasePathUsed ?: hostInfo.basePath) ?: "/"
            def cleanUser = normalize(server.username)
            def cleanPass = normalize(server.password)
            
            SftpClient sftpClient = new SftpClient((String) cleanHost, (String) cleanUser, (int) cleanPort)
            
            if (cleanPass) sftpClient.password((String) cleanPass)
            if (server.privateKey) sftpClient.privateKey((String) server.privateKey)
            
            logMsg("Uploading result ${diffFileName} to SFTP Server 1 (${cleanHost}:${cleanPort}) at ${remoteResultDir} ...")
            try {
                sftpClient.connect()
                try { sftpClient.mkdirs(remoteResultDir) } catch (Exception ignored) {}
                String remoteResultPath = (remoteResultDir.endsWith("/") ? remoteResultDir + diffFileName : remoteResultDir + "/" + diffFileName)
                
                // Read local file stream
                InputStream resultStream = resultFile.openStream()
                try {
                    sftpClient.put(remoteResultDir, diffFileName, resultStream)
                    logMsg("Result uploaded successfully to ${remoteResultPath}")
                } finally {
                    try { resultStream?.close() } catch (Exception ignored) {}
                }
            } catch (Exception e) {
                logMsg("Error uploading result to SFTP: ${e.message}")
                logger.error("SFTP Upload Error", e)
            } finally {
                try { sftpClient.close() } catch (Exception ignored) {}
            }
        }
    } else {
        logMsg("Result file ${diffFileName} not found at ${outputLoc}, skipping upload.")
    }
} catch (Exception e) {
    logMsg("Failed to initiate result upload: ${e.message}")
}

statusMessage = messages.toString()
