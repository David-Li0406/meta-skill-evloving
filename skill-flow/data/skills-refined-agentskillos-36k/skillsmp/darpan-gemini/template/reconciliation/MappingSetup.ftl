<#macro mappingRow index systemField columnField selectedSystem selectedColumn="">
    <div class="form-group">
        <label for="${systemField}" class="col-sm-2 control-label">System ${index}</label>
        <div class="col-sm-2" style="padding-right: 5px;">
            <select id="${systemField}" name="${systemField}" class="form-control" required aria-label="System ${index}">
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
        <div class="col-sm-3" style="padding-left: 5px;">
            <input id="${columnField}" name="${columnField}" type="text" class="form-control"
                    placeholder="Column name" required value="${(selectedColumn!'')?html}">
        </div>
    </div>
</#macro>
<div class="container">
    <div class="page-header">
        <h2>Mapping Builder</h2>
        <p class="text-muted">Define a mapping between two systems by naming the mapping and the column to compare in each system.</p>
        <#if createdMappingId?has_content>
            <p class="text-success">Saved mapping ${(createdMappingName!'')?html}. It is now available in CSV Reconciliation.</p>
        </#if>
    </div>

    <form method="post" action="${sri.buildUrl('createMapping').url}" class="form-horizontal">
        <input type="hidden" name="moquiSessionToken" value="${ec.web.sessionToken}">

        <div class="form-group">
            <label for="mappingName" class="col-sm-2 control-label">Mapping name</label>
            <div class="col-sm-6">
                <input id="mappingName" name="mappingName" type="text" class="form-control" required
                        value="${(mappingName!'')?html}">
                <span class="help-block text-muted">This name appears in the reconciliation mapping list.</span>
            </div>
        </div>

        <@mappingRow index=1 systemField="system1EnumId" columnField="system1FieldName"
                selectedSystem=system1EnumId!'' selectedColumn=system1FieldName />
        <@mappingRow index=2 systemField="system2EnumId" columnField="system2FieldName"
                selectedSystem=system2EnumId!'' selectedColumn=system2FieldName />

        <div class="form-group">
            <div class="col-sm-offset-2 col-sm-6">
                <button type="submit" class="btn btn-primary">Save Mapping</button>
            </div>
        </div>
    </form>
</div>
