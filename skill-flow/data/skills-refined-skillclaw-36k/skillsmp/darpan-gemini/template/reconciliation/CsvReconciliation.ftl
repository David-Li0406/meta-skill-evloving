<#macro csvUploadRow index fileField systemField selectedSystem="">
    <div class="form-group">
        <label for="${fileField}" class="col-sm-2 control-label">CSV ${index}</label>
        <div class="col-sm-3" style="padding-right: 5px;">
            <input id="${fileField}" name="${fileField}" type="file" class="form-control" accept=".csv,text/csv" required>
        </div>
        <div class="col-sm-3" style="padding-left: 5px;">
            <select id="${systemField}" name="${systemField}" class="form-control" required aria-label="CSV ${index} System">
                <option value="">Select system</option>
                <#if systemEnumList?has_content>
                    <#list systemEnumList as systemEnum>
                        <#assign systemLabel = (systemEnum.description?has_content)?then(systemEnum.description, systemEnum.enumId)>
                        <option value="${systemEnum.enumId?html}" <#if selectedSystem?has_content && selectedSystem == systemEnum.enumId>selected</#if>>
                            ${systemLabel?html}
                        </option>
                    </#list>
                </#if>
            </select>
        </div>
    </div>
</#macro>
<div class="container">
    <div class="page-header">
        <h2>CSV Reconciliation</h2>
        <p class="text-muted">Upload two CSV files, choose the system sources and mapping, and generate a reconciliation diff listing IDs that only appear in one file.</p>
    </div>

    <form method="post" action="${sri.buildUrl('runCsvReconciliation').url}" enctype="multipart/form-data" class="form-horizontal">
        <input type="hidden" name="moquiSessionToken" value="${ec.web.sessionToken}">
        <input type="hidden" name="hasHeader" value="true">

        <@csvUploadRow index=1 fileField="csv1File" systemField="csv1SystemEnumId" selectedSystem=csv1SystemEnumId />
        <@csvUploadRow index=2 fileField="csv2File" systemField="csv2SystemEnumId" selectedSystem=csv2SystemEnumId />

        <div class="form-group">
            <label for="reconciliationMappingId" class="col-sm-2 control-label">Mapping</label>
            <div class="col-sm-6">
                <select id="reconciliationMappingId" name="reconciliationMappingId" class="form-control" required>
                    <option value="">Select mapping</option>
                    <#if mappingList?has_content>
                        <#list mappingList as mapping>
                            <#assign mappingLabel = (mapping.mappingName?has_content)?then(mapping.mappingName, mapping.reconciliationMappingId)>
                            <option value="${mapping.reconciliationMappingId?html}" <#if reconciliationMappingId?has_content && reconciliationMappingId == mapping.reconciliationMappingId>selected</#if>>
                                ${mappingLabel?html}<#if mapping.description?has_content> - ${mapping.description?html}</#if>
                            </option>
                        </#list>
                    </#if>
                </select>
                <#if !mappingList?has_content>
                    <span class="help-block text-danger">No mappings configured yet.</span>
                </#if>
            </div>
        </div>

        <div class="form-group">
            <div class="col-sm-offset-2 col-sm-6">
                <button type="submit" class="btn btn-primary">Reconcile</button>
            </div>
        </div>
    </form>

    <hr/>

    <h4>Generated Reconciliation Files</h4>
    <#if latestFile?has_content>
        <p>
            <a class="btn btn-success btn-sm" href="${sri.buildUrl('downloadDiff').addParameter('filename', latestFile).urlWithParams}" target="_blank" rel="noopener" download="${latestFile?html}">
                Download Latest (${latestFile?html})
            </a>
        </p>
    </#if>
    <#if diffFiles?has_content>
        <table class="table table-striped table-condensed">
            <thead>
                <tr>
                    <th>File</th>
                    <th>Last Modified</th>
                    <th>Size</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <#list diffFiles as diffFile>
                    <#if diffFile?is_hash>
                        <#assign fileName = diffFile['fileName']!>
                        <#assign fileLastModified = diffFile['fileLastModified']!0>
                        <#assign fileSizeBytes = diffFile['fileSize']!0>
                    <#else>
                        <#assign fileName = diffFile.getFileName()!>
                        <#assign fileLastModified = diffFile.getLastModified()!0>
                        <#assign fileSizeBytes = diffFile.getSize()!0>
                    </#if>
                    <tr>
                        <td>${fileName?html}</td>
                        <td>${ec.l10n.format(fileLastModified?number_to_datetime, null)}</td>
                        <#assign fileSizeBytesNum = fileSizeBytes?number>
                        <#assign fileSizeUnit = "Kb">
                        <#assign fileSizeValue = fileSizeBytesNum / 1024>
                        <#if fileSizeBytesNum >= 1048576>
                            <#assign fileSizeValue = fileSizeBytesNum / 1048576>
                            <#assign fileSizeUnit = "Mb">
                        </#if>
                        <td>${ec.l10n.format(fileSizeValue, '#,##0.##')} ${fileSizeUnit}</td>
                        <td>
                            <#if fileName?has_content>
                                <a class="btn btn-default btn-xs" href="${sri.buildUrl('downloadDiff').addParameter('filename', fileName).urlWithParams}" target="_blank" rel="noopener" download="${fileName?html}">Download</a>
                            </#if>
                        </td>
                    </tr>
                </#list>
            </tbody>
        </table>
    <#else>
        <p class="text-muted">No reconciliation outputs generated yet.</p>
    </#if>

    <p class="text-muted">Output CSV columns: <strong>source</strong> (Only in &lt;system&gt;) and the mapped field.</p>
</div>
